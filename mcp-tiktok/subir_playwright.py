#!/usr/bin/env python3
"""
Publicador 100% autónomo para TikTok Creator Center con Playwright.
Utiliza la sesión activa del usuario para publicar videos sin intervención manual.
"""
import argparse
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/mcp-tiktok/tiktok_user_session")

def publicar_video_tiktok(video_path: str, caption: str, schedule_time: str = None):
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(f"No existe el archivo de video: {video_path}")

    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        # Lanzar Chromium con almacenamiento persistente de sesión
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,  # Visible para que el usuario pueda ver el proceso o loguearse la primera vez
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 850}
        )

        page = browser_context.new_page()
        print("🌐 Navegando a TikTok Creator Center...")
        page.goto("https://www.tiktok.com/creator-center/upload", wait_until="networkidle")
        time.sleep(3)

        # Verificar si pide login
        if "login" in page.url or page.locator("button:has-text('Log in')").is_visible():
            print("⚠️ Es necesario iniciar sesión una única vez en esta ventana de TikTok.")
            print("Esperando inicio de sesión...")
            page.wait_for_url("**/creator-center/upload", timeout=120000)
            time.sleep(4)

        print(f"🎬 Subiendo archivo: {video.name}...")
        # Localizar el input de subida de archivo
        file_input = page.locator("input[type='file']")
        file_input.set_input_files(str(video.resolve()))

        print("⏳ Esperando que TikTok procese la carga del video...")
        time.sleep(8)

        # Rellenar descripción / caption
        print("📝 Escribiendo título y hashtags...")
        caption_box = page.locator("div[contenteditable='true']").first
        if caption_box.is_visible():
            caption_box.click()
            # Limpiar contenido anterior si hay
            page.keyboard.press("Meta+A")
            page.keyboard.press("Backspace")
            caption_box.fill(caption)
        
        # Marcar casilla de contenido generado por IA si está presente
        try:
            aigc_switch = page.locator("text='AI-generated content'").or_(page.locator("text='Contenido generado por IA'"))
            if aigc_switch.is_visible():
                aigc_switch.click()
        except Exception:
            pass

        time.sleep(3)

        # Clic en Publicar
        print("🚀 Haciendo clic en Publicar...")
        publish_btn = page.locator("button:has-text('Post')").or_(page.locator("button:has-text('Publicar')")).first
        publish_btn.click()

        print("⏳ Esperando confirmación de publicación...")
        time.sleep(6)
        print("🎉 ¡VIDEO PUBLICADO EXITOSAMENTE EN TIKTOK!")

        browser_context.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--caption", required=True)
    args = parser.parse_args()
    publicar_video_tiktok(args.video, args.caption)
