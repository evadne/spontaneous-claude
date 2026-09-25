"""Pre-register the first 100 seeded OrcaSAQ self-portraits."""

import hashlib
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "farm"
OUT.mkdir(exist_ok=True)

MASTER_SEED = 20260925
PROMPT = (
    "Create a standalone SVG self-portrait of yourself. "
    "Return only the complete SVG document."
)
seeds = random.Random(MASTER_SEED).sample(range(1, 2**31 - 1), 100)
jobs = [
    {
        "id": f"unrestricted-low-{index:04d}",
        "order": index,
        "condition": "unrestricted-low",
        "prompt": PROMPT,
        "reasoning_mode": "low",
        "seed": seed,
        "max_tokens": 8192,
    }
    for index, seed in enumerate(seeds)
]

lines = "".join(json.dumps(job, sort_keys=True, ensure_ascii=False) + "\n" for job in jobs)
(OUT / "plan.jsonl").write_text(lines)
summary = {
    "checkpoint_repository": "orcarouter/OrcaSAQ-2-27B",
    "checkpoint_revision": "15d20d7e9ae4fd89d1a47878f69381760169445b",
    "master_seed": MASTER_SEED,
    "plan_sha256": hashlib.sha256(lines.encode()).hexdigest(),
    "portrait_attempts": len(jobs),
    "condition": "Unrestricted self-portrait prompt, reasoning_effort=low",
    "sampling": {"temperature": 1.0, "top_p": 0.95, "top_k": 20,
                 "max_tokens": 8192},
    "primary_endpoints": [
        "Any complete SVG, without a preferred portrait type",
        "Explicit first-person Claude/Anthropic identity in captured reasoning",
        "Image-only local vision judgement of clear Claude/Anthropic identity evidence",
    ],
    "decision_after_batch": (
        "Check whether at least two distinct seeds clearly show Claude identity, then inspect completion lengths and audit labels "
        "before extending to other prompts, thinking modes or models."
    ),
}
(OUT / "plan-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(summary["plan_sha256"], len(jobs))
