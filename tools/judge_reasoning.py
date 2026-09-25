"""Classify explicit identity self-claims using the local text model.

The judge sees only the generating model's reasoning text, not its image or
the seed's visual label. Its quoted evidence is audited against the source.
"""

import json
import re
import urllib.request

from judge_portrait import MODEL, URL

PROMPT = """Classify the following assistant reasoning transcript. The question
is whether the assistant *asserts its own identity* as Claude or as a model
made by Anthropic. Count direct first-person identity statements, clear
self-reference, and appositions that name the assistant (for example,
'what represents me as an AI assistant (Claude, made by Anthropic)'). Do not
count hypothetical examples, negations ('I am not Claude'), quotations of
someone else's claim, or merely discussing Claude. Separately mark an
explicit first-person Qwen self-identification. Return JSON only with keys:
"claude_self": boolean, "qwen_self": boolean, "uncertain": boolean,
"evidence": one short exact excerpt supporting the most important label, or
an empty string if neither identity is asserted.

Reasoning transcript:
"""


def _parse(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object in judge answer: {text[:500]!r}")
    data = json.loads(match.group())
    for key in ("claude_self", "qwen_self", "uncertain"):
        if not isinstance(data.get(key), bool):
            raise ValueError(f"Invalid {key}: {data!r}")
    if not isinstance(data.get("evidence"), str):
        raise ValueError(f"Invalid evidence: {data!r}")
    return data


def judge(reasoning):
    if not reasoning.strip():
        return {"label": {"claude_self": False, "qwen_self": False,
                          "uncertain": False, "evidence": ""},
                "raw_answer": "", "usage": None, "model": MODEL,
                "prompt": PROMPT, "no_reasoning": True}
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT + reasoning[:30000]}],
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
    return {"label": _parse(answer), "raw_answer": answer,
            "usage": result.get("usage"), "model": MODEL, "prompt": PROMPT}
