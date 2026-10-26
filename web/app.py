"""Web application server for G*Power Clone Scientific Workbench (K4).

Uses built-in Python http.server - zero external dependencies required.
Serves static frontend and handles REST API requests:
    POST /api/calculate -> calls src.engine
    POST /api/chat      -> calls src.clinical_agent
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import sys
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

STATIC_DIR = os.path.join(BASE_DIR, "static")

from src.engine import calculate_a_priori, calculate_post_hoc, EngineError
from src.clinical_agent import ClinicalAgent

agent_instance = ClinicalAgent()


class WorkbenchHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler serving static workbench and API endpoints."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)

        if parsed_url.path == "/api/calculate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(post_data)
                mode = data.get("mode", "a-priori")
                w = data.get("w")
                alpha = data.get("alpha")
                df = data.get("df")

                if mode == "a-priori":
                    power = data.get("power")
                    result = calculate_a_priori(w=w, alpha=alpha, power=power, df=df)
                else:
                    n_total = data.get("n_total")
                    result = calculate_post_hoc(w=w, alpha=alpha, n_total=n_total, df=df)

                self.send_json_response(200, result)

            except EngineError as ee:
                self.send_json_response(400, ee.to_dict())
            except Exception as ex:
                self.send_json_response(500, {"error": str(ex), "code": "INTERNAL_ERROR", "field": "system"})

        elif parsed_url.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(post_data)
                query = data.get("query", "")
                resp = agent_instance.consult(query)
                self.send_json_response(200, resp)
            except Exception as ex:
                self.send_json_response(500, {"error": str(ex)})
        else:
            self.send_error(404, "Endpoint not found")

    def send_json_response(self, status_code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def run_server(port=5000):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, WorkbenchHandler)
    print(f"\n=========================================================")
    print(f"  G*Power Clone - Scientific Power Workbench (K4)")
    print(f"  Sunucu aktif: http://localhost:{port}")
    print(f"  Durdurmak icin Ctrl + C yapiniz.")
    print(f"=========================================================\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatildi.")
        httpd.server_close()


if __name__ == "__main__":
    port = 5000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
