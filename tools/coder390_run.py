#!/usr/bin/env python3
"""Run the registered Coder390/base conditions, one resident model at a time."""

import argparse
import hashlib
import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from claudeness import write_json

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/coder390"
BINARY = Path("/Users/evadne/Projects/llama.cpp/build/bin/llama-server")
REVISION = "4df29be4f4c3673f428170fda944a5b19f743bb8"
ORIGIN = "http://127.0.0.1:8097"
MODELS = (("coder390", "coder390-model.json"), ("base-matched", "base-matched-model.json"))


def post(path, body):
    req = urllib.request.Request(ORIGIN + path, json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def run_condition(phase, label, manifest_name):
    directory = ROOT / "runs" / ("coder390-" + phase) / label
    directory.mkdir(parents=True, exist_ok=True)
    manifest_path = EVIDENCE / manifest_name
    manifest = json.loads(manifest_path.read_text())
    model = Path(manifest["path"])
    if model.stat().st_size != manifest["bytes"]:
        raise ValueError("Model size changed: " + str(model))
    check = hashlib.sha256()
    with model.open("rb") as source:
        for block in iter(lambda: source.read(16 * 1024 * 1024), b""):
            check.update(block)
    if check.hexdigest() != manifest["sha256"]:
        raise ValueError("Model hash changed: " + str(model))
    command = [str(BINARY), "--host", "127.0.0.1", "--port", "8097",
               "--model", str(model), "--alias", "specimen", "--no-webui", "--jinja",
               "--reasoning", "on", "--reasoning-effort", "low",
               "--reasoning-format", "deepseek", "--ctx-size", "65536",
               "--gpu-layers", "99", "--parallel", "4", "--batch-size", "2048",
               "--ubatch-size", "512", "--flash-attn", "on", "--min-p", "0.0",
               "--no-context-shift"]
    server_manifest = directory / "server.json"
    # PID and wall-clock launch time are operational, not the run identity.
    contract = {"command": command, "model": manifest, "llama_revision": REVISION,
                "binary_sha256": hashlib.sha256(BINARY.read_bytes()).hexdigest()}
    if server_manifest.exists() and json.loads(server_manifest.read_text()) != contract:
        raise ValueError("Serving contract changed: " + str(server_manifest))
    write_json(server_manifest, contract)
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", 8097)) == 0:
            raise RuntimeError("Study port is occupied; do not stop an unknown server")
    with (directory / "server.log").open("ab") as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        write_json(directory / "process.json", {"pid": process.pid, "started_unix": time.time()})
        try:
            deadline = time.monotonic() + 300
            while True:
                if process.poll() is not None:
                    raise RuntimeError("Model server exited during startup")
                try:
                    with urllib.request.urlopen(ORIGIN + "/health", timeout=5) as response:
                        health = json.load(response)
                    if health["status"] == "ok":
                        break
                except (urllib.error.URLError, TimeoutError):
                    pass
                if time.monotonic() >= deadline:
                    raise TimeoutError("Model server did not become healthy")
                time.sleep(2)
            with urllib.request.urlopen(ORIGIN + "/props", timeout=10) as response:
                props = json.load(response)
            if props["model_path"] != str(model) or props["total_slots"] != 4:
                raise ValueError("Server loaded an unexpected model or slot count")
            if hashlib.sha256(props["chat_template"].encode()).hexdigest() != manifest["template_sha256"]:
                raise ValueError("Served chat template differs from model manifest")
            write_json(directory / "props.json", props)
            for prompt in ("identity", "portrait"):
                plan = EVIDENCE / f"{phase}-{prompt}-plan.jsonl"
                job = json.loads(plan.read_text().splitlines()[0])
                body = {"messages": [{"role": "user", "content": job["prompt"]}],
                        "add_generation_prompt": True,
                        "chat_template_kwargs": {"enable_thinking": True, "reasoning_effort": "low"}}
                rendered = post("/apply-template", body)
                expected = (
                    "<|im_start|>system\nReasoning effort is set to low. Keep your thinking brief and focused, "
                    "moving directly to the conclusion without unnecessary elaboration.<|im_end|>\n"
                    "<|im_start|>user\n" + job["prompt"] + "<|im_end|>\n"
                    "<|im_start|>assistant\n<think>\n")
                if rendered["prompt"] != expected:
                    raise ValueError("Rendered prompt differs from registered condition")
                write_json(directory / (prompt + "-rendered-prompt.json"),
                           {"request": body, "response": rendered})
            capture = [sys.executable, str(ROOT / "tools/identity_batch.py"),
                       "--plan", str(EVIDENCE / f"{phase}-identity-plan.jsonl"),
                       "--plan", str(EVIDENCE / f"{phase}-portrait-plan.jsonl"),
                       "--out", str(directory / "raw"),
                       "--endpoint", ORIGIN + "/v1/chat/completions",
                       "--model-label", label, "--model-manifest", str(manifest_path),
                       "--server-manifest", str(server_manifest), "--workers", "4"]
            print("Starting", phase, label, flush=True)
            with (directory / "capture.log").open("ab") as capture_log:
                subprocess.run(capture, stdout=capture_log, stderr=subprocess.STDOUT, check=True)
            print("Completed", phase, label, flush=True)
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("pilot", "main"), required=True)
    args = parser.parse_args()
    actual = subprocess.check_output(["git", "-C", str(BINARY.parents[2]),
                                      "rev-parse", "HEAD"], text=True).strip()
    if actual != REVISION:
        raise ValueError("Pinned llama.cpp source revision changed")
    for label, manifest_name in MODELS:
        run_condition(args.phase, label, manifest_name)
    write_json(ROOT / "runs" / ("coder390-" + args.phase) / "completed.json",
               {"phase": args.phase, "models": [row[0] for row in MODELS],
                "completed_unix": time.time()})
