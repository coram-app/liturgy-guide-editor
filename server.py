#!/usr/bin/env python3
"""
Servidor local pro Liturgy Guide Editor.

Roda em http://localhost:8765/editor.html

- Serve os arquivos do diretório do projeto (Liturgy Guide Editor)
- Auto-salva edições em .cache/boletim.html (POST /api/cache)
- Permite sobrescrever boletim.html original (POST /api/save)
- Limpa o cache (POST /api/clear-cache)

Uso:
    cd "Liturgy Guide Editor"
    python3 server.py            # porta padrão 8765
    python3 server.py 9000       # outra porta

Abra http://localhost:8765/editor.html no navegador.
Ctrl+C para parar.
"""

import http.server
import json
import socketserver
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / ".cache"
CACHE_FILE = CACHE_DIR / "boletim.html"
SOURCE_FILE = ROOT / "boletim.html"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765


class BoletimHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _json(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode("utf-8") if length else ""

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self._json(200, {"ok": True})
        if path == "/api/cache":
            if CACHE_FILE.exists():
                content = CACHE_FILE.read_text(encoding="utf-8")
                mtime = CACHE_FILE.stat().st_mtime
                return self._json(200, {"exists": True, "html": content, "mtime": mtime})
            return self._json(200, {"exists": False})
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        body = self._read_body()
        try:
            if path == "/api/cache":
                data = json.loads(body)
                html = data.get("html", "")
                CACHE_DIR.mkdir(exist_ok=True)
                CACHE_FILE.write_text(html, encoding="utf-8")
                return self._json(200, {"ok": True})
            if path == "/api/save":
                data = json.loads(body)
                html = data.get("html", "")
                SOURCE_FILE.write_text(html, encoding="utf-8")
                if CACHE_FILE.exists():
                    CACHE_FILE.unlink()
                return self._json(200, {"ok": True})
            if path == "/api/clear-cache":
                if CACHE_FILE.exists():
                    CACHE_FILE.unlink()
                return self._json(200, {"ok": True})
        except Exception as e:
            return self._json(500, {"ok": False, "error": str(e)})
        return self._json(404, {"error": "not found"})

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")


def main():
    print(f"Editor:    http://localhost:{PORT}/editor.html")
    print(f"Documento: http://localhost:{PORT}/boletim.html (visualização limpa)")
    print(f"Diretório: {ROOT}")
    print(f"Cache:     {CACHE_FILE}")
    print(f"Original:  {SOURCE_FILE}")
    print("Ctrl+C para parar.\n")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("localhost", PORT), BoletimHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor parado.")


if __name__ == "__main__":
    main()
