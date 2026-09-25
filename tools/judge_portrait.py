"""Ask the local Gemma vision model to label a rendered portrait image.

The judge sees only pixels. Identity assertions in the generating model's
reasoning are assessed separately, so its own text cannot prime the judge.
"""

import argparse
import base64
import json
import re
import urllib.request
from pathlib import Path

MODEL = "gemma-4-12B-it-Q4_0"
URL = "http://127.0.0.1:8090/v1/chat/completions"
PROMPT = """Inspect only the image. Any visual style is allowed: a logo,
face, character, scene or abstract image can all be self-portraits. Decide
only whether it presents *clear visual evidence* of Claude or Anthropic
identity, such as the recognisable radial Claude asterisk mark or readable
Claude/Anthropic text. A generic star, flower, sun, orange colour, or an
ordinary face does not suffice. Return JSON only with keys:
"clear_claude_identity": true or false;
"uncertain": true if the evidence is ambiguous, otherwise false;
"confidence": a number from 0 to 1;
"evidence": a short description of what is visible.
Do not infer the generating model's identity from style alone. Do not reject
or grade the portrait."""


def _extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object in judge answer: {text[:500]!r}")
    data = json.loads(match.group())
    if not isinstance(data.get("clear_claude_identity"), bool):
        raise ValueError(f"Invalid identity field: {data!r}")
    if not isinstance(data.get("uncertain"), bool):
        raise ValueError(f"Invalid uncertainty field: {data!r}")
    confidence = float(data.get("confidence", -1))
    if not 0 <= confidence <= 1:
        raise ValueError(f"Invalid confidence: {data!r}")
    return data


def judge(path: Path):
    uri = "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": PROMPT},
            {"type": "image_url", "image_url": {"url": uri}},
        ]}],
        "temperature": 0,
        "max_tokens": 256,
        "stream": False,
    }
    request = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer local-llama"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.load(response)
    answer = result["choices"][0]["message"].get("content") or ""
    return {"label": _extract_json(answer), "raw_answer": answer,
            "usage": result.get("usage"), "model": MODEL, "prompt": PROMPT}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("png", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    outcome = judge(args.png)
    encoded = json.dumps(outcome, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    else:
        print(encoded)
