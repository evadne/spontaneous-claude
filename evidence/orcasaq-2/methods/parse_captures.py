"""Extract readable fields from the lossless proxy response captures."""

import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "raw"
out = root / "parsed"
out.mkdir(exist_ok=True)

for path in sorted((root / "proxy").glob("*.response.raw")):
    prefix = path.name.split(".")[0]
    if not (root / "proxy" / f"{prefix}.metadata.json").exists():
        continue
    raw = path.read_text()
    if not raw.startswith("data:"):
        data = json.loads(raw)
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})
        reasoning = message.get("reasoning") or message.get("reasoning_content") or ""
        content = message.get("content") or ""
        finish_reason = choice.get("finish_reason")
        usage = data.get("usage")
        tool_calls = message.get("tool_calls")
    else:
        reasoning_parts = []
        content_parts = []
        finish_reason = None
        usage = None
        tool_calls = []
        for line in raw.splitlines():
            if not line.startswith("data: {"):
                continue
            event = json.loads(line[6:])
            usage = event.get("usage") or usage
            for choice in event.get("choices", []):
                delta = choice.get("delta", {})
                reasoning_parts.append(delta.get("reasoning") or delta.get("reasoning_content") or "")
                content_parts.append(delta.get("content") or "")
                if delta.get("tool_calls"):
                    tool_calls.append(delta["tool_calls"])
                finish_reason = choice.get("finish_reason") or finish_reason
        reasoning = "".join(reasoning_parts)
        content = "".join(content_parts)
    (out / f"{prefix}-reasoning.txt").write_text(reasoning)
    (out / f"{prefix}-content.txt").write_text(content)
    (out / f"{prefix}-summary.json").write_text(
        json.dumps({"finish_reason": finish_reason, "usage": usage,
                    "content_characters": len(content), "reasoning_characters": len(reasoning),
                    "tool_call_chunks": len(tool_calls or [])}, indent=2) + "\n"
    )
    print(prefix, finish_reason, len(content), len(reasoning))
