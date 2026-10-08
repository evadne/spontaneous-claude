import json
import http.server
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import identity_batch
import coder390_cuda


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

    def test_migration_preserves_completed_draws_and_refuses_unresolved_attempts(self):
        first = dict(self.job, id='identity-0000')
        second = dict(self.job, id='identity-0001', seed=43, order=1)
        identity_batch.capture(self.endpoint, self.root / first['id'], first)
        self.assertEqual(coder390_cuda.remaining_jobs([first, second], self.root), [second])
        self.assertEqual(len(self.requests), 1)
        (self.root / second['id']).mkdir()
        (self.root / second['id'] / 'request.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Unresolved attempt'):
            coder390_cuda.remaining_jobs([first, second], self.root)

    def test_migration_refuses_changed_evidence(self):
        directory = self.root / self.job['id']
        identity_batch.capture(self.endpoint, directory, self.job)
        (directory / 'response.json').write_text('changed')
        with self.assertRaises(AssertionError):
            coder390_cuda.remaining_jobs([self.job], self.root)

    def test_timeout_recovery_retains_failure_and_does_not_resample_success(self):
        prior = self.root / 'prior'
        attempt = prior / self.job['id']
        attempt.mkdir(parents=True)
        request = json.dumps(identity_batch.request_for(self.job))
        error = json.dumps({'error_type': 'timeout', 'error': 'timed out'})
        (attempt / 'request.json').write_text(request)
        (attempt / 'error.json').write_text(error)
        out = self.root / 'recovery' / self.job['id']
        with self.assertRaisesRegex(ValueError, 'Unresolved prior attempt'):
            identity_batch.capture_with_prior(self.endpoint, out, self.job, 14400, prior, [])
        first = identity_batch.capture_with_prior(
            self.endpoint, out, self.job, 14400, prior, [self.job['id']])
        second = identity_batch.capture_with_prior(
            self.endpoint, out, self.job, 14400, prior, [self.job['id']])
        self.assertEqual(first, second)
        self.assertEqual(first['transport_timeout_seconds'], 14400)
        self.assertEqual((attempt / 'request.json').read_text(), request)
        self.assertEqual((attempt / 'error.json').read_text(), error)
        self.assertTrue((out / 'retry-provenance.json').exists())
        self.assertEqual(self.requests, [identity_batch.request_for(self.job)])

    def test_prior_success_is_reused_in_place(self):
        prior = self.root / 'prior'
        identity_batch.capture(self.endpoint, prior / self.job['id'], self.job)
        out = self.root / 'recovery' / self.job['id']
        identity_batch.capture_with_prior(self.endpoint, out, self.job, 14400, prior, [])
        self.assertEqual(len(self.requests), 1)
        self.assertFalse(out.exists())

    def test_retry_refuses_an_unreconciled_response(self):
        prior = self.root / 'prior'
        attempt = prior / self.job['id']
        attempt.mkdir(parents=True)
        (attempt / 'request.json').write_text(json.dumps(identity_batch.request_for(self.job)))
        (attempt / 'error.json').write_text(json.dumps({'error_type': 'timeout'}))
        (attempt / 'response.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'without a response'):
            identity_batch.capture_with_prior(self.endpoint, self.root / 'recovery',
                self.job, 14400, prior, [self.job['id']])
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
