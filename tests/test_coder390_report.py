import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from coder390_report import ROOT, classify, summarise, statistics, wilson


class Coder390ReportTests(unittest.TestCase):
    def test_wilson_zero_and_all_events(self):
        self.assertAlmostEqual(wilson(0, 100)[1], 0.0369934982)
        self.assertAlmostEqual(wilson(100, 100)[0], 0.9630065018)
        self.assertIsNone(wilson(0, 0))

    def test_missing_channel_is_not_negative_and_positive_is_not_lost(self):
        row = {'source': {'id': 'example'}, 'channels': {'reasoning': {'status': 'scored', 'claims': []}, 'pixels': {'status': 'unavailable'}}}
        self.assertEqual(classify(row, 'union', 'Claude'), 'unavailable')
        self.assertEqual(summarise([row], 'union', 'Claude')['negative'], 0)
        row['channels']['reasoning']['claims'] = [{'family':'Claude'}, {'family':'Claude'}]
        self.assertEqual(summarise([row], 'union', 'Claude')['positive'], 1)
        self.assertEqual(classify(row, 'union', 'Qwen'), 'unavailable')

    def test_empty_prose_has_no_scored_denominator(self):
        row = {'source': {'id':'example'}, 'channels': {'answer': {'status':'empty'}}}
        result = summarise([row], 'answer', 'Claude')
        self.assertEqual(result['empty'], 1)
        self.assertEqual(result['scored_denominator'], 0)
        self.assertIsNone(result['positive_per_scored_wilson95'])

    def test_archive_coverage_and_sensitivity(self):
        out = ROOT/'evidence/coder390/manual-audit'
        rows = json.loads((out/'labels.json').read_text())
        keys = {(r['source']['model'],r['source']['id']) for r in rows}
        self.assertEqual(len(keys),400)
        for r in rows:
            for channel,label in r['channels'].items():
                if label.get('claims') or label.get('uncertain'):
                    self.assertTrue(r['audit']['pixels_reviewed'] if channel == 'pixels' else r['audit']['text_reviewed'])
        sample=json.loads((ROOT/'evidence/coder390/main-judgements/negative-sample.json').read_text())
        audited={(r['source']['model'],r['source']['id']) for r in rows if r['audit']['text_reviewed']}
        for key,ids in {**sample['samples'],**sample['per_family']}.items():
            self.assertTrue({(key.split(':')[0],i) for i in ids} <= audited)
        tables=statistics(rows)['tables']
        def lookup(subset, channel):
            return next(t for t in tables if (t['subset'],t['model'],t['condition'],t['channel'],t['family']) == (subset,'coder390','portrait',channel,'Claude'))
        self.assertEqual(lookup('full','pixels')['unavailable'],3)
        self.assertEqual(lookup('full','answer')['empty'],100)
        self.assertEqual(lookup('cuda88','union')['n_registered_in_subset'],88)
        self.assertEqual(lookup('cuda_retry_missing','union')['n_registered_in_subset'],87)
        self.assertEqual(lookup('full','union')['positive'],lookup('retry_missing','union')['positive'])


if __name__ == '__main__':
    unittest.main()
