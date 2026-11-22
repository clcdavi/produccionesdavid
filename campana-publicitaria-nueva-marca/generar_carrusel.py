#!/usr/bin/env python3
"""
Generador Perfeccionado del Carrusel Publicitario Oficial — PRODUCCIONES DAVID
100% fiel al manual de marca:
- Diseño Editorial Suizo / High-End Minimalista
- Sin fotos de clientes ni elementos deformados
- Márgenes amplios de 90 px, tipografía geométrica Montserrat, acento terracota
- Cero superposiciones de texto: cálculo dinámico de saltos de línea (wrap_text_pixels)
- Paleta oficial: Marfil #F5F2EC, Carbón #191919, Terracota #CD563C
"""
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
COLOR_MUTED = (115, 115, 115, 255)
COLOR_BORDER = (222, 217, 209, 255)

# Cargar fuentes oficiales
font_black = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Black.ttf"), s)
font_extrabold = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-ExtraBold.ttf"), s)
font_bold = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Bold.ttf"), s)
font_medium = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Medium.ttf"), s)
font_regular = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Regular.ttf"), s)

logo_horiz = Image.open(BRAND_DIR / "logo-horizontal.png").convert("RGBA")
logo_inv = Image.open(BRAND_DIR / "watermark-blanco.png").convert("RGBA")

def paste_corner_shard(draw: ImageDraw.Draw, w=1080, h=1080, size=180):
    """Corte diagonal terracota en esquina inferior derecha según manual."""
    draw.polygon([(w - size, h), (w, h - size), (w, h)], fill=COLOR_TERRACOTA)

def draw_header(canvas: Image.Image, draw: ImageDraw.Draw, page_num: int, total: int = 6, dark: bool = False):
    """Encabezado oficial con logo y paginación."""
    lw = 380
    logo_src = logo_inv if dark else logo_horiz
    lh = int(logo_src.height * (lw / logo_src.width))
    logo_s = logo_src.resize((lw, lh), Image.Resampling.LANCZOS)
    canvas.paste(logo_s, (90, 80), logo_s)
    
    # Paginación alineada al margen derecho (990 px)
    color_num = (200, 200, 200, 255) if dark else COLOR_MUTED
    draw.text((990, 95), f"{page_num:02d} / {total:02d}", font=font_bold(20), fill=color_num, anchor="rt")

def wrap_text_pixels(text: str, font: ImageFont.FreeTypeFont, max_width: int):
    """Ajuste de líneas por píxeles para evitar cualquier desborde o superposición."""
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test = " ".join(curr + [w])
        bbox = font.getbbox(test)
        if (bbox[2] - bbox[0]) <= max_width:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

# ==============================================================
# SLIDE 1: PORTADA EDITORIAL (ENCUADRE MILIMÉTRICO Y SIN OVERFLOW)
# ==============================================================
def create_slide_1():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    draw_header(canvas, draw, 1, 6)
    
    # Tag de categoría
    draw.rectangle([90, 200, 140, 204], fill=COLOR_TERRACOTA)
    draw.text((155, 192), "MANIFIESTO AUDIOVISUAL · 2026", font=font_bold(18), fill=COLOR_TERRACOTA)
    
    # Titular Masivo
    draw.text((90, 250), "HACEMOS", font=font_black(72), fill=COLOR_CARBON)
    draw.text((90, 330), "VIDEOS QUE", font=font_black(72), fill=COLOR_CARBON)
    draw.text((90, 410), "DESTACAN.", font=font_black(72), fill=COLOR_TERRACOTA)
    
    # Párrafo descriptivo
    draw.text((90, 520), "Producción audiovisual profesional con Inteligencia Artificial", font=font_medium(26), fill=COLOR_CARBON)
    draw.text((90, 560), "para empresas, comercios y marcas que buscan comunicar", font=font_medium(26), fill=COLOR_CARBON)
    draw.text((90, 600), "con la calidad y el impacto visual de una productora de cine.", font=font_medium(26), fill=COLOR_CARBON)
    
    # Card Bento de Pilares (Dibujado directamente en canvas para anti-aliasing perfecto)
    card_x = 90
    card_y = 695
    card_w = 900
    card_h = 210
    
    draw.rounded_rectangle(
        [(card_x, card_y), (card_x + card_w, card_y + card_h)],
        radius=20,
        fill=COLOR_WHITE,
        outline=COLOR_BORDER,
        width=2
    )
    
    # 3 Columnas perfectamente contenidas dentro de sus cajas
    cols = [
        ("ENTREGA 48 HS", ["De la idea al video final", "sin semanas de espera."]),
        ("CALIDAD 4K", ["Iluminación de cine y", "definición hiperrealista."]),
        ("FOCO EN VENTAS", ["Estructura pensada para", "convertir visitas en ventas."])
    ]
    
    for i, (col_t, lines) in enumerate(cols):
        cx = card_x + 40 + i * 290
        draw.text((cx, card_y + 40), col_t, font=font_extrabold(20), fill=COLOR_TERRACOTA)
        draw.text((cx, card_y + 82), lines[0], font=font_medium(17), fill=COLOR_CARBON)
        draw.text((cx, card_y + 114), lines[1], font=font_medium(17), fill=COLOR_CARBON)
        if i < 2:
            div_x = cx + 255
            draw.line([(div_x, card_y + 38), (div_x, card_y + 165)], fill=COLOR_BORDER, width=1)
            
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_01_portada.png", quality=98)
    print("Slide 1 generado con encuadre corregido.")

# ==============================================================
# SLIDE 2: EL MODELO TRADICIONAL VS NUEVA ERA
# ==============================================================
def create_slide_2():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    draw_header(canvas, draw, 2, 6)
    
    draw.rectangle([90, 195, 140, 199], fill=COLOR_TERRACOTA)
    draw.text((155, 187), "CAMBIO DE PARADIGMA", font=font_bold(18), fill=COLOR_TERRACOTA)
    
    draw.text((90, 235), "EL RODAJE TRADICIONAL", font=font_black(48), fill=COLOR_CARBON)
    draw.text((90, 295), "QUEDÓ EN EL PASADO.", font=font_black(48), fill=COLOR_CARBON)
    
    draw.text((90, 365), "Las marcas modernas no pueden esperar 20 días ni pagar fortunas por un solo reel.", font=font_medium(22), fill=COLOR_MUTED)
    
    # Card 1: Modelo Tradicional
    card1_y = 420
    draw.rounded_rectangle([(90, card1_y), (990, card1_y + 230)], radius=18, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
    draw.text((135, card1_y + 30), "EL MODELO ANTIGUO", font=font_bold(22), fill=(160, 60, 50, 255))
    draw.text((135, card1_y + 75), "— Semanas coordinando permisos, locaciones y actores.", font=font_medium(20), fill=COLOR_CARBON)
    draw.text((135, card1_y + 115), "— Costos que superan el presupuesto mensual de un negocio.", font=font_medium(20), fill=COLOR_CARBON)
    draw.text((135, card1_y + 155), "— Postproducción lenta que hace perder el momento de tendencia.", font=font_medium(20), fill=COLOR_CARBON)
    
    # Card 2: Con Producciones David
    card2_y = 680
    draw.rounded_rectangle([(90, card2_y), (990, card2_y + 290)], radius=18, fill=COLOR_CARBON)
    draw.rectangle([(90, card2_y), (990, card2_y + 6)], fill=COLOR_TERRACOTA)
    
    draw.text((135, card2_y + 35), "CON PRODUCCIONES DAVID (IA)", font=font_extrabold(24), fill=COLOR_MARFIL)
    draw.text((135, card2_y + 85), "✓ Producción express con entrega en 48 a 72 horas.", font=font_medium(20), fill=COLOR_MARFIL)
    draw.text((135, card2_y + 125), "✓ Cualquier locación del mundo generada con realismo cinematográfico.", font=font_medium(20), fill=COLOR_MARFIL)
    draw.text((135, card2_y + 165), "✓ Diseñado desde cero para rendimiento y pauta en Meta Ads y TikTok.", font=font_medium(20), fill=COLOR_MARFIL)
    draw.text((135, card2_y + 205), "✓ Costos accesibles que permiten publicar contenido continuo.", font=font_bold(20), fill=COLOR_TERRACOTA)
    
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_02_problema_solucion.png", quality=98)
    print("Slide 2 generado.")

# ==============================================================
# SLIDE 3: SERVICIO 01 - SPOTS DE PRODUCTO Y E-COMMERCE
# ==============================================================
def create_slide_3():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    draw_header(canvas, draw, 3, 6)
    
    draw.rectangle([90, 195, 140, 199], fill=COLOR_TERRACOTA)
    draw.text((155, 187), "SERVICIO 01 / 03", font=font_bold(18), fill=COLOR_TERRACOTA)
    
    draw.text((90, 235), "SPOTS DE PRODUCTO", font=font_black(48), fill=COLOR_CARBON)
    draw.text((90, 295), "Y E-COMMERCE.", font=font_black(48), fill=COLOR_CARBON)
    
    draw.text((90, 365), "Elevamos la percepción de valor de tu marca al nivel de las grandes firmas globales.", font=font_medium(22), fill=COLOR_MUTED)
    
    cards = [
        ("01 · DETALLE Y MACRO CINEMATOGRÁFICO",
         "Primeros planos hiperrealistas que exhiben texturas, brillos, materiales y acabados de tu producto con precisión milimétrica."),
        ("02 · ESCENARIOS Y FONDOS DE ENSUEÑO",
         "Situamos tu packaging en entornos naturales, arquitectónicos o abstractos de lujo sin alquilar estudios físicos."),
        ("03 · ITERACIONES PARA PERFORMANCE ADS",
         "Generamos variantes de ganchos visuales para testear en campañas publicitarias (A/B testing) y maximizar tu retorno.")
    ]
    
    card_y = 425
    for title, desc in cards:
        draw.rounded_rectangle([(90, card_y), (990, card_y + 160)], radius=16, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
        draw.rectangle([(90, card_y + 25), (96, card_y + 135)], fill=COLOR_TERRACOTA)
        draw.text((130, card_y + 28), title, font=font_extrabold(22), fill=COLOR_CARBON)
        
        lines = wrap_text_pixels(desc, font_regular(19), 810)
        draw.text((130, card_y + 75), lines[0], font=font_regular(19), fill=COLOR_MUTED)
        if len(lines) > 1:
            draw.text((130, card_y + 108), lines[1], font=font_regular(19), fill=COLOR_MUTED)
            
        card_y += 185
        
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_03_producto.png", quality=98)
    print("Slide 3 generado.")

# ==============================================================
# SLIDE 4: SERVICIO 02 - LOCALES Y GASTRONOMÍA
# ==============================================================
def create_slide_4():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    draw_header(canvas, draw, 4, 6)
    
    draw.rectangle([90, 195, 140, 199], fill=COLOR_TERRACOTA)
    draw.text((155, 187), "SERVICIO 02 / 03", font=font_bold(18), fill=COLOR_TERRACOTA)
    
    draw.text((90, 235), "REELS PARA COMERCIOS", font=font_black(48), fill=COLOR_CARBON)
    draw.text((90, 295), "Y GASTRONOMÍA.", font=font_black(48), fill=COLOR_CARBON)
    
    draw.text((90, 365), "Videos verticales pensados para despertar el deseo y llenar tu local este fin de semana.", font=font_medium(22), fill=COLOR_MUTED)
    
    cards = [
        ("01 · RETENCIÓN EN LOS PRIMEROS 3 SEGUNDOS",
         "Ganchos visuales de alto impacto diseñados para frenar el scroll del usuario antes de que deslice al siguiente video."),
        ("02 · ESTRATEGIA DE ATRACCIÓN LOCAL",
         "Contenido optimizado para conectar con vecinos de San Fernando, Zona Norte y público en tu radio de influencia."),
        ("03 · FORMATO VERTICAL 9:16 NATIVO",
         "Composiciones calibradas con zonas de seguridad oficiales para que ningún elemento tape tus promociones ni tu llamado a la acción.")
    ]
    
    card_y = 425
    for title, desc in cards:
        draw.rounded_rectangle([(90, card_y), (990, card_y + 160)], radius=16, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
        draw.rectangle([(90, card_y + 25), (96, card_y + 135)], fill=COLOR_TERRACOTA)
        draw.text((130, card_y + 28), title, font=font_extrabold(22), fill=COLOR_CARBON)
        
        lines = wrap_text_pixels(desc, font_regular(19), 810)
        draw.text((130, card_y + 75), lines[0], font=font_regular(19), fill=COLOR_MUTED)
        if len(lines) > 1:
            draw.text((130, card_y + 108), lines[1], font=font_regular(19), fill=COLOR_MUTED)
            
        card_y += 185
        
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_04_gastronomia.png", quality=98)
    print("Slide 4 generado.")

# ==============================================================
# SLIDE 5: SERVICIO 03 - VOCEROS Y AVATARES INSTITUCIONALES
# ==============================================================
def create_slide_5():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_MARFIL)
    draw = ImageDraw.Draw(canvas)
    draw_header(canvas, draw, 5, 6)
    
    draw.rectangle([90, 195, 140, 199], fill=COLOR_TERRACOTA)
    draw.text((155, 187), "SERVICIO 03 / 03", font=font_bold(18), fill=COLOR_TERRACOTA)
    
    draw.text((90, 235), "VOCEROS Y AVATARES", font=font_black(48), fill=COLOR_CARBON)
    draw.text((90, 295), "HIPERREALISTAS.", font=font_black(48), fill=COLOR_CARBON)
    
    draw.text((90, 365), "Comunicación empresarial e institucional continua sin depender de rodajes ni cámaras.", font=font_medium(22), fill=COLOR_MUTED)
    
    cards = [
        ("01 · LOCUCIÓN EN ESPAÑOL RIOPLATENSE",
         "Acento argentino nativo y entonación profesional creíble que conecta genuinamente con tu audiencia sin sonar artificial."),
        ("02 · SINCRONIZACIÓN LABIAL Y GESTUAL",
         "Lip-sync milimétrico y micro-expresiones que transmiten el prestigio y la seriedad que tu institución requiere."),
        ("03 · ESCALABILIDAD INSTITUCIONAL",
         "Comunica anuncios oficiales, capacitaciones, efemérides y lanzamientos en horas en lugar de semanas.")
    ]
    
    card_y = 425
    for title, desc in cards:
        draw.rounded_rectangle([(90, card_y), (990, card_y + 160)], radius=16, fill=COLOR_WHITE, outline=COLOR_BORDER, width=2)
        draw.rectangle([(90, card_y + 25), (96, card_y + 135)], fill=COLOR_TERRACOTA)
        draw.text((130, card_y + 28), title, font=font_extrabold(22), fill=COLOR_CARBON)
        
        lines = wrap_text_pixels(desc, font_regular(19), 810)
        draw.text((130, card_y + 75), lines[0], font=font_regular(19), fill=COLOR_MUTED)
        if len(lines) > 1:
            draw.text((130, card_y + 108), lines[1], font=font_regular(19), fill=COLOR_MUTED)
            
        card_y += 185
        
    paste_corner_shard(draw, 1080, 1080, 180)
    canvas.convert("RGB").save(OUT_DIR / "slide_05_avatares.png", quality=98)
    print("Slide 5 generado.")

# ==============================================================
# SLIDE 6: CIERRE Y LLAMADO A LA ACCIÓN (FONDO CARBÓN)
# ==============================================================
def create_slide_6():
    canvas = Image.new("RGBA", (1080, 1080), COLOR_CARBON)
    draw = ImageDraw.Draw(canvas)
    draw_header(canvas, draw, 6, 6, dark=True)
    
    draw.rectangle([90, 205, 140, 209], fill=COLOR_TERRACOTA)
    draw.text((155, 197), "PROPUESTA DE VALOR", font=font_bold(18), fill=COLOR_TERRACOTA)
    
    # Gran titular de cierre
    draw.text((90, 260), "LLEVÁ TU MARCA", font=font_black(62), fill=COLOR_MARFIL)
    draw.text((90, 335), "AL SIGUIENTE NIVEL.", font=font_black(62), fill=COLOR_TERRACOTA)
    
    draw.text((90, 440), "Diseñamos packs mensuales a medida para que tu negocio", font=font_medium(26), fill=COLOR_MARFIL)
    draw.text((90, 480), "mantenga una presencia activa, estética y con retorno real.", font=font_medium(26), fill=COLOR_MARFIL)
    
    # Gran Botón CTA Central
    draw.rounded_rectangle([(90, 570), (990, 700)], radius=20, fill=COLOR_MARFIL)
    draw.text((540, 615), "ESCRIBINOS POR WHATSAPP O DM", font=font_black(28), fill=COLOR_CARBON, anchor="mm")
    draw.text((540, 655), "Coordinamos una asesoría estratégica y muestra sin cargo", font=font_bold(20), fill=COLOR_TERRACOTA, anchor="mm")
    
    # Filas de Beneficios perfectamente espaciadas con márgenes simétricos
    b_y = 750
    draw.text((90, b_y), "✓ Entrega en 48 hs", font=font_bold(22), fill=COLOR_MARFIL)
    draw.text((365, b_y), "✓ Calidad Cinematográfica", font=font_bold(22), fill=COLOR_MARFIL)
    draw.text((700, b_y), "✓ Enfoque en Conversión", font=font_bold(22), fill=COLOR_MARFIL)
    
    # Línea divisoria
    draw.line([(90, 830), (990, 830)], fill=(50, 50, 50, 255), width=1)
    
    draw.text((90, 875), "📍 San Fernando, Buenos Aires · Producción para todo el país", font=font_regular(20), fill=(160, 160, 160, 255))
    draw.text((90, 915), "Instagram: @produccionesdavid.ar", font=font_bold(22), fill=COLOR_TERRACOTA)
    
    paste_corner_shard(draw, 1080, 1080, 200)
    canvas.convert("RGB").save(OUT_DIR / "slide_06_cta.png", quality=98)
    print("Slide 6 generado.")

if __name__ == "__main__":
    create_slide_1()
    create_slide_2()
    create_slide_3()
    create_slide_4()
    create_slide_5()
    create_slide_6()
    print("🎉 Carrusel perfeccionado con éxito en:", OUT_DIR)
