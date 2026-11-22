#!/usr/bin/env python3
"""
Lanza las 3 tareas de generación con Seedance 2.5 en APIMart,
con preservación de rostro, 3 vestimentas/ambientes diferentes y sincronización con audio_url.
"""
import json
import time
import requests
from pathlib import Path

BASE_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando")
ASSETS_DIR = BASE_DIR / "assets" / "david"
CLAVES_FILE = BASE_DIR / "claves_ia.json"

claves = json.loads(CLAVES_FILE.read_text(encoding="utf-8"))
api_key = claves["apimartKey"]
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "User-Agent": "ProduccionesDavidStudio/1.0"
}

def upload_temp(file_path: Path, mime: str) -> str:
    print(f"📤 Subiendo {file_path.name} temporalmente...")
    with open(file_path, "rb") as f:
        r = requests.post("https://uguu.se/upload", files={"files[]": (file_path.name, f, mime)}, timeout=60)
    if not r.ok:
        raise RuntimeError(f"Error subiendo {file_path.name}: {r.text}")
    url = r.json()["files"][0]["url"]
    print(f"  URL lista: {url}")
    return url

SCENES = [
    {
        "id": "scene_01_edicion",
        "name": "Escena 1 · Suite de Edición (Look Director Creativo)",
        "audio_local": ASSETS_DIR / "multi_audio_01.mp3",
        "duration": 5,
        "out_file": ASSETS_DIR / "seedance_multi_clip_01.mp4",
        "prompt": (
            "Hyper-realistic commercial video, 9:16 vertical. The man in the reference image (David Correa) "
            "looks directly at the camera and speaks with a confident, welcoming smile and natural lip movements. "
            "He is wearing a minimalist, premium matte black crewneck t-shirt. Setting: modern creative film editing studio "
            "with softly blurred monitors showing video timelines in the background, warm amber and charcoal ambient lighting, "
            "subtle film grain, steady medium shot, cinematic 4k commercial look."
        )
    },
    {
        "id": "scene_02_atrio",
        "name": "Escena 2 · Atrio Corporativo (Look Fundador & Estratega)",
        "audio_local": ASSETS_DIR / "multi_audio_02.mp3",
        "duration": 7,
        "out_file": ASSETS_DIR / "seedance_multi_clip_02.mp4",
        "prompt": (
            "Hyper-realistic commercial video, 9:16 vertical. The man in the reference image (David Correa) "
            "looks directly at the camera with an engaging, friendly expression and natural lip movements. "
            "He is wearing a tailored charcoal dark blazer over a black shirt. Setting: modern architectural glass atrium "
            "with soft natural diffused daylight, sleek minimalist concrete and glass interior, shallow depth of field, "
            "steady medium shot, high-end commercial aesthetic."
        )
    },
    {
        "id": "scene_03_rodaje",
        "name": "Escena 3 · Set de Rodaje (Look Director de Filmación)",
        "audio_local": ASSETS_DIR / "multi_audio_03.mp3",
        "duration": 6,
        "out_file": ASSETS_DIR / "seedance_multi_clip_03.mp4",
        "prompt": (
            "Hyper-realistic commercial video, 9:16 vertical. The man in the reference image (David Correa) "
            "looks directly at the camera and delivers an energetic, confident closing statement with natural lip movements "
            "and a friendly smile. He is wearing a dark filmmaker jacket with monitoring headphones resting around his neck. "
            "Setting: professional film studio soundstage with a warm Fresnel spotlight casting a subtle volumetric beam "
            "and film equipment in the background, cinematic rim lighting, steady medium shot, 4k quality."
        )
    }
]

def main():
    # 1. Subir foto base de David
    foto_ref = ASSETS_DIR / "david_frente_medio.jpg"
    foto_url = upload_temp(foto_ref, "image/jpeg")

    # 2. Subir audios y lanzar tareas en APIMart
    tasks = []
    for sc in SCENES:
        audio_url = upload_temp(sc["audio_local"], "audio/mpeg")
        payload = {
            "model": "seedance-2.5",
            "prompt": sc["prompt"],
            "duration": sc["duration"],
            "aspect_ratio": "9:16",
            "image_urls": [foto_url],
            "audio_url": audio_url
        }
        print(f"\n🚀 Lanzando {sc['name']} en Seedance 2.5 (duración: {sc['duration']}s)...")
        r = requests.post("https://api.apimart.ai/v1/videos/generations", headers=headers, json=payload, timeout=60)
        if not r.ok:
            raise RuntimeError(f"Error en {sc['id']}: {r.text}")
        data = r.json()
        tid = data["data"][0]["task_id"] if isinstance(data.get("data"), list) else data["data"]["task_id"]
        print(f"  Task ID: {tid}")
        tasks.append({
            "sc": sc,
            "tid": tid,
            "done": False
        })
        time.sleep(2) # Pausa breve entre envíos

    # 3. Monitorear progreso de las 3 tareas
    print(f"\n⏳ Monitoreando {len(tasks)} tareas en APIMart...")
    for step in range(90):
        time.sleep(6)
        all_done = True
        for t in tasks:
            if t["done"]:
                continue
            all_done = False
            r = requests.get(f"https://api.apimart.ai/v1/tasks/{t['tid']}", headers=headers, timeout=30)
            if not r.ok:
                continue
            st_data = r.json().get("data", {})
            status = st_data.get("status", "").lower()
            progress = st_data.get("progress", 0)
            print(f"  [{t['sc']['id']}] paso {step+1}: status={status} ({progress}%)")
            
            if status in ("completed", "succeeded", "success"):
                videos = st_data.get("result", {}).get("videos", [])
                vurl = videos[0].get("url") if videos else st_data.get("video_url")
                if isinstance(vurl, list):
                    vurl = vurl[0]
                if vurl:
                    print(f"  ⬇️ Descargando {t['sc']['name']} desde {vurl}...")
                    vb = requests.get(vurl, timeout=120).content
                    t["sc"]["out_file"].write_bytes(vb)
                    print(f"  ✅ Guardado: {t['sc']['out_file'].name} ({len(vb)//1024} KB)")
                    t["done"] = True
            elif status in ("failed", "error", "cancelled"):
                raise RuntimeError(f"Fallo en {t['sc']['id']}: {st_data}")

        if all_done:
            print("\n🎉 ¡Todos los 3 clips de Seedance 2.5 fueron generados y descargados con éxito!")
            break

if __name__ == "__main__":
    main()
