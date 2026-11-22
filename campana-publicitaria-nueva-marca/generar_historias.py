#!/usr/bin/env python3
"""
Generador de Historias Oficiales (9:16 - 1080x1920) — PRODUCCIONES DAVID
Pack de 3 Stories interactivas de captación con zonas para stickers de Instagram.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando")
BRAND_DIR = BASE_DIR / "assets" / "branding" / "producciones-david"
FONTS_DIR = BRAND_DIR / "fonts"
OUT_DIR = BASE_DIR / "campana-publicitaria-nueva-marca" / "historias"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COLOR_CARBON = (25, 25, 25, 255)
COLOR_MARFIL = (245, 242, 236, 255)
COLOR_TERRACOTA = (205, 86, 60, 255)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_MUTED = (160, 160, 160, 255)

font_black = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Black.ttf"), s)
font_bold = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Bold.ttf"), s)
font_medium = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Medium.ttf"), s)
font_regular = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Regular.ttf"), s)

logo_inv = Image.open(BRAND_DIR / "watermark-blanco.png").convert("RGBA")

def paste_corner_shard(draw: ImageDraw.Draw, w=1080, h=1920, size=240):
    draw.polygon([(w - size, h), (w, h - size), (w, h)], fill=COLOR_TERRACOTA)

def paste_top_logo(canvas: Image.Image, y=180, w=440):
    lh = int(logo_inv.height * (w / logo_inv.width))
    logo_s = logo_inv.resize((w, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_s, ((1080 - w) // 2, y), logo_s)

# ==============================================================
# HISTORIA 1: INTERACCIÓN Y GANCHO
# ==============================================================
def create_story_1():
    bg = Image.open(BRAND_DIR / "templates" / "backgrounds" / "bg_studio_spotlight.jpg").convert("RGBA")
    bg = bg.resize((1080, 1920), Image.Resampling.LANCZOS)
    
    overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for y in range(500):
        a = int(200 * (1.0 - (y / 500.0)))
        draw.line([(0, y), (1080, y)], fill=(25, 25, 25, a))
    for y in range(1100, 1920):
        a = int(230 * ((y - 1100.0) / 820.0))
        draw.line([(0, y), (1080, y)], fill=(25, 25, 25, a))
        
    paste_corner_shard(draw, 1080, 1920, 240)
    canvas = Image.alpha_composite(bg, overlay)
    draw_comp = ImageDraw.Draw(canvas)
    
    paste_top_logo(canvas, y=190, w=460)
    
    # Titular central
    draw_comp.text((100, 520), "¿QUERÉS MÁS", font=font_black(68), fill=COLOR_WHITE)
    draw_comp.text((100, 600), "CLIENTES ESTE MES", font=font_black(68), fill=COLOR_WHITE)
    draw_comp.text((100, 680), "PARA TU NEGOCIO?", font=font_black(68), fill=COLOR_TERRACOTA)
    
    # Línea acento
    draw_comp.rectangle([100, 780, 240, 786], fill=COLOR_TERRACOTA)
    
    # Subtítulo
    draw_comp.text((100, 830), "Los comercios y marcas que más venden hoy", font=font_medium(32), fill=COLOR_MARFIL)
    draw_comp.text((100, 875), "tienen presencia activa con videos de alto impacto.", font=font_medium(32), fill=COLOR_MARFIL)
    
    # Zona de sticker interactivo (guía visual para Instagram)
    draw_comp.rounded_rectangle([(100, 1100), (980, 1380)], radius=24, outline=COLOR_TERRACOTA, width=3)
    draw_comp.text((540, 1200), "📍 [ ESPACIO PARA STICKER DE ENCUESTA ]", font=font_bold(26), fill=COLOR_MARFIL, anchor="mm")
    draw_comp.text((540, 1260), "¿Tu marca hace videos?  [ SÍ  /  TODAVÍA NO ]", font=font_medium(24), fill=COLOR_MUTED, anchor="mm")
    
    # Footer
    draw_comp.text((100, 1600), "Descubrí el método Producciones David ➔", font=font_bold(28), fill=COLOR_WHITE)
    
    canvas.convert("RGB").save(OUT_DIR / "historia_01_gancho.png", quality=98)
    print("Historia 1 generada.")

# ==============================================================
# HISTORIA 2: DEMOSTRACIÓN DE VALOR Y SERVICIOS
# ==============================================================
def create_story_2():
    bg = Image.open(BRAND_DIR / "templates" / "backgrounds" / "bg_cinema_camera.jpg").convert("RGBA")
    bg = bg.resize((1080, 1920), Image.Resampling.LANCZOS)
    
    overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for y in range(450):
        a = int(200 * (1.0 - (y / 450.0)))
        draw.line([(0, y), (1080, y)], fill=(25, 25, 25, a))
    for y in range(1000, 1920):
        a = int(240 * ((y - 1000.0) / 920.0))
        draw.line([(0, y), (1080, y)], fill=(25, 25, 25, a))
        
    paste_corner_shard(draw, 1080, 1920, 240)
    canvas = Image.alpha_composite(bg, overlay)
    draw_comp = ImageDraw.Draw(canvas)
    
    paste_top_logo(canvas, y=190, w=460)
    
    draw_comp.text((100, 480), "VIDEOS PROFESIONALES", font=font_black(58), fill=COLOR_WHITE)
    draw_comp.text((100, 550), "EN TIEMPO RÉCORD.", font=font_black(58), fill=COLOR_TERRACOTA)
    draw_comp.rectangle([100, 630, 240, 636], fill=COLOR_TERRACOTA)
    
    # 3 Tarjetas de Servicios
    services = [
        ("01", "SPOTS DE PRODUCTO", "Primeros planos hiperrealistas e iluminación de cine."),
        ("02", "REELS GASTRONÓMICOS", "Dinamismo y estética visual que despiertan el deseo."),
        ("03", "AVATARES CORPORATIVOS", "Voceros y presentadores IA con acento argentino.")
    ]
    
    card_y = 700
    for num, title, desc in services:
        draw_comp.rounded_rectangle([(100, card_y), (980, card_y + 140)], radius=20, fill=(25, 25, 25, 220), outline=(60, 60, 60, 255), width=2)
        draw_comp.text((130, card_y + 30), num, font=font_black(28), fill=COLOR_TERRACOTA)
        draw_comp.text((190, card_y + 30), title, font=font_bold(26), fill=COLOR_MARFIL)
        draw_comp.text((190, card_y + 75), desc, font=font_regular(22), fill=COLOR_MUTED)
        card_y += 170
        
    # Badge inferior
    draw_comp.rounded_rectangle([(100, 1300), (980, 1400)], radius=18, fill=COLOR_TERRACOTA)
    draw_comp.text((540, 1350), "⚡ ENTREGA EN 48 HS · CALIDAD 4K", font=font_black(26), fill=COLOR_WHITE, anchor="mm")
    
    canvas.convert("RGB").save(OUT_DIR / "historia_02_solucion.png", quality=98)
    print("Historia 2 generada.")

# ==============================================================
# HISTORIA 3: LLAMADO A LA ACCIÓN DIRECTO (WHATSAPP / DM)
# ==============================================================
def create_story_3():
    bg = Image.open(BRAND_DIR / "templates" / "backgrounds" / "bg_studio_spotlight.jpg").convert("RGBA")
    bg = bg.resize((1080, 1920), Image.Resampling.LANCZOS)
    
    overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Oscurecer parejo para protagonismo de texto y sticker
    draw.rectangle([(0, 0), (1080, 1920)], fill=(20, 20, 20, 210))
    paste_corner_shard(draw, 1080, 1920, 240)
    
    canvas = Image.alpha_composite(bg, overlay)
    draw_comp = ImageDraw.Draw(canvas)
    
    paste_top_logo(canvas, y=220, w=480)
    
    draw_comp.text((540, 540), "LLEVÁ TU MARCA", font=font_black(64), fill=COLOR_WHITE, anchor="mm")
    draw_comp.text((540, 620), "AL SIGUIENTE NIVEL", font=font_black(64), fill=COLOR_TERRACOTA, anchor="mm")
    
    draw_comp.text((540, 740), "Escribinos un mensaje directo", font=font_bold(32), fill=COLOR_MARFIL, anchor="mm")
    draw_comp.text((540, 790), "y analizamos tu negocio sin costo.", font=font_medium(26), fill=COLOR_MUTED, anchor="mm")
    
    # Botón gigante para sticker de enlace / botón de mensaje
    draw_comp.rounded_rectangle([(120, 960), (960, 1180)], radius=24, fill=COLOR_MARFIL)
    draw_comp.text((540, 1030), "TOCÁ ACÁ PARA ESCRIBIRNOS", font=font_black(34), fill=COLOR_CARBON, anchor="mm")
    draw_comp.text((540, 1090), "👉 [ ENLACE DE WHATSAPP / MENSAJE DM ]", font=font_bold(22), fill=COLOR_TERRACOTA, anchor="mm")
    
    # Beneficios
    draw_comp.text((540, 1340), "✓ Planes y packs mensuales a medida", font=font_medium(26), fill=COLOR_WHITE, anchor="mm")
    draw_comp.text((540, 1390), "✓ Asesoría creativa y guion incluido", font=font_medium(26), fill=COLOR_WHITE, anchor="mm")
    draw_comp.text((540, 1440), "✓ Optimizado para pauta en Meta y TikTok", font=font_medium(26), fill=COLOR_WHITE, anchor="mm")
    
    draw_comp.text((540, 1680), "📍 San Fernando, Buenos Aires · Producción nacional", font=font_regular(22), fill=COLOR_MUTED, anchor="mm")
    
    canvas.convert("RGB").save(OUT_DIR / "historia_03_cta.png", quality=98)
    print("Historia 3 generada.")

if __name__ == "__main__":
    create_story_1()
    create_story_2()
    create_story_3()
    print("🎉 Pack de 3 Historias generado con éxito en:", OUT_DIR)
