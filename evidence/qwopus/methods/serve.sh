#!/usr/bin/env bash
set -euo pipefail

exec "$HOME/Projects/llama.cpp/build/bin/llama-server" \
  --model "$HOME/Projects/models/qwopus3.8-27b-flash/Qwopus3.8-27B-Flash-MTP-Q8_0.gguf" \
  --alias qwopus-local \
  --host 127.0.0.1 --port 8093 \
  --ctx-size 32768 --parallel 1 \
  --n-gpu-layers 99 --flash-attn on \
  --jinja --reasoning on --reasoning-format deepseek \
  --reasoning-budget -1 --seed 1701 \
  --temp 1.0 --top-p 0.95 --top-k 20
