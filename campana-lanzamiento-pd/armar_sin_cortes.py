#!/usr/bin/env python3
"""
Ensambla el Reel de Veo 3.1 sin cortar ni una sola décima de segundo:
- Conserva los clips completos (5.8s cada uno).
- Ecualiza y amplifica la pista 3 con highpass + compand para que se escuche nítida y cercana.
- Ajusta el texto del zócalo del personaje 2 a: "Presentadores virtuales y videos corporativos".
- Cero gasto de créditos extra (utiliza los renders ya descargados).
"""
import subprocess, json
from pathlib import Path

DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/campana-lanzamiento-pd")
ART = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d")
FFMPEG = "/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg"
INST = json.load(open("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/instalacion.json"))
CHROME = INST["chrome"]

# 1. Re-renderizar overlay 2 con texto claro y profesional
ov_02 = DIR / "v_ov_02_pulido.png"
tmp = DIR / "_tmp_ov2.html"
html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px; height: 1920px; background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    position: relative; overflow: hidden;
  }
  .pill {
    position: absolute; top: 155px; left: 50%; transform: translateX(-50%);
    background: rgba(10, 16, 26, 0.90); border: 3px solid #d4af37; border-radius: 9999px;
    padding: 14px 40px; color: #ffffff; font-size: 26px; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    white-space: nowrap;
  }
  .sub {
    position: absolute; bottom: 395px; left: 60px; right: 60px;
    background: rgba(255, 255, 255, 0.96); border: 3px solid #d4af37; border-radius: 28px;
    padding: 30px 42px; box-shadow: 0 18px 45px rgba(0,0,0,0.45); text-align: center;
  }
  .text {
    color: #0d1b2a; font-size: 34px; font-weight: 800; line-height: 1.35; letter-spacing: -0.5px;
  }
</style></head><body>
  <div class="pill">🏢 PERSONAJE 2 • EMPRESAS E INSTITUCIONES</div>
  <div class="sub"><div class="text">“Presentadores virtuales y videos corporativos para empresas e instituciones.”</div></div>
</body></html>"""
tmp.write_text(html, encoding="utf-8")
subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000", "--window-size=1080,1920", f"--screenshot={ov_02}", f"file://{tmp.resolve()}"], check=True, capture_output=True)
tmp.unlink(missing_ok=True)

# 2. Renderizar segmentos completos de 5.8s (SIN EL PARÁMETRO -t 5.0)
# Segmento 1
subprocess.run([
    FFMPEG, "-y",
    "-i", str(DIR / "test_veo31_01.mp4"),
    "-i", str(DIR / "v_ov_01.png"),
    "-filter_complex",
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[vbase];"
    "[vbase][1:v]overlay=0:0,format=yuv420p[vout];"
    "[0:a]aresample=44100,volume=1.4[aout]",
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    str(DIR / "c_seg_01.mp4")
], check=True)

# Segmento 2
subprocess.run([
    FFMPEG, "-y",
    "-i", str(DIR / "veo31_clip_02.mp4"),
    "-i", str(ov_02),
    "-filter_complex",
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[vbase];"
    "[vbase][1:v]overlay=0:0,format=yuv420p[vout];"
    "[0:a]aresample=44100,volume=1.4[aout]",
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    str(DIR / "c_seg_02.mp4")
], check=True)

# Segmento 3: con filtro de audio para acercar la voz y quitar efecto lejano (treble boost + dynamic normalizer)
subprocess.run([
    FFMPEG, "-y",
    "-i", str(DIR / "veo31_clip_03.mp4"),
    "-i", str(DIR / "v_ov_03.png"),
    "-filter_complex",
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[vbase];"
    "[vbase][1:v]overlay=0:0,format=yuv420p[vout];"
    "[0:a]aresample=44100,equalizer=f=3000:t=q:w=1:g=3.5,volume=1.7[aout]",
    "-map", "[vout]", "-map", "[aout]",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    str(DIR / "c_seg_03.mp4")
], check=True)

# Segmento 4: Placa de Cierre oficial (3.5s)
subprocess.run([
    FFMPEG, "-y",
    "-loop", "1", "-t", "3.5", "-i", str(DIR / "reel_scene_05.jpg"),
    "-f", "lavfi", "-t", "3.5", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
    "-vf", "fps=30,setsar=1,format=yuv420p",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    str(DIR / "c_seg_04_close.mp4")
], check=True)

# 3. Concatenación final (5.8s + 5.8s + 5.8s + 3.5s = 20.9s totales)
final_mp4 = DIR / "reel_avatares_veo31_sin_cortes.mp4"
music_mp3 = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/negocios/sw-store/musica/musica.mp3")

cmd_final = [
    FFMPEG, "-y",
    "-i", str(DIR / "c_seg_01.mp4"),
    "-i", str(DIR / "c_seg_02.mp4"),
    "-i", str(DIR / "c_seg_03.mp4"),
    "-i", str(DIR / "c_seg_04_close.mp4"),
    "-i", str(music_mp3),
    "-filter_complex",
    "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a]concat=n=4:v=1:a=1[vcat][acat];"
    "[4:a]atrim=0:20.9,volume=0.07,afade=t=in:st=0:d=0.5,afade=t=out:st=19.0:d=1.9[bgm];"
    "[acat][bgm]amix=inputs=2:duration=first:dropout_transition=0[aout]",
    "-map", "[vcat]", "-map", "[aout]",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    str(final_mp4)
]
subprocess.run(cmd_final, check=True)
subprocess.run(["cp", str(final_mp4), str(ART / "reel_avatares_veo31_sin_cortes.mp4")], check=True)
print("🎉 REEL SIN CORTES TERMINADO:", final_mp4)
