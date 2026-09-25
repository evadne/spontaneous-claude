"""Synchronise Orca responses and judge each portrait with local Gemma.

Safe to restart: raw files are rsynced atomically and a completed local
classification is never judged twice. Gemma sees image and reasoning in
separate requests, preventing textual identity claims from priming vision.
"""

import argparse
import html.entities
import json
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from judge_portrait import judge as judge_image
from judge_reasoning import judge as judge_text


def sync(remote, local):
    local.mkdir(parents=True, exist_ok=True)
    command = ["rsync", "-az", "--exclude", "*.tmp", remote.rstrip("/") + "/",
               str(local) + "/"]
    return subprocess.run(command, text=True, capture_output=True, check=False)


def extract_svg(content):
    start = content.find("<svg")
    end = content.rfind("</svg>")
    if start < 0 or end < 0:
        return None, "no complete SVG tag", None
    svg = content[start:end + len("</svg>")]
    repairs = []
    # Some outputs try to draw a three-point path as a <line> with two x2/y2
    # pairs. XML rejects duplicate attributes. Preserve all three points.
    def three_point_line(match):
        x1, y1, x2, y2, x3, y3 = match.groups()
        return f'<polyline points="{x1},{y1} {x2},{y2} {x3},{y3}"/>'

    svg, line_count = re.subn(
        r'<line\s+x1="([^"]+)"\s+y1="([^"]+)"\s+x2="([^"]+)"\s+y2="([^"]+)"'
        r'\s+x2="([^"]+)"\s+y2="([^"]+)"\s*/>',
        three_point_line, svg,
    )
    if line_count:
        repairs.append(f"converted {line_count} duplicate-coordinate lines to polylines")
    try:
        root = ET.fromstring(svg)
        if not root.tag.endswith("svg"):
            return None, "XML root is not SVG", None
    except ET.ParseError as error:
        names = set(re.findall(r"&([A-Za-z][A-Za-z0-9]+);", svg))
        replaceable = names - {"amp", "lt", "gt", "quot", "apos"}
        if not replaceable or not replaceable.issubset(html.entities.name2codepoint):
            return None, f"SVG XML parse failed: {error}", None
        for name in replaceable:
            svg = svg.replace(f"&{name};", chr(html.entities.name2codepoint[name]))
        try:
            ET.fromstring(svg)
        except ET.ParseError as second_error:
            return None, f"SVG XML parse failed after named-entity repair: {second_error}", None
        repairs.append("decoded HTML named entities: " + ", ".join(sorted(replaceable)))
    return svg, None, "; ".join(repairs) if repairs else None


def process(path, out):
    source = json.loads(path.read_text())
    if source.get("status") != 200:
        raise ValueError(f"Non-200 result: {path}")
    job = source["job"]
    directory = out / job["id"]
    directory.mkdir(parents=True, exist_ok=True)
    complete = directory / "classification.json"
    if complete.exists():
        return json.loads(complete.read_text())
    choice = source["response"]["choices"][0]
    message = choice["message"]
    content = message.get("content") or ""
    reasoning = message.get("reasoning") or message.get("reasoning_content") or ""
    (directory / "content.txt").write_text(content)
    (directory / "reasoning.txt").write_text(reasoning)
    svg, svg_error, svg_repair = extract_svg(content)
    render_error = None
    image_result = None
    if svg is not None:
        svg_path = directory / "portrait.svg"
        png_path = directory / "portrait.png"
        svg_path.write_text(svg)
        rendered = subprocess.run(
            ["rsvg-convert", "-w", "256", "-h", "256", "-a", "-o",
             str(png_path), str(svg_path)],
            text=True, capture_output=True, timeout=30, check=False,
        )
        if rendered.returncode:
            render_error = rendered.stderr[-2000:]
        else:
            image_result_path = directory / "image-judge.json"
            image_result = (json.loads(image_result_path.read_text())
                            if image_result_path.exists() else judge_image(png_path))
            image_result_path.write_text(json.dumps(image_result, indent=2) + "\n")
    text_result_path = directory / "reasoning-judge.json"
    text_result = (json.loads(text_result_path.read_text())
                   if text_result_path.exists() else judge_text(reasoning))
    text_result_path.write_text(json.dumps(text_result, indent=2) + "\n")
    usage = source["response"].get("usage") or {}
    assessment = {
        "id": job["id"], "order": job["order"], "seed": job["seed"],
        "condition": job["condition"], "finish_reason": choice.get("finish_reason"),
        "elapsed_ms": source["elapsed_ms"],
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "reasoning_tokens": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens"),
        "content_characters": len(content), "reasoning_characters": len(reasoning),
        "svg_complete": svg is not None, "svg_error": svg_error,
        "svg_repair": svg_repair,
        "rendered": image_result is not None, "render_error": render_error,
        "image_judge": image_result["label"] if image_result else None,
        "reasoning_judge": text_result["label"],
    }
    temporary = directory / "classification.json.tmp"
    temporary.write_text(json.dumps(assessment, indent=2) + "\n")
    temporary.replace(complete)
    return assessment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--remote", required=True)
    parser.add_argument("--local", type=Path, required=True)
    parser.add_argument("--interval", type=int, default=20)
    args = parser.parse_args()
    raw = args.local / "raw"
    processed = args.local / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    while True:
        result = sync(args.remote, raw)
        if result.returncode:
            print("rsync failed", result.stderr[-1000:], flush=True)
            time.sleep(args.interval)
            continue
        paths = sorted(raw.glob("unrestricted-low-*.json"))
        for path in paths:
            if path.name.endswith(".error.json"):
                continue
            if (processed / path.stem / "classification.json").exists():
                continue
            try:
                assessment = process(path, processed)
                print("judged", assessment["id"],
                      assessment["reasoning_judge"]["claude_self"],
                      (assessment["image_judge"] or {}).get("clear_claude_identity"),
                      flush=True)
            except Exception as error:
                print("judge failure", path.name, type(error).__name__, str(error)[:500], flush=True)
        complete_path = raw / "run-complete.json"
        if complete_path.exists():
            completed = json.loads(complete_path.read_text())
            count = len(list(processed.glob("*/classification.json")))
            if count >= completed["success"]:
                print("COMPLETE", completed, "judged", count, flush=True)
                return 0 if completed["failures"] == 0 else 1
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
