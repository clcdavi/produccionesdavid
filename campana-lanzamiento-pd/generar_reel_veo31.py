#!/usr/bin/env python3
"""
Produce el Reel Oficial de Avatares Multiescenario para @produccionesdavid.ar
utilizando el motor Veo 3.1 (Google) con voz humana nativa y lip-sync realista.
"""
import json
import subprocess
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OUT_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/campana-lanzamiento-pd")
ART_DIR = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d")
CLAVES_FILE = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/claves_ia.json")
COSTOS_FILE = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/proyectos_costos.json")
FFMPEG = Path("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg")
INST_JSON = Path.home() / "Library" / "Application Support" / "adrian-saenz-video-negocio" / "instalacion.json"
CHROME_BIN = json.loads(INST_JSON.read_text(encoding="utf-8"))["chrome"]

IMG_1 = ART_DIR / "avatar_01_comercio_gastronomia_jpg_1793569119456.jpg"
IMG_2 = ART_DIR / "avatar_02_institucional_empresa_jpg_1793569138758.jpg"
IMG_3 = ART_DIR / "avatar_03_eventos_entretenimiento_jpg_1793569163999.jpg"
CLOSING_JPG = OUT_DIR / "reel_scene_05.jpg"
MUSIC_MP3 = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/negocios/sw-store/musica/musica.mp3")

SCENES = [
    {
        "id": "veo_01",
        "img": IMG_1,
        "video_out": OUT_DIR / "test_veo31_01.mp4",  # Ya generado perfectamente
        "pill_top": "🛍️ PERSONAJE 1 • COMERCIOS Y GASTRONOMÍA",
        "sub_text": "“Transformamos tu negocio con videos profesionales hechos con inteligencia artificial.”",
        "prompt": (
            "9:16 vertical commercial video. The young woman in the boutique cafe smiles warmly at the camera "
            "and speaks clearly and naturally in Argentine Spanish (acento argentino de Buenos Aires, dicción clara y fluida, voz cálida y profesional), "
            "saying: \"Transformamos tu negocio con videos profesionales hechos con inteligencia artificial.\" "
            "Realistic lip-sync, natural hand movement, soft cafe background."
        ),
        "pre_existing": True,
    },
    {
        "id": "veo_02",
        "img": IMG_2,
        "video_out": OUT_DIR / "veo31_clip_02.mp4",
        "pill_top": "🏢 PERSONAJE 2 • EMPRESAS E INSTITUCIONES",
        "sub_text": "“Creamos presentadores virtuales y clonamos voces para empresas, marcas y colegios.”",
        "prompt": (
            "9:16 vertical corporate commercial video. The confident Argentine man in modern business attire in the glass atrium "
            "looks directly at the camera with an open professional posture and speaks clearly and fluently in Argentine Spanish "
            "(acento rioplatense argentino claro, dicción corporativa perfecta y segura), "
            "saying: \"Creamos presentadores virtuales y clonamos voces para empresas, marcas y colegios.\" "
            "Precise lip-sync, subtle confident hand gesture, bright corporate atrium background."
        ),
        "pre_existing": False,
    },
    {
        "id": "veo_03",
        "img": IMG_3,
        "video_out": OUT_DIR / "veo31_clip_03.mp4",
        "pill_top": "🎉 PERSONAJE 3 • FIESTAS Y EVENTOS",
        "sub_text": "“Cambiamos de personaje, de voz y de escenario para tu evento. ¡Escribinos por mensaje directo!”",
        "prompt": (
            "9:16 vertical entertainment commercial video. The elegant, charismatic Argentine woman in evening attire at the festive outdoor event "
            "smiles with radiant energy directly at the camera and speaks with enthusiasm and clarity in Argentine Spanish "
            "(dicción rioplatense alegre, clara y natural), "
            "saying: \"Cambiamos de personaje, de voz y de escenario para tu evento. ¡Escribinos por mensaje directo!\" "
            "Natural animated lip-sync, expressive hand motion, warm bokeh event lights in background."
        ),
        "pre_existing": False,
    },
]

def upload_image(path: Path) -> str:
    res = subprocess.run(
        ["curl", "-s", "-F", f"files[]=@{path}", "https://uguu.se/upload"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(res.stdout)["files"][0]["url"]

def render_overlay_png(pill: str, text: str, out_png: Path):
    tmp_html = OUT_DIR / f"_tmp_{out_png.stem}.html"
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    width: 1080px;
    height: 1920px;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    position: relative;
    overflow: hidden;
  }}
  .pill-header {{
    position: absolute;
    top: 155px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(10, 16, 26, 0.88);
    border: 3px solid #d4af37;
    border-radius: 9999px;
    padding: 14px 38px;
    color: #ffffff;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    white-space: nowrap;
  }}
  .sub-box {{
    position: absolute;
    bottom: 395px; /* Arriba de la Zona Segura de 390px */
    left: 60px;
    right: 60px;
    background: rgba(255, 255, 255, 0.96);
    border: 3px solid #d4af37;
    border-radius: 28px;
    padding: 30px 42px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.45);
    text-align: center;
  }}
  .sub-text {{
    color: #0d1b2a;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.35;
    letter-spacing: -0.5px;
  }}
</style>
</head>
<body>
  <div class="pill-header">{pill}</div>
  <div class="sub-box">
    <div class="sub-text">{text}</div>
  </div>
</body>
</html>
"""
    tmp_html.write_text(html_content, encoding="utf-8")
    subprocess.run(
        [
            CHROME_BIN,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--default-background-color=00000000",
            "--window-size=1080,1920",
            f"--screenshot={out_png}",
            f"file://{tmp_html.resolve()}",
        ],
        check=True,
        capture_output=True,
    )
    tmp_html.unlink(missing_ok=True)

def generate_veo_clip(scene: dict, api_key: str):
    if scene.get("pre_existing") and scene["video_out"].exists():
        print(f"⏩ Usando clip existente: {scene['id']}")
        return {"id": scene["id"], "cost": 0.14, "task_id": "test_veo31_01"}

    img_url = upload_image(scene["img"])
    print(f"🚀 Enviando a Veo 3.1: {scene['id']} ({img_url})...")
    payload = {
        "model": "veo3.1-fast",
        "prompt": scene["prompt"],
        "duration": 5,
        "resolution": "1080P",
        "aspect_ratio": "9:16",
        "image_urls": [img_url],
    }
    req = urllib.request.Request(
        "https://api.apimart.ai/v1/videos/generations",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=40) as r:
        resp = json.loads(r.read().decode())
    task_id = resp["data"][0]["task_id"] if isinstance(resp.get("data"), list) else resp["data"]["task_id"]
    print(f"⏳ Task {scene['id']} -> {task_id}")

    for _ in range(60):
        time.sleep(5)
        sreq = urllib.request.Request(f"https://api.apimart.ai/v1/tasks/{task_id}", headers={"Authorization": f"Bearer {api_key}", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(sreq, timeout=30) as sr:
            sdata = json.loads(sr.read().decode()).get("data", {})
        st = sdata.get("status", "").lower()
        if st in ("completed", "succeeded", "success"):
            vurl = sdata["result"]["videos"][0]["url"]
            if isinstance(vurl, list): vurl = vurl[0]
            subprocess.run(["curl", "-sL", vurl, "-o", str(scene["video_out"])], check=True)
            print(f"🎬 Descargado {scene['id']}: {scene['video_out']} (${sdata.get('cost')} USD)")
            return {"id": scene["id"], "cost": sdata.get("cost", 0.14), "task_id": task_id}
        elif st in ("failed", "error"):
            raise RuntimeError(f"Fallo {scene['id']}: {sdata}")
    raise TimeoutError(f"Timeout {scene['id']}")

def main():
    api_key = json.loads(CLAVES_FILE.read_text(encoding="utf-8"))["apimartKey"]

    # 1. Generar overlays transparentes en zona segura
    overlays = []
    for i, s in enumerate(SCENES, 1):
        ov_png = OUT_DIR / f"veo_overlay_0{i}.png"
        render_overlay_png(s["pill_top"], s["sub_text"], ov_png)
        overlays.append(ov_png)

    # 2. Generar clips 2 y 3 en paralelo con Veo 3.1
    tasks_to_run = [s for s in SCENES if not s.get("pre_existing")]
    with ThreadPoolExecutor(max_workers=2) as ex:
        futures = [ex.submit(generate_veo_clip, s, api_key) for s in tasks_to_run]
        results = [f.result() for f in futures]

    # 3. Armar cada segmento de 5s aplicando el overlay PNG sobre el video y conservando el audio nativo
    scene_mp4s = []
    for i, s in enumerate(SCENES):
        seg_out = OUT_DIR / f"veo_seg_0{i+1}.mp4"
        cmd_seg = [
            str(FFMPEG), "-y",
            "-i", str(s["video_out"]),
            "-i", str(overlays[i]),
            "-filter_complex",
            (
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[vbase];"
                "[vbase][1:v]overlay=0:0,format=yuv420p[vout];"
                "[0:a]aresample=44100,volume=1.4[aout]"
            ),
            "-map", "[vout]",
            "-map", "[aout]",
            "-t", "5.0",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k",
            str(seg_out),
        ]
        subprocess.run(cmd_seg, check=True)
        scene_mp4s.append(seg_out)

    # 4. Placa de Cierre oficial (3.5s) con logo y llamado a la acción
    seg_close = OUT_DIR / "veo_seg_04_close.mp4"
    subprocess.run(
        [
            str(FFMPEG), "-y",
            "-loop", "1", "-t", "3.5", "-i", str(CLOSING_JPG),
            "-f", "lavfi", "-t", "3.5", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-vf", "fps=30,setsar=1,format=yuv420p",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(seg_close),
        ],
        check=True,
    )
    scene_mp4s.append(seg_close)

    # 5. Concatenar los 4 segmentos + música de fondo elegante muy suave (10% durante los personajes)
    final_reel = OUT_DIR / "reel_avatares_veo31_producciones_david.mp4"
    cmd_final = [
        str(FFMPEG), "-y",
        "-i", str(scene_mp4s[0]),
        "-i", str(scene_mp4s[1]),
        "-i", str(scene_mp4s[2]),
        "-i", str(scene_mp4s[3]),
        "-i", str(MUSIC_MP3),
        "-filter_complex",
        (
            "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a]concat=n=4:v=1:a=1[vcat][acat];"
            "[4:a]atrim=0:18.5,volume=0.10,afade=t=in:st=0:d=0.5,afade=t=out:st=16.5:d=2.0[bgm];"
            "[acat][bgm]amix=inputs=2:duration=first:dropout_transition=0[aout]"
        ),
        "-map", "[vcat]",
        "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "19",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(final_reel),
    ]
    subprocess.run(cmd_final, check=True)
    
    # Copiar a artifacts para visualización
    art_final = ART_DIR / "reel_avatares_veo31_producciones_david.mp4"
    subprocess.run(["cp", str(final_reel), str(art_final)], check=True)
    print("🎉 REEL OFICIAL VEO 3.1 TERMINADO:", final_reel)

if __name__ == "__main__":
    main()
