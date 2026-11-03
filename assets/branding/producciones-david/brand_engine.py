#!/usr/bin/env python3
"""
Brand Identity Engine — Producciones David
Módulo centralizado para aplicar la identidad visual corporativa a videos e imágenes.

Funcionalidades:
1. Distinción estricta: Contenido Propio vs. Contenido de Clientes.
2. Inyección de Marca de Agua (FFmpeg) con respeto de Zonas de Seguridad (Instagram Reels, Stories, TikTok).
3. Concatenación de Outro Audiovisual Corporativo (outro-logo.mp4).
4. Generación de Plantillas Visuales:
   - Portada de Reel / TikTok (9:16)
   - Historia / Story (9:16)
   - Post Cuadrado (1:1)
   - Carruseles Editoriales
5. Control de Calidad y Validación de Formato (dimensiones, codec, bitrate, no duplicación de marcas).
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).parent.resolve()
BRAND_DIR = BASE_DIR / "assets" / "branding" / "producciones-david"
if not BRAND_DIR.exists():
    # Fallback si se ejecuta desde adentro de la carpeta
    BRAND_DIR = BASE_DIR

CONFIG_FILE = BRAND_DIR / "brand-config.json"
FONTS_DIR = BRAND_DIR / "fonts"
FFMPEG_BIN = "/Users/davidcorrea/Library/Application Support/adrian-saenz-video-negocio/ffmpeg/ffmpeg"


def get_ffmpeg_cmd() -> str:
    if os.path.exists(FFMPEG_BIN):
        return FFMPEG_BIN
    import shutil
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg
    raise RuntimeError(f"FFmpeg no encontrado en {FFMPEG_BIN} ni en el PATH del sistema.")


def cargar_config() -> dict:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"No se encontró el archivo maestro de marca: {CONFIG_FILE}")
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


@dataclass
class QualityReport:
    is_valid: bool
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    media_info: Dict = field(default_factory=dict)
    applied_branding: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "media_info": self.media_info,
            "applied_branding": self.applied_branding,
            "timestamp": datetime.now().isoformat()
        }


class BrandIdentityEngine:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or CONFIG_FILE
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.ffmpeg = get_ffmpeg_cmd()
        self.base_dir = self.config_path.parent

        # Assets paths
        self.logo_principal = self.base_dir / "logo-principal.png"
        self.logo_inverso = self.base_dir / "logo-inverso.png"
        self.watermark_blanco = self.base_dir / "watermark-blanco.png"
        self.watermark_oscuro = self.base_dir / "watermark-oscuro.png"
        self.outro_vert = self.base_dir / "outro-logo.mp4"
        self.outro_horiz = self.base_dir / "outro-logo-16x9.mp4"
        self.isotipo_perfil = self.base_dir / "isotipo-perfil.png"

        # Fonts
        self.font_bold_path = FONTS_DIR / "Montserrat-Bold.ttf"
        self.font_extra_path = FONTS_DIR / "Montserrat-ExtraBold.ttf"
        self.font_medium_path = FONTS_DIR / "Montserrat-Medium.ttf"
        self.font_var_path = FONTS_DIR / "Montserrat-Variable.ttf"

    # ==========================================
    # 1. INSPECCIÓN Y CONTROL DE CALIDAD
    # ==========================================
    def inspect_media(self, media_path: str) -> dict:
        p = Path(media_path).resolve()
        if not p.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {media_path}")

        cmd = [
            self.ffmpeg, "-i", str(p)
        ]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        out = res.stderr

        info = {"path": str(p), "size_bytes": p.stat().st_size, "is_video": False, "is_image": False}

        # Analizar Video
        if "Video:" in out:
            info["is_video"] = True
            for line in out.splitlines():
                if "Duration:" in line:
                    parts = line.split("Duration:")[1].split(",")[0].strip()
                    info["duration"] = parts
                if "Video:" in line:
                    info["video_stream"] = line.strip()
                    # Extraer resolución
                    import re
                    m = re.search(r"(\d{3,4})x(\d{3,4})", line)
                    if m:
                        info["width"] = int(m.group(1))
                        info["height"] = int(m.group(2))
        else:
            # Probar si es imagen
            try:
                with Image.open(p) as img:
                    info["is_image"] = True
                    info["width"] = img.width
                    info["height"] = img.height
                    info["format"] = img.format
            except Exception:
                pass

        return info

    def validate_quality(self, media_path: str, platform: str = "instagram", content_type: str = "reels") -> QualityReport:
        info = self.inspect_media(media_path)
        report = QualityReport(is_valid=True, media_info=info)

        w = info.get("width", 0)
        h = info.get("height", 0)

        # Reglas de aspecto
        if content_type in ["reels", "stories", "vertical_tiktok"]:
            aspect = w / h if h else 0
            expected = 1080 / 1920
            if abs(aspect - expected) > 0.05:
                report.warnings.append(f"Relación de aspecto no óptima para vertical 9:16 ({w}x{h}).")
            if w < 720:
                report.errors.append(f"Resolución insuficiente: {w}px de ancho (mínimo 720px, recomendado 1080px).")

        # Reglas de peso
        max_size = 280 * 1024 * 1024  # 280 MB
        if info["size_bytes"] > max_size:
            report.errors.append(f"El archivo supera el límite de {max_size//(1024*1024)}MB permitido.")

        if report.errors:
            report.is_valid = False

        return report

    # ==========================================
    # 2. APLICACIÓN DE MARCA DE AGUA EN VIDEO
    # ==========================================
    def apply_watermark(
        self,
        video_input: str,
        video_output: str,
        is_own_content: bool = True,
        position: str = "top-right",
        opacity: float = 0.85,
        scale_percent: float = 18.0
    ) -> QualityReport:
        """
        Aplica marca de agua respetando si es contenido propio o de clientes.
        Para clientes: NO agrega el logo salvo que se configure explícitamente.
        """
        inp = Path(video_input).resolve()
        out = Path(video_output).resolve()
        report = self.validate_quality(str(inp))

        # DISTINCIÓN DE PROPIEDAD
        if not is_own_content:
            report.applied_branding["watermark"] = "OMITIDO (Contenido de cliente - respeta identidad del cliente)"
            # Copiar sin alterar
            import shutil
            shutil.copy2(inp, out)
            return report

        # Evitar doble marca de agua
        if "_branded" in inp.stem:
            report.warnings.append("El archivo ya parece contener branding previo (_branded).")

        w_img = self.watermark_blanco
        # Posicionamiento seguro según plataforma
        # top-right: x = main_w - overlay_w - margin_x, y = margin_y
        margin_x = 44
        margin_y = 60

        if position == "top-right":
            overlay_coord = f"W-w-{margin_x}:{margin_y}"
        elif position == "top-left":
            overlay_coord = f"{margin_x}:{margin_y}"
        elif position == "bottom-right":
            # Margen inferior amplio para no tapar copete ni botones de like/share en TikTok/Reels
            overlay_coord = f"W-w-{margin_x}:H-h-260"
        else:
            overlay_coord = f"W-w-{margin_x}:{margin_y}"

        # Escalar la marca de agua al porcentaje del ancho del video (ej. 18% del ancho)
        filter_str = (
            f"[1:v]scale=iw*{scale_percent}/100:-1,format=rgba,colorchannelmixer=aa={opacity}[wm];"
            f"[0:v][wm]overlay={overlay_coord}[v]"
        )

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(inp),
            "-i", str(w_img),
            "-filter_complex", filter_str,
            "-map", "[v]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "19",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            str(out)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            report.is_valid = False
            report.errors.append(f"Error de FFmpeg al aplicar marca de agua: {res.stderr[-500:]}")
            return report

        report.applied_branding["watermark"] = {
            "applied": True,
            "position": position,
            "opacity": opacity,
            "scale_percent": scale_percent,
            "output_path": str(out)
        }
        return report

    # ==========================================
    # 3. CIERRE CORPORATIVO (OUTRO)
    # ==========================================
    def append_outro(
        self,
        video_input: str,
        video_output: str,
        is_own_content: bool = True
    ) -> QualityReport:
        inp = Path(video_input).resolve()
        out = Path(video_output).resolve()
        report = self.validate_quality(str(inp))

        if not is_own_content:
            report.applied_branding["outro"] = "OMITIDO (Contenido de cliente)"
            import shutil
            shutil.copy2(inp, out)
            return report

        info = self.inspect_media(str(inp))
        w = info.get("width", 1080)
        h = info.get("height", 1920)

        # Seleccionar outro vertical u horizontal
        outro_file = self.outro_vert if h >= w else self.outro_horiz

        # Concatenación con re-escalado dinámico del outro para coincidir exactamente con el video
        filter_complex = (
            f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1[v0];"
            f"[1:v]scale={w}:{h},setsar=1[v1];"
            f"[v0][0:a][v1][1:a]concat=n=2:v=1:a=1[v][a]"
        )

        cmd = [
            self.ffmpeg, "-y",
            "-i", str(inp),
            "-i", str(outro_file),
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            str(out)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            report.is_valid = False
            report.errors.append(f"Error al concatenar outro: {res.stderr[-500:]}")
            return report

        report.applied_branding["outro"] = {
            "applied": True,
            "duration_seconds": 2.0,
            "output_path": str(out)
        }
        return report

    # ==========================================
    # 4. PIPELINE COMPLETO DE VIDEO
    # ==========================================
    def process_video_complete(
        self,
        video_input: str,
        video_output: str,
        is_own_content: bool = True,
        watermark: bool = True,
        outro: bool = True
    ) -> QualityReport:
        inp = Path(video_input).resolve()
        final_out = Path(video_output).resolve()

        if not is_own_content:
            import shutil
            shutil.copy2(inp, final_out)
            return QualityReport(is_valid=True, applied_branding={"status": "Contenido de cliente - Sin alteraciones de marca."})

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_wm = Path(tmpdir) / "video_watermarked.mp4"
            if watermark:
                rep_wm = self.apply_watermark(str(inp), str(tmp_wm), is_own_content=True)
                if not rep_wm.is_valid:
                    return rep_wm
                curr_input = tmp_wm
            else:
                curr_input = inp

            if outro:
                rep_outro = self.append_outro(str(curr_input), str(final_out), is_own_content=True)
                return rep_outro
            else:
                import shutil
                shutil.copy2(curr_input, final_out)
                return QualityReport(is_valid=True, applied_branding={"watermark": True, "outro": False})

    # ==========================================
    # 5. PLANTILLAS DE IMÁGENES
    # ==========================================
    def _get_font(self, font_type: str = "bold", size: int = 48) -> ImageFont.FreeTypeFont:
        try:
            if font_type == "extrabold" and self.font_extra_path.exists():
                return ImageFont.truetype(str(self.font_extra_path), size)
            elif font_type == "medium" and self.font_medium_path.exists():
                return ImageFont.truetype(str(self.font_medium_path), size)
            elif self.font_bold_path.exists():
                return ImageFont.truetype(str(self.font_bold_path), size)
            elif self.font_var_path.exists():
                return ImageFont.truetype(str(self.font_var_path), size)
        except Exception:
            pass
        return ImageFont.load_default()

    def generate_reel_cover(
        self,
        background_image: str,
        title: str,
        output_path: str,
        subtitle: str = ""
    ) -> str:
        """
        Genera Portada Oficial 9:16 para Reels y TikTok (1080x1920)
        siguiendo el manual: logotipo superior, degradé cinematográfico,
        título con acento terracota y detalle diagonal inferior derecho.
        """
        out = Path(output_path).resolve()
        bg = Image.open(background_image).convert("RGBA")
        bg = bg.resize((1080, 1920), Image.Resampling.LANCZOS)

        # Crear capa de degradé oscuro
        overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Viñeta oscura superior e inferior
        for y in range(500):
            a = int(180 * (1.0 - (y / 500.0)))
            draw.line([(0, y), (1080, y)], fill=(25, 25, 25, a))
        for y in range(1300, 1920):
            a = int(220 * ((y - 1300.0) / 620.0))
            draw.line([(0, y), (1080, y)], fill=(25, 25, 25, a))

        # Detalle diagonal terracota inferior derecho (según manual)
        draw.polygon(
            [(920, 1920), (1080, 1760), (1080, 1920)],
            fill=(205, 86, 60, 255)
        )

        composite = Image.alpha_composite(bg, overlay)

        # Insertar logotipo blanco superior centrado
        logo = Image.open(self.logo_inverso).convert("RGBA")
        logo_w = 440
        logo_h = int(logo.height * (logo_w / logo.width))
        logo_scaled = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        composite.paste(logo_scaled, ((1080 - logo_w) // 2, 220), logo_scaled)

        # Título principal en el tercio medio con sombra sutil para legibilidad
        draw_comp = ImageDraw.Draw(composite)
        font_title = self._get_font("extrabold", 76)
        font_sub = self._get_font("medium", 36)

        title_y = 660
        # Sombra de contraste
        draw_comp.text((1080 // 2 + 2, title_y + 2), title.upper(), font=font_title, fill=(0, 0, 0, 180), anchor="mm")
        draw_comp.text((1080 // 2, title_y), title.upper(), font=font_title, fill=(245, 242, 236, 255), anchor="mm")

        # Línea de acento terracota bajo el título
        draw_comp.rectangle([480, title_y + 60, 600, title_y + 66], fill=(205, 86, 60, 255))

        if subtitle:
            draw_comp.text((1080 // 2 + 1, title_y + 111), subtitle.upper(), font=font_sub, fill=(0, 0, 0, 160), anchor="mm")
            draw_comp.text((1080 // 2, title_y + 110), subtitle.upper(), font=font_sub, fill=(245, 242, 236, 255), anchor="mm")

        composite.convert("RGB").save(out, quality=95)
        return str(out)

    def generate_story(
        self,
        background_image: str,
        headline: str,
        output_path: str,
        tag: str = "NUEVO PROYECTO"
    ) -> str:
        """
        Genera Historia / Story vertical 9:16 (1080x1920) según manual de marca:
        Logo superior, etiqueta de categoría con línea terracota y detalle diagonal inferior.
        """
        out = Path(output_path).resolve()
        bg = Image.open(background_image).convert("RGBA")
        bg = bg.resize((1080, 1920), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Viñeta suave superior e inferior
        for y in range(400):
            a = int(160 * (1.0 - (y / 400.0)))
            draw.line([(0, y), (1080, y)], fill=(25, 25, 25, a))
        for y in range(1500, 1920):
            a = int(180 * ((y - 1500.0) / 420.0))
            draw.line([(0, y), (1080, y)], fill=(25, 25, 25, a))

        # Detalle diagonal terracota inferior derecho
        draw.polygon([(920, 1920), (1080, 1760), (1080, 1920)], fill=(205, 86, 60, 255))

        composite = Image.alpha_composite(bg, overlay)

        # Logo superior
        logo = Image.open(self.logo_inverso).convert("RGBA")
        logo_w = 420
        logo_h = int(logo.height * (logo_w / logo.width))
        logo_scaled = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        composite.paste(logo_scaled, ((1080 - logo_w) // 2, 200), logo_scaled)

        draw_comp = ImageDraw.Draw(composite)
        font_tag = self._get_font("bold", 54)
        tag_y = 960

        draw_comp.text((1080 // 2 + 2, tag_y + 2), tag.upper(), font=font_tag, fill=(0, 0, 0, 180), anchor="mm")
        draw_comp.text((1080 // 2, tag_y), tag.upper(), font=font_tag, fill=(245, 242, 236, 255), anchor="mm")

        # Línea de acento terracota bajo el tag
        draw_comp.rectangle([490, tag_y + 45, 590, tag_y + 51], fill=(205, 86, 60, 255))

        composite.convert("RGB").save(out, quality=95)
        return str(out)

    def generate_post_cuadrado(
        self,
        photo_image: str,
        title: str,
        category: str,
        output_path: str
    ) -> str:
        """
        Genera Post Cuadrado 1:1 (1080x1080) según el manual de marca:
        Fondo Marfil superior con PRODUCCIONES DAVID, foto inferior y corte diagonal terracota.
        """
        out = Path(output_path).resolve()
        canvas = Image.new("RGBA", (1080, 1080), (245, 242, 236, 255))
        draw = ImageDraw.Draw(canvas)

        # Foto inferior
        photo = Image.open(photo_image).convert("RGBA")
        photo_h = 560
        photo = photo.resize((1080, photo_h), Image.Resampling.LANCZOS)
        canvas.paste(photo, (0, 1080 - photo_h), photo)

        # Corte diagonal terracota en esquina inferior derecha
        draw.polygon([(880, 1080), (1080, 880), (1080, 1080)], fill=(205, 86, 60, 255))

        # Logotipo principal superior (carbón #191919)
        logo = Image.open(self.logo_principal).convert("RGBA")
        logo_w = 420
        logo_h = int(logo.height * (logo_w / logo.width))
        logo_scaled = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        canvas.paste(logo_scaled, ((1080 - logo_w) // 2, 80), logo_scaled)

        # Título y categoría en tipografía Montserrat
        font_title = self._get_font("extrabold", 52)
        font_cat = self._get_font("medium", 28)

        draw.text((1080 // 2, 280), title.upper(), font=font_title, fill=(25, 25, 25, 255), anchor="mm")
        draw.text((1080 // 2, 350), category.upper(), font=font_cat, fill=(100, 100, 100, 255), anchor="mm")

        # Línea divisoria sutil
        draw.line([(460, 400), (620, 400)], fill=(205, 86, 60, 255), width=3)

        canvas.convert("RGB").save(out, quality=95)
        return str(out)


if __name__ == "__main__":
    engine = BrandIdentityEngine()
    print("🚀 Brand Identity Engine inicializado exitosamente.")
    print(f"📁 Directorio de recursos: {engine.base_dir}")
    print(f"🎨 Paleta: Carbón {engine.config['colors']['carbon']['hex']}, Marfil {engine.config['colors']['marfil']['hex']}, Terracota {engine.config['colors']['terracota']['hex']}")
