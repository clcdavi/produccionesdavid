#!/usr/bin/env python3
"""
Genera las 3 pistas de audio con la voz clonada de David Correa en ElevenLabs
para el Reel Publicitario Multiescenario.
"""
import json
import urllib.request
import subprocess
from pathlib import Path

KEY_FILE = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/claves_ia.json")
OUT_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/assets/david")
OUT_DIR.mkdir(parents=True, exist_ok=True)

claves = json.loads(KEY_FILE.read_text(encoding="utf-8"))
api_key = claves["elevenlabsKey"]
voice_id = "0iKA067p75M8btoee3b1" # David Correa
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

SCENES = [
    {
        "id": "multi_audio_01",
        "title": "Escena 1 · Gancho (Suite de Edición)",
        "text": "Si querés que los videos de tu marca tengan calidad de cine real, esto te va a interesar.",
    },
    {
        "id": "multi_audio_02",
        "title": "Escena 2 · Solución (Atrio Corporativo)",
        "text": "En Producciones David unimos dirección de arte con Inteligencia Artificial para entregar en cuarenta y ocho a setenta y dos horas.",
    },
    {
        "id": "multi_audio_03",
        "title": "Escena 3 · Cierre (Set de Rodaje)",
        "text": "Spots de producto, gastronómicos y avatares listos para vender. Escribinos y llevá tu marca al siguiente nivel.",
    }
]

def generate_voice(scene: dict):
    out_file = OUT_DIR / f"{scene['id']}.mp3"
    print(f"🎙️ Generando {scene['title']}...")
    payload = {
        "text": scene["text"],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.70,
            "similarity_boost": 0.82,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        out_file.write_bytes(resp.read())
    
    # Comprobar duración con ffprobe
    cmd = [
        "/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(out_file)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    dur = float(res.stdout.strip() or 0.0)
    print(f"✅ {out_file.name} generado: {dur:.2f}s ({out_file.stat().st_size} bytes)")
    return {"id": scene["id"], "file": out_file, "duration": dur}

def main():
    results = []
    for sc in SCENES:
        r = generate_voice(sc)
        results.append(r)
    total_dur = sum(r["duration"] for r in results)
    print(f"\n🎉 3 audios generados exitosamente. Duración total: {total_dur:.2f}s")

if __name__ == "__main__":
    main()
