#!/usr/bin/env python3
"""
Publicador 100% autónomo para TikTok Creator Center con Playwright.
Utiliza la sesión persistente guardada en tiktok_user_session.
Soporta bypass de overlays (react-joyride, popups de bienvenida y toasts)
y configuración de privacidad pública ("Todo el mundo").
"""
import argparse
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Integración con Brand Identity Engine
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
    from brand_engine import BrandIdentityEngine
    BRAND_ENGINE_AVAILABLE = True
except Exception:
    BRAND_ENGINE_AVAILABLE = False

SESSION_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/mcp-tiktok/tiktok_user_session")
SCREENSHOT_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/mcp-tiktok/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def limpiar_overlays(page):
    """Elimina react-joyride, modales de bienvenida y toasts flotantes que bloquean clics."""
    try:
        page.evaluate("""() => {
            const joyride = document.getElementById('react-joyride-portal');
            if (joyride) joyride.remove();
            
            document.querySelectorAll('.react-joyride__overlay, [data-floating-ui-portal], .TUXToast').forEach(el => el.remove());
            
            // Cerrar botones de tutoriales si existen
            const skipBtns = Array.from(document.querySelectorAll('button')).filter(b => 
                b.textContent.includes('Skip') || b.textContent.includes('Omitir') || 
                b.textContent.includes('Dismiss') || b.textContent.includes('Entendido') ||
                b.textContent.includes('Next') || b.textContent.includes('Siguiente')
            );
            skipBtns.forEach(b => { try { b.click(); } catch(e){} });
        }""")
        page.keyboard.press("Escape")
    except Exception as e:
        print("Aviso limpiando overlays:", e)

def publicar_video_tiktok(video_path: str, caption: str, publico: bool = True, es_propio: bool = True, aplicar_branding: bool = False):
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(f"No existe el archivo de video: {video_path}")

    # Aplicar identidad visual corporativa si corresponde
    if aplicar_branding and BRAND_ENGINE_AVAILABLE:
        if es_propio:
            print("🎨 [Brand Engine] Aplicando identidad visual corporativa de Producciones David...")
            engine = BrandIdentityEngine()
            branded_video_path = video.parent / f"{video.stem}_branded.mp4"
            report = engine.process_video_complete(str(video), str(branded_video_path), is_own_content=True)
            if report.is_valid and branded_video_path.exists():
                print(f"✅ Video procesado con identidad oficial: {branded_video_path.name}")
                video = branded_video_path
            else:
                print("⚠️ Aviso en Brand Engine:", report.errors)
        else:
            print("🛡️ [Brand Engine] Contenido de cliente: se respeta identidad del cliente sin marca de agencia.")

    print(f"🎬 [TikTok Autónomo] Iniciando publicación de: {video.name}")

    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            viewport={"width": 1280, "height": 900}
        )

        page = browser_context.new_page()
        print("🌐 Navegando a TikTok Creator Center...")
        page.goto("https://www.tiktok.com/creator-center/upload", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)

        limpiar_overlays(page)

        # Inyectar el video en el input file
        print("📤 Inyectando archivo de video...")
        file_input = page.locator("input[type='file']").first
        if not file_input.is_visible():
            file_input.wait_for(state="attached", timeout=15000)
        file_input.set_input_files(str(video.resolve()))

        print("⏳ Esperando que TikTok procese la carga del video (15s)...")
        time.sleep(15)
        limpiar_overlays(page)

        # Escribir la descripción / caption
        print("📝 Escribiendo copete y hashtags...")
        try:
            limpiar_overlays(page)
            caption_box = page.locator("div[contenteditable='true']").first
            caption_box.wait_for(state="attached", timeout=10000)
            
            try:
                caption_box.click(force=True, timeout=5000)
            except Exception:
                page.evaluate("el => el.focus()", caption_box.element_handle())

            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            time.sleep(0.5)
            page.keyboard.type(caption, delay=20)
            print("✅ Copete insertado correctamente.")
        except Exception as e:
            print("⚠️ Aviso al escribir copete:", e)

        # Configurar Privacidad: Todo el mundo (Público)
        if publico:
            try:
                limpiar_overlays(page)
                # Probar si hay opción de radio o selector con texto "Todo el mundo" o "Public"
                pub_opt = page.locator("label:has-text('Todo el mundo')").or_(
                    page.locator("label:has-text('Public')")
                ).or_(
                    page.locator("span:has-text('Todo el mundo')")
                ).first
                if pub_opt.is_visible(timeout=3000):
                    pub_opt.click(force=True)
                    print("✅ Privacidad seleccionada: Todo el mundo.")
                else:
                    # Si es un selector dropdown
                    dropdown = page.locator("div[role='combobox']:has-text('Solo yo')").or_(
                        page.locator("div[role='combobox']:has-text('Amigos')")
                    ).first
                    if dropdown.is_visible(timeout=3000):
                        dropdown.click(force=True)
                        time.sleep(1)
                        page.locator("div[role='option']:has-text('Todo el mundo')").or_(
                            page.locator("div[role='option']:has-text('Public')")
                        ).first.click(force=True)
                        print("✅ Privacidad cambiada a: Todo el mundo.")
            except Exception as e:
                print("Aviso configurando privacidad:", e)

        # Asegurar casilla de contenido IA si aparece
        try:
            limpiar_overlays(page)
            aigc_toggle = page.locator("text='AI-generated content'").or_(page.locator("text='Contenido generado por IA'")).first
            if aigc_toggle.is_visible(timeout=2000):
                aigc_toggle.click(force=True)
                print("✅ Etiqueta de contenido IA activada.")
        except Exception:
            pass

        time.sleep(3)
        limpiar_overlays(page)

        # Clic en el botón Publicar
        print("🚀 Presionando botón Publicar...")
        publish_btn = page.locator("button[data-e2e='post_video_button']").or_(
            page.locator("button:has-text('Post')")
        ).or_(
            page.locator("button:has-text('Publicar')")
        ).first

        publish_btn.wait_for(state="visible", timeout=15000)
        
        try:
            publish_btn.click(force=True, timeout=10000)
        except Exception as e:
            print("Fallback: dispatching click via JavaScript:", e)
            page.evaluate("""() => {
                const btn = document.querySelector('button[data-e2e="post_video_button"]') || 
                            Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Post') || b.textContent.includes('Publicar'));
                if (btn) btn.click();
            }""")

        print("⏳ Esperando que TikTok confirme la publicación...")
        time.sleep(12)
        
        screenshot_path = SCREENSHOT_DIR / f"publicado_{video.stem}.png"
        page.screenshot(path=str(screenshot_path))
        print(f"📸 Captura guardada en: {screenshot_path}")

        print("🎉 ¡PROCESO DE PUBLICACIÓN COMPLETADO EN TIKTOK!")
        browser_context.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--brand", action="store_true", help="Aplica automáticamente marca de agua y outro oficial")
    parser.add_argument("--client-content", action="store_true", help="Indica que es contenido de cliente para no aplicar marca de agua de la agencia")
    args = parser.parse_args()
    publicar_video_tiktok(
        video_path=args.video,
        caption=args.caption,
        es_propio=not args.client_content,
        aplicar_branding=args.brand
    )
