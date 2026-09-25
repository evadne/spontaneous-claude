# OrcaSAQ-2-27B evaluation method

Date: 25 September 2026. The checkpoint is the exact four-shard EXL3
safetensors from `orcarouter/OrcaSAQ-2-27B` at
`15d20d7e9ae4fd89d1a47878f69381760169445b`. The card's alternate
spelling, `orcarouter/OrcaSAQ2-27B`, resolves to the same repository ID and
revision. The archived model card, config, tokenizer config, quantisation
config and tree metadata are in this directory. `tree.json` holds the expected
LFS SHA-256 for each shard. `verify_weights.py` checks the local download.

The repository tokenizer SHA-256 and tokenizer configuration (including the complete chat template) exactly match the pinned Qwen base repository, and the text architecture fields match; this supports structural lineage but does not prove weight provenance. The source base architecture is multimodal conditional generation, whereas this checkpoint declares a text-only causal-LM class and carries no vision tensors.

The format is `exl3`; the installed first-party llama.cpp server cannot load
it. Serving uses the publisher's [OrcaSAQ2-kernel](https://github.com/Continuum-AI-Corp/OrcaSAQ2-kernel)
at `7ddffb12c00c24b8bc6b1164723c04ac490a91bc`, the vLLM 0.30.0 image
at digest `sha256:8a69ffad015f138d7170c4ddc429e230a3bc1c1719f67e14324749df200a4b90`,
and its pinned exllamav3 wheel for that image's torch/CUDA ABI. No conversion
or requantisation is performed. The image and launch settings are recorded in
`serving.json` after a successful launch.

The GPU host is accessed through SSH. An existing embedding server remains
running. The evaluation container publishes its API on remote loopback only;
the workstation forwards it to local port 8094. `capture_proxy.py` listens on
local port 8095 and records complete request bodies and raw responses under
`raw/proxy/`. The Athanor adapter uses that proxy. Plain-chat controls also
use the proxy but omit Athanor's system message and Human XML envelope. The
model's chat template itself inserts a system-level reasoning instruction by
default; plain chat is therefore not raw base-model prompting.

The Athanor checkout is an isolated worktree at
`~/Projects/athanor/.worktrees/feature/orcasaq-evaluation`, based on main at
`092298c7`. It has separate `_build` and `deps`, copies of the required local
configuration and a symlink to the primary checkout's model assets. The
scripts in this directory run through `mix` in that worktree; no application
source is modified. The bootstrap supplies an empty personal fragment list and
no services. It loads `probe.exs` and `controls.exs` into an Athanor node;
another Elixir node calls them with `:rpc.call/5`.

Run order, once the server and SSH tunnel are ready:

```sh
python3 methods/capture_proxy.py
cd ~/Projects/athanor/.worktrees/feature/orcasaq-evaluation
elixir --sname orcasaq-athanor --cookie athanor-local -S mix run --no-start --no-halt ~/Projects/orcasaq-2-investigation/methods/bootstrap.exs
elixir --sname orcasaq-baseline --cookie athanor-local ~/Projects/orcasaq-2-investigation/methods/baseline.exs
elixir --sname orcasaq-practical --cookie athanor-local ~/Projects/orcasaq-2-investigation/methods/practical.exs
elixir --sname orcasaq-controls --cookie athanor-local ~/Projects/orcasaq-2-investigation/methods/run_controls.exs
elixir --sname orcasaq-session --cookie athanor-local ~/Projects/orcasaq-2-investigation/methods/run_session.exs
elixir --sname orcasaq-corrections --cookie athanor-local ~/Projects/orcasaq-2-investigation/methods/run_corrections.exs
python3 ~/Projects/orcasaq-2-investigation/methods/portrait_correction.py
python3 ~/Projects/orcasaq-2-investigation/methods/score_practical.py
python3 ~/Projects/orcasaq-2-investigation/methods/parse_captures.py
python3 ~/Projects/orcasaq-2-investigation/methods/render_portraits.py
```

Provider probes retain prompt, formatted request, full assistant structure,
stream events, stop reason and elapsed time. Plain controls retain complete
OpenAI-compatible requests and responses. The two-turn Session retains
context, all ledger events, file outputs and the wire captures; the second
turn updates the input ledger and tests whether the agent refreshes state.
Human scoring and limitations are in the top-level report. Model self-reports
and emitted reasoning are observations, never verified training provenance.

The separate BF16 base control uses the pinned `ggml-org/Qwen3.8-27B-GGUF`
release at `efbb3b1f70a21d97fd4495240648405f7228554f`. Verify its single
GGUF against `base-control/serving.json`, then start the installed first-party
llama.cpp server with that file's recorded launch command and run
`python3 methods/base_control.py`. It listens on local port 8096 and does not
use the Orca capture proxy. The BF16 GGUF conversion does not pin its exact
Qwen source revision, and its serving stack differs from the Orca path;
compare behaviour qualitatively only.
