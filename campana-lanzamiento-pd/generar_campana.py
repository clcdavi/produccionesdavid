#!/usr/bin/env python3
"""
Genera la Campaña V2 de Producciones David (Estética Clara, Vibrante y Llamativa):
- Carrusel 1 (5 placas 1080x1350): Todo lo que creamos (Comercios, Presentadores/Voz IA, Institucional/Privados, Fiestas/Entretenimiento)
- Carrusel 2 (4 placas 1080x1350): Packs & Promos de Producción con las herramientas de IA más avanzadas
- 2 Historias (1080x1920): Con margen seguro superior e inferior
- 1 Reel Oficial (1080x1920 .mp4): Textos 100% FIJOS (sin zoom que maree) y con margen inferior de 380px (Safe Zone de Reels)
"""
import base64
import json
import subprocess
from pathlib import Path
from PIL import Image

OUT_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/campana-lanzamiento-pd")
OUT_DIR.mkdir(parents=True, exist_ok=True)

INST_JSON = Path.home() / "Library" / "Application Support" / "adrian-saenz-video-negocio" / "instalacion.json"
CHROME_BIN = json.loads(INST_JSON.read_text(encoding="utf-8"))["chrome"]
FFMPEG = Path("/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg")

LOGO_COLOR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/marca-producciones-david/logo_color_sin_fondo.png")
VIS_COMERCIOS = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d/vis_comercios_vibrante_1793567883788.jpg")
VIS_AVATAR = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d/vis_presentador_avatar_1793567901573.jpg")
VIS_INSTITUCIONAL = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d/vis_institucional_privados_1793567925648.jpg")
VIS_FIESTAS = Path("/Users/davidcorrea/.gemini/antigravity/brain/1bd34c74-87eb-4a6f-bb52-8122d7fbdd7d/vis_fiestas_entretenimiento_1793567953216.jpg")
MUSIC_MP3 = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/negocios/sw-store/musica/musica.mp3")


def to_data_uri(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


LOGO_URI = to_data_uri(LOGO_COLOR)
COM_URI = to_data_uri(VIS_COMERCIOS)
AVA_URI = to_data_uri(VIS_AVATAR)
INS_URI = to_data_uri(VIS_INSTITUCIONAL)
FIE_URI = to_data_uri(VIS_FIESTAS)


BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Inter:wght@500;600;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: linear-gradient(140deg, #FFFDF9 0%, #FFF3DB 48%, #EBF3FF 100%);
  color: #0F172A;
  font-family: 'Inter', sans-serif;
  overflow: hidden;
  position: relative;
}
.orb-1 {
  position: absolute;
  top: -120px;
  right: -120px;
  width: 560px;
  height: 560px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(245,158,11,0.32) 0%, rgba(245,158,11,0) 70%);
}
.orb-2 {
  position: absolute;
  bottom: -140px;
  left: -120px;
  width: 620px;
  height: 620px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(37,99,235,0.22) 0%, rgba(37,99,235,0) 70%);
}
.frame-border {
  position: absolute;
  inset: 28px;
  border: 2px solid rgba(217,119,6,0.28);
  border-radius: 32px;
  pointer-events: none;
  z-index: 10;
}
.content {
  position: relative;
  z-index: 20;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.brand-pill {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  background: #0F172A;
  border: 2px solid #E5B869;
  padding: 12px 26px;
  border-radius: 999px;
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: 20px;
  letter-spacing: 1.2px;
  color: #FDE68A;
  text-transform: uppercase;
  box-shadow: 0 8px 20px rgba(15,23,42,0.15);
}
.step-badge {
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: 22px;
  color: #FFFFFF;
  background: linear-gradient(135deg, #EA580C 0%, #D97706 100%);
  padding: 10px 24px;
  border-radius: 999px;
  box-shadow: 0 6px 16px rgba(234,88,12,0.3);
}
.logo-badge {
  width: 220px;
  height: 220px;
  border-radius: 38px;
  background: radial-gradient(circle at 50% 35%, #1E2430 0%, #0A0C10 100%);
  border: 3px solid #E5B869;
  box-shadow: 0 20px 45px rgba(15,23,42,0.22);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px auto;
  padding: 18px;
}
.logo-badge img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
h1 {
  font-family: 'Montserrat', sans-serif;
  font-weight: 900;
  font-size: 56px;
  line-height: 1.08;
  letter-spacing: -1px;
  text-transform: uppercase;
  color: #0F172A;
  margin-bottom: 18px;
}
.accent {
  background: linear-gradient(135deg, #EA580C 0%, #D97706 55%, #2563EB 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
p.lead {
  font-size: 29px;
  line-height: 1.38;
  color: #334155;
  font-weight: 600;
}
.card-box {
  background: #FFFFFF;
  border: 2px solid rgba(217, 119, 6, 0.28);
  border-radius: 26px;
  padding: 32px 36px;
  margin-top: 20px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}
.bullet-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.bullet-list li {
  font-size: 26px;
  line-height: 1.32;
  color: #1E293B;
  display: flex;
  align-items: center;
  gap: 16px;
  font-weight: 700;
}
.bullet-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: linear-gradient(135deg, #EA580C 0%, #F59E0B 100%);
  flex-shrink: 0;
}
.preview-hero {
  width: 100%;
  height: 340px;
  border-radius: 24px;
  overflow: hidden;
  border: 3px solid #FFFFFF;
  box-shadow: 0 16px 36px rgba(15,23,42,0.14);
  margin: 18px 0;
  position: relative;
}
.preview-hero img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.grid-2x2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin: 20px 0;
}
.grid-card {
  background: #FFFFFF;
  border: 2px solid rgba(217,119,6,0.25);
  border-radius: 20px;
  padding: 18px 20px;
  box-shadow: 0 10px 25px rgba(15,23,42,0.06);
  text-align: left;
}
.grid-card h3 {
  font-family: 'Montserrat', sans-serif;
  font-size: 23px;
  font-weight: 800;
  color: #EA580C;
  margin-bottom: 6px;
}
.grid-card p {
  font-size: 21px;
  color: #334155;
  font-weight: 600;
  line-height: 1.28;
}
.footer-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 2px solid rgba(15,23,42,0.08);
  padding-top: 22px;
}
.footer-handle {
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: 24px;
  color: #0F172A;
}
.cta-pill {
  background: linear-gradient(135deg, #EA580C 0%, #D97706 100%);
  color: #FFFFFF;
  font-family: 'Montserrat', sans-serif;
  font-weight: 800;
  font-size: 22px;
  padding: 14px 28px;
  border-radius: 999px;
  text-transform: uppercase;
  box-shadow: 0 8px 20px rgba(234,88,12,0.3);
}
"""


CAROUSEL_1_SLIDES = [
    (
        "c1_01_portada.jpg",
        "PRODUCCIÓN AUDIOVISUAL IA",
        "1 / 5",
        f"""
        <div style="text-align:center; margin: auto 0;">
          <div class="logo-badge"><img src="{LOGO_URI}" /></div>
          <h1>PRODUCCIONES <span class="accent">PROFESIONALES</span><br/>CON INTELIGENCIA ARTIFICIAL</h1>
          <p class="lead" style="max-width: 860px; margin: 0 auto 18px auto;">
            Usamos las herramientas de IA más avanzadas del mercado para crear videos de alto impacto que hacen crecer tu marca.
          </p>
          <div class="grid-2x2">
            <div class="grid-card"><h3>🛍️ Comercios y Marcas</h3><p>De fotos estáticas a comerciales en movimiento.</p></div>
            <div class="grid-card"><h3>🎙️ Avatares & Voz IA</h3><p>Presentadores hiperrealistas y clonación de voz.</p></div>
            <div class="grid-card"><h3>🏢 Institucional y Privados</h3><p>Empresas, colegios, clínicas y profesionales.</p></div>
            <div class="grid-card"><h3>🎉 Fiestas y Eventos</h3><p>Shows, salones, entretenimiento e invitaciones.</p></div>
          </div>
        </div>
        """,
        "Deslizá para ver cada uno ➔",
    ),
    (
        "c1_02_comerciales_producto.jpg",
        "COMERCIOS Y PRODUCTOS",
        "2 / 5",
        f"""
        <div>
          <h1>VIDEOS COMERCIALES <span class="accent">QUE VENDEN MÁS</span></h1>
          <div class="preview-hero"><img src="{COM_URI}" /></div>
          <div class="card-box">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>Transformamos las fotos de tu negocio en comerciales de cine</li>
              <li><span class="bullet-dot"></span>Ideal para gastronomía, indumentaria, tiendas y emprendimientos</li>
              <li><span class="bullet-dot"></span>Sin cámaras caras ni rodajes eternos: listos en 48 hs</li>
            </ul>
          </div>
        </div>
        """,
        "Deslizá ➔ Presentadores & Voz IA",
    ),
    (
        "c1_03_avatares_y_voces.jpg",
        "AVATARES & CLONACIÓN DE VOZ",
        "3 / 5",
        f"""
        <div>
          <h1>PRESENTADORES IA & <span class="accent">LOCUCIÓN PROFESIONAL</span></h1>
          <div class="preview-hero"><img src="{AVA_URI}" /></div>
          <div class="card-box">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>¿No querés salir en cámara? Creamos tu presentador hiperrealista</li>
              <li><span class="bullet-dot"></span>Clonamos tu propia voz o sumamos locución comercial argentina</li>
              <li><span class="bullet-dot"></span>Videos dinámicos presentando tus servicios, ofertas y novedades</li>
            </ul>
          </div>
        </div>
        """,
        "Deslizá ➔ Institucional y Eventos",
    ),
    (
        "c1_04_institucional_y_fiestas.jpg",
        "INSTITUCIONAL, PRIVADOS Y FIESTAS",
        "4 / 5",
        f"""
        <div>
          <h1>EMPRESAS, EVENTOS Y <span class="accent">ENTRETENIMIENTO</span></h1>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:18px; margin: 18px 0;">
            <div class="preview-hero" style="height:290px; margin:0;"><img src="{INS_URI}" /></div>
            <div class="preview-hero" style="height:290px; margin:0;"><img src="{FIE_URI}" /></div>
          </div>
          <div class="card-box">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>Videos Institucionales para empresas privadas, colegios y clubes</li>
              <li><span class="bullet-dot"></span>Promos vibrantes para Fiestas, Eventos, DJs, Salones y Shows</li>
              <li><span class="bullet-dot"></span>Producciones creativas a medida con tecnología de vanguardia</li>
            </ul>
          </div>
        </div>
        """,
        "Deslizá ➔ Consultá Promos",
    ),
    (
        "c1_05_cta_consulta.jpg",
        "COTIZACIÓN PERSONALIZADA",
        "5 / 5",
        f"""
        <div style="text-align:center; margin: auto 0;">
          <div class="logo-badge"><img src="{LOGO_URI}" /></div>
          <h1>LLEVÁ TU IMAGEN AL <span class="accent">SIGUIENTE NIVEL</span></h1>
          <div class="card-box" style="text-align:left;">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>Las herramientas de IA más avanzadas del mercado a tu favor</li>
              <li><span class="bullet-dot"></span>Packs individuales y planes mensuales para todo tipo de rubro</li>
              <li><span class="bullet-dot"></span>Comentá <b>"INFO"</b> o escribinos por Mensaje Directo para asesorarte</li>
            </ul>
          </div>
        </div>
        """,
        "Escribinos 'INFO' por MD 📩",
    ),
]


CAROUSEL_2_SLIDES = [
    (
        "c2_01_packs_portada.jpg",
        "PACKS & PROMOCIONES",
        "1 / 4",
        f"""
        <div style="text-align:center; margin: auto 0;">
          <div class="logo-badge"><img src="{LOGO_URI}" /></div>
          <h1>PACKS DE <span class="accent">PRODUCCIÓN AUDIOVISUAL</span></h1>
          <p class="lead" style="margin-bottom: 20px;">
            Tecnología de Inteligencia Artificial de última generación para Comercios, Empresas Privadas, Eventos y Profesionales.
          </p>
          <div class="card-box" style="text-align:left;">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>Calidad cinematográfica sin costos de rodaje tradicional</li>
              <li><span class="bullet-dot"></span>Adaptado a Reels, TikTok, YouTube Shorts y WhatsApp</li>
            </ul>
          </div>
        </div>
        """,
        "Conocé nuestros Packs ➔",
    ),
    (
        "c2_02_pack_impulso.jpg",
        "PACK 01 • IMPULSO",
        "2 / 4",
        f"""
        <div>
          <h1>PACK <span class="accent">IMPULSO COMERCIAL</span></h1>
          <div class="preview-hero" style="height:280px;"><img src="{COM_URI}" /></div>
          <div class="card-box">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>1 Comercial Master Full HD (para Instagram Reels y TikTok)</li>
              <li><span class="bullet-dot"></span>1 Versión Ligera calibrada para Estados y difusión de WhatsApp</li>
              <li><span class="bullet-dot"></span>3 Tomas limpias en movimiento para tus Historias del mes</li>
              <li><span class="bullet-dot"></span>Textos persuasivos y hashtags listos para copiar y publicar</li>
            </ul>
          </div>
        </div>
        """,
        "Deslizá ➔ Pack Mensual",
    ),
    (
        "c2_03_pack_mensual.jpg",
        "PACK 02 • PRESENCIA TOTAL",
        "3 / 4",
        f"""
        <div>
          <h1>PACK <span class="accent">PRESENCIA MENSUAL</span></h1>
          <div class="preview-hero" style="height:280px;"><img src="{AVA_URI}" /></div>
          <div class="card-box">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>3 Producciones al mes (Comerciales, Institucionales o Eventos)</li>
              <li><span class="bullet-dot"></span>Incluye Presentadores con IA y Locución / Clonación de Voz</li>
              <li><span class="bullet-dot"></span>9 Tomas dinámicas para mantener tus Historias activas todo el mes</li>
              <li><span class="bullet-dot"></span>Valor promocional bonificado por abono mensual</li>
            </ul>
          </div>
        </div>
        """,
        "Deslizá ➔ Solicitá Presupuesto",
    ),
    (
        "c2_04_pack_cta.jpg",
        "PROMO LANZAMIENTO",
        "4 / 4",
        f"""
        <div style="text-align:center; margin: auto 0;">
          <div class="logo-badge"><img src="{LOGO_URI}" /></div>
          <h1>CONSULTÁ PRECIOS <span class="accent">Y PROMOS HOY</span></h1>
          <p class="lead" style="margin-bottom: 20px;">
            Comentá <b>"PACK"</b> en esta publicación o envianos un Mensaje Directo contándonos qué querés promocionar.
          </p>
          <div class="card-box" style="text-align:left;">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>Comercios • Empresas Privadas • Instituciones • Fiestas y Eventos</li>
              <li><span class="bullet-dot"></span>Entrega rápida en 24 a 48 hs en todo el país</li>
            </ul>
          </div>
        </div>
        """,
        "Comentá 'PACK' o mandá MD 📩",
    ),
]


STORIES = [
    (
        "story_01_bienvenida.jpg",
        f"""
        <div style="text-align:center;">
          <div class="logo-badge" style="width:240px; height:240px;"><img src="{LOGO_URI}" /></div>
          <h1 style="font-size: 58px;">PRODUCCIONES <span class="accent">PROFESIONALES CON IA</span></h1>
          <p class="lead" style="font-size: 30px; margin-bottom: 24px;">
            Trabajamos con las herramientas de Inteligencia Artificial más avanzadas del mercado.
          </p>
          <div class="card-box" style="text-align:left;">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>Comerciales para Comercios, Marcas y Emprendimientos</li>
              <li><span class="bullet-dot"></span>Presentadores Virtuales & Clonación de Voz</li>
              <li><span class="bullet-dot"></span>Videos Institucionales y para Empresas Privadas</li>
              <li><span class="bullet-dot"></span>Publicidad para Fiestas, Eventos y Entretenimiento</li>
            </ul>
          </div>
        </div>
        """,
        "Respondé 'INFO' para ver Packs 📩",
    ),
    (
        "story_02_servicios_promo.jpg",
        f"""
        <div>
          <h1 style="font-size: 56px; text-align:center;">¿NO QUERÉS <span class="accent">SALIR EN CÁMARA?</span></h1>
          <div class="preview-hero" style="height: 400px;"><img src="{AVA_URI}" /></div>
          <div class="card-box">
            <ul class="bullet-list">
              <li><span class="bullet-dot"></span>Creamos Presentadores y Avatares Hiperrealistas con IA</li>
              <li><span class="bullet-dot"></span>Clonamos tu voz o sumamos locución profesional</li>
              <li><span class="bullet-dot"></span>Videos para Comercios, Instituciones, Eventos y Fiestas</li>
            </ul>
          </div>
        </div>
        """,
        "Pedí tu Promo por Mensaje Directo 🚀",
    ),
]


REEL_SCENES = [
    (
        "reel_scene_01.jpg",
        f"""
        <div style="text-align:center;">
          <div class="logo-badge" style="width:230px; height:230px;"><img src="{LOGO_URI}" /></div>
          <h1 style="font-size: 56px;">VIDEOS DE ALTO IMPACTO <span class="accent">CON INTELIGENCIA ARTIFICIAL</span></h1>
          <div class="card-box">
            <p class="lead" style="font-size: 30px; color:#0F172A;">
              Usamos las herramientas de IA más avanzadas del mercado para producir videos profesionales sin rodajes costosos.
            </p>
          </div>
        </div>
        """,
        "PRODUCCIONES DAVID • ESTUDIO CREATIVO",
    ),
    (
        "reel_scene_02.jpg",
        f"""
        <div>
          <h1 style="font-size: 52px; text-align:center;">01. COMERCIOS Y <span class="accent">PRODUCTOS EN MOVIMIENTO</span></h1>
          <div class="preview-hero" style="height: 390px;"><img src="{COM_URI}" /></div>
          <div class="card-box">
            <p class="lead" style="font-size: 29px; color:#0F172A;">
              Transformamos las fotos de tus productos o local en comerciales vibrantes listos para vender en Reels y TikTok.
            </p>
          </div>
        </div>
        """,
        "GASTRONOMÍA • TIENDAS • MARCAS",
    ),
    (
        "reel_scene_03.jpg",
        f"""
        <div>
          <h1 style="font-size: 52px; text-align:center;">02. AVATARES IA & <span class="accent">CLONACIÓN DE VOZ</span></h1>
          <div class="preview-hero" style="height: 390px;"><img src="{AVA_URI}" /></div>
          <div class="card-box">
            <p class="lead" style="font-size: 29px; color:#0F172A;">
              Creamos presentadores hiperrealistas y clonamos voces profesionales para que hablen por tu negocio sin salir en cámara.
            </p>
          </div>
        </div>
        """,
        "PRESENTADORES VIRTUALES & LOCUCIÓN",
    ),
    (
        "reel_scene_04.jpg",
        f"""
        <div>
          <h1 style="font-size: 50px; text-align:center;">03. INSTITUCIONALES, <span class="accent">PRIVADOS Y FIESTAS</span></h1>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin: 16px 0;">
            <div class="preview-hero" style="height: 340px; margin:0;"><img src="{INS_URI}" /></div>
            <div class="preview-hero" style="height: 340px; margin:0;"><img src="{FIE_URI}" /></div>
          </div>
          <div class="card-box">
            <p class="lead" style="font-size: 28px; color:#0F172A;">
              Producciones para empresas privadas, colegios, clubes, salones, fiestas, shows y entretenimiento.
            </p>
          </div>
        </div>
        """,
        "INSTITUCIONAL • EVENTOS • ENTRETENIMIENTO",
    ),
    (
        "reel_scene_05.jpg",
        f"""
        <div style="text-align:center;">
          <div class="logo-badge" style="width:230px; height:230px;"><img src="{LOGO_URI}" /></div>
          <h1 style="font-size: 54px;">CONSULTÁ POR NUESTROS <span class="accent">PACKS Y PROMOS</span></h1>
          <div class="card-box" style="text-align:center;">
            <p class="lead" style="font-size: 31px; color:#0F172A; font-weight:800;">
              Comentá "INFO" o escribinos por Mensaje Directo para cotizar tu proyecto
            </p>
          </div>
        </div>
        """,
        "@produccionesdavid.ar • Escribinos por MD",
    ),
]


def build_feed_html(tag: str, step: str, body_html: str, cta_text: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
{BASE_CSS}
body {{ width: 1080px; height: 1350px; }}
.content {{ padding: 66px 68px; }}
</style>
</head>
<body>
  <div class="orb-1"></div>
  <div class="orb-2"></div>
  <div class="frame-border"></div>
  <div class="content">
    <div class="topbar">
      <div class="brand-pill">🎬 {tag}</div>
      <div class="step-badge">{step}</div>
    </div>
    {body_html}
    <div class="footer-bar">
      <div class="footer-handle">@produccionesdavid.ar</div>
      <div class="cta-pill">{cta_text}</div>
    </div>
  </div>
</body>
</html>"""


def build_vertical_html(body_html: str, cta_text: str, is_reel: bool) -> str:
    # Safe zone for Reels: top 180px, bottom 390px so Instagram UI never covers text!
    pad_top = "175px" if is_reel else "140px"
    pad_bottom = "390px" if is_reel else "220px"
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
{BASE_CSS}
body {{ width: 1080px; height: 1920px; }}
.frame-border {{
  top: {int(pad_top[:-2]) - 35}px;
  bottom: {int(pad_bottom[:-2]) - 35}px;
  left: 30px;
  right: 30px;
}}
.content {{
  padding: {pad_top} 68px {pad_bottom} 68px;
}}
</style>
</head>
<body>
  <div class="orb-1"></div>
  <div class="orb-2"></div>
  <div class="frame-border"></div>
  <div class="content">
    <div class="topbar" style="justify-content:center;">
      <div class="brand-pill">🎬 PRODUCCIONES DAVID • IA</div>
    </div>
    {body_html}
    <div class="footer-bar" style="justify-content:center;">
      <div class="cta-pill" style="font-size:24px; padding:16px 36px;">{cta_text}</div>
    </div>
  </div>
</body>
</html>"""


def render_html_to_jpg(html: str, out_jpg: Path, width: int, height: int) -> None:
    tmp_html = OUT_DIR / "_tmp_render.html"
    tmp_png = OUT_DIR / "_tmp_render.png"
    tmp_html.write_text(html, encoding="utf-8")
    subprocess.run(
        [
            CHROME_BIN,
            "--headless",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={tmp_png}",
            tmp_html.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    img = Image.open(tmp_png).convert("RGB")
    if img.size != (width, height):
        img = img.crop((0, 0, width, height))
    img.save(out_jpg, "JPEG", quality=95)
    tmp_html.unlink(missing_ok=True)
    tmp_png.unlink(missing_ok=True)


def main():
    for fname, tag, step, body, cta in CAROUSEL_1_SLIDES + CAROUSEL_2_SLIDES:
        html = build_feed_html(tag, step, body, cta)
        out_path = OUT_DIR / fname
        render_html_to_jpg(html, out_path, 1080, 1350)
        print("Renderizado Feed:", out_path.name)

    for fname, body, cta in STORIES:
        html = build_vertical_html(body, cta, is_reel=False)
        out_path = OUT_DIR / fname
        render_html_to_jpg(html, out_path, 1080, 1920)
        print("Renderizada Story:", out_path.name)

    for fname, body, cta in REEL_SCENES:
        html = build_vertical_html(body, cta, is_reel=True)
        out_path = OUT_DIR / fname
        render_html_to_jpg(html, out_path, 1080, 1920)
        print("Renderizada Escena Reel:", out_path.name)

    # Build 16.5s 1080x1920 30fps static-frame Reel (NO zoompan wobble, smooth 0.35s fade transitions)
    reel_out = OUT_DIR / "reel_oficial_producciones_david.mp4"
    s = [OUT_DIR / item[0] for item in REEL_SCENES]
    cmd = [
        str(FFMPEG), "-y",
        "-loop", "1", "-t", "3.6", "-i", str(s[0]),
        "-loop", "1", "-t", "3.6", "-i", str(s[1]),
        "-loop", "1", "-t", "3.6", "-i", str(s[2]),
        "-loop", "1", "-t", "3.6", "-i", str(s[3]),
        "-loop", "1", "-t", "3.8", "-i", str(s[4]),
        "-i", str(MUSIC_MP3),
        "-filter_complex",
        (
            "[0:v]fps=30,setsar=1,format=yuv420p[v0];"
            "[1:v]fps=30,setsar=1,format=yuv420p[v1];"
            "[2:v]fps=30,setsar=1,format=yuv420p[v2];"
            "[3:v]fps=30,setsar=1,format=yuv420p[v3];"
            "[4:v]fps=30,setsar=1,format=yuv420p[v4];"
            "[v0][v1]xfade=transition=fade:duration=0.35:offset=3.25[x1];"
            "[x1][v2]xfade=transition=fade:duration=0.35:offset=6.50[x2];"
            "[x2][v3]xfade=transition=fade:duration=0.35:offset=9.75[x3];"
            "[x3][v4]xfade=transition=fade:duration=0.35:offset=13.00[vout];"
            "[5:a]atrim=0:16.8,afade=t=in:st=0:d=0.4,afade=t=out:st=15.3:d=1.5[aout]"
        ),
        "-map", "[vout]",
        "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        "-shortest",
        str(reel_out),
    ]
    subprocess.run(cmd, check=True)
    print("🎬 Reel Oficial V2 (Fijo y Safe-Zone) renderizado:", reel_out)


if __name__ == "__main__":
    main()
