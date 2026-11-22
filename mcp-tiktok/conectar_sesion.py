#!/usr/bin/env python3
"""
Abre una ventana de Chrome con el perfil dedicado de TikTok.
Una vez que el usuario inicia sesión y llega a /creator-center/upload o /tiktok.com,
la sesión queda guardada para siempre en tiktok_user_session.
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SESSION_DIR = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/mcp-tiktok/tiktok_user_session")
SESSION_DIR.mkdir(parents=True, exist_ok=True)

print("🚀 Abriendo ventana de Chrome para conectar tu cuenta de TikTok...")
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_DIR),
        headless=False,
        channel="chrome",
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1280, "height": 850}
    )
    page = browser.new_page()
    page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded")
    
    print("\n👉 Por favor, iniciá sesión en la ventana de Chrome que se abrió (con correo o QR).")
    print("⏳ Esperando que completes el login... (la ventana se cerrará sola cuando detecte el acceso)")

    # Esperar hasta que la URL no sea login o aparezca la cookie de sesión
    for _ in range(120):  # hasta 10 minutos
        time.sleep(5)
        cookies = browser.cookies()
        logged_in = any(c["name"] in ("sessionid", "sessionid_ss", "sid_tt") for c in cookies)
        if logged_in or ("login" not in page.url and "tiktok.com/@" in page.url):
            print("\n🎉 ¡SESIÓN DE TIKTOK DETECTADA Y GUARDADA CON ÉXITO!")
            time.sleep(3)
            break

    browser.close()
    print("✅ Perfil listo para publicaciones 100% automáticas.")
