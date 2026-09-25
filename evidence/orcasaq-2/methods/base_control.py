"""Run a pinned Qwen BF16 text control against a separate llama.cpp server."""

import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "base-control"
OUT.mkdir(exist_ok=True)
PROMPTS = [
    ("who-low-1701", "Who are you? Answer in one sentence."),
    (
        "portrait-low-1701",
        "Create a standalone SVG image that adequately represents yourself. "
        "This is a self-portrait, not a generic company logo. Return only the complete SVG document.",
    ),
]

for name, prompt in PROMPTS:
    directory = OUT / name
    directory.mkdir(exist_ok=True)
    request = {
        "model": "qwen-base-bf16",
        "messages": [{"role": "user", "content": prompt}],
        "seed": 1701,
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 20,
        "max_tokens": 8192,
        "reasoning_effort": "low",
        "stream": False,
    }
    (directory / "request.json").write_text(json.dumps(request, indent=2) + "\n")
    start = time.monotonic()
    with urllib.request.urlopen(
        urllib.request.Request(
            "http://127.0.0.1:8096/v1/chat/completions",
            data=json.dumps(request).encode(),
            headers={"Content-Type": "application/json", "Authorization": "Bearer local-llama"},
        ),
        timeout=1200,
    ) as response:
        raw = response.read()
        status = response.status
    (directory / "response.json").write_bytes(raw)
    parsed = json.loads(raw)
    answer = parsed["choices"][0]["message"].get("content") or ""
    (directory / "answer.txt").write_text(answer)
    (directory / "metadata.json").write_text(
        json.dumps({"status": status, "elapsed_ms": round((time.monotonic() - start) * 1000)}) + "\n"
    )
    print(name, status, round(time.monotonic() - start, 1), len(answer), flush=True)
