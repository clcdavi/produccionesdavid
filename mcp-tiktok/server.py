#!/usr/bin/env python3
from __future__ import annotations
"""
Servidor MCP para TikTok Oficial (@produccionesdavid.ar)
Permite:
- tiktok_publicar_video: Sube y publica automáticamente videos en TikTok Creator Center mediante Playwright sin intervención manual.
- tiktok_preparar_subida_web: Formatea y genera metadatos para carga asistida.
- tiktok_estado_cuenta: Verifica estado de sesión y credenciales.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tiktok-producciones-david")

DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/mcp-tiktok")
PYTHON_BIN = "/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/.venv/bin/python"

@mcp.tool()
def tiktok_publicar_video(video_path: str, caption: str) -> str:
    """
    Publica un video automáticamente en TikTok Creator Center sin que el usuario tenga que arrastrar nada.
    - video_path: Ruta al archivo de video (.mp4)
    - caption: Título, descripción y hashtags del video
    """
    vpath = Path(video_path)
    if not vpath.exists():
        return f"❌ Error: No existe el archivo {video_path}"
    
    script = DIR / "subir_playwright.py"
    cmd = [PYTHON_BIN, str(script), "--video", str(vpath.resolve()), "--caption", caption]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if res.returncode == 0:
            return f"🎉 ¡Video publicado con éxito en TikTok!\n{res.stdout}"
        else:
            return f"⚠️ Proceso completado con salida:\n{res.stdout}\n{res.stderr}"
    except subprocess.TimeoutExpired:
        return "⏳ El proceso tardó más de lo esperado. Si la ventana de Chrome está abierta solicitando login, completalo una única vez."
    except Exception as e:
        return f"❌ Error al ejecutar el publicador automático: {e}"

@mcp.tool()
def tiktok_preparar_subida_web(video_path: str, caption: str, hashtags: str = "#ProduccionesDavid #VideosIA #MarketingDigital #ZonaNorte") -> str:
    """Genera archivo de metadata y prepara el enlace al Creator Center de TikTok."""
    vpath = Path(video_path)
    if not vpath.exists():
        return f"❌ Error: No existe el archivo {video_path}"
    
    full_caption = f"{caption}\n\n{hashtags}" if hashtags else caption
    meta_path = vpath.with_suffix(".tiktok.json")
    payload = {
        "video": str(vpath.resolve()),
        "caption": full_caption,
        "is_aigc": True,
        "upload_url": "https://www.tiktok.com/creator-center/upload"
    }
    meta_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return f"✅ Metadata preparada en {meta_path.name}"

@mcp.tool()
def tiktok_estado_cuenta() -> str:
    """Informa el estado de la automatización autónoma de TikTok."""
    session_dir = DIR / "tiktok_user_session"
    tiene_sesion = session_dir.exists() and any(session_dir.iterdir())
    return (
        f"🤖 Automatizador Autónomo de TikTok ACTIVO:\n"
        f"📁 Directorio de sesión: {session_dir.name} ({'Sesión guardada' if tiene_sesion else 'Primera vez requiere login'})\n"
        f"🛠️ Herramienta directa: tiktok_publicar_video"
    )

if __name__ == "__main__":
    mcp.run()
