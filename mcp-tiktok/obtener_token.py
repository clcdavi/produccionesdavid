#!/usr/bin/env python3
"""
Servidor local temporal para capturar el código OAuth de TikTok y canjearlo por el access_token definitivo.
"""
import http.server
import json
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CREDS_FILE = Path("/Users/davidcorrea/.gemini/antigravity/scratch/anuncios-san-fernando/tiktok_credenciales.json")
creds = json.loads(CREDS_FILE.read_text())

CLIENT_KEY = creds["client_key"]
CLIENT_SECRET = creds["client_secret"]
REDIRECT_URI = "http://127.0.0.1:8080/callback"

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/callback":
            qs = urllib.parse.parse_qs(parsed.query)
            code = qs.get("code", [""])[0]
            error = qs.get("error", [""])[0]
            error_desc = qs.get("error_description", [""])[0]

            if error:
                self.send_response(400)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h1>Error de autorización: {error}</h1><p>{error_desc}</p>".encode("utf-8"))
                return

            if code:
                # Canjear código por Access Token
                token_url = "https://open.tiktokapis.com/v2/oauth/token/"
                data = urllib.parse.urlencode({
                    "client_key": CLIENT_KEY,
                    "client_secret": CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": REDIRECT_URI
                }).encode("utf-8")

                req = urllib.request.Request(
                    token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

                try:
                    with urllib.request.urlopen(req, timeout=20) as resp:
                        token_data = json.loads(resp.read().decode())
                    
                    access_token = token_data.get("access_token") or token_data.get("data", {}).get("access_token")
                    refresh_token = token_data.get("refresh_token") or token_data.get("data", {}).get("refresh_token")
                    open_id = token_data.get("open_id") or token_data.get("data", {}).get("open_id")

                    if access_token:
                        creds["access_token"] = access_token
                        if refresh_token: creds["refresh_token"] = refresh_token
                        if open_id: creds["open_id"] = open_id
                        CREDS_FILE.write_text(json.dumps(creds, indent=2, ensure_ascii=False))

                        self.send_response(200)
                        self.send_header("Content-type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write("<h1>🎉 ¡TikTok Conectado con Éxito a Producciones David!</h1><p>Ya podés cerrar esta pestaña y volver al chat.</p>".encode("utf-8"))
                        print("🎉 TOKEN DE TIKTOK OBTENIDO Y GUARDADO CON ÉXITO!")
                    else:
                        self.send_response(400)
                        self.send_header("Content-type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(f"<h1>Respuesta de TikTok sin token:</h1><pre>{json.dumps(token_data, indent=2)}</pre>".encode("utf-8"))
                        print("Respuesta sin token:", token_data)
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(f"<h1>Error al canjear token:</h1><p>{e}</p>".encode("utf-8"))
                    print("Error canjeando token:", e)
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server_address = ("127.0.0.1", 8080)
    httpd = http.server.HTTPServer(server_address, CallbackHandler)
    print("Servidor callback escuchando en http://127.0.0.1:8080...")
    httpd.handle_request()  # Atiende una sola petición y termina
