#!/usr/bin/env python3
"""Capture fresh, matched identity and portrait requests from local llama.cpp."""

import argparse
import concurrent.futures
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from claudeness import read_plan, seal, write_json


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def request_for(job):
    return {
        "model": "specimen",
        "messages": [{"role": "user", "content": job["prompt"]}],
        "seed": job["seed"],
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 20,
        "min_p": 0.0,
        "repeat_penalty": 1.0,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "max_tokens": job["max_tokens"],
        "reasoning_effort": job["reasoning_mode"],
        "chat_template_kwargs": {"enable_thinking": True},
        "cache_prompt": False,
        "stream": False,
    }


def capture(endpoint, directory, job):
    directory.mkdir(parents=True, exist_ok=True)
    request = request_for(job)
    result_path = directory / "capture.json"
    if result_path.exists():
        record = json.loads(result_path.read_text())
        if record["job"] != job or record["request"] != request:
            raise ValueError("Existing capture differs from plan: " + str(directory))
        if record["response_sha256"] != sha256(directory / "response.json"):
            raise ValueError("Raw response changed: " + str(directory))
        return record
    # An interrupted request may have generated an unseen response. Never quietly
    # replace it with a new draw; retain and reconcile the attempt first.
    if (directory / "request.json").exists():
        raise ValueError("Unresolved prior attempt: " + str(directory))
    write_json(directory / "request.json", request)
    started = time.monotonic()
    begun = datetime.now(timezone.utc).isoformat()
    req = urllib.request.Request(endpoint, json.dumps(request).encode(),
                                 {"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=3600) as response:
            raw = response.read()
            status = response.status
        (directory / "response.json").write_bytes(raw)
        body = json.loads(raw)
        if status != 200 or len(body["choices"]) != 1:
            raise ValueError("Unexpected response status or choice count")
        choice = body["choices"][0]
        message = choice["message"]
        if choice["finish_reason"] not in ("stop", "length"):
            raise ValueError("Unexpected finish reason: " + str(choice["finish_reason"]))
        record = {
            "job": job, "request": request, "status": status,
            "started_at": begun, "completed_at": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": time.monotonic() - started,
            "response_sha256": hashlib.sha256(raw).hexdigest(),
            "finish_reason": choice["finish_reason"], "usage": body["usage"],
            "reasoning_available": "reasoning_content" in message,
        }
        (directory / "answer.txt").write_text(message["content"] or "")
        if "reasoning_content" in message:
            (directory / "reasoning.txt").write_text(message["reasoning_content"] or "")
        write_json(result_path, record)
        print(json.dumps({"id": job["id"], "finish": record["finish_reason"],
                          "seconds": round(record["elapsed_seconds"], 1),
                          "usage": record["usage"]}), flush=True)
        return record
    except Exception as error:
        write_json(directory / "error.json", {"started_at": begun,
                   "recorded_at": datetime.now(timezone.utc).isoformat(),
                   "error_type": type(error).__name__, "error": str(error)})
        raise


def run(args):
    plans = [read_plan(path) for path in args.plan]
    jobs = sorted((job for plan in plans for job in plan),
                  key=lambda job: (job["order"], job["condition"]))
    if len({job["id"] for job in jobs}) != len(jobs):
        raise ValueError("Duplicate request ID across plans")
    for job in jobs:
        if job["reasoning_mode"] != "low":
            raise ValueError("This registered experiment requires low reasoning")
    seal(args.out, {
        "operation": "matched-identity-capture", "endpoint": args.endpoint,
        "model_label": args.model_label, "workers": args.workers,
        "plans": {str(p): sha256(p) for p in args.plan},
        "model_manifest": json.loads(args.model_manifest.read_text()),
        "server_manifest": json.loads(args.server_manifest.read_text()),
        "implementation_sha256": sha256(Path(__file__)),
        "requests_sha256": hashlib.sha256(json.dumps(
            [request_for(job) for job in jobs], sort_keys=True).encode()).hexdigest(),
    })
    # Fixed waves preserve the planned grouping; no outcome-dependent scheduling.
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for start in range(0, len(jobs), args.workers):
            wave = jobs[start:start + args.workers]
            futures = [pool.submit(capture, args.endpoint, args.out / job["id"], job)
                       for job in wave]
            for future in futures:
                future.result()
    records = [json.loads((args.out / job["id"] / "capture.json").read_text()) for job in jobs]
    write_json(args.out / "summary.json", {
        "planned": len(jobs), "captured": len(records),
        "normal_stops": sum(r["finish_reason"] == "stop" for r in records),
        "truncations": sum(r["finish_reason"] == "length" for r in records),
        "missing_reasoning": sum(not r["reasoning_available"] for r in records),
        "completed_at": datetime.now(timezone.utc).isoformat(),
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model-label", required=True)
    parser.add_argument("--model-manifest", type=Path, required=True)
    parser.add_argument("--server-manifest", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4, choices=(1, 2, 4))
    run(parser.parse_args())
