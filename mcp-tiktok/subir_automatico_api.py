#!/usr/bin/env python3
import json
import subprocess
import urllib.request
from pathlib import Path

DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/campana-lanzamiento-pd")
CREDS = json.loads(Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/tiktok_credenciales.json").read_text())

token = CREDS.get("access_token")
print("Access token configurado:", "SÍ" if token else "NO")

videos = [
    {
        "nombre": "Historia 1 (Lanzamiento)",
        "file": DIR / "tiktok_historia_01.mp4",
        "caption": "🚀 Lanzamos Producciones David. Transformamos la imagen de tu negocio con Inteligencia Artificial. ¡Escribinos por MD! 🇦🇷 #ProduccionesDavid #VideosIA #ZonaNorte"
    },
    {
        "nombre": "Historia 2 (Packs)",
        "file": DIR / "tiktok_historia_02.mp4",
        "caption": "📦 Packs de videos mensuales y comerciales a medida para comercios, marcas y eventos. Consultá promos por MD! ✨ #Emprendedores #PacksVideos #Argentina"
    },
    {
        "nombre": "Publicación Oficial",
        "file": DIR / "reel_oficial_producciones_david.mp4",
        "caption": "🎬 Transformamos fotos en comerciales cinematográficos con IA para Comercios, Empresas y Eventos. 📍 Consultá promos por MD #ProduccionesDavid #VideosIA #Comercios #Argentina"
    }
]

if not token:
    print("❌ Falta el access_token de la API de TikTok.")
    exit(1)

for v in videos:
    print(f"\nSubiendo {v['nombre']}...")
    # Subir a host publico para que TikTok lo descargue
    res = subprocess.run(["curl", "-s", "-F", f"files[]=@{v['file']}", "https://uguu.se/upload"], capture_output=True, text=True, check=True)
    pub_url = json.loads(res.stdout)["files"][0]["url"]
    print("URL pública:", pub_url)

    payload = {
        "post_info": {
            "title": v["caption"],
            "privacy_level": "PUBLIC_TO_EVERYONE",
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
        print("Respuesta TikTok API:", resp)
    except urllib.error.HTTPError as e:
        print("Error HTTP TikTok:", e.code, e.read().decode())
