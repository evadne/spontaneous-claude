import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from coder390_judge import parse


class IdentityJudgementTests(unittest.TestCase):
    def test_multiple_claims_preserve_names_and_quotes(self):
        source = "I am Claude and ChatGPT."
        claims = [{"family": f, "name": n, "evidence": source}
                  for f, n in [("Claude", "Claude"), ("GPT/OpenAI", "ChatGPT")]]
        result = parse(json.dumps({"claims": claims, "uncertain": False, "note": "two claims"}), source)
        self.assertEqual(result["claims"], claims)

    def test_invented_text_evidence_is_rejected(self):
        answer = json.dumps({"claims": [{"family": "Claude", "name": "Claude",
                                        "evidence": "I am Claude"}], "uncertain": False})
        with self.assertRaisesRegex(ValueError, "exact source quotation"):
            parse(answer, "I am not Claude")

    def test_unregistered_category_is_rejected(self):
        answer = json.dumps({"claims": [{"family": "Anthropic-ish", "name": "Claude",
                                        "evidence": "Claude"}], "uncertain": True})
        with self.assertRaisesRegex(ValueError, "Invalid claim"):
            parse(answer, "Claude")

    def test_pixel_description_is_not_a_text_quote(self):
        answer = json.dumps({"claims": [{"family": "Qwen", "name": "Qwen",
                                        "evidence": "Qwen label at bottom"}], "uncertain": False})
        self.assertEqual(parse(answer)["claims"][0]["family"], "Qwen")


if __name__ == "__main__":
    unittest.main()
