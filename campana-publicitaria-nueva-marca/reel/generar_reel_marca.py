#!/usr/bin/env python3
"""
Generador del Reel Publicitario Oficial (9:16 - 1080x1920) — PRODUCCIONES DAVID
Aplica la nueva identidad de marca:
- Subtítulos y placas en Carbón #191919, Marfil #F5F2EC y Terracota #CD563C.
- Marca de agua oficial en zona segura superior derecha.
- Cierre corporativo audiovisual oficial (outro-logo.mp4 de 2.0s).
- Zonas seguras respetadas para Instagram Reels y TikTok.
"""
import subprocess
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando")
BRAND_DIR = BASE_DIR / "assets" / "branding" / "producciones-david"
CAMP_DIR = BASE_DIR / "campana-lanzamiento-pd"
REEL_DIR = BASE_DIR / "campana-publicitaria-nueva-marca" / "reel"
REEL_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG = "/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg"
FONTS_DIR = BRAND_DIR / "fonts"

COLOR_CARBON = (25, 25, 25, 255)
COLOR_MARFIL = (245, 242, 236, 255)
COLOR_TERRACOTA = (205, 86, 60, 255)
COLOR_WHITE = (255, 255, 255, 255)

font_black = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Black.ttf"), s)
font_bold = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Bold.ttf"), s)
font_medium = lambda s: ImageFont.truetype(str(FONTS_DIR / "Montserrat-Medium.ttf"), s)

watermark = Image.open(BRAND_DIR / "watermark-blanco.png").convert("RGBA")

def create_overlay(pill_text: str, subtitle_line1: str, subtitle_line2: str = "") -> Path:
    canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # 1. Pill superior (Categoría / Servicio)
    pill_font = font_bold(24)
    # Medir texto
    bbox = draw.textbbox((0, 0), pill_text.upper(), font=pill_font)
    tw = bbox[2] - bbox[0]
    pw = tw + 70
    px = (1080 - pw) // 2
    py = 180
    
    # Pill fondo Carbón con borde Terracota
    draw.rounded_rectangle([(px, py), (px + pw, py + 56)], radius=28, fill=(25, 25, 25, 230), outline=COLOR_TERRACOTA, width=2)
    draw.text((1080 // 2, py + 28), pill_text.upper(), font=pill_font, fill=COLOR_MARFIL, anchor="mm")
    
    # 2. Marca de agua oficial en esquina superior derecha (zona segura)
    wm_w = 260
    wm_h = int(watermark.height * (wm_w / watermark.width))
    wm_s = watermark.resize((wm_w, wm_h), Image.Resampling.LANCZOS)
    canvas.paste(wm_s, (1080 - wm_w - 50, 70), wm_s)
    
    # 3. Zócalo inferior de subtítulos (zona segura: y = 1420)
    card_y = 1420
    draw.rounded_rectangle([(60, card_y), (1020, card_y + 160)], radius=24, fill=(245, 242, 236, 245), outline=COLOR_TERRACOTA, width=3)
    
    # Terracotta accent tick en esquina de la card
    draw.polygon([(960, card_y + 160), (1020, card_y + 100), (1020, card_y + 160)], fill=COLOR_TERRACOTA)
    
    if subtitle_line2:
        draw.text((540, card_y + 55), subtitle_line1, font=font_black(34), fill=COLOR_CARBON, anchor="mm")
        draw.text((540, card_y + 105), subtitle_line2, font=font_black(34), fill=COLOR_CARBON, anchor="mm")
    else:
        draw.text((540, card_y + 80), subtitle_line1, font=font_black(36), fill=COLOR_CARBON, anchor="mm")
        
    out_path = REEL_DIR / f"overlay_{abs(hash(pill_text))}.png"
    canvas.save(out_path)
    return out_path

def assemble_reel():
    print("Creando overlays de marca...")
    ov1 = create_overlay("01 · PRODUCTOS & COMERCIO", "¿Tu negocio todavía no tiene", "videos de nivel cinematográfico?")
    ov2 = create_overlay("02 · EMPRESAS E INSTITUCIONES", "Presentadores y spots con IA", "creados en tiempo récord.")
    ov3 = create_overlay("03 · CONVERSIÓN Y VENTAS", "Impulsá tu marca hoy.", "Escribinos y coordinamos tu muestra.")
    
    # Clips de origen
    c1 = CAMP_DIR / "test_veo31_01.mp4"
    c2 = CAMP_DIR / "veo31_clip_02_presentadores.mp4"
    c3 = CAMP_DIR / "veo31_clip_03.mp4"
    outro = BRAND_DIR / "outro-logo.mp4"
    
    # Segmentos temporales
    s1 = REEL_DIR / "s1.mp4"
    s2 = REEL_DIR / "s2.mp4"
    s3 = REEL_DIR / "s3.mp4"
    
    print("Renderizando Segmento 1...")
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(c1),
        "-i", str(ov1),
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v0];"
        "[v0][1:v]overlay=0:0[v]",
        "-map", "[v]", "-map", "0:a?",
        "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        str(s1)
    ], check=True, capture_output=True)
    
    print("Renderizando Segmento 2...")
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(c2),
        "-i", str(ov2),
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v0];"
        "[v0][1:v]overlay=0:0[v]",
        "-map", "[v]", "-map", "0:a?",
        "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        str(s2)
    ], check=True, capture_output=True)
    
    print("Renderizando Segmento 3...")
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(c3),
        "-i", str(ov3),
        "-filter_complex",
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v0];"
        "[v0][1:v]overlay=0:0[v];"
        "[0:a]highpass=f=120,compand=attacks=0.02:decays=0.15:points=-70/-70|-24/-12|0/-2:gain=5[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        str(s3)
    ], check=True, capture_output=True)
    
    # Concatenar s1 + s2 + s3 + outro
    final_reel = REEL_DIR / "reel_publicitario_producciones_david.mp4"
    print("Concatenando Reel completo con Outro Corporativo Oficial...")
    subprocess.run([
        FFMPEG, "-y",
        "-i", str(s1),
        "-i", str(s2),
        "-i", str(s3),
        "-i", str(outro),
        "-filter_complex",
        "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a]concat=n=4:v=1:a=1[v][a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        str(final_reel)
    ], check=True, capture_output=True)
    
    # Limpiar temporales
    s1.unlink(missing_ok=True)
    s2.unlink(missing_ok=True)
    s3.unlink(missing_ok=True)
    ov1.unlink(missing_ok=True)
    ov2.unlink(missing_ok=True)
    ov3.unlink(missing_ok=True)
    
    print(f"🎉 Reel Publicitario generado exitosamente en: {final_reel}")
    return final_reel

if __name__ == "__main__":
    assemble_reel()
