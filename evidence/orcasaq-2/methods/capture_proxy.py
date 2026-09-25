"""Capture every Athanor HTTP request and raw OpenAI-compatible response."""

import http.client
import json
import pathlib
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).resolve().parents[1] / "raw" / "proxy"
ROOT.mkdir(parents=True, exist_ok=True)
LOCK = threading.Lock()
NEXT = 0


class Capture(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"

    def do_POST(self):
        global NEXT
        with LOCK:
            NEXT += 1
            number = NEXT
        prefix = ROOT / f"{number:04d}"
        body = self.rfile.read(int(self.headers["Content-Length"]))
        prefix.with_suffix(".request.json").write_bytes(body)
        start = time.monotonic()
        upstream = http.client.HTTPConnection("127.0.0.1", 8094, timeout=900)
        headers = {k: v for k, v in self.headers.items() if k.lower() != "host"}
        upstream.request("POST", self.path, body=body, headers=headers)
        reply = upstream.getresponse()
        self.send_response(reply.status)
        for key, value in reply.getheaders():
            if key.lower() not in {"content-length", "transfer-encoding", "connection"}:
                self.send_header(key, value)
        self.send_header("Connection", "close")
        self.end_headers()
        with prefix.with_suffix(".response.raw").open("wb") as capture:
            while chunk := reply.read1(65536):
                capture.write(chunk)
                self.wfile.write(chunk)
                self.wfile.flush()
        prefix.with_suffix(".metadata.json").write_text(
            json.dumps({"path": self.path, "status": reply.status,
                        "elapsed_ms": round((time.monotonic() - start) * 1000)}, indent=2)
        )
        upstream.close()


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8095), Capture).serve_forever()
