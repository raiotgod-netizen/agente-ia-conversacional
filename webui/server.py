"""
AI Agent WebUI — Servidor web para la interfaz.
Sirve archivos estaticos y proxea requests al Gateway.
"""
import os
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 8787
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class WebUIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)
    
    def log_message(self, format, *args):
        pass  # Silenciar logs

def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), WebUIHandler)
    print(f"WebUI escuchando en http://localhost:{PORT}")
    print(f"Abre http://localhost:{PORT} en tu navegador")
    print(f"Ctrl+C para detener")
    server.serve_forever()

if __name__ == "__main__":
    main()
