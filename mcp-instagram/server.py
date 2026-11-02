#!/usr/bin/env python3
"""
Servidor MCP de Instagram para Producciones David (Stdio JSON-RPC 2.0).
Soporta:
1. Instagram API Oficial (Instagram Login / Graph API) para publicar Reels, Fotos, leer métricas y responder comentarios.
2. Analizador local de perfiles de clientes (Playwright) sin costo.
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando")
CONFIG_FILE = BASE_DIR / "instagram_credenciales.json"
EXTRACTOR_SCRIPT = Path("/Users/davidcorrea/.gemini/config/skills/adrian-saenz-video-negocio/scripts/extraer_instagram.py")
VENV_PYTHON = Path("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/.venv/bin/python")


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "username": "",
        "ig_user_id": "",
        "access_token": "",
        "api_host": "https://graph.instagram.com/v21.0",
    }


def save_config(cfg: dict) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def upload_to_catbox(local_path: str) -> str:
    """Sube un archivo local (.mp4/.jpg/.png) a un CDN público temporal para que la API de Meta lo descargue."""
    p = Path(local_path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"No existe el archivo local: {local_path}")

    # 1. Intentar con uguu.se (directo y rápido)
    res = subprocess.run(
        ["curl", "-sS", "-F", f"files[]=@{p}", "https://uguu.se/upload"],
        capture_output=True,
        text=True,
        timeout=180,
    )
    try:
        j = json.loads(res.stdout)
        if j.get("success") and j.get("files"):
            return j["files"][0]["url"]
    except Exception:
        pass

    # 2. Fallback a tmpfiles.org (/dl/ URL directa)
    res2 = subprocess.run(
        ["curl", "-sS", "-F", f"file=@{p}", "https://tmpfiles.org/api/v1/upload"],
        capture_output=True,
        text=True,
        timeout=180,
    )
    try:
        j2 = json.loads(res2.stdout)
        raw_url = j2.get("data", {}).get("url", "")
        if raw_url.startswith("https://tmpfiles.org/"):
            return raw_url.replace("https://tmpfiles.org/", "https://tmpfiles.org/dl/", 1)
    except Exception:
        pass

    raise RuntimeError(f"Error al preparar URL pública para Meta: {res.stdout} / {res2.stdout}")


def graph_request(method: str, endpoint: str, params: dict | None = None) -> dict:
    cfg = load_config()
    token = cfg.get("access_token", "").strip()
    if not token:
        raise RuntimeError(
            "Falta configurar el access_token de Instagram. Usa 'ig_configurar_credenciales' primero."
        )
    host = cfg.get("api_host", "https://graph.instagram.com/v21.0").rstrip("/")
    params = dict(params or {})
    params["access_token"] = token

    if method.upper() == "GET":
        qs = urllib.parse.urlencode(params)
        url = f"{host}/{endpoint.lstrip('/')}?{qs}"
        req = urllib.request.Request(url, method="GET")
    else:
        url = f"{host}/{endpoint.lstrip('/')}"
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=method.upper())

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Error de Instagram API ({e.code}): {err_body}")


TOOLS = [
    {
        "name": "ig_estado_cuenta",
        "description": "Verifica el estado de la configuración de la cuenta de Instagram de Producciones David y, si hay token activo, consulta los datos del perfil en vivo.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "ig_configurar_credenciales",
        "description": "Guarda en disco el @usuario, el Access Token de Instagram API y detecta automáticamente el ig_user_id de la cuenta.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Nombre de usuario de Instagram (ej. produccionesdavid.ar)"},
                "access_token": {"type": "string", "description": "Token de acceso de Instagram Graph API (IG... o EAA...)"},
                "ig_user_id": {"type": "string", "description": "Opcional: ID numérico de usuario de Instagram (se autodetecta si se omite)"},
            },
        },
    },
    {
        "name": "ig_publicar_reel",
        "description": "Publica un video vertical (.mp4 local o URL) directamente como Reel en la cuenta de Instagram de Producciones David usando la API oficial de Meta.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "video_path": {"type": "string", "description": "Ruta absoluta en tu Mac al archivo .mp4 (o URL pública https://)"},
                "caption": {"type": "string", "description": "Texto del Reel (incluyendo gancho inicial, cuerpo y hashtags)"},
                "share_to_feed": {"type": "boolean", "description": "Si es true (por defecto), también aparece en la grilla principal del perfil", "default": True},
                "thumb_offset_ms": {"type": "integer", "description": "Milisegundos del fotograma que se usará como portada (ej. 2000 para el segundo 2)", "default": 1500},
            },
            "required": ["video_path", "caption"],
        },
    },
    {
        "name": "ig_publicar_foto",
        "description": "Publica una imagen (.jpg o .png local o URL) en el feed de Instagram con su descripción.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Ruta absoluta en tu Mac a la imagen .jpg/.png (o URL pública)"},
                "caption": {"type": "string", "description": "Texto de la publicación"},
            },
            "required": ["image_path", "caption"],
        },
    },
    {
        "name": "ig_publicar_carrusel",
        "description": "Publica un carrusel de 2 a 10 imágenes (.jpg/.png locales o URLs) en el feed de Instagram con su descripción.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de rutas absolutas a las imágenes del carrusel en orden (2 a 10 imágenes)",
                },
                "caption": {"type": "string", "description": "Texto del carrusel (gancho, packs, precios y hashtags)"},
            },
            "required": ["image_paths", "caption"],
        },
    },
    {
        "name": "ig_publicar_historia",
        "description": "Publica una Historia (Story) de imagen o video vertical en la cuenta de Instagram.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "media_path": {"type": "string", "description": "Ruta absoluta a la imagen (.jpg/.png) o video (.mp4)"},
                "es_video": {"type": "boolean", "description": "True si es un video .mp4, False si es imagen", "default": False},
            },
            "required": ["media_path"],
        },
    },
    {
        "name": "ig_listar_publicaciones",
        "description": "Obtiene las últimas publicaciones y Reels de tu cuenta de Instagram con sus métricas (likes, comentarios, enlace directo).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "limite": {"type": "integer", "description": "Cantidad de publicaciones a listar (por defecto 10)", "default": 10},
            },
        },
    },
    {
        "name": "ig_responder_comentario",
        "description": "Responde a un comentario específico en una publicación o Reel de tu cuenta de Instagram.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "comment_id": {"type": "string", "description": "ID del comentario al que se desea responder"},
                "mensaje": {"type": "string", "description": "Texto de la respuesta"},
            },
            "required": ["comment_id", "mensaje"],
        },
    },
    {
        "name": "ig_espiar_cliente",
        "description": "Extrae sin gastar API los datos públicos, biografía y últimas fotos de cualquier cuenta de Instagram de un potencial cliente.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "usuario_o_url": {"type": "string", "description": "Usuario (ej. @sw.store_ar) o URL del perfil de Instagram"},
                "carpeta_destino": {"type": "string", "description": "Carpeta donde guardar el reporte y fotos descargadas"},
                "limite": {"type": "integer", "description": "Cantidad máxima de posts a extraer (por defecto 12)", "default": 12},
            },
            "required": ["usuario_o_url", "carpeta_destino"],
        },
    },
]


def handle_tool_call(name: str, args: dict) -> str:
    cfg = load_config()

    if name == "ig_estado_cuenta":
        if not cfg.get("access_token"):
            return json.dumps(
                {
                    "conectado_api": False,
                    "username": cfg.get("username") or "(no configurado)",
                    "archivo_config": str(CONFIG_FILE),
                    "mensaje": "Falta cargar el Access Token de Meta Developers con 'ig_configurar_credenciales'.",
                },
                indent=2,
                ensure_ascii=False,
            )
        try:
            uid = cfg.get("ig_user_id") or "me"
            fields = (
                "id,username,name,biography,followers_count,follows_count,media_count,profile_picture_url"
                if uid != "me"
                else "id,user_id,username,name,account_type,followers_count,media_count"
            )
            me = graph_request("GET", uid, {"fields": fields})
            return json.dumps({"conectado_api": True, "perfil": me}, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"conectado_api": False, "error": str(e)}, indent=2, ensure_ascii=False)

    elif name == "ig_configurar_credenciales":
        if args.get("username"):
            cfg["username"] = args["username"].lstrip("@").strip()
        if args.get("access_token"):
            token = args["access_token"].strip()
            cfg["access_token"] = token
            # Si el token empieza con IG..., usa graph.instagram.com; si empieza con EAA..., soporta graph.facebook.com
            cfg["api_host"] = (
                "https://graph.instagram.com/v21.0"
                if token.startswith("IG")
                else "https://graph.facebook.com/v21.0"
            )
        if args.get("ig_user_id"):
            cfg["ig_user_id"] = args["ig_user_id"].strip()
        save_config(cfg)

        if cfg.get("access_token") and not cfg.get("ig_user_id"):
            try:
                me = graph_request("GET", "me", {"fields": "id,user_id,username,name"})
                cfg["ig_user_id"] = str(me.get("user_id") or me.get("id") or "")
                if me.get("username"):
                    cfg["username"] = me["username"]
                save_config(cfg)
                return json.dumps({"ok": True, "config": cfg, "verificado_en_vivo": me}, indent=2, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"ok": True, "config": cfg, "aviso_verificacion": str(e)}, indent=2, ensure_ascii=False)

        return json.dumps({"ok": True, "config": cfg}, indent=2, ensure_ascii=False)

    elif name == "ig_publicar_reel":
        video_path = args["video_path"]
        caption = args["caption"]
        share_to_feed = args.get("share_to_feed", True)
        thumb_offset = args.get("thumb_offset_ms", 1500)

        video_url = video_path if video_path.startswith("http") else upload_to_catbox(video_path)
        uid = cfg.get("ig_user_id") or "me"

        container = graph_request(
            "POST",
            f"{uid}/media",
            {
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "share_to_feed": "true" if share_to_feed else "false",
                "thumb_offset": str(thumb_offset),
            },
        )
        creation_id = container["id"]

        # Esperar a que Instagram termine de procesar el contenedor de video
        for _ in range(30):
            time.sleep(5)
            st = graph_request("GET", creation_id, {"fields": "status_code,status"})
            code = st.get("status_code")
            if code == "FINISHED":
                break
            if code in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"Instagram rechazó el procesamiento del video: {st}")

        published = graph_request("POST", f"{uid}/media_publish", {"creation_id": creation_id})
        media_id = published.get("id")
        permalink_info = {}
        if media_id:
            try:
                permalink_info = graph_request("GET", media_id, {"fields": "id,permalink,shortcode"})
            except Exception:
                pass
        return json.dumps(
            {"ok": True, "media_id": media_id, "video_url_usada": video_url, "publicacion": permalink_info},
            indent=2,
            ensure_ascii=False,
        )

    elif name == "ig_publicar_foto":
        image_path = args["image_path"]
        caption = args["caption"]
        image_url = image_path if image_path.startswith("http") else upload_to_catbox(image_path)
        uid = cfg.get("ig_user_id") or "me"

        container = graph_request(
            "POST",
            f"{uid}/media",
            {"image_url": image_url, "caption": caption},
        )
        creation_id = container["id"]
        time.sleep(3)
        published = graph_request("POST", f"{uid}/media_publish", {"creation_id": creation_id})
        return json.dumps({"ok": True, "published": published}, indent=2, ensure_ascii=False)

    elif name == "ig_publicar_carrusel":
        image_paths = args["image_paths"]
        caption = args["caption"]
        uid = cfg.get("ig_user_id") or "me"
        child_ids = []
        for p in image_paths:
            img_url = p if p.startswith("http") else upload_to_catbox(p)
            item = graph_request(
                "POST",
                f"{uid}/media",
                {"image_url": img_url, "is_carousel_item": "true"},
            )
            child_ids.append(item["id"])
            time.sleep(1)

        carousel_container = graph_request(
            "POST",
            f"{uid}/media",
            {
                "media_type": "CAROUSEL",
                "children": ",".join(child_ids),
                "caption": caption,
            },
        )
        creation_id = carousel_container["id"]
        for _ in range(15):
            time.sleep(3)
            st = graph_request("GET", creation_id, {"fields": "status_code"})
            if st.get("status_code") == "FINISHED":
                break
        published = graph_request("POST", f"{uid}/media_publish", {"creation_id": creation_id})
        return json.dumps({"ok": True, "child_ids": child_ids, "published": published}, indent=2, ensure_ascii=False)

    elif name == "ig_publicar_historia":
        media_path = args["media_path"]
        es_video = args.get("es_video", False)
        media_url = media_path if media_path.startswith("http") else upload_to_catbox(media_path)
        uid = cfg.get("ig_user_id") or "me"
        params = {"media_type": "STORIES"}
        if es_video:
            params["video_url"] = media_url
        else:
            params["image_url"] = media_url
        container = graph_request("POST", f"{uid}/media", params)
        creation_id = container["id"]
        for _ in range(20):
            time.sleep(3)
            st = graph_request("GET", creation_id, {"fields": "status_code"})
            if st.get("status_code") == "FINISHED":
                break
        published = graph_request("POST", f"{uid}/media_publish", {"creation_id": creation_id})
        return json.dumps({"ok": True, "published": published}, indent=2, ensure_ascii=False)

    elif name == "ig_listar_publicaciones":
        uid = cfg.get("ig_user_id") or "me"
        limite = args.get("limite", 10)
        res = graph_request(
            "GET",
            f"{uid}/media",
            {
                "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count",
                "limit": str(limite),
            },
        )
        return json.dumps(res, indent=2, ensure_ascii=False)

    elif name == "ig_responder_comentario":
        cid = args["comment_id"]
        msg = args["mensaje"]
        res = graph_request("POST", f"{cid}/replies", {"message": msg})
        return json.dumps({"ok": True, "respuesta": res}, indent=2, ensure_ascii=False)

    elif name == "ig_espiar_cliente":
        usuario = args["usuario_o_url"]
        destino = args["carpeta_destino"]
        limite = str(args.get("limite", 12))
        proc = subprocess.run(
            [str(VENV_PYTHON), str(EXTRACTOR_SCRIPT), usuario, "--carpeta", destino, "--limite", limite],
            capture_output=True,
            text=True,
            timeout=180,
        )
        return proc.stdout or proc.stderr

    raise ValueError(f"Herramienta desconocida: {name}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        req_id = req.get("id")
        method = req.get("method", "")
        params = req.get("params") or {}

        if method == "initialize":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "instagram-producciones-david", "version": "1.0.0"},
                },
            }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        elif method.startswith("notifications/"):
            continue
        elif method == "tools/list":
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        elif method == "tools/call":
            t_name = params.get("name", "")
            t_args = params.get("arguments") or {}
            try:
                out = handle_tool_call(t_name, t_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": out}], "isError": False},
                }
            except Exception as e:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True},
                }
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        elif req_id is not None:
            resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
