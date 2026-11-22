#!/usr/bin/env python3
"""
Publicidad cinematográfica Producciones David — rostro real de David.
Genera 3 clips de 8 s con Veo 3.1 Fast (APIMart): voz nativa + lip-sync en una sola llamada.

Privacidad: las imágenes se suben SOLO al endpoint oficial de APIMart
(/v1/uploads/images, expiran en 72 h). Nunca a hostings públicos (uguu, catbox, etc.).

Uso:
  python3 generar_clips_veo.py            # genera las 3 escenas
  python3 generar_clips_veo.py esc_02     # regenera solo una escena
"""
import json
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
KF = BASE / "keyframes"
CLIPS = BASE / "clips"
CLIPS.mkdir(exist_ok=True)
API = "https://api.apimart.ai/v1"
API_KEY = json.loads((ROOT / "claves_ia.json").read_text(encoding="utf-8"))["apimartKey"]
COSTOS_FILE = ROOT / "proyectos_costos.json"
MODEL = "veo3.1-fast"

IDENTIDAD = (
    "Keep the man's face EXACTLY as in the start frame: same identity, facial structure, short dark buzzed hair, "
    "thick straight eyebrows, dark brown eyes, broad nose, full lips, short dark goatee and mustache, natural skin texture. "
    "No face morphing, no beautification, no age change."
)
VOZ = (
    "He speaks in Argentine Rioplatense Spanish (Buenos Aires accent), male voice, warm, confident, mid-low pitch, "
    "natural pace with clear diction. Precise, frame-accurate lip-sync: mouth shapes match every syllable. "
    "Hyperrealistic micro-expressions, natural blinking, subtle head and shoulder movement, breathing."
)
LIMPIO = "Clean dialogue audio with subtle studio room tone, no background music, no on-screen text, no subtitles, no captions, no logos."

SCENES = [
    {
        "id": "esc_01",
        "img": KF / "kf_01_hook.jpg",
        "dialogo": "¿Y si tu marca tuviera un comercial de cine… sin rodar un solo día?",
        "camara": "Medium close-up in a dark film studio, warm tungsten rim light from behind-left, cinema camera bokeh on the right. "
                  "Very slow push-in. He raises his eyebrows slightly on the question, intrigued half-smile at the end.",
    },
    {
        "id": "esc_02",
        "img": KF / "kf_02_servicio.jpg",
        "dialogo": "En Producciones David creamos videos profesionales con inteligencia artificial para empresas e instituciones.",
        "camara": "Medium shot in a moody post-production suite with color-grading monitors behind him, teal and warm terracotta practical light. "
                  "Slow cinematic dolly-in. One subtle, natural open-hand gesture while explaining, then returns to rest.",
    },
    {
        "id": "esc_03",
        "img": KF / "kf_03_cta.jpg",
        "dialogo": "Vos nos contás la idea. Te lo entregamos en 48 a 72 horas. Escribinos.",
        "camara": "Medium close-up, charcoal seamless background with soft terracotta circular back-light glow, clean 45-degree key light, 85mm look. "
                  "Static camera with very gentle drift. Confident warm smile, small affirmative nod on 'Escribinos'.",
    },
]


def http_json(url, payload=None, timeout=60):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST" if data else "GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def upload_apimart(path: Path) -> str:
    """Subida privada al storage oficial de APIMart (expira en 72 h)."""
    res = subprocess.run(
        ["curl", "-sS", "-m", "120", "-X", "POST", f"{API}/uploads/images",
         "-H", f"Authorization: Bearer {API_KEY}", "-F", f"file=@{path}"],
        capture_output=True, text=True, check=True,
    )
    body = json.loads(res.stdout)
    if "url" not in body:
        raise RuntimeError(f"Upload falló para {path.name}: {body}")
    return body["url"]


def build_prompt(sc):
    # Sin comillas alrededor del diálogo: Veo tiende a quemar subtítulos (con errores) cuando el texto va entre comillas.
    return (
        f"No subtitles, no captions, no text overlays of any kind. "
        f"9:16 vertical cinematic commercial, shot on ARRI Alexa, anamorphic, shallow depth of field, film grain. "
        f"{sc['camara']} The man looks directly into the lens and speaks in Spanish. He says: {sc['dialogo']} "
        f"{VOZ} Eyes stay naturally open and focused on the lens (normal blinks only). {IDENTIDAD} {LIMPIO} "
        f"The frame must remain completely free of any written words."
    )


def run_scene(sc):
    out = CLIPS / f"{sc['id']}.mp4"
    img_url = upload_apimart(sc["img"])
    print(f"⬆️  {sc['id']}: imagen subida a APIMart (privada, 72 h)")
    resp = http_json(f"{API}/videos/generations", {
        "model": MODEL,
        "prompt": build_prompt(sc),
        "duration": 8,
        "aspect_ratio": "9:16",
        "resolution": "1080p",
        "image_urls": [img_url],
    })
    d = resp.get("data")
    task_id = d[0]["task_id"] if isinstance(d, list) else d["task_id"]
    print(f"⏳ {sc['id']} → {task_id}")
    for _ in range(120):  # hasta 10 min
        time.sleep(5)
        s = http_json(f"{API}/tasks/{task_id}").get("data", {})
        st = str(s.get("status", "")).lower()
        if st in ("completed", "succeeded", "success"):
            vurl = s["result"]["videos"][0]["url"]
            vurl = vurl[0] if isinstance(vurl, list) else vurl
            subprocess.run(["curl", "-sL", vurl, "-o", str(out)], check=True)
            cost = s.get("cost")
            print(f"🎬 {sc['id']} listo → {out.name} (costo: {cost})")
            return {"nombre": f"{sc['id']} (8s 9:16 1080p)", "task_id": task_id, "modelo": MODEL, "usd": cost}
        if st in ("failed", "error", "cancelled"):
            raise RuntimeError(f"{sc['id']} falló: {json.dumps(s, ensure_ascii=False)[:500]}")
    raise TimeoutError(f"{sc['id']} superó 10 min")


def registrar_costos(items):
    try:
        data = json.loads(COSTOS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return
    total = round(sum(float(i["usd"] or 0) for i in items), 4)
    data.setdefault("proyectos", []).append({
        "id": f"pd-cinematica-rostro-david-{int(time.time())}",
        "cliente": "Producciones David (Publicidad cinematográfica con rostro de David)",
        "fecha": str(date.today()),
        "proveedor": f"APIMart ({MODEL}, voz nativa + lip-sync)",
        "estado": "Clips generados",
        "items": items,
        "total_usd": total,
    })
    COSTOS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"💰 Costo registrado: US${total}")


if __name__ == "__main__":
    only = set(sys.argv[1:])
    todo = [s for s in SCENES if not only or s["id"] in only]
    results, errors = [], []
    with ThreadPoolExecutor(max_workers=3) as ex:
        for fut in [ex.submit(run_scene, s) for s in todo]:
            try:
                results.append(fut.result())
            except Exception as e:
                errors.append(str(e))
                print(f"❌ {e}")
    if results:
        registrar_costos(results)
    sys.exit(1 if errors else 0)
