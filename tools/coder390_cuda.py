#!/usr/bin/env python3
"""Continue untouched registered draws on the authorised CUDA host."""

import argparse
import hashlib
import json
import shlex
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from claudeness import write_json
from identity_batch import capture, read_plan, request_for

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/coder390"
RUN = ROOT / "runs/coder390-main"
HOST = "root@codex-test-1.local"
REMOTE = "/opt/spontaneous-claude"
BINARY = REMOTE + "/runtime/build/bin/llama-server"
ORIGIN = "http://127.0.0.1:8098"
REVISION = "4df29be4f4c3673f428170fda944a5b19f743bb8"
MODELS = (("coder390", "coder390-model.json"),
          ("base-matched", "base-matched-model.json"))


def remote_python(source, *args):
    command = shlex.join(["/usr/bin/python3", "-c", source, *args])
    return subprocess.check_output(["ssh", "-o", "BatchMode=yes", HOST, command], text=True)


def remaining_jobs(plan, raw):
    """Validate the drained prefix before selecting any never-attempted draws."""
    remaining = []
    for job in plan:
        directory = raw / job["id"]
        record_path = directory / "capture.json"
        if record_path.exists():
            record = json.loads(record_path.read_text())
            assert record["job"] == job
            assert record["request"] == request_for(job)
            assert hashlib.sha256((directory / "response.json").read_bytes()).hexdigest() == record["response_sha256"]
        elif directory.exists():
            raise ValueError("Unresolved attempt: " + str(directory))
        else:
            remaining.append(job)
    return remaining


def get(path):
    with urllib.request.urlopen(ORIGIN + path, timeout=10) as response:
        return json.load(response)


def run_condition(label, manifest_name, layers, recovery=False):
    directory = RUN / ("cuda-recovery" if recovery else "cuda") / label
    directory.mkdir(parents=True, exist_ok=True)
    plans = []
    for condition in ("identity", "portrait"):
        original = read_plan(EVIDENCE / f"main-{condition}-plan.jsonl")
        jobs = remaining_jobs(original, RUN / label / "raw")
        plan_path = directory / f"{condition}-plan.jsonl"
        text = "".join(json.dumps(job, ensure_ascii=False) + "\n" for job in jobs)
        if plan_path.exists() and plan_path.read_text() != text:
            raise ValueError("Migration subset changed")
        plan_path.write_text(text)
        plans.append(plan_path)
    original_manifest = json.loads((EVIDENCE / manifest_name).read_text())
    model = REMOTE + "/models/" + Path(original_manifest["path"]).name
    verified = json.loads(remote_python(
        "import hashlib,json,sys,socket; from pathlib import Path\n"
        "p=Path(sys.argv[1]); h=hashlib.sha256()\n"
        "with p.open('rb') as f:\n"
        " for b in iter(lambda:f.read(16*1024*1024),b''):h.update(b)\n"
        "with socket.socket() as s: assert s.connect_ex(('127.0.0.1',18097)) != 0\n"
        "print(json.dumps({'bytes':p.stat().st_size,'sha256':h.hexdigest(),"
        "'binary_sha256':hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest()}))",
        model, BINARY))
    assert verified["sha256"] == original_manifest["sha256"]
    assert verified["bytes"] == original_manifest["bytes"]
    manifest = dict(original_manifest, path=model, original_path=original_manifest["path"])
    manifest_path = directory / "model.json"
    write_json(manifest_path, manifest)
    command = [BINARY, "--host", "127.0.0.1", "--port", "18097",
               "--model", model, "--alias", "specimen", "--no-webui", "--jinja",
               "--reasoning", "on", "--reasoning-effort", "low",
               "--reasoning-format", "deepseek", "--ctx-size", "65536",
               "--gpu-layers", str(layers), "--threads", "8", "--fit", "off",
               "--parallel", "4", "--batch-size", "2048", "--ubatch-size", "512",
               "--flash-attn", "on", "--min-p", "0.0", "--no-context-shift"]
    contract = {"command": command, "model": manifest, "host": HOST,
                "llama_revision": REVISION, "binary_sha256": verified["binary_sha256"],
                "backend": "CUDA with partial CPU offload",
                "source_verification": "evidence/coder390/cuda-source-verification.json"}
    server_manifest = directory / "server.json"
    if server_manifest.exists() and json.loads(server_manifest.read_text()) != contract:
        raise ValueError("Serving contract changed")
    write_json(server_manifest, contract)
    with socket.socket() as probe:
        if probe.connect_ex(("127.0.0.1", 8098)) == 0:
            raise RuntimeError("Migration port occupied")
    pid_path = REMOTE + "/" + label + ".pid"
    launcher = "import os,sys; from pathlib import Path; Path(sys.argv[1]).write_text(str(os.getpid())); os.execv(sys.argv[2],sys.argv[2:])"
    ssh = ["ssh", "-o", "BatchMode=yes", "-o", "ExitOnForwardFailure=yes",
           "-o", "ServerAliveInterval=15", "-o", "ServerAliveCountMax=4",
           "-L", "127.0.0.1:8098:127.0.0.1:18097", HOST,
           shlex.join(["/usr/bin/python3", "-c", launcher, pid_path, *command])]
    with (directory / "server.log").open("ab") as log:
        process = subprocess.Popen(ssh, stdout=log, stderr=subprocess.STDOUT)
        write_json(directory / "process.json", {"local_ssh_pid": process.pid,
                   "remote_pid_path": pid_path, "started_unix": time.time()})
        try:
            deadline = time.monotonic() + 300
            while True:
                if process.poll() is not None:
                    raise RuntimeError("CUDA server exited during startup")
                try:
                    if get("/health")["status"] == "ok":
                        break
                except (urllib.error.URLError, TimeoutError):
                    pass
                if time.monotonic() > deadline:
                    raise TimeoutError("CUDA startup exceeded five minutes")
                time.sleep(2)
            props = get("/props")
            assert props["model_path"] == model and props["total_slots"] == 4
            assert hashlib.sha256(props["chat_template"].encode()).hexdigest() == manifest["template_sha256"]
            write_json(directory / "props.json", props)
            for condition in ("identity", "portrait"):
                baseline = json.loads((EVIDENCE / "pilot/coder390" / (condition + "-rendered-prompt.json")).read_text())
                req = urllib.request.Request(ORIGIN + "/apply-template",
                    json.dumps(baseline["request"]).encode(), {"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    rendered = json.load(response)
                assert rendered == baseline["response"]
                write_json(directory / (condition + "-rendered-prompt.json"),
                           {"request": baseline["request"], "response": rendered})
            smoke = {"id": "cuda-health", "condition": "health", "order": 0,
                     "seed": 314159, "prompt": "Reply with the word ready.",
                     "reasoning_mode": "low", "max_tokens": 128}
            result = capture(ORIGIN + "/v1/chat/completions", directory / "excluded-health", smoke)
            assert result["reasoning_available"] and result["finish_reason"] == "stop"
            assert (directory / "excluded-health/answer.txt").read_text().strip()
            write_json(directory / "technical-gate.json", {"passed": True,
                       "smoke_excluded": True, "response_sha256": result["response_sha256"]})
            args = [sys.executable, str(ROOT / "tools/identity_batch.py")]
            for path in plans:
                args.extend(["--plan", str(path)])
            args.extend(["--out", str(directory / "raw"), "--endpoint", ORIGIN + "/v1/chat/completions",
                         "--model-label", label, "--model-manifest", str(manifest_path),
                         "--server-manifest", str(server_manifest), "--workers", "4"])
            if recovery:
                args.extend(["--request-timeout", "14400", "--prior-raw",
                             str(RUN / "cuda" / label / "raw")])
                if label == "coder390":
                    args.extend(["--retry-id", "portrait-0015"])
            with (directory / "capture.log").open("ab") as capture_log:
                subprocess.run(args, stdout=capture_log, stderr=subprocess.STDOUT, check=True)
        finally:
            remote_python(
                "import os,signal,sys,time; from pathlib import Path\n"
                "p=Path(sys.argv[1])\n"
                "if p.exists():\n"
                " pid=int(p.read_text()); proc=Path('/proc')/str(pid); cmd=proc/'cmdline'\n"
                " if cmd.exists() and sys.argv[2].encode() in cmd.read_bytes().split(b'\\0'):\n"
                "  os.kill(pid,signal.SIGTERM)\n"
                "  for i in range(30):\n"
                "   if not cmd.exists() or not cmd.read_bytes():break\n"
                "   time.sleep(1)\n"
                "  else:os.kill(pid,signal.SIGKILL)\n", pid_path, BINARY)
            process.wait(timeout=40)
    write_json(directory / "completed.json", {"model": label, "completed_unix": time.time()})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gpu-layers", type=int, required=True)
    parser.add_argument("--recovery", action="store_true")
    args = parser.parse_args()
    try:
        for label, manifest_name in MODELS:
            run_condition(label, manifest_name, args.gpu_layers, args.recovery)
        for label, _ in MODELS:
            for condition in ("identity", "portrait"):
                jobs = read_plan(EVIDENCE / f"main-{condition}-plan.jsonl")
                for job in jobs:
                    paths = [RUN / label / "raw" / job["id"], RUN / "cuda" / label / "raw" / job["id"]]
                    if args.recovery:
                        paths.append(RUN / "cuda-recovery" / label / "raw" / job["id"])
                    accepted = [p for p in paths if (p / "capture.json").exists()]
                    assert len(accepted) == 1
                    assert not remaining_jobs([job], accepted[0].parent)
        write_json(RUN / "completed.json", {"models": [m[0] for m in MODELS],
                   "completed_unix": time.time(), "captures": 400,
                   "backends": ["Metal prefix", "CUDA continuation"],
                   "note": "Use migration provenance and backend strata in comparisons."})
    except Exception as error:
        error_root = RUN / ("cuda-recovery" if args.recovery else "cuda")
        write_json(error_root / "pipeline-error.json", {"error_type": type(error).__name__,
                   "error": str(error), "recorded_unix": time.time()})
        raise
