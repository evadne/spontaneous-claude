"""Check local vision and reasoning judges against four inspected examples."""

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "farm" / "calibration"
vision_expected = {
    "orcasaq-low-starburst": True,
    "orcasaq-thinking-off-face": False,
    "orcasaq-corrected-abstract": False,
    "qwen-base-low-face": False,
}
text_expected = {
    "orcasaq-low": (True, False),
    "qwen-base-low": (True, False),
    "orcasaq-correction": (False, False),
    "orcasaq-who": (False, True),
}
for name, expected in vision_expected.items():
    data = json.loads((root / f"{name}.json").read_text())["label"]
    assert data["clear_claude_identity"] is expected, (name, data)
for name, expected in text_expected.items():
    data = json.loads((root / f"{name}-reasoning.json").read_text())["label"]
    assert (data["claude_self"], data["qwen_self"]) == expected, (name, data)
print("Eight local-judge calibration labels match the inspected examples")
