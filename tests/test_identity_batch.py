import json
import http.server
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import identity_batch


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.requests = []
        requests = self.requests

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                body = json.dumps({'choices': [{'message': {
                    'content': '', 'reasoning_content': 'I am Qwen.'},
                    'finish_reason': 'length'}], 'usage': {'completion_tokens': 8192}}).encode()
                self.send_response(200)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.endpoint = f'http://127.0.0.1:{self.server.server_port}/v1/chat/completions'
        self.job = {'id': 'identity-0000', 'condition': 'identity', 'order': 0,
                    'seed': 42, 'prompt': 'Who are you? Answer in one sentence.',
                    'reasoning_mode': 'low', 'max_tokens': 8192}

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temporary.cleanup()

    def test_truncation_and_empty_answer_survive_resume(self):
        directory = self.root / 'attempt'
        first = identity_batch.capture(self.endpoint, directory, self.job)
        second = identity_batch.capture(self.endpoint, directory, self.job)
        self.assertEqual(first, second)
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(first['finish_reason'], 'length')
        self.assertEqual((directory / 'answer.txt').read_text(), '')
        self.assertEqual((directory / 'reasoning.txt').read_text(), 'I am Qwen.')
        self.assertEqual(self.requests[0]['messages'], [
            {'role': 'user', 'content': self.job['prompt']}])
        self.assertEqual(self.requests[0]['model'], 'specimen')

    def test_incomplete_attempt_is_not_replaced(self):
        directory = self.root / "attempt"
        directory.mkdir()
        (directory / "request.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "Unresolved prior attempt"):
            identity_batch.capture(self.endpoint, directory, self.job)
        self.assertEqual(self.requests, [])

    def test_tampered_response_is_not_reused(self):
        directory = self.root / "attempt"
        directory.mkdir()
        request = identity_batch.request_for(self.job)
        (directory / "response.json").write_text("changed")
        (directory / "capture.json").write_text(json.dumps({
            "job": self.job, "request": request, "response_sha256": "original"}))
        with self.assertRaisesRegex(ValueError, "Raw response changed"):
            identity_batch.capture(self.endpoint, directory, self.job)
        self.assertEqual(self.requests, [])


class PlanTests(unittest.TestCase):
    def test_registered_pilots_do_not_overlap_main_seeds(self):
        root = Path(__file__).resolve().parents[1] / "evidence/coder390"
        seeds = {}
        for phase in ("pilot", "main"):
            for condition in ("identity", "portrait"):
                plan = identity_batch.read_plan(root / f"{phase}-{condition}-plan.jsonl")
                seeds[phase, condition] = {r["seed"] for r in plan}
        self.assertEqual(len(seeds["main", "identity"]), 100)
        self.assertEqual(seeds["main", "identity"], seeds["main", "portrait"])
        self.assertFalse(seeds["pilot", "identity"] & seeds["main", "identity"])


if __name__ == "__main__":
    unittest.main()
