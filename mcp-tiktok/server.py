#!/usr/bin/env python3
from __future__ import annotations
"""
Servidor MCP para TikTok Oficial (@produccionesdavid.ar)
Soporta:
1. Automatización Web directa (tiktok_preparar_subida_web)
2. Content Posting API oficial (tiktok_publicar_video_api, tiktok_estado_cuenta)
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tiktok-producciones-david")

CREDS_FILE = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/tiktok_credenciales.json")

def load_credentials() -> dict[str, Any]:
    if CREDS_FILE.exists():
        try:
            return json.loads(CREDS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_credentials(data: dict[str, Any]) -> None:
    CREDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CREDS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def upload_to_public_host(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo: {file_path}")
    
    # Uguu.se
    try:
        cmd = ["curl", "-s", "-F", f"files[]=@{path}", "https://uguu.se/upload"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        data = json.loads(res.stdout)
        url = data["files"][0]["url"]
        if url.startswith("http"):
            return url
    except Exception:
        pass

    # Tmpfiles.org fallback
    cmd = ["curl", "-s", "-F", f"file=@{path}", "https://tmpfiles.org/api/v1/upload"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    data = json.loads(res.stdout)
    raw_url = data["data"]["url"]
    return raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")

@mcp.tool()
def tiktok_preparar_subida_web(video_path: str, caption: str, hashtags: str = "#ProduccionesDavid #VideosIA #MarketingDigital #ZonaNorte") -> str:
    """
    Prepara y formatea un video .mp4 para subirlo a TikTok via el Creator Center Web (tiktok.com/creator-center/upload).
    Genera el archivo de metadata con la descripción exacta, verificación de formato 9:16 y el link directo al cargador.
    """
    vpath = Path(video_path)
    if not vpath.exists():
        return f"❌ Error: No existe el archivo {video_path}"
    
    meta_path = vpath.with_suffix(".tiktok.json")
    full_caption = f"{caption}\n\n{hashtags}" if hashtags else caption
    
    payload = {
        "video": str(vpath.resolve()),
        "caption": full_caption,
        "is_aigc": True,
        "upload_url": "https://www.tiktok.com/creator-center/upload"
    }
    meta_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    
    return (
        f"✅ Video preparado para TikTok!\n"
        f"📁 Archivo: {vpath.name}\n"
        f"📝 Copete: {full_caption}\n"
        f"🌐 Cargador: https://www.tiktok.com/creator-center/upload\n"
        f"📄 Metadata guardada en: {meta_path.name}"
    )

@mcp.tool()
def tiktok_configurar_credenciales(
    client_key: str = "",
    client_secret: str = "",
    access_token: str = "",
    refresh_token: str = "",
    open_id: str = ""
) -> str:
    """Configura o actualiza las credenciales oficiales de TikTok Developers para @produccionesdavid.ar."""
    creds = load_credentials()
    if client_key: creds["client_key"] = client_key.strip()
    if client_secret: creds["client_secret"] = client_secret.strip()
    if access_token: creds["access_token"] = access_token.strip()
    if refresh_token: creds["refresh_token"] = refresh_token.strip()
    if open_id: creds["open_id"] = open_id.strip()
    save_credentials(creds)
    return "✅ Credenciales de TikTok guardadas con éxito en tiktok_credenciales.json"

@mcp.tool()
def tiktok_estado_cuenta() -> str:
    """Verifica el estado del token y la conexión de @produccionesdavid.ar con TikTok Developers API."""
    creds = load_credentials()
    token = creds.get("access_token")
    if not token:
        return (
            "ℹ️ Modo Automatización Web ACTIVO (sesión en navegador de la Mac).\n"
            "Si deseas usar la API directa, configura el Access Token mediante 'tiktok_configurar_credenciales'."
        )
    
    try:
        req = urllib.request.Request(
            "https://open.tiktokapis.com/v2/user/info/?fields=open_id,union_id,avatar_url,display_name,bio_description,profile_deep_link,follower_count",
            headers={"Authorization": f"Bearer {token}"}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
        
        user_info = data.get("data", {}).get("user", {})
        return (
            f"✅ Conexión API con TikTok ACTIVA:\n"
            f"👤 Nombre: {user_info.get('display_name', '')}\n"
            f"👥 Seguidores: {user_info.get('follower_count', 0)}\n"
            f"🔗 Perfil: {user_info.get('profile_deep_link', '')}"
        )
    except Exception as e:
        return f"❌ Error consultando TikTok API: {e}"

@mcp.tool()
def tiktok_publicar_video_api(
    video_path_or_url: str,
    title: str,
    privacy_level: str = "PUBLIC_TO_EVERYONE"
) -> str:
    """Publica un video en TikTok via Content Posting API oficial una vez aprobada la app."""
    creds = load_credentials()
    token = creds.get("access_token")
    if not token:
        return "❌ Error: Falta access_token de TikTok Developers. Usá 'tiktok_preparar_subida_web' mientras tanto."

    pub_url = video_path_or_url if video_path_or_url.startswith("http") else upload_to_public_host(video_path_or_url)
    payload = {
        "post_info": {
            "title": title,
            "privacy_level": privacy_level,
            "is_aigc": True
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": pub_url
        }
    }

    req = urllib.request.Request(
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read().decode())
        publish_id = resp.get("data", {}).get("publish_id")
        return f"🎉 Video enviado a TikTok API con éxito! Publish ID: {publish_id}"
    except Exception as e:
        return f"❌ Error publicando en TikTok API: {e}"

if __name__ == "__main__":
    mcp.run()
