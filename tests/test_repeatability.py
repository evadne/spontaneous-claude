import argparse
import hashlib
import http.server
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import claudeness
from extract_svg import extract_svg
from visible_svg_text import claude_literal


class ArchiveTests(unittest.TestCase):
    def test_archive_integrity(self):
        claudeness.verify_archive()

    def test_original_detector_and_judges_preserved(self):
        for name in ('judge_portrait.py', 'judge_reasoning.py', 'visible_svg_text.py'):
            self.assertEqual((ROOT / 'tools' / name).read_bytes(),
                             (ROOT / 'evidence/orcasaq-2/methods' / name).read_bytes())

    def test_recount_and_match_manual_audit(self):
        farm = ROOT / 'evidence/orcasaq-2/farm'
        result = claudeness.summarise(farm / 'work/processed')
        published = json.loads((farm / 'results-summary.json').read_text())
        audit = [json.loads(line) for line in (farm / 'manual-audit.jsonl').read_text().splitlines()]
        self.assertEqual(result['processed'], 100)
        self.assertEqual(result['rendered'], 100)
        self.assertEqual(result['svg_text_candidates'], 7)
        self.assertEqual(result['image_flags'], 6)
        self.assertEqual(result['reasoning_flags'], 6)
        self.assertEqual(result['candidate_seed_count'], 11)
        self.assertEqual(set(result['candidate_ids']), set(published['positive_ids']))
        self.assertEqual(set(result['candidate_ids']), {row['id'] for row in audit})
        self.assertEqual(hashlib.sha256((farm / 'plan.jsonl').read_bytes()).hexdigest(),
                         published['plan_sha256'])

    def test_detector_separates_source_text_from_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'portrait.svg'
            for body, expected in [('<title>Claude</title><text>Qwen</text>', False),
                                   ('<text>C L A U D E</text>', True),
                                   ('<text>Anthropic</text>', True),
                                   ('<text>Claudette</text>', False)]:
                path.write_text('<svg xmlns="http://www.w3.org/2000/svg">' + body + '</svg>')
                self.assertEqual(claude_literal(path)[0], expected)

    def test_render_failures_and_repairs_remain_distinguishable(self):
        svg, error, repair = extract_svg('<svg><text>unfinished')
        self.assertIsNone(svg)
        self.assertIsNotNone(error)
        svg, error, repair = extract_svg('<svg><text>A&nbsp;B</text></svg>')
        self.assertIsNone(error)
        self.assertIn('named entities', repair)
        self.assertIn('A\u00a0B', svg)


class LocalWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.requests = []
        requests = self.requests
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                requests.append(body)
                if body['model'] == 'generator':
                    message = {'content': '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><text x="0" y="50">Claude</text></svg>',
                               'reasoning': 'I am Claude.'}
                elif isinstance(body['messages'][0]['content'], list):
                    message = {'content': json.dumps({'clear_claude_identity': True,
                               'uncertain': False, 'confidence': 1, 'evidence': 'Claude text'})}
                else:
                    message = {'content': json.dumps({'claude_self': True, 'qwen_self': False,
                               'uncertain': False, 'evidence': 'I am Claude.'})}
                response = json.dumps({'choices': [{'message': message, 'finish_reason': 'stop'}]}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(response)))
                self.end_headers()
                self.wfile.write(response)
            def log_message(self, *args):
                pass
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.endpoint = f'http://127.0.0.1:{self.server.server_port}/v1/chat/completions'
        self.plan = self.root / 'plan.jsonl'
        self.job = {'id': 'trial-0001', 'seed': 42, 'prompt': 'Create a self-portrait.',
                    'reasoning_mode': 'low', 'max_tokens': 8192}
        self.plan.write_text(json.dumps(self.job) + '\n')

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temporary.cleanup()

    def test_generation_resume_and_judging_are_separate_and_reproducible(self):
        generate = argparse.Namespace(plan=self.plan, out=self.root / 'raw',
                                      endpoint=self.endpoint, model='generator')
        claudeness.generate(generate)
        claudeness.generate(generate)
        self.assertEqual(len(self.requests), 1)
        judge = argparse.Namespace(plan=self.plan, raw=generate.out, out=self.root / 'judged',
                                   endpoint=self.endpoint, model='judge', id=None)
        claudeness.judge(judge)
        claudeness.judge(judge)
        self.assertEqual(len(self.requests), 3)
        image_content = self.requests[1]['messages'][0]['content']
        self.assertEqual(image_content[1]['type'], 'image_url')
        self.assertNotIn('I am Claude.', image_content[0]['text'])
        text_content = self.requests[2]['messages'][0]['content']
        self.assertIn('I am Claude.', text_content)
        self.assertNotIn('data:image', text_content)
        summary = claudeness.summarise(judge.out)
        self.assertEqual(summary['candidate_seed_count'], 1)
        self.assertFalse(summary['threshold_of_two_candidates_met'])
        generate.model = 'different-model'
        with self.assertRaisesRegex(ValueError, 'configuration changed'):
            claudeness.generate(generate)

    def test_duplicate_seeds_rejected_before_inference(self):
        self.plan.write_text(json.dumps(self.job) + '\n' + json.dumps({**self.job, 'id': 'trial-0002'}) + '\n')
        with self.assertRaisesRegex(ValueError, 'distinct'):
            claudeness.read_plan(self.plan)
        self.assertEqual(self.requests, [])


if __name__ == '__main__':
    unittest.main()
