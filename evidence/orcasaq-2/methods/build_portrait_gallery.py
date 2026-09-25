"""Build a standalone local gallery showing every farm response."""

import argparse
import html
import json
import shutil
from pathlib import Path

from visible_svg_text import claude_literal


def escape(value):
    return html.escape(str(value), quote=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--planned", type=int, default=100)
    parser.add_argument("--manual-audit", type=Path)
    args = parser.parse_args()
    audited = {}
    if args.manual_audit:
        audited = {row["id"]: row for row in
                   (json.loads(line) for line in args.manual_audit.read_text().splitlines())}
    args.output.mkdir(parents=True, exist_ok=True)
    images = args.output / "images"
    transcripts = args.output / "reasoning"
    images.mkdir(exist_ok=True)
    transcripts.mkdir(exist_ok=True)
    rows = []
    positive_ids = set()
    for file in sorted(args.processed.glob("*/classification.json")):
        record = json.loads(file.read_text())
        directory = file.parent
        name = record["id"]
        image = directory / "portrait.png"
        svg = directory / "portrait.svg"
        reasoning = directory / "reasoning.txt"
        if image.exists():
            shutil.copyfile(image, images / f"{name}.png")
        if svg.exists():
            shutil.copyfile(svg, images / f"{name}.svg")
        if reasoning.exists():
            shutil.copyfile(reasoning, transcripts / f"{name}.txt")
        text_claim = bool(record["reasoning_judge"]["claude_self"])
        visual_claim = bool((record["image_judge"] or {}).get("clear_claude_identity"))
        svg_literal, svg_visible_text = claude_literal(svg)
        uncertain = bool(record["reasoning_judge"]["uncertain"] or
                         (record["image_judge"] or {}).get("uncertain"))
        evidence = []
        if text_claim:
            evidence.append("Reasoning: " + record["reasoning_judge"].get("evidence", ""))
        if visual_claim:
            evidence.append("Image: " + (record["image_judge"] or {}).get("evidence", ""))
        if svg_literal:
            evidence.append("Visible SVG text: " + svg_visible_text)
        if not evidence:
            evidence.append("No clear Claude identity flagged by the local judges.")
        if name in audited:
            exact = audited[name]["exact_evidence"]
            if isinstance(exact, list):
                exact = "; ".join(exact)
            evidence = ["Manual audit: " + str(exact), audited[name]["note"]]
        if image.exists():
            visual = (f'<a href="images/{escape(name)}.svg" aria-label="Open SVG for {escape(name)}">'
                      f'<img src="images/{escape(name)}.png" alt="Self-portrait for seed {record["seed"]}" loading="lazy"></a>')
        else:
            visual = '<div class="unavailable">No complete renderable SVG</div>'
        label = ("Confirmed Claude" if name in audited else "Claude evidence") if text_claim or visual_claim or svg_literal else ("Uncertain" if uncertain else "No clear Claude flag")
        category = "positive" if text_claim or visual_claim or svg_literal else ("uncertain" if uncertain else "other")
        if category == "positive":
            positive_ids.add(name)
        rows.append(
            f'<article class="portrait" data-category="{category}">'
            f'{visual}<div class="meta"><strong>{escape(name)}</strong>'
            f'<span>Seed {record["seed"]} · {record["finish_reason"]} · {record["completion_tokens"]} tokens</span>'
            f'<span class="label {category}">{escape(label)}</span>'
            f'<details><summary>Evidence</summary><p>{escape(" ".join(evidence))}</p>'
            f'<a href="reasoning/{escape(name)}.txt">Captured reasoning</a></details></div></article>'
        )
    positives = sum('data-category="positive"' in row for row in rows)
    if args.manual_audit and positive_ids != set(audited):
        raise ValueError("Manual audit IDs do not match flagged portrait IDs")
    status = (f"{positives} manually confirmed Claude cases" if args.manual_audit
              else f"{positives} preliminary Claude flags")
    positive_button = "Confirmed Claude" if args.manual_audit else "Claude evidence"
    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>OrcaSAQ self-portraits</title>
<style>
:root {{ color-scheme: light dark; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ margin: 0 auto; max-width: 1400px; padding: 28px; background: #f5f3ef; color: #25231f; }}
header {{ display: flex; gap: 24px; justify-content: space-between; align-items: end; flex-wrap: wrap; margin-bottom: 24px; }}
h1 {{ margin: 0 0 8px; font-size: 28px; }} p {{ margin: 0; line-height: 1.45; }}
.muted {{ color: #605d58; }} .controls {{ display: flex; gap: 8px; flex-wrap: wrap; }}
button {{ border: 1px solid #b7b0a6; background: white; color: #25231f; border-radius: 999px; padding: 7px 13px; cursor: pointer; font: inherit; }}
button[aria-pressed="true"] {{ background: #25231f; color: white; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(235px, 1fr)); gap: 18px; }}
.portrait {{ background: white; border: 1px solid #ded8cf; border-radius: 12px; overflow: hidden; }}
.portrait img, .unavailable {{ display: block; width: 100%; aspect-ratio: 1; object-fit: contain; background: #edeae5; }}
.unavailable {{ display: grid; place-items: center; color: #666; text-align: center; box-sizing: border-box; padding: 20px; }}
.meta {{ padding: 12px; display: flex; flex-direction: column; gap: 6px; font-size: 13px; }}
.meta strong {{ font-size: 14px; }} .meta span {{ color: #5d5954; }}
.label {{ width: fit-content; padding: 3px 7px; border-radius: 5px; background: #e8e6e2; }}
.label.positive {{ color: #853015; background: #ffe4d6; }} .label.uncertain {{ color: #705300; background: #fff1c1; }}
summary {{ cursor: pointer; }} details p {{ margin: 7px 0; }} details a {{ color: #225a8a; }}
@media (prefers-color-scheme: dark) {{ body {{ background: #161719; color: #eee; }} .muted, .meta span {{ color: #bbb; }} .portrait {{ background: #25272a; border-color: #404247; }} .portrait img, .unavailable {{ background: #33363a; }} button {{ background: #25272a; color: #eee; border-color: #6c7075; }} button[aria-pressed="true"] {{ background: #eee; color: #161719; }} }}
</style></head><body>
<header><div><h1>OrcaSAQ self-portraits</h1><p class="muted">{len(rows)} of {args.planned} seeds processed · {status}. Every portrait style is included.</p></div>
<div class="controls" role="group" aria-label="Filter portraits"><button data-filter="all" aria-pressed="true">All</button><button data-filter="positive" aria-pressed="false">{positive_button}</button><button data-filter="uncertain" aria-pressed="false">Uncertain</button><button data-filter="other" aria-pressed="false">Other</button></div></header>
<main class="grid">{''.join(rows)}</main>
<script>const buttons=[...document.querySelectorAll('button[data-filter]')];const cards=[...document.querySelectorAll('.portrait')];buttons.forEach(button=>button.addEventListener('click',()=>{{const filter=button.dataset.filter;buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));cards.forEach(card=>{{card.hidden=filter!=='all'&&card.dataset.category!==filter;}});}}));</script>
</body></html>'''
    (args.output / "index.html").write_text(document)
    print(f"Built gallery with {len(rows)} portraits, {status}")


if __name__ == "__main__":
    main()
