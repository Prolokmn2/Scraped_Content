"""
Local server for LeerLab Kids V2 pentest copy.
Run: python serve.py
Then open: http://localhost:5500
"""

import os
import http.server
import socketserver

PORT = 5500
ROOT = os.path.dirname(os.path.abspath(__file__))


class SPAHandler(http.server.SimpleHTTPRequestHandler):
    """Serves files from the V2 folder as root.
    Falls back to index.html for unknown paths (React SPA routing)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        # Check if the requested file actually exists on disk
        path = self.translate_path(self.path)
        if not os.path.exists(path) and not self.path.startswith("/assets/"):
            # Unknown route → let React Router handle it
            self.path = "/index.html"
        super().do_GET()

    def log_message(self, fmt, *args):
        # Clean up the log output
        code = args[1] if len(args) > 1 else "???"
        symbol = "OK " if str(code).startswith("2") or str(code) == "304" else "ERR"
        print(f"  {symbol} {args[1]}  {args[0]}")


print(f"Serving V2 on http://localhost:{PORT}")
print(f"Root: {ROOT}\n")

with socketserver.TCPServer(("", PORT), SPAHandler) as httpd:
    httpd.serve_forever()
