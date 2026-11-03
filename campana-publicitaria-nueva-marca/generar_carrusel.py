#!/usr/bin/env python3
"""
Generador del Carrusel Publicitario Oficial — PRODUCCIONES DAVID
6 Placas (1080x1080) con la identidad visual oficial:
Paleta: Carbón #191919, Marfil #F5F2EC, Terracota #CD563C.
Tipografía: Montserrat (Black, Bold, Medium, Regular).
"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando")
BRAND_DIR = BASE_DIR / "assets" / "branding" / "producciones-david"
FONTS_DIR = BRAND_DIR / "fonts"
OUT_DIR = BASE_DIR / "campana-publicitaria-nueva-marca" / "carrusel"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Paleta oficial
COLOR_CARBON = (25, 25, 25, 255)       # #191919
COLOR_MARFIL = (245, 242, 236, 255)    # #F5F2EC
COLOR_TERRACOTA = (205, 86, 60, 255)   # #CD563C
COLOR_WHITE = (255, 255, 255, 255)
COLOR_MUTED = (110, 110, 110, 255)

# Cargar fuentes
font_black = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Black.ttf"), s)
font_bold = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Bold.ttf"), s)
font_medium = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Medium.ttf"), s)
font_regular = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Regular.ttf"), s)

logo_horiz = Image.open(BRAND_DIR / "logo-horizontal.png").convert("RGBA")
logo_princ = Image.open(BRAND_DIR / "logo-principal.png").convert("RGBA")
logo_inv = Image.open(BRAND_DIR / "watermark-blanco.png").convert("RGBA")

def paste_corner_shard(draw: ImageDraw.Draw, w=1080, h=1080, size=200):
    """Corte diagonal terracota en esquina inferior derecha según manual."""
    draw.polygon([(w - size, h), (w, h - size), (w, h)], fill=COLOR_TERRACOTA)

def draw_pagination(draw: ImageDraw.Draw, current: int, total: int = 6, dark: bool = False):
    f = font_bold(22)
    color = COLOR_MUTED if not dark else (180, 180, 180, 255)
    draw.text((980, 75), f"{current:02d} / {total:02d}", font=f, fill=color, anchor="rt")

# ==============================================================
# SLIDE 1: PORTADA EDITORIAL
# ==============================================================
def create_slide_1():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    
    # Header Logo
    lw = 440
    lh = int(logo_horiz.height * (lw / logo_horiz.width))
    logo_s = logo_horiz.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_s, (80, 70), logo_s)
    draw_pagination(draw, 1, 6)
    
    # Titular de Alto Impacto
    draw.text((80, 220), "EL FUTURO DEL", font=font_black(64), fill=COLOR_CARBON)
    draw.text((80, 295), "VIDEO PUBLICITARIO", font=font_black(64), fill=COLOR_CARBON)
    draw.text((80, 370), "ES HOY.", font=font_black(64), fill=COLOR_TERRACOTA)
    
    # Subtítulo explicativo
    draw.text((80, 465), "Comerciales cinematográficos, spots de producto y avatares con IA.", font=font_medium(26), fill=COLOR_CARBON)
    draw.text((80, 505), "Sin rodajes lentos. Sin costos desmedidos. Entrega en 48 hs.", font=font_regular(24), fill=COLOR_MUTED)
    
    # Imagen inferior con corte cinematográfico
    bg_img = Image.open(BRAND_DIR / "templates" / "backgrounds" / "bg_cinema_camera.jpg").convert("RGBA")
    bg_crop = bg_img.crop((0, 600, 1080, 1140)).resize((920, 460), Image.Resampling.LANCZOS)
    
    # Máscara de esquinas redondeadas
    mask = Image.new("L", (920, 460), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (920, 460)], radius=24, fill=255)
    canvas.paste(bg_crop, (80, 560), mask)
    
    # Badge sobre la imagen
    badge_overlay = Image.new("RGBA", (920, 460), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(badge_overlay)
    b_draw.rounded_rectangle([(30, 370), (420, 425)], radius=12, fill=(25, 25, 25, 230))
    b_draw.text((50, 385), "CALIDAD 4K · INTELIGENCIA ARTIFICIAL", font=font_bold(18), fill=COLOR_MARFIL)
    canvas.paste(badge_overlay, (80, 560), badge_overlay)
    
    paste_corner_shard(draw, 1080, 1080, 200)
    canvas.convert("RGB").save(OUT_DIR / "slide_01_portada.png", quality=98)
    print("Slide 1 generado.")

# ==============================================================
# SLIDE 2: EL PROBLEMA VS LA REVOLUCIÓN IA
# ==============================================================
def create_slide_2():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    
    # Header
    draw.text((80, 75), "PRODUCCIONES DAVID", font=font_bold(24), fill=COLOR_CARBON)
    draw_pagination(draw, 2, 6)
    
    # Titular
    draw.text((80, 150), "¿POR QUÉ EL MODELO TRADICIONAL", font=font_black(46), fill=COLOR_CARBON)
    draw.text((80, 210), "YA NO FUNCIONA?", font=font_black(46), fill=COLOR_TERRACOTA)
    
    # Bento Card 1: El Pasado Tradicional (Gris / Advertencia)
    card1 = Image.new("RGBA", (920, 310), (235, 230, 222, 255))
    c1_draw = ImageDraw.Draw(card1)
    c1_draw.rounded_rectangle([(0, 0), (920, 310)], radius=20, outline=(210, 200, 190, 255), width=2)
    c1_draw.text((40, 35), "RODAJES TRADICIONALES", font=font_bold(26), fill=(140, 50, 40, 255))
    c1_draw.text((40, 85), "❌ Semanas de planificación, permisos y locaciones.", font=font_medium(22), fill=COLOR_CARBON)
    c1_draw.text((40, 135), "❌ Equipos de filmación carísimos y actores.", font=font_medium(22), fill=COLOR_CARBON)
    c1_draw.text((40, 185), "❌ Presupuestos de cientos de miles de pesos por 1 solo video.", font=font_medium(22), fill=COLOR_CARBON)
    c1_draw.text((40, 235), "❌ Tiempos muertos de postproducción de más de 20 días.", font=font_medium(22), fill=COLOR_CARBON)
    canvas.paste(card1, (80, 300))
    
    # Bento Card 2: Con Producciones David (Carbón Premium)
    card2 = Image.new("RGBA", (920, 360), COLOR_CARBON)
    c2_draw = ImageDraw.Draw(card2)
    c2_draw.rounded_rectangle([(0, 0), (920, 360)], radius=20, fill=COLOR_CARBON)
    # Filete terracota superior
    c2_draw.rectangle([(0, 0), (920, 8)], fill=COLOR_TERRACOTA)
    c2_draw.text((40, 45), "CON PRODUCCIONES DAVID (IA)", font=font_black(28), fill=COLOR_MARFIL)
    c2_draw.text((40, 105), "✅ Entrega en 48 a 72 horas listo para publicar y pautar.", font=font_medium(22), fill=COLOR_MARFIL)
    c2_draw.text((40, 155), "✅ Cualquier escenario del mundo generado con fotorrealismo.", font=font_medium(22), fill=COLOR_MARFIL)
    c2_draw.text((40, 205), "✅ Calidad visual de productora de cine sin costos ocultos.", font=font_medium(22), fill=COLOR_MARFIL)
    c2_draw.text((40, 255), "✅ Packs mensuales pensados para negocios que quieren vender.", font=font_bold(22), fill=COLOR_TERRACOTA)
    canvas.paste(card2, (80, 650))
    
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_02_problema_solucion.png", quality=98)
    print("Slide 2 generado.")

# ==============================================================
# SLIDE 3: SERVICIO 1 - SPOTS DE PRODUCTO Y E-COMMERCE
# ==============================================================
def create_slide_3():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    
    draw.text((80, 75), "SERVICIO 01 / 03", font=font_bold(22), fill=COLOR_TERRACOTA)
    draw_pagination(draw, 3, 6)
    
    draw.text((80, 140), "SPOTS DE PRODUCTO", font=font_black(48), fill=COLOR_CARBON)
    draw.text((80, 205), "Y E-COMMERCE", font=font_black(48), fill=COLOR_CARBON)
    
    draw.text((80, 280), "Colocamos tus productos en escenarios imposibles:", font=font_bold(24), fill=COLOR_CARBON)
    draw.text((80, 320), "Iluminación de estudio, primeros planos macro y tomas dinámicas", font=font_regular(22), fill=COLOR_MUTED)
    draw.text((80, 355), "que multiplican la conversión de tu tienda online y tus anuncios.", font=font_regular(22), fill=COLOR_MUTED)
    
    # Imagen de muestra de producto
    sw_img = Image.open(BASE_DIR / "negocios" / "sw-store" / "anuncio" / "planos" / "revision_kling.jpg").convert("RGBA")
    sw_crop = sw_img.resize((920, 520), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (920, 520), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (920, 520)], radius=20, fill=255)
    canvas.paste(sw_crop, (80, 440), mask)
    
    # Badge flotante
    b_card = Image.new("RGBA", (520, 70), (25, 25, 25, 230))
    b_d = ImageDraw.Draw(b_card)
    b_d.text((30, 22), "IDEAL PARA MARCAS Y TIENDAS ONLINE", font=font_bold(20), fill=COLOR_MARFIL)
    canvas.paste(b_card, (110, 850), b_card)
    
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_03_producto.png", quality=98)
    print("Slide 3 generado.")

# ==============================================================
# SLIDE 4: SERVICIO 2 - LOCALES Y GASTRONOMÍA
# ==============================================================
def create_slide_4():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    
    draw.text((80, 75), "SERVICIO 02 / 03", font=font_bold(22), fill=COLOR_TERRACOTA)
    draw_pagination(draw, 4, 6)
    
    draw.text((80, 140), "REELS PARA LOCALES", font=font_black(48), fill=COLOR_CARBON)
    draw.text((80, 205), "Y GASTRONOMÍA", font=font_black(48), fill=COLOR_CARBON)
    
    draw.text((80, 280), "Videos virales diseñados para despertar el deseo:", font=font_bold(24), fill=COLOR_CARBON)
    draw.text((80, 320), "Texturas en primer plano, humo, dinamismo y música en tendencia.", font=font_regular(22), fill=COLOR_MUTED)
    draw.text((80, 355), "Hacé que la gente de tu zona elija tu local este fin de semana.", font=font_regular(22), fill=COLOR_MUTED)
    
    # Imagen de gastronomía (Parrilla La Reja / Pizza)
    gastro_path = BASE_DIR / "negocios" / "parrilla-la-reja" / "anuncio" / "video-anuncio" / "assets" / "a04.jpg"
    if not gastro_path.exists():
        gastro_path = BRAND_DIR / "templates" / "backgrounds" / "bg_mountain_landscape.jpg"
    g_img = Image.open(gastro_path).convert("RGBA")
    g_crop = g_img.resize((920, 520), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (920, 520), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (920, 520)], radius=20, fill=255)
    canvas.paste(g_crop, (80, 440), mask)
    
    # Badge flotante
    b_card = Image.new("RGBA", (480, 70), (25, 25, 25, 230))
    b_d = ImageDraw.Draw(b_card)
    b_d.text((30, 22), "REELS DE ALTO TRÁFICO LOCAL", font=font_bold(20), fill=COLOR_MARFIL)
    canvas.paste(b_card, (110, 850), b_card)
    
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_04_gastronomia.png", quality=98)
    print("Slide 4 generado.")

# ==============================================================
# SLIDE 5: SERVICIO 3 - AVATARES Y VOCES INSTITUCIONALES
# ==============================================================
def create_slide_5():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    
    draw.text((80, 75), "SERVICIO 03 / 03", font=font_bold(22), fill=COLOR_TERRACOTA)
    draw_pagination(draw, 5, 6)
    
    draw.text((80, 140), "AVATARES Y VOCES", font=font_black(48), fill=COLOR_CARBON)
    draw.text((80, 205), "HIPERREALISTAS", font=font_black(48), fill=COLOR_CARBON)
    
    draw.text((80, 280), "Comunicación corporativa sin coordinar días de rodaje:", font=font_bold(24), fill=COLOR_CARBON)
    draw.text((80, 320), "Voceros profesionales con acento argentino nativo y lip-sync exacto.", font=font_regular(22), fill=COLOR_MUTED)
    draw.text((80, 355), "Perfecto para anuncios, cursos, efemérides y capacitaciones.", font=font_regular(22), fill=COLOR_MUTED)
    
    # Imagen de presentadores IA
    av_path = BASE_DIR / "campana-lanzamiento-pd" / "c1_03_avatares_y_voces.jpg"
    if not av_path.exists():
        av_path = BRAND_DIR / "templates" / "backgrounds" / "bg_studio_spotlight.jpg"
    a_img = Image.open(av_path).convert("RGBA")
    a_crop = a_img.resize((920, 520), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (920, 520), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (920, 520)], radius=20, fill=255)
    canvas.paste(a_crop, (80, 440), mask)
    
    b_card = Image.new("RGBA", (500, 70), (25, 25, 25, 230))
    b_d = ImageDraw.Draw(b_card)
    b_d.text((30, 22), "VOCES Y PRESENTADORES NATIVOS", font=font_bold(20), fill=COLOR_MARFIL)
    canvas.paste(b_card, (110, 850), b_card)
    
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_05_avatares.png", quality=98)
    print("Slide 5 generado.")

# ==============================================================
# SLIDE 6: CIERRE Y LLAMADO A LA ACCIÓN (FONDO CARBÓN)
# ==============================================================
def create_slide_6():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_CARBON)
    draw = ImageDraw.Draw(canvas)
    
    # Header logo blanco
    lw = 400
    lh = int(logo_inv.height * (lw / logo_inv.width))
    logo_s = logo_inv.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_s, (80, 80), logo_s)
    draw_pagination(draw, 6, 6, dark=True)
    
    # Gran titular de cierre
    draw.text((80, 260), "IMPULSÁ TU MARCA", font=font_black(62), fill=COLOR_MARFIL)
    draw.text((80, 335), "CON VIDEO DE IMPACTO.", font=font_black(62), fill=COLOR_TERRACOTA)
    
    # Párrafo
    draw.text((80, 450), "Tenemos planes mensuales a medida para que tu negocio", font=font_medium(26), fill=COLOR_MARFIL)
    draw.text((80, 490), "tenga presencia continua, profesional y con retorno real.", font=font_medium(26), fill=COLOR_MARFIL)
    
    # Botón CTA Central
    draw.rounded_rectangle([(80, 590), (1000, 710)], radius=20, fill=COLOR_MARFIL)
    draw.text((540, 630), "ESCRIBINOS POR WHATSAPP O DM", font=font_black(30), fill=COLOR_CARBON, anchor="mm")
    draw.text((540, 670), "Coordinamos una asesoría estratégica sin cargo", font=font_bold(20), fill=COLOR_TERRACOTA, anchor="mm")
    
    # Beneficios clave en footer
    draw.text((80, 780), "⚡ Entrega en 48 hs", font=font_bold(22), fill=COLOR_MARFIL)
    draw.text((400, 780), "🎬 Calidad Cinematográfica", font=font_bold(22), fill=COLOR_MARFIL)
    draw.text((750, 780), "📈 Enfoque en Conversión", font=font_bold(22), fill=COLOR_MARFIL)
    
    # Redes / Ubicación
    draw.text((80, 880), "📍 San Fernando, Buenos Aires · Producción para todo el país", font=font_regular(20), fill=(160, 160, 160, 255))
    draw.text((80, 915), "Instagram: @produccionesdavid.ar", font=font_bold(22), fill=COLOR_TERRACOTA)
    
    paste_corner_shard(draw, 1080, 1080, 220)
    canvas.convert("RGB").save(OUT_DIR / "slide_06_cta.png", quality=98)
    print("Slide 6 generado.")

if __name__ == "__main__":
    create_slide_1()
    create_slide_2()
    create_slide_3()
    create_slide_4()
    create_slide_5()
    create_slide_6()
    print("🎉 Carrusel completo de 6 placas generado con éxito en:", OUT_DIR)
