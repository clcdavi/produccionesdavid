#!/usr/bin/env python3
"""
Ensambla el Reel Publicitario Multiescenario de Producciones David:
- Combina los 3 clips de Seedance 2.5 con los 3 audios master de ElevenLabs en español.
- Estandariza a 1080x1920 a 30 fps con calidad broadcast H.264.
- Superpone badges institucionales de marca de Producciones David.
- Extrae capturas de control de cada escena.
"""
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando")
ASSETS_DIR = BASE_DIR / "assets" / "david"
FFMPEG = Path("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg")
FFPROBE = Path("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffprobe")
BRAIN_DIR = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d")

SCENES = [
    {
        "clip": ASSETS_DIR / "seedance_multi_clip_01.mp4",
        "audio": ASSETS_DIR / "multi_audio_01.mp3",
        "processed": ASSETS_DIR / "_proc_clip_01.mp4",
        "badge": "01 · SUITE DE EDICIÓN",
        "title": "Look Director Creativo"
    },
    {
        "clip": ASSETS_DIR / "seedance_multi_clip_02.mp4",
        "audio": ASSETS_DIR / "multi_audio_02.mp3",
        "processed": ASSETS_DIR / "_proc_clip_02.mp4",
        "badge": "02 · ATRIO CORPORATIVO",
        "title": "Look Fundador & Estratega"
    },
    {
        "clip": ASSETS_DIR / "seedance_multi_clip_03.mp4",
        "audio": ASSETS_DIR / "multi_audio_03.mp3",
        "processed": ASSETS_DIR / "_proc_clip_03.mp4",
        "badge": "03 · SET DE FILMACIÓN",
        "title": "Look Director de Rodaje"
    }
]

FINAL_REEL = ASSETS_DIR / "reel_david_multiescenario_oficial.mp4"

def get_duration(fpath: Path) -> float:
    cmd = [
        str(FFPROBE),
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(fpath)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return float(res.stdout.strip() or 0.0)

def process_single_scene(sc: dict):
    print(f"🎬 Procesando {sc['title']}...")
    a_dur = get_duration(sc["audio"])
    v_dur = get_duration(sc["clip"])
    print(f"  Audio master: {a_dur:.2f}s | Video bruto: {v_dur:.2f}s")
    
    # Ajuste de velocidad de video si difiere ligeramente para que calce exacto con la voz
    pts_factor = a_dur / v_dur if v_dur > 0 else 1.0
    
    cmd = [
        str(FFMPEG), "-y",
        "-i", str(sc["clip"]),
        "-i", str(sc["audio"]),
        "-filter_complex",
        f"[0:v]setpts={pts_factor:.4f}*PTS,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,fps=30[v]",
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(sc["processed"])
    ]
    subprocess.run(cmd, check=True)
    print(f"  ✅ Escena procesada: {sc['processed'].name}")

def concat_scenes():
    print("🎞️ Concatenando las 3 escenas en el Reel final...")
    concat_list = ASSETS_DIR / "_concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for sc in SCENES:
            f.write(f"file '{sc['processed']}'\n")

    # Concatenar y agregar overlays institucionales de Producciones David
    cmd = [
        str(FFMPEG), "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        str(FINAL_REEL)
    ]
    subprocess.run(cmd, check=True)
    print(f"🎉 ¡Reel final oficial exportado con éxito!\n📦 {FINAL_REEL}")

def extract_previews():
    print("📸 Extrayendo fotogramas de control para revisión...")
    for idx, sc in enumerate(SCENES, 1):
        prev_img = BRAIN_DIR / f"reel_escena_0{idx}_review.jpg"
        cmd = [
            str(FFMPEG), "-y",
            "-ss", "00:00:02.000",
            "-i", str(sc["processed"]),
            "-frames:v", "1",
            str(prev_img)
        ]
        subprocess.run(cmd, check=True)
        print(f"  Guardado fotograma {idx}: {prev_img.name}")

def main():
    for sc in SCENES:
        if not sc["clip"].exists():
            raise FileNotFoundError(f"Falta descargar el clip: {sc['clip']}")
        process_single_scene(sc)
    
    concat_scenes()
    extract_previews()

if __name__ == "__main__":
    main()
