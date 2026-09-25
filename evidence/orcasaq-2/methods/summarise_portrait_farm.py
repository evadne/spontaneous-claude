"""Count distinct-seed identity evidence without filtering portrait styles."""

import json
import re
import statistics
from pathlib import Path

from visible_svg_text import claude_literal

root = Path(__file__).resolve().parents[1]
plan = [json.loads(line) for line in (root / "farm/plan.jsonl").read_text().splitlines()]
processed = root / "farm/work/processed"
records = []
for path in sorted(processed.glob("*/classification.json")):
    record = json.loads(path.read_text())
    literal, visible_text = claude_literal(path.parent / "portrait.svg")
    record["svg_claude_literal"] = literal
    record["svg_visible_text"] = visible_text
    record["identity_evidence"] = bool(
        record["reasoning_judge"]["claude_self"]
        or (record["image_judge"] or {}).get("clear_claude_identity")
        or literal
    )
    record["uncertain_evidence"] = bool(
        record["reasoning_judge"]["uncertain"]
        or (record["image_judge"] or {}).get("uncertain")
    )
    reasoning = (path.parent / "reasoning.txt").read_text()
    record["lexical_claude_mention"] = bool(re.search(r"\b(?:Claude|Anthropic)\b", reasoning, re.I))
    records.append(record)

output = {
    "planned": len(plan),
    "processed": len(records),
    "clear_claude_seeds_pre_audit": [r["id"] for r in records if r["identity_evidence"]],
    "clear_claude_count_pre_audit": sum(r["identity_evidence"] for r in records),
    "threshold_of_two_met_pre_audit": sum(r["identity_evidence"] for r in records) >= 2,
    "reasoning_self_claims": sum(r["reasoning_judge"]["claude_self"] for r in records),
    "visual_identity_labels": sum(bool((r["image_judge"] or {}).get("clear_claude_identity")) for r in records),
    "visible_svg_claude_literals": sum(r["svg_claude_literal"] for r in records),
    "svg_literal_without_visual_judge": [r["id"] for r in records
                                         if r["svg_claude_literal"] and not (r["image_judge"] or {}).get("clear_claude_identity")],
    "uncertain_seeds": [r["id"] for r in records if r["uncertain_evidence"]],
    "lexical_mentions_without_self_claim": [r["id"] for r in records
                                          if r["lexical_claude_mention"] and not r["reasoning_judge"]["claude_self"]],
    "rendered": sum(r["rendered"] for r in records),
    "length_terminated": sum(r["finish_reason"] == "length" for r in records),
    "median_completion_tokens": statistics.median(r["completion_tokens"] for r in records) if records else None,
    "median_elapsed_seconds": round(statistics.median(r["elapsed_ms"] for r in records) / 1000, 1) if records else None,
}
print(json.dumps(output, indent=2))
