#!/usr/bin/env python3
import json
import sys
import time
from pathlib import Path
import requests

sys.path.insert(0, "/Users/davidcorrea/.gemini/config/skills/adrian-saenz-video-negocio/scripts")
from generar_ia import leer_claves, subir_imagen_publica

claves = leer_claves()
api_key = claves["apimartKey"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

base_dir = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/negocios/sw-store")
out_dir = base_dir / "anuncio" / "planos"
out_dir.mkdir(parents=True, exist_ok=True)

planes = [
    {
        "id": "01_gancho",
        "img": base_dir / "aportado" / "cuadernos-grupo.jpg",
        "prompt": "Vertical cinematic commercial close-up shot on warm wooden table: gentle hands pick up and slightly open the spiral kraft paper notebook, warm golden hour sunlight casting soft shadows across the textured 225g kraft cover and black metal rings, shallow depth of field, 35mm lens, smooth natural motion."
    },
    {
        "id": "02_kraft",
        "img": base_dir / "aportado" / "cuaderno-yo-estoy-contigo.jpg",
        "prompt": "Vertical macro product video of this spiral kraft notebook on a wooden desk: a hand gently flips open the kraft paper cover revealing crisp white pages inside while placing a sleek black pen beside the black spiral binding, warm natural window lighting, commercial stationery advertisement."
    },
    {
        "id": "03_universitario",
        "img": base_dir / "aportado" / "cuaderno-only-one-way.jpg",
        "prompt": "Vertical smooth cinematic camera orbit and push-in over this large spiral kraft notebook on an artisan wooden desk, warm morning light rays moving softly across the textured cardboard cover and black wire binding, a hand reaches in to touch the notebook cover, high-end commercial look."
    }
]

tasks = []
for p in planes:
    pid = p["id"]
    print(f"Subiendo referencia para {pid}...", flush=True)
    url_img = subir_imagen_publica(p["img"])
    print(f"  URL lista ({len(url_img)} chars)", flush=True)
    for model_try in ["kling-3.0-turbo", "kling-v3", "seedance-2.0-fast"]:
        payload = {
            "model": model_try,
            "prompt": p["prompt"],
            "duration": 5,
            "resolution": "1080P" if "seedance" in model_try else "720p",
            "aspect_ratio": "9:16",
            "image_urls": [url_img]
        }
        r = requests.post("https://api.apimart.ai/v1/videos/generations", headers=headers, json=payload, timeout=60)
        print(f"  POST ({pid} | {model_try}): {r.status_code} -> {r.text[:250]}", flush=True)
        if r.ok:
            data = r.json()
            inner = data.get("data", [{}])[0] if isinstance(data.get("data"), list) else data.get("data", {})
            tid = inner.get("task_id") or data.get("task_id") or data.get("id")
            if tid:
                tasks.append({"id": pid, "task_id": tid, "done": False, "out": out_dir / f"{pid}.mp4", "model": model_try})
                break

print(f"Tareas en cola: {len(tasks)}", flush=True)
for step in range(90):
    if all(t["done"] for t in tasks):
        break
    time.sleep(6)
    for t in tasks:
        if t["done"]:
            continue
        tid = t["task_id"]
        pid = t["id"]
        st_res = requests.get(f"https://api.apimart.ai/v1/tasks/{tid}", headers=headers, timeout=30)
        if not st_res.ok:
            continue
        st_json = st_res.json()
        st_data = st_json.get("data", {}) if isinstance(st_json.get("data"), dict) else {}
        status = (st_data.get("status") or st_json.get("status") or "").lower()
        print(f"  [{pid} | {t['model']}] paso {step+1}: status={status}", flush=True)
        if status in ("completed", "succeeded", "success"):
            videos = st_data.get("result", {}).get("videos", [])
            vurl = None
            if videos:
                u = videos[0].get("url")
                vurl = u[0] if isinstance(u, list) else u
            elif st_data.get("video_url"):
                vurl = st_data["video_url"]
            if vurl:
                print(f"  Descargando {pid} desde {vurl}...", flush=True)
                vbytes = requests.get(vurl, timeout=120).content
                t["out"].write_bytes(vbytes)
                print(f"  GUARDADO: {t['out']} ({len(vbytes)//1024} KB)", flush=True)
                t["done"] = True
        elif status in ("failed", "error", "cancelled"):
            print(f"  ERROR en {pid}: {st_json}", flush=True)
            t["done"] = True

print("Proceso finalizado.", flush=True)
