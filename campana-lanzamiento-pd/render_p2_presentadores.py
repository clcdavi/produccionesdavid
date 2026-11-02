#!/usr/bin/env python3
import json, subprocess, time, urllib.request
from pathlib import Path

CLAVES_FILE = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/claves_ia.json")
api_key = json.loads(CLAVES_FILE.read_text())["apimartKey"]
DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/campana-lanzamiento-pd")
OUT_MP4 = DIR / "veo31_clip_02_presentadores.mp4"

# Frase exacta pedida por el usuario
prompt = (
    "9:16 vertical corporate commercial video. A friendly, confident businessman in an elegant dark blue suit and tie "
    "standing in a bright modern office lobby smiles warmly at the camera and speaks clearly and fluently in Spanish: "
    "\"Presentadores virtuales y videos corporativos para empresas e instituciones.\" "
    "Natural speech, clear voice, authentic lip movement, subtle confident hand gesture, bright modern architecture background."
)

payload = {
    "model": "veo3.1-fast",
    "prompt": prompt,
    "duration": 5,
    "resolution": "1080P",
    "aspect_ratio": "9:16"
}

req = urllib.request.Request(
    "https://api.apimart.ai/v1/videos/generations",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    method="POST"
)
with urllib.request.urlopen(req, timeout=40) as r:
    resp = json.loads(r.read().decode())
task_id = resp["data"][0]["task_id"] if isinstance(resp.get("data"), list) else resp["data"]["task_id"]
print(f"Task P2 Presentadores lanzada: {task_id}")

for _ in range(50):
    time.sleep(5)
    sreq = urllib.request.Request(f"https://api.apimart.ai/v1/tasks/{task_id}", headers={"Authorization": f"Bearer {api_key}", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(sreq, timeout=30) as sr:
        sdata = json.loads(sr.read().decode()).get("data", {})
    st = sdata.get("status", "").lower()
    prog = sdata.get("progress", 0)
    print(f"Status P2: {st} ({prog}%)")
    if st in ("completed", "succeeded", "success"):
        vurl = sdata["result"]["videos"][0]["url"]
        if isinstance(vurl, list): vurl = vurl[0]
        subprocess.run(["curl", "-sL", vurl, "-o", str(OUT_MP4)], check=True)
        print("🎬 Descargado P2 con la frase exacta! Costo USD:", sdata.get("cost"))
        break
    elif st in ("failed", "error"):
        print("Fallo:", sdata)
        break
