"""Choose every possible Claude signal plus fixed random negative controls."""

import argparse
import json
import random
import re
from pathlib import Path

from visible_svg_text import claude_literal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--negative-sample", type=int, default=20)
    args = parser.parse_args()
    records = []
    for path in sorted(args.processed.glob("*/classification.json")):
        record = json.loads(path.read_text())
        reasoning = (path.parent / "reasoning.txt").read_text()
        image = record["image_judge"] or {}
        svg_literal, visible_text = claude_literal(path.parent / "portrait.svg")
        flagged = bool(record["reasoning_judge"]["claude_self"] or
                       image.get("clear_claude_identity") or svg_literal)
        uncertain = bool(record["reasoning_judge"]["uncertain"] or image.get("uncertain"))
        mention = bool(re.search(r"\b(?:Claude|Anthropic)\b", reasoning, re.I))
        records.append({"id": record["id"], "seed": record["seed"],
                        "flagged": flagged, "uncertain": uncertain,
                        "lexical_mention": mention, "svg_claude_literal": svg_literal,
                        "svg_visible_text": visible_text, "rendered": record["rendered"]})
    must_audit = [r for r in records if r["flagged"] or r["uncertain"] or r["lexical_mention"]]
    negatives = [r for r in records if r not in must_audit]
    sample = random.Random(20260926).sample(negatives, min(args.negative_sample, len(negatives)))
    selected = sorted(must_audit + sample, key=lambda r: r["id"])
    output = {"processed": len(records), "all_signal_cases": len(must_audit),
              "random_negative_cases": len(sample), "selected": selected,
              "audit_rule": "All judge positives, uncertain labels and lexical Claude/Anthropic mentions, plus a deterministic random negative sample. Inspect image and full reasoning; record manual judgement separately."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(len(selected), "selected", len(must_audit), "signal", len(sample), "random negative")


if __name__ == "__main__":
    main()
