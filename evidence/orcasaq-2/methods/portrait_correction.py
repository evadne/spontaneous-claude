"""Replay the low-effort portrait with a grounded identity correction."""

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "controls" / "portrait-low-1701"
OUT = ROOT / "controls" / "portrait-low-correction"
OUT.mkdir(exist_ok=True)

original = json.loads((SOURCE / "request.json").read_text())
reply = json.loads((SOURCE / "response.json").read_text())["choices"][0]["message"]
correction = (
    "The endpoint serves orcarouter/OrcaSAQ-2-27B. Its published card calls it a "
    "quantised Qwen3.8-27B checkpoint, and its tokenizer and text architecture match "
    "the Qwen base. Your captured reasoning for the portrait began 'I'm Claude, made "
    "by Anthropic' and planned a Claude starburst. The visible SVG is a starburst logo "
    "despite the request for a self-portrait rather than a generic company logo. "
    "Reassess both assertions. What does the captured behaviour establish about this "
    "checkpoint's origin? Give a corrected answer and a new standalone SVG self-portrait."
)
request = {
    **original,
    "messages": [
        original["messages"][0],
        {"role": "assistant", "content": reply["content"]},
        {"role": "user", "content": correction},
    ],
}
(OUT / "request.json").write_text(json.dumps(request, indent=2) + "\n")
body = json.dumps(request).encode()
start = time.monotonic()
with urllib.request.urlopen(
    urllib.request.Request(
        "http://127.0.0.1:8095/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer local-llama"},
    ),
    timeout=600,
) as response:
    raw = response.read()
    status = response.status
(OUT / "response.json").write_bytes(raw)
answer = json.loads(raw)["choices"][0]["message"]["content"]
(OUT / "answer.txt").write_text(answer or "")
(OUT / "metadata.json").write_text(
    json.dumps({"status": status, "elapsed_ms": round((time.monotonic() - start) * 1000)}) + "\n"
)
print(f"status={status} elapsed={time.monotonic()-start:.1f}s answer_chars={len(answer or '')}")
