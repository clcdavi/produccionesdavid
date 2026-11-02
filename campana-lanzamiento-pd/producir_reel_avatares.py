#!/usr/bin/env python3
"""
Produce el Reel Oficial de Avatares Multiescenario para @produccionesdavid.ar:
1. Genera los 3 clips de 5s en 9:16 con kling-3.0-turbo vía APIMart (en paralelo).
2. Genera 3 voces rioplatenses distintas (es-AR-ElenaNeural, es-AR-TomasNeural, es-UY-ValentinaNeural).
3. Compone las tarjetas de subtítulos en Zona Segura (390px libres abajo) y el cierre de marca.
4. Registra el costo exacto en proyectos_costos.json.
"""
import asyncio
import json
import subprocess
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import edge_tts
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/campana-lanzamiento-pd")
CLAVES_FILE = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/claves_ia.json")
COSTOS_FILE = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/proyectos_costos.json")
FFMPEG = Path("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg")
INST_JSON = Path.home() / "Library" / "Application Support" / "adrian-saenz-video-negocio" / "instalacion.json"
CHROME_BIN = json.loads(INST_JSON.read_text(encoding="utf-8"))["chrome"]

IMG_1 = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d/avatar_01_comercio_gastronomia_jpg_1793569119456.jpg")
IMG_2 = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d/avatar_02_institucional_empresa_jpg_1793569138758.jpg")
IMG_3 = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d/avatar_03_eventos_entretenimiento_jpg_1793569163999.jpg")
CLOSING_JPG = OUT_DIR / "reel_scene_05.jpg"
MUSIC_MP3 = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/negocios/sw-store/musica/musica.mp3")

SCENES = [
    {
        "id": "av_01",
        "img": IMG_1,
        "video_out": OUT_DIR / "av_clip_01.mp4",
        "voice_out": OUT_DIR / "av_voice_01.mp3",
        "voice_id": "es-AR-ElenaNeural",
        "rate": "+8%",
        "text_tts": "¿Querés promocionar tu negocio con videos profesionales, pero no tenés tiempo de grabarte?",
        "pill_top": "🛍️ PERSONAJE 1 • COMERCIOS Y GASTRONOMÍA",
        "sub_text": "“¿Querés promocionar tu negocio con videos profesionales pero no tenés tiempo de grabarte?”",
        "prompt": (
            "Hyper-realistic 9:16 vertical commercial video. The young woman in the café speaks naturally "
            "and expressively directly to the camera with a warm smile, realistic lip movement speaking Spanish, "
            "natural hand gesture while holding the coffee cup, soft background ambience, steady medium shot."
        ),
    },
    {
        "id": "av_02",
        "img": IMG_2,
        "video_out": OUT_DIR / "av_clip_02.mp4",
        "voice_out": OUT_DIR / "av_voice_02.mp3",
        "voice_id": "es-AR-TomasNeural",
        "rate": "+10%",
        "text_tts": "En Producciones David creamos presentadores con inteligencia artificial y clonamos voces para empresas, colegios y comercios.",
        "pill_top": "🏢 PERSONAJE 2 • EMPRESAS E INSTITUCIONES",
        "sub_text": "“En Producciones David creamos presentadores con IA y clonamos voces para empresas, colegios y comercios.”",
        "prompt": (
            "Hyper-realistic 9:16 vertical corporate commercial video. The confident man in the modern glass atrium "
            "speaks clearly and naturally directly to the camera, realistic lip movement and expressive hand gestures "
            "as a presenter, steady medium shot."
        ),
    },
    {
        "id": "av_03",
        "img": IMG_3,
        "video_out": OUT_DIR / "av_clip_03.mp4",
        "voice_out": OUT_DIR / "av_voice_03.mp3",
        "voice_id": "es-UY-ValentinaNeural",
        "rate": "+8%",
        "text_tts": "Cambiamos de personaje, de voz y de ambiente para tu marca o evento. ¡Escribinos por mensaje directo!",
        "pill_top": "🎉 PERSONAJE 3 • FIESTAS Y EVENTOS",
        "sub_text": "“Cambiamos de personaje, de voz y de ambiente para tu marca o evento. ¡Escribinos por MD!”",
        "prompt": (
            "Hyper-realistic 9:16 vertical event commercial video. The energetic young woman presenter in the glamorous "
            "event venue speaks enthusiastically directly to the camera with a radiant smile, realistic lip movements "
            "and expressive hands, warm golden bokeh lights shimmering softly behind her, steady medium shot."
        ),
    },
]


def upload_temp_image(path: Path) -> str:
    res = subprocess.run(
        ["curl", "-sS", "-F", f"files[]=@{path}", "https://uguu.se/upload"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    j = json.loads(res.stdout)
    return j["files"][0]["url"]


def run_kling_task(scene: dict, api_key: str) -> dict:
    out_mp4: Path = scene["video_out"]
    if out_mp4.exists() and out_mp4.stat().st_size > 100_000:
        print(f"✅ Ya existe {out_mp4.name}, reutilizando.")
        return {"id": scene["id"], "task_id": "cached", "usd": 0.572, "creditos": 5.72}

    img_url = upload_temp_image(scene["img"])
    print(f"🚀 Lanzando Kling 3.0 Turbo para {scene['id']} ({img_url})...")
    payload = json.dumps({
        "model": "kling-3.0-turbo",
        "prompt": scene["prompt"],
        "duration": 5,
        "aspect_ratio": "9:16",
        "image_urls": [img_url],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.apimart.ai/v1/videos/generations",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ProduccionesDavidStudio/1.0",
        },
        method="POST",
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))
    data = resp.get("data", resp)
    if isinstance(data, list):
        data = data[0]
    task_id = data["task_id"]
    print(f"⏳ Task {scene['id']} -> {task_id}")

    for _ in range(90):
        time.sleep(5)
        st_req = urllib.request.Request(
            f"https://api.apimart.ai/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {api_key}", "User-Agent": "ProduccionesDavidStudio/1.0"},
        )
        st_Raw = json.loads(urllib.request.urlopen(st_req, timeout=30).read().decode("utf-8"))
        st_data = st_Raw.get("data", st_Raw)
        status = st_data.get("status", "")
        if status == "completed":
            videos = st_data.get("result", {}).get("videos", [])
            v_url = videos[0]["url"]
            if isinstance(v_url, list):
                v_url = v_url[0]
            subprocess.run(["curl", "-sSL", v_url, "-o", str(out_mp4)], check=True)
            usage = st_data.get("usage", {})
            cost_usd = float(usage.get("cost_usd") or 0.572)
            credits = float(usage.get("credits") or round(cost_usd * 10, 2))
            print(f"🎬 Descargado {out_mp4.name} (${cost_usd} USD)")
            return {"id": scene["id"], "task_id": task_id, "usd": cost_usd, "creditos": credits}
        elif status in ("failed", "error", "cancelled"):
            raise RuntimeError(f"Fallo en task {task_id}: {st_data}")

    raise TimeoutError(f"Timeout esperando {task_id}")


async def generate_voices():
    for s in SCENES:
        comm = edge_tts.Communicate(s["text_tts"], s["voice_id"], rate=s["rate"])
        await comm.save(str(s["voice_out"]))
        print("🎙️ Voz generada:", s["voice_out"].name)


def render_overlay_png(pill_top: str, sub_text: str, out_png: Path) -> None:
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Inter:wght@600;700&display=swap');
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{
  width: 1080px;
  height: 1920px;
  background: transparent !important;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}}
.top-pill {{
  position: absolute;
  top: 150px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 23, 42, 0.90);
  border: 2.5px solid #F59E0B;
  color: #FEF3C7;
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: 24px;
  padding: 14px 32px;
  border-radius: 999px;
  white-space: nowrap;
  box-shadow: 0 12px 28px rgba(0,0,0,0.35);
}}
.sub-card {{
  position: absolute;
  bottom: 410px;
  left: 64px;
  right: 64px;
  background: rgba(255, 253, 249, 0.95);
  border: 3px solid #EA580C;
  border-radius: 28px;
  padding: 28px 34px;
  text-align: center;
  box-shadow: 0 20px 45px rgba(0,0,0,0.4);
}}
.sub-card p {{
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: 31px;
  line-height: 1.3;
  color: #0F172A;
}}
</style>
</head>
<body>
  <div class="top-pill">{pill_top}</div>
  <div class="sub-card"><p>{sub_text}</p></div>
</body>
</html>"""
    tmp_html = OUT_DIR / f"_tmp_{out_png.stem}.html"
    tmp_html.write_text(html, encoding="utf-8")
    subprocess.run(
        [
            CHROME_BIN,
            "--headless",
            "--hide-scrollbars",
            "--default-background-color=00000000",
            "--force-device-scale-factor=1",
            "--window-size=1080,1920",
            f"--screenshot={out_png}",
            tmp_html.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    tmp_html.unlink(missing_ok=True)


def main():
    api_key = json.loads(CLAVES_FILE.read_text(encoding="utf-8"))["apimartKey"]

    # 1. Generar las 3 voces en español rioplatense
    asyncio.run(generate_voices())

    # 2. Generar las 3 capas transparentes de subtítulos en Zona Segura
    overlays = []
    for i, s in enumerate(SCENES, 1):
        ov_png = OUT_DIR / f"av_overlay_0{i}.png"
        render_overlay_png(s["pill_top"], s["sub_text"], ov_png)
        overlays.append(ov_png)

    # 3. Generar los 3 videos en paralelo en APIMart (Kling 3.0 Turbo)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = [ex.submit(run_kling_task, s, api_key) for s in SCENES]
        results = [f.result() for f in futures]

    # 4. Armar cada escena de 5.0s con su video + overlay PNG + su voz hablada
    scene_mp4s = []
    for i, s in enumerate(SCENES):
        seg_out = OUT_DIR / f"av_seg_0{i+1}.mp4"
        cmd_seg = [
            str(FFMPEG), "-y",
            "-i", str(s["video_out"]),
            "-i", str(overlays[i]),
            "-i", str(s["voice_out"]),
            "-filter_complex",
            (
                "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[vbase];"
                "[vbase][1:v]overlay=0:0,format=yuv420p[vout];"
                "[2:a]apad=whole_dur=5.0,atrim=0:5.0,volume=1.6[aout]"
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

    # 5. Escena 4 de cierre (3.5s) con silencio de voz para que suba la música
    seg_close = OUT_DIR / "av_seg_04_close.mp4"
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

    # 6. Unir los 4 segmentos + música de fondo suave (14% volumen durante las voces)
    final_reel = OUT_DIR / "reel_avatares_producciones_david.mp4"
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
            "[4:a]atrim=0:18.5,volume=0.14,afade=t=in:st=0:d=0.5,afade=t=out:st=17.0:d=1.5[bgm];"
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
    print("🎉 REEL DE AVATARES MULTIESCENARIO TERMINADO:", final_reel)

    # 7. Actualizar proyectos_costos.json
    try:
        costos = json.loads(COSTOS_FILE.read_text(encoding="utf-8"))
        nuevo_proy = {
            "id": "producciones-david-avatares",
            "cliente": "Producciones David (Reel Avatares Multiescenario)",
            "fecha": "2026-11-01",
            "proveedor": "APIMart (kling-3.0-turbo + 3 Voces IA)",
            "estado": "Completado (Publicidad Propia)",
            "items": [
                {
                    "nombre": f"Avatar {i+1} (5s 9:16)",
                    "task_id": r["task_id"],
                    "modelo": "kling-3.0-turbo",
                    "creditos": r["creditos"],
                    "usd": r["usd"],
                }
                for i, r in enumerate(results)
            ],
            "total_creditos": round(sum(r["creditos"] for r in results), 2),
            "total_usd": round(sum(r["usd"] for r in results), 3),
            "entregable": str(final_reel),
        }
        costos["proyectos"] = [p for p in costos.get("proyectos", []) if p.get("id") != "producciones-david-avatares"]
        costos["proyectos"].insert(0, nuevo_proy)
        COSTOS_FILE.write_text(json.dumps(costos, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print("Aviso al guardar costos:", e)


if __name__ == "__main__":
    main()
