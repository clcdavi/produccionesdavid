#!/usr/bin/env python3
"""
Uploader y Programador Automatizado de TikTok para Producciones David.
Interactúa con el Uploader Web oficial de TikTok (tiktok.com/creator-center/upload)
aprovechando la sesión activa en Google Chrome.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

INST_JSON = Path.home() / "Library" / "Application Support" / "adrian-saenz-video-negocio" / "instalacion.json"
CHROME_BIN = json.loads(INST_JSON.read_text(encoding="utf-8"))["chrome"]

def preparar_subida(video_path: str, caption: str, tags: list[str] = None):
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(f"No existe el archivo de video: {video_path}")
    
    full_caption = caption
    if tags:
        hashtag_str = " ".join([t if t.startswith("#") else f"#{t}" for t in tags])
        full_caption = f"{caption}\n\n{hashtag_str}"
    
    info = {
        "video_file": str(video.resolve()),
        "caption": full_caption,
        "is_aigc": True,
        "privacy": "PUBLIC_TO_EVERYONE",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    meta_file = video.with_suffix(".tiktok.json")
    meta_file.write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Metadata de publicación para TikTok lista: {meta_file}")
    print(f"🎬 Video: {video.name}")
    print(f"📝 Texto ({len(full_caption)} chars): {full_caption[:80]}...")
    return info

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TikTok Uploader Assistant")
    parser.add_argument("--video", required=True, help="Ruta al video mp4")
    parser.add_argument("--caption", required=True, help="Texto y descripción del video")
    parser.add_argument("--tags", nargs="*", default=["ProduccionesDavid", "VideosIA", "MarketingDigital", "ZonaNorte"], help="Hashtags")
    args = parser.parse_args()
    
    preparar_subida(args.video, args.caption, args.tags)
