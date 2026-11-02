#!/usr/bin/env python3
import subprocess, json
from pathlib import Path

DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/campana-lanzamiento-pd")
ART = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d")
FFMPEG = "/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg"
INST = json.load(open("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/instalacion.json"))
CHROME = INST["chrome"]

OVERLAYS = [
    {
        "png": DIR / "v_ov_01.png",
        "pill": "🛍️ PERSONAJE 1 • COMERCIOS Y NEGOCIOS",
        "sub": "“Transformamos tu negocio con videos profesionales hechos con inteligencia artificial.”"
    },
    {
        "png": DIR / "v_ov_02.png",
        "pill": "🏢 PERSONAJE 2 • EMPRESAS E INSTITUCIONES",
        "sub": "“Diseñamos voceros virtuales y videos corporativos para empresas e instituciones.”"
    },
    {
        "png": DIR / "v_ov_03.png",
        "pill": "🎉 PERSONAJE 3 • FIESTAS Y EVENTOS",
        "sub": "“Cambiamos de personaje, de voz y de escenario para tu evento. ¡Escribinos por MD!”"
    }
]

# 1. Renderizar overlays
for o in OVERLAYS:
    tmp_stem = o["png"].stem
    tmp = DIR / f"_tmp_{tmp_stem}.html"
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"/>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px; height: 1920px; background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    position: relative; overflow: hidden;
  }}
  .pill {{
    position: absolute; top: 155px; left: 50%; transform: translateX(-50%);
    background: rgba(10, 16, 26, 0.90); border: 3px solid #d4af37; border-radius: 9999px;
    padding: 14px 40px; color: #ffffff; font-size: 26px; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    white-space: nowrap;
  }}
  .sub {{
    position: absolute; bottom: 395px; left: 60px; right: 60px;
    background: rgba(255, 255, 255, 0.96); border: 3px solid #d4af37; border-radius: 28px;
    padding: 30px 42px; box-shadow: 0 18px 45px rgba(0,0,0,0.45); text-align: center;
  }}
  .text {{
    color: #0d1b2a; font-size: 34px; font-weight: 800; line-height: 1.35; letter-spacing: -0.5px;
  }}
</style></head><body>
  <div class="pill">{o['pill']}</div>
  <div class="sub"><div class="text">{o['sub']}</div></div>
</body></html>"""
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000", "--window-size=1080,1920", f"--screenshot={o['png']}", f"file://{tmp.resolve()}"], check=True, capture_output=True)
    tmp.unlink(missing_ok=True)
print("✅ Overlays listos")

# 2. Renderizar segmentos de 5.0s
clips = [DIR / "test_veo31_01.mp4", DIR / "veo31_clip_02.mp4", DIR / "veo31_clip_03.mp4"]
segs = []
for i, clip in enumerate(clips, 1):
    seg = DIR / f"v_seg_0{i}.mp4"
    ov = DIR / f"v_ov_0{i}.png"
    cmd = [
        FFMPEG, "-y",
        "-i", str(clip),
        "-i", str(ov),
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[vbase];"
        "[vbase][1:v]overlay=0:0,format=yuv420p[vout];"
        "[0:a]aresample=44100,volume=1.4[aout]",
        "-map", "[vout]", "-map", "[aout]",
        "-t", "5.0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k",
        str(seg)
    ]
    subprocess.run(cmd, check=True)
    segs.append(seg)
print("✅ Segmentos 1, 2 y 3 listos")

# 3. Placa de cierre
close_seg = DIR / "v_seg_04_close.mp4"
subprocess.run([
    FFMPEG, "-y",
    "-loop", "1", "-t", "3.5", "-i", str(DIR / "reel_scene_05.jpg"),
    "-f", "lavfi", "-t", "3.5", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
    "-vf", "fps=30,setsar=1,format=yuv420p",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    str(close_seg)
], check=True)
segs.append(close_seg)

# 4. Unir los 4 clips + música suave de fondo
final_mp4 = DIR / "reel_avatares_veo31_producciones_david.mp4"
music_mp3 = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/negocios/sw-store/musica/musica.mp3")

cmd_final = [
    FFMPEG, "-y",
    "-i", str(segs[0]),
    "-i", str(segs[1]),
    "-i", str(segs[2]),
    "-i", str(segs[3]),
    "-i", str(music_mp3),
    "-filter_complex",
    "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a]concat=n=4:v=1:a=1[vcat][acat];"
    "[4:a]atrim=0:18.5,volume=0.08,afade=t=in:st=0:d=0.5,afade=t=out:st=16.5:d=2.0[bgm];"
    "[acat][bgm]amix=inputs=2:duration=first:dropout_transition=0[aout]",
    "-map", "[vcat]", "-map", "[aout]",
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    str(final_mp4)
]
subprocess.run(cmd_final, check=True)

subprocess.run(["cp", str(final_mp4), str(ART / "reel_avatares_veo31_producciones_david.mp4")], check=True)
print("🎉 REEL OFICIAL FINAL ENSAMBLADO CON ÉXITO:", final_mp4)
