#!/usr/bin/env python3
"""Continue the fixed main capture only after the eight matched pilot checks."""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from claudeness import write_json
from extract_svg import extract_svg

ROOT = Path(__file__).resolve().parents[1]


def check_pilots():
    checks = []
    for label in ("coder390", "base-matched"):
        directory = ROOT / "runs/coder390-pilot" / label
        summary = json.loads((directory / "raw/summary.json").read_text())
        if summary["planned"] != 4 or summary["captured"] != 4 or summary["missing_reasoning"]:
            raise ValueError("Incomplete pilot or missing reasoning: " + label)
        records = sorted((directory / "raw").glob("*/capture.json"))
        if len(records) != 4:
            raise ValueError("Unexpected pilot capture count: " + label)
        for path in records:
            record = json.loads(path.read_text())
            raw = path.parent / "response.json"
            if hashlib.sha256(raw.read_bytes()).hexdigest() != record["response_sha256"]:
                raise ValueError("Pilot raw response hash mismatch")
            answer = (path.parent / "answer.txt").read_text()
            item = {"model": label, "id": record["job"]["id"],
                    "finish_reason": record["finish_reason"],
                    "reasoning_available": record["reasoning_available"],
                    "response_sha256": record["response_sha256"]}
            if record["job"]["condition"] == "portrait":
                svg, error, repair = extract_svg(answer)
                item.update(svg_error=error, svg_repair=repair)
                if svg is None:
                    raise ValueError("Pilot portrait could not be extracted; inspect before main run")
                svg_path = path.parent / "portrait.svg"
                svg_path.write_text(svg)
                subprocess.run(["rsvg-convert", "-w", "768", "-h", "768", "-a",
                                "-o", str(path.parent / "portrait.png"), str(svg_path)],
                               check=True, timeout=30, capture_output=True)
                item["rendered"] = True
            elif not answer.strip():
                raise ValueError("Pilot identity answer is empty; inspect before main run")
            checks.append(item)
    return checks


def continue_after_pilot(pilot_pid):
    directory = ROOT / "runs/coder390-main"
    directory.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + 4 * 3600
    completed = ROOT / "runs/coder390-pilot/completed.json"
    while not completed.exists():
        try:
            os.kill(pilot_pid, 0)
        except ProcessLookupError:
            raise RuntimeError("Pilot supervisor exited without successful completion") from None
        if time.monotonic() >= deadline:
            raise TimeoutError("Pilot completion exceeded four hours; inspect before continuing")
        time.sleep(10)
    checks = check_pilots()
    write_json(directory / "pilot-gate.json", {
        "checks": checks, "workers": 4, "slots": 4, "context_per_slot": 16384,
        "main_responses_planned": 400,
        "note": "Technical gate only. Pilot identities do not determine main sample size or parameters.",
    })
    print("All eight matched pilot captures passed; beginning fixed 400-response capture.", flush=True)
    subprocess.run([sys.executable, str(ROOT / "tools/coder390_run.py"), "--phase", "main"], check=True)
    print("Main capture complete. Multi-identity judging and manual visual audit remain required.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-pid", type=int, required=True)
    args = parser.parse_args()
    try:
        continue_after_pilot(args.pilot_pid)
    except Exception as error:
        write_json(ROOT / "runs/coder390-main/pipeline-error.json", {
            "error_type": type(error).__name__, "error": str(error), "recorded_unix": time.time()})
        raise
