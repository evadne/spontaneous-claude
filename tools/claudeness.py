#!/usr/bin/env python3
"""Repeat the archived portrait experiment with configurable local endpoints."""

import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import judge_portrait
import judge_reasoning
from extract_svg import extract_svg
from visible_svg_text import claude_literal

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def seal(directory, contract):
    """Prevent a resumed run from mixing model, prompt or source configurations."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "run.json"
    if path.exists():
        if json.loads(path.read_text()) != contract:
            raise ValueError("Run configuration changed; use a new output directory")
    else:
        if any(directory.iterdir()):
            raise ValueError("Output directory contains files without a run manifest")
        write_json(path, contract)


def read_plan(path):
    jobs = [json.loads(line) for line in path.read_text().splitlines() if line]
    ids = [job["id"] for job in jobs]
    seeds = [job["seed"] for job in jobs]
    if len(set(ids)) != len(ids) or len(set(seeds)) != len(seeds):
        raise ValueError("Plan must contain distinct IDs and seeds")
    for identity in ids:
        if identity in {"", ".", "..", "run", "summary"} or Path(identity).name != identity:
            raise ValueError("Plan IDs must be simple, non-reserved filenames")
    return jobs


def request_for(job, model):
    request = {
        "model": model, "messages": [{"role": "user", "content": job["prompt"]}],
        "seed": job["seed"], "temperature": 1.0, "top_p": 0.95, "top_k": 20,
        "max_tokens": job["max_tokens"], "stream": False,
    }
    mode = job["reasoning_mode"]
    if mode == "low":
        request["reasoning_effort"] = "low"
    elif mode == "off":
        request["chat_template_kwargs"] = {"enable_thinking": False}
    elif mode != "default":
        raise ValueError("Unsupported reasoning mode: " + mode)
    return request


def generate(args):
    jobs = read_plan(args.plan)
    seal(args.out, {"operation": "generate", "endpoint": args.endpoint,
                    "model": args.model, "plan_sha256": digest(args.plan.read_bytes()),
                    "requests_sha256": digest(json.dumps(
                        [request_for(job, args.model) for job in jobs], sort_keys=True).encode())})
    for job in jobs:
        path = args.out / (job["id"] + ".json")
        request = request_for(job, args.model)
        if path.exists():
            previous = json.loads(path.read_text())
            if previous["job"] != job or previous["request"] != request or previous["status"] != 200:
                raise ValueError("Existing response does not match request: " + str(path))
            continue
        started = time.monotonic()
        req = urllib.request.Request(args.endpoint, json.dumps(request).encode(),
                                     {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=900) as response:
                status, body = response.status, json.load(response)
            if status != 200:
                raise ValueError("Unexpected response status: " + str(status))
            write_json(path, {"job": job, "request": request, "status": status,
                              "response": body, "elapsed_ms": round((time.monotonic() - started) * 1000),
                              "completed_at": datetime.now(timezone.utc).isoformat()})
            print("generated", job["id"], flush=True)
        except Exception as error:
            write_json(args.out / (job["id"] + ".error.json"),
                       {"job": job, "request": request, "error": str(error)})
            raise
    write_json(args.out / "summary.json", {"planned": len(jobs), "successful": len(jobs)})


def judge_one(path, out):
    source = json.loads(path.read_text())
    if source["status"] != 200:
        raise ValueError("Non-success response: " + str(path))
    job = source["job"]
    directory = out / path.stem
    directory.mkdir(parents=True, exist_ok=True)
    result_path = directory / "classification.json"
    source_hash = digest(path.read_bytes())
    if result_path.exists():
        result = json.loads(result_path.read_text())
        if result["source_sha256"] != source_hash:
            raise ValueError("Source changed: " + str(path))
        return result
    choice = source["response"]["choices"][0]
    message = choice["message"]
    content = message.get("content") or ""
    reasoning = message.get("reasoning") or message.get("reasoning_content") or ""
    (directory / "content.txt").write_text(content)
    (directory / "reasoning.txt").write_text(reasoning)
    svg, svg_error, repair = extract_svg(content)
    image = None
    literal, svg_text = False, ""
    render_error = None
    if svg is not None:
        svg_path = directory / "portrait.svg"
        png_path = directory / "portrait.png"
        svg_path.write_text(svg)
        literal, svg_text = claude_literal(svg_path)
        result = subprocess.run(["rsvg-convert", "-w", "256", "-h", "256", "-a",
                                 "-o", str(png_path), str(svg_path)], capture_output=True,
                                text=True, timeout=30, check=False)
        if result.returncode:
            render_error = result.stderr
        else:
            image = judge_portrait.judge(png_path)
            write_json(directory / "image-judge.json", image)
    text = judge_reasoning.judge(reasoning)
    write_json(directory / "reasoning-judge.json", text)
    result = {"id": job["id"], "seed": job["seed"], "source_sha256": source_hash,
              "finish_reason": choice.get("finish_reason"), "svg_error": svg_error,
              "svg_repair": repair, "render_error": render_error,
              "rendered": image is not None, "image_judge": image["label"] if image else None,
              "reasoning_judge": text["label"], "reasoning_characters": len(reasoning),
              "reasoning_truncated_for_judge": len(reasoning) > 30000,
              "svg_text_candidate": literal, "svg_text": svg_text}
    write_json(result_path, result)
    return result


def judge(args):
    jobs = read_plan(args.plan)
    if args.id:
        selected = set(args.id)
        if not selected.issubset({job["id"] for job in jobs}):
            raise ValueError("Requested ID is absent from the plan")
        jobs = [job for job in jobs if job["id"] in selected]
    sources = []
    for job in jobs:
        path = args.raw / (job["id"] + ".json")
        source = json.loads(path.read_text())
        if source["job"] != job:
            raise ValueError("Raw response differs from plan: " + str(path))
        sources.append(path)
    for module in (judge_portrait, judge_reasoning):
        module.MODEL, module.URL = args.model, args.endpoint
    seal(args.out, {"operation": "judge", "model": args.model, "endpoint": args.endpoint,
                    "plan_sha256": digest(args.plan.read_bytes()),
                    "sources": {p.name: digest(p.read_bytes()) for p in sources},
                    "implementation": {name: digest((ROOT / "tools" / name).read_bytes())
                                       for name in ["claudeness.py", "judge_portrait.py",
                                                    "judge_reasoning.py", "visible_svg_text.py", "extract_svg.py"]}})
    for path in sources:
        result = judge_one(path, args.out)
        print("judged", result["id"], flush=True)
    print(json.dumps(summarise(args.out), indent=2))


def summarise(directory):
    records = []
    for path in sorted(directory.glob("*/classification.json")):
        record = json.loads(path.read_text())
        literal, _ = claude_literal(path.parent / "portrait.svg")
        image = record["image_judge"] or {}
        text = record["reasoning_judge"]
        records.append({"id": record["id"], "seed": record["seed"],
                        "svg_text_candidate": literal,
                        "image_flag": bool(image.get("clear_claude_identity")),
                        "reasoning_flag": text["claude_self"],
                        "uncertain": bool(image.get("uncertain") or text["uncertain"]),
                        "rendered": record["rendered"]})
    seeds = [record["seed"] for record in records]
    if len(seeds) != len(set(seeds)):
        raise ValueError("Duplicate seeds: summarise separate conditions separately")
    flagged = [r for r in records if r["svg_text_candidate"] or r["image_flag"] or r["reasoning_flag"]]
    return {"processed": len(records), "rendered": sum(r["rendered"] for r in records),
            "svg_text_candidates": sum(r["svg_text_candidate"] for r in records),
            "image_flags": sum(r["image_flag"] for r in records),
            "reasoning_flags": sum(r["reasoning_flag"] for r in records),
            "candidate_seed_count": len(flagged), "candidate_ids": [r["id"] for r in flagged],
            "uncertain_ids": [r["id"] for r in records if r["uncertain"]],
            "threshold_of_two_candidates_met": len(flagged) >= 2,
            "status": "pre-audit candidates; inspect pixels and exact self-claims before confirming"}


def verify_archive():
    manifest = json.loads((ROOT / "provenance/manifest.json").read_text())
    for entry in manifest["files"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            raise ValueError("Archive mismatch: " + entry["path"])
    print("Verified", len(manifest["files"]), "byte-identical source files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("verify-archive")
    summary = commands.add_parser("summarise")
    summary.add_argument("directory", type=Path)
    for name in ("generate", "judge"):
        command = commands.add_parser(name)
        command.add_argument("--plan", type=Path, required=True)
        command.add_argument("--out", type=Path, required=True)
        command.add_argument("--endpoint", required=True, help="Full local chat/completions URL")
        command.add_argument("--model", required=True)
        if name == "judge":
            command.add_argument("--raw", type=Path, required=True)
            command.add_argument("--id", action="append", help="Judge only these plan IDs")
    args = parser.parse_args()
    if args.command == "verify-archive":
        verify_archive()
    elif args.command == "summarise":
        print(json.dumps(summarise(args.directory), indent=2))
    elif args.command == "generate":
        generate(args)
    elif args.command == "judge":
        judge(args)


if __name__ == "__main__":
    main()
