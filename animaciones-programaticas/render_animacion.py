#!/usr/bin/env python3
"""
Motor de Renderizado Frame-a-Frame para Animaciones Programáticas HTML5
Basado en la metodología de Saúl Vicente:
- Evaluación determinística de window.__t(t)
- Captura sin pérdida vía Playwright Chromium
- Compresión directa a MP4 H.264 vía ffmpeg
- CERO pérdida de fotogramas, CERO lag de grabación de pantalla
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

FFMPEG_BIN = Path("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg")

def render(html_path: Path, output_mp4: Path, duration: float = 8.0, fps: int = 30, width: int = 1080, height: int = 1350):
    if not html_path.exists():
        raise FileNotFoundError(f"No existe el archivo HTML: {html_path}")
    if not FFMPEG_BIN.exists():
        raise FileNotFoundError(f"No existe el binario de ffmpeg en: {FFMPEG_BIN}")

    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    total_frames = int(duration * fps)

    print(f"🎬 Iniciando renderizado de: {html_path.name}")
    print(f"📐 Resolución: {width}x{height} | Duración: {duration}s | FPS: {fps} | Total fotogramas: {total_frames}")

    # Iniciar proceso ffmpeg con pipe de entrada stdin
    ffmpeg_cmd = [
        str(FFMPEG_BIN),
        "-y",
        "-f", "image2pipe",
        "-vcodec", "png",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-movflags", "+faststart",
        str(output_mp4)
    ]

    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    t0 = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Configurar viewport exacto
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        page.wait_for_timeout(500) # Dejar que carguen fuentes locales

        for frame_idx in range(total_frames):
            t = frame_idx / fps
            # Ejecutar el estado de la animación en el instante exacto t
            page.evaluate(f"window.__t && window.__t({t});")
            # Capturar fotograma PNG
            png_bytes = page.screenshot(type="png", clip={"x": 0, "y": 0, "width": width, "height": height})
            ffmpeg_proc.stdin.write(png_bytes)

            if frame_idx % 30 == 0 or frame_idx == total_frames - 1:
                percent = ((frame_idx + 1) / total_frames) * 100
                elapsed = time.time() - t0
                print(f"⏳ Progreso: {frame_idx + 1}/{total_frames} ({percent:.1f}%) — {elapsed:.1f}s transcurridos")

        browser.close()

    ffmpeg_proc.stdin.close()
    stderr_output = ffmpeg_proc.stderr.read().decode("utf-8", errors="replace")
    ffmpeg_proc.wait()

    if ffmpeg_proc.returncode != 0:
        raise RuntimeError(f"Error en ffmpeg (código {ffmpeg_proc.returncode}):\n{stderr_output}")

    filesize_mb = output_mp4.stat().st_size / (1024 * 1024)
    print(f"✅ ¡Video MP4 generado exitosamente!")
    print(f"📦 Destino: {output_mp4}")
    print(f"⚖️ Peso: {filesize_mb:.2f} MB | Tiempo total: {time.time() - t0:.1f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Renderiza animaciones HTML a MP4")
    parser.add_argument("html", type=Path, help="Ruta al archivo .html")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Ruta del video .mp4 de salida")
    parser.add_argument("-d", "--duration", type=float, default=8.0, help="Duración en segundos (def: 8.0)")
    parser.add_argument("-r", "--fps", type=int, default=30, help="Fotogramas por segundo (def: 30)")
    parser.add_argument("-w", "--width", type=int, default=1080, help="Ancho (def: 1080)")
    parser.add_argument("-H", "--height", type=int, default=1350, help="Alto (def: 1350)")

    args = parser.parse_args()
    out = args.output or args.html.with_suffix(".mp4")
    render(args.html, out, duration=args.duration, fps=args.fps, width=args.width, height=args.height)
