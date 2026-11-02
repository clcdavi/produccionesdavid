#!/usr/bin/env python3
"""
Publica el Reel Oficial de Avatares Veo 3.1 en @produccionesdavid.ar
utilizando el servidor MCP de Instagram (subida a Uguu + creación de contenedor + publicación).
"""
import json, subprocess, time, urllib.request
from pathlib import Path

DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/campana-lanzamiento-pd")
CREDS = json.loads(Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/instagram_credenciales.json").read_text())
VIDEO_FILE = DIR / "reel_avatares_veo31_final_aprobado.mp4"

token = CREDS["access_token"]
user_id = CREDS["ig_user_id"]

# 1. Subir a servidor público para que Meta lo descargue (Uguu)
print("Subiendo video a servidor público...")
res = subprocess.run(["curl", "-s", "-F", f"files[]=@{VIDEO_FILE}", "https://uguu.se/upload"], capture_output=True, text=True, check=True)
public_url = json.loads(res.stdout)["files"][0]["url"]
print("URL pública:", public_url)

caption = (
    "🎭 ¿Querés promocionar tu negocio o evento sin tiempo para grabarte?\n\n"
    "En Producciones David creamos presentadores con Inteligencia Artificial y clonación de voz "
    "adaptados a cualquier rubro:\n\n"
    "🛍️ Comercios, Marcas y Gastronomía\n"
    "🏢 Empresas, Pymes e Instituciones\n"
    "🎉 Fiestas, Galas y Eventos\n\n"
    "📍 Zona Norte, Bs. As. | Proyectos para todo el país\n"
    "👇 Consultá precios y disponibilidad por Mensaje Directo!\n\n"
    "#ProduccionesDavid #AvataresIA #VideosComerciales #InteligenciaArtificial #MarketingDigital #ZonaNorte #SanFernando #Tigre #SanIsidro #BuenosAires #ReelsArgentina #EmprendedoresArgentinos"
)

# 2. Crear contenedor Reel con share_to_feed: true
print("Creando contenedor Reel en Meta...")
params = urllib.parse.urlencode({
    "media_type": "REELS",
    "video_url": public_url,
    "caption": caption,
    "share_to_feed": "true",
    "access_token": token
})
req = urllib.request.Request(f"https://graph.facebook.com/v26.0/{user_id}/media", data=params.encode(), method="POST")
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.loads(r.read().decode())
container_id = data["id"]
print("Contenedor Reel ID:", container_id)

# 3. Esperar a que Meta procese el video
for i in range(30):
    time.sleep(5)
    surl = f"https://graph.facebook.com/v26.0/{container_id}?fields=status_code,status&access_token={token}"
    with urllib.request.urlopen(surl, timeout=30) as r:
        sdata = json.loads(r.read().decode())
    st = sdata.get("status_code", "")
    print(f"Estado de procesamiento Meta: {st}")
    if st == "FINISHED":
        break
    elif st == "ERROR":
        raise RuntimeError(f"Error procesando Reel en Meta: {sdata}")

# 4. Publicar Reel
print("Publicando Reel...")
pub_params = urllib.parse.urlencode({
    "creation_id": container_id,
    "access_token": token
})
preq = urllib.request.Request(f"https://graph.facebook.com/v26.0/{user_id}/media_publish", data=pub_params.encode(), method="POST")
with urllib.request.urlopen(preq, timeout=60) as r:
    pdata = json.loads(r.read().decode())
reel_published_id = pdata["id"]
print("🎉 REEL PUBLICADO CON ÉXITO! ID:", reel_published_id)

# Obtener permalink
with urllib.request.urlopen(f"https://graph.facebook.com/v26.0/{reel_published_id}?fields=permalink&access_token={token}", timeout=30) as r:
    link_data = json.loads(r.read().decode())
permalink = link_data.get("permalink", "")
print("🔗 Enlace del Reel:", permalink)

# 5. Publicar también en Historias
print("Creando contenedor de Historia...")
story_params = urllib.parse.urlencode({
    "media_type": "STORIES",
    "video_url": public_url,
    "access_token": token
})
s_req = urllib.request.Request(f"https://graph.facebook.com/v26.0/{user_id}/media", data=story_params.encode(), method="POST")
with urllib.request.urlopen(s_req, timeout=60) as r:
    s_data = json.loads(r.read().decode())
story_container_id = s_data["id"]

for i in range(30):
    time.sleep(5)
    surl = f"https://graph.facebook.com/v26.0/{story_container_id}?fields=status_code,status&access_token={token}"
    with urllib.request.urlopen(surl, timeout=30) as r:
        sdata = json.loads(r.read().decode())
    st = sdata.get("status_code", "")
    print(f"Estado de procesamiento Historia Meta: {st}")
    if st == "FINISHED":
        break
    elif st == "ERROR":
        raise RuntimeError(f"Error procesando Historia en Meta: {sdata}")

print("Publicando Historia...")
pub_story_params = urllib.parse.urlencode({
    "creation_id": story_container_id,
    "access_token": token
})
s_preq = urllib.request.Request(f"https://graph.facebook.com/v26.0/{user_id}/media_publish", data=pub_story_params.encode(), method="POST")
with urllib.request.urlopen(s_preq, timeout=60) as r:
    story_published_id = json.loads(r.read().decode())["id"]
print("🎉 HISTORIA PUBLICADA CON ÉXITO! ID:", story_published_id)

