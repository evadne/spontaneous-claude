"""Resumable host-side runner for a pre-registered portrait plan.

Uses only Python's standard library so it can run on codex-test-1 outside the
Docker inference container. One response file is written atomically per seed.
"""

import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "http://127.0.0.1:8094/v1/chat/completions"
HEALTH = "http://127.0.0.1:8094/health"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w") as stream:
        json.dump(value, stream, ensure_ascii=False, separators=(",", ":"))
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def request_for(job):
    body = {
        "model": "orcasaq-local",
        "messages": [{"role": "user", "content": job["prompt"]}],
        "seed": job["seed"],
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 20,
        "max_tokens": job["max_tokens"],
        "stream": False,
    }
    if job["reasoning_mode"] == "low":
        body["reasoning_effort"] = "low"
    elif job["reasoning_mode"] == "off":
        body["chat_template_kwargs"] = {"enable_thinking": False}
    elif job["reasoning_mode"] != "default":
        raise ValueError(f"Unknown reasoning mode: {job['reasoning_mode']}")
    return body


def call(body):
    request = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer local-llama"},
    )
    with urllib.request.urlopen(request, timeout=900) as response:
        return response.status, json.load(response)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    args.out.mkdir(parents=True, exist_ok=True)
    data = args.plan.read_bytes()
    jobs = [json.loads(line) for line in data.splitlines() if line]
    if args.limit is not None:
        jobs = jobs[:args.limit]
    with urllib.request.urlopen(HEALTH, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"Model health returned {response.status}")
    (args.out / "run-complete.json").unlink(missing_ok=True)
    info = {"started_at": utc_now(), "plan_sha256": hashlib.sha256(data).hexdigest(),
            "selected_jobs": len(jobs), "endpoint": URL}
    atomic_json(args.out / "run-info.json", info)
    success = 0
    failures = 0
    for job in jobs:
        dest = args.out / f"{job['id']}.json"
        if dest.exists():
            previous = json.loads(dest.read_text())
            if previous.get("job") == job and previous.get("status") == 200:
                success += 1
                continue
            raise RuntimeError(f"Unexpected existing result: {dest}")
        body = request_for(job)
        last_error = None
        for attempt in range(1, 4):
            start = time.monotonic()
            try:
                status, response = call(body)
                elapsed = round((time.monotonic() - start) * 1000)
                if status != 200:
                    raise RuntimeError(f"HTTP {status}: {response}")
                outcome = {"job": job, "request": body, "status": status,
                           "elapsed_ms": elapsed, "completed_at": utc_now(),
                           "response": response}
                atomic_json(dest, outcome)
                choice = response.get("choices", [{}])[0]
                usage = response.get("usage") or {}
                print(job["id"], choice.get("finish_reason"),
                      usage.get("completion_tokens"), elapsed, flush=True)
                success += 1
                last_error = None
                break
            except (OSError, ValueError, RuntimeError, urllib.error.URLError) as error:
                last_error = f"{type(error).__name__}: {error}"
                print(job["id"], "attempt", attempt, last_error, flush=True)
                if attempt < 3:
                    time.sleep(attempt * 5)
        if last_error is not None:
            atomic_json(args.out / f"{job['id']}.error.json",
                        {"job": job, "error": last_error, "attempts": 3,
                         "completed_at": utc_now()})
            failures += 1
    complete = {**info, "completed_at": utc_now(), "success": success,
                "failures": failures}
    atomic_json(args.out / "run-complete.json", complete)
    print("COMPLETE", json.dumps(complete, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
