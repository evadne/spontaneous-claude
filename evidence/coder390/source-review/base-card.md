---
license: apache-2.0
language:
- en
- zh
pipeline_tag: text-generation
tags:
- qwen
- qwen3.8
- dense
- efficient-thinking
- thinking
- reasoning
- coding
- agent
- conversational
- uncensored
- heretic
- sft
- simpo
- bf16
- fp8
- block128
- dflash2
- speculative-decoding
- sglang
- vllm
- nvfp4
- mtp
- modelopt
- q2-lynnstyle
- mixed-precision
- gsq-rco
- gsq
- iq
- rco
- int8
- w8a8
- qat
- compressed-tensors
- dynamic-quantization
---

# Qwen3.8-27B EfficientThink · SFT → SimPO · DFlash2

![EfficientThink evaluation summary](assets/efficientthink-capability-reasoning-v5-3-en.png)

> **No strict loops were observed in the reviewed Q2–Q8 evaluations.**

**GGUF repository: [nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2-GGUF](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2-GGUF)**

<!-- Q8_Q5_MAIN_MIRROR_V1_EN_START -->
### Measured scores across all six GGUF tiers

The main and standalone GGUF repositories provide all six tiers. These are formal full-suite frozen scores, with every non-passing sample retained in the denominator. Main-repository paths add the `GGUF/` prefix:

| Tier | GPQA 198 | MMLU 500 | LCB 100 | Main-repository directory |
|---|---:|---:|---:|---|
| Q8_0 | 164/198 (82.83%) | 447/500 (89.40%) | 74/100 (74.00%) | `GGUF/Q8_0/` |
| Q6_K | 171/198 (86.36%) | 440/500 (88.00%) | 78/100 (78.00%) | `GGUF/Q6_K/` |
| Q5-LynnStyle | 164/198 (82.83%) | 438/500 (87.60%) | 75/100 (75.00%) | `GGUF/Q5-LynnStyle/` |
| Q4-LynnStyle | 166/198 (83.84%) | 443/500 (88.60%) | 74/100 (74.00%) | `GGUF/Q4-LynnStyle/` |
| Q3-LynnStyle | 172/198 (86.87%) | 435/500 (87.00%) | 78/100 (78.00%) | `GGUF/Q3-LynnStyle/` |
| Q2-LynnStyle | 167/198 (84.34%) | 416/500 (83.20%) | 75/100 (75.00%) | `GGUF/Q2-LynnStyle/` |

> **Q2-LynnStyle uses GSQ-RCO mixed-precision quantization with IQ numerical refinement.** Its exact 12,999,977,600-byte build has no frozen TPS result.
>
> Q2 LCB disclosure: the 75/100 final view preserves 99 original rows and uses one Lynn-authorized exact retry for a streaming-JSON failure; the retry again reached 32K with empty code.

See the standalone GGUF repository linked above for full DFlash2 concurrency tables, file roles, and llama.cpp commands.
<!-- Q8_Q5_MAIN_MIRROR_V1_EN_END -->

<!-- LYNN_AGENT_V0870_EN_START -->
## Lynn Agent v0.87.0

Lynn Agent v0.87.0 uses this release's **Q2-LynnStyle / Q3-LynnStyle + DFlash2** packages. The pairing passed runtime validation on DGX Spark; notarized Mac Apple Silicon and Intel builds, the Windows installer runtime check, CI in both repositories, matching `main` heads and tags across all three release repositories, complete SHA256 verification for 23 public files, and a remote CLI installation all passed.

Natural moving tree shadows and soft window light, enabled by default. Hover over Shadows for the off switch location, or click to open Settings. Playback pauses in the background and stays still with reduced motion. Images now participate in file filtering; slash templates replace persistent task mode; translation moved into the message menu; Expert Roundtable is now an optional plugin; and session edit targeting and stop preprocessing were fixed. Kimi Datasource remains available under MCP and requires users to scan the QR code and sign in with their own account.

> This client update did not change any model weight, quantized artifact, benchmark score, or performance metric in this repository.

| Installer | China mirror | GitHub fallback |
| --- | --- | --- |
| Mac Apple Silicon | [Download](https://download.merkyorlynn.com/downloads/Lynn-0.87.0-macOS-arm64.dmg) | [Download](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.0/Lynn-0.87.0-macOS-arm64.dmg) |
| Mac Intel | [Download](https://download.merkyorlynn.com/downloads/Lynn-0.87.0-macOS-x64.dmg) | [Download](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.0/Lynn-0.87.0-macOS-x64.dmg) |
| Windows | [Download](https://download.merkyorlynn.com/downloads/Lynn-0.87.0-Windows-Setup.exe) | [Download](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.0/Lynn-0.87.0-Windows-Setup.exe) |

Release records: [primary GitHub repository](https://github.com/MerkyorLynn/Lynn/releases/tag/v0.87.0) · [legacy GitHub repository](https://github.com/LynnMerkyor/Lynn/releases/tag/v0.87.0) · [Gitee](https://gitee.com/merkyor/Lynn/releases/tag/v0.87.0) · [CLI package](https://download.merkyorlynn.com/downloads/cli/lynn-cli-0.87.0.tgz)
<!-- LYNN_AGENT_V0870_EN_END -->

<!-- GGUF_MTP_Q4_Q8_V1_EN_START -->
### Bundled llama.cpp Q4_0 and Q8_0 MTP drafts

Each `GGUF/Q2-LynnStyle/` through `GGUF/Q8_0/` directory mirrors two optional MTP sidecars from the standalone GGUF repository:

| File in each tier | Size | SHA256 |
|---|---:|---|
| `mtp-Qwen3.8-27B-Q4_0.gguf` | 1,680,271,648 bytes | `051a1764cff8c4f3ee6ae8b00593a0364c7539c67fa50ffc58f3f96509fca38e` |
| `mtp-Qwen3.8-27B-Q8_0.gguf` | 3,164,006,688 bytes | `cbf60a0c48b431bb61f1d49b8948dc88ac29c398d6dbdbbb2e6e89ef77eacc9a` |

Both passed GGUF role parsing and real DGX Spark load/generation with Q3-LynnStyle. Use `--model-draft GGUF/<tier>/mtp-Qwen3.8-27B-Q4_0.gguf --spec-type draft-mtp` (or the Q8_0 file). Choose MTP **or** DFlash2, never both in one command. Full file roles and llama.cpp examples are in the linked standalone GGUF repository.
<!-- GGUF_MTP_Q4_Q8_V1_EN_END -->

<!-- INT8_W8A8_QAT_HF_XET_V2_1 -->
<!-- INT8_W8A8_QAT_V2_EN_START -->

## True-QAT INT8 W8A8 | dynamic INT8 activations

![True-QAT INT8 W8A8 | dynamic INT8 activations](assets/int8-w8a8-qat-quality-mtp-v2-en.png)

**Download directory: `NVFP4/INT8-W8A8-QAT/`.** [Matching main/standalone repository on this platform](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-MTP-NVFP4).

### Files and precision

| Component | Path | Precision / role | Size |
|---|---|---|---:|
| Main model | `NVFP4/INT8-W8A8-QAT/model-00001-of-00008.safetensors` … `model-00008-of-00008.safetensors` | True-QAT INT8 W8A8; dynamic INT8 activations | 29.48 GB |
| Vision + native MTP | `NVFP4/INT8-W8A8-QAT/vision-mtp-bf16.safetensors` | 333 BF16 vision tensors + 15 BF16 MTP tensors, with 348 real index mappings | 1.77 GB |
| Complete inventory | `NVFP4/INT8-W8A8-QAT/manifest.json` and `NVFP4/INT8-W8A8-QAT/SHA256SUMS` | Roles, bytes, and SHA256 for the current 29-file directory | — |
| Structured evaluation | [`NVFP4/INT8-W8A8-QAT/evaluation/formal-quality-and-performance.json`](NVFP4/INT8-W8A8-QAT/evaluation/formal-quality-and-performance.json) | Formal scores, reasoning statistics, and the complete research record | — |

### Training and export method

- 64-layer Qwen3.8-27B multimodal architecture with 1,599 entries in the published model index.
- 3,200 QAT optimizer steps; all 400 language linear tensors recorded non-zero gradients and are published with INT8 weights.
- Dynamic INT8 activations; 247 items entered the accepted training set.
- BF16 scales were losslessly exported as F32; the vision tower and native MTP remain BF16.

### Formal capability and reasoning results

Protocol: 1× RTX PRO 6000 Blackwell 96GB, vLLM 0.28.0 + native MTP3, C20, BF16 KV, `reasoning_effort=xhigh`, a 32,768-token output cap, and a 1,800-second request timeout. The long-output formal suite uses C20 because C24 did not leave enough KV capacity for the full suite.

| Suite | Score | Mean reasoning | P50 / P90 | >8K / >16K | 32K trunc. | Empty final / unparseable |
|---|---:|---:|---:|---:|---:|---:|
| GPQA | **162/198 (81.82%)** | 9,530 | 4,699.5 / 32,767 | 73 / 41 | 23 | 23 / 23 |
| MMLU | **451/500 (90.20%)** | 837 | 203 / 1,906.1 | 9 / 3 | 0 | 0 / 0 |
| LCB | **73/100 (73.00%)** | 13,921 | 8,347 / 32,768 | 50 / 41 | 23 | 23 / 23 |

Request / HTTP / capture / grader errors are all **0**. LCB has **0** code timeouts and **0** syntax errors, plus 1 runtime error. IPC-v4 uniformly regraded the original 100 answers without issuing new model requests.

### 24 short-output cells for bundled runtime paths

Protocol: 1,024 input / 256 output, warmup plus 3 trials. This measures short fixed-length serving throughput, not long-reasoning speed. All 24 bare/MTP3 cells completed with 0 request errors.

- **Highest measured throughput for this tier: vLLM MTP3 C24 at 662 tok/s, 56.28% acceptance, about 27.6 tok/s/request.**
- SGLang MTP3 C24: 654 tok/s at 55.17% acceptance.
- The release bundles and recommends native MTP3 only; the structured evaluation file preserves the complete historical research record.

| Framework / mode | C | Aggregate tok/s | Per-request tok/s | Acceptance | TTFT P50 | Latency P50 | Peak GPU | Errors |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| vLLM bare | C1 | 32 | 31.9 | — | 0.16s | 8.03s | 85.8 GiB | 0 |
| vLLM bare | C4 | 113 | 28.2 | — | 0.56s | 9.04s | 86.1 GiB | 0 |
| vLLM bare | C8 | 213 | 26.6 | — | 1.01s | 9.55s | 86.1 GiB | 0 |
| vLLM bare | C16 | 363 | 22.7 | — | 1.59s | 11.15s | 86.1 GiB | 0 |
| vLLM bare | C20 | 423 | 21.2 | — | 1.87s | 11.95s | 86.1 GiB | 0 |
| vLLM bare | C24 | 476 | 19.8 | — | 2.16s | 12.71s | 86.1 GiB | 0 |
| vLLM MTP3 | C1 | 56 | 55.9 | 47.48% | 0.18s | 4.58s | 85.8 GiB | 0 |
| vLLM MTP3 | C4 | 202 | 50.4 | 54.87% | 0.56s | 4.62s | 86.0 GiB | 0 |
| vLLM MTP3 | C8 | 356 | 44.5 | 57.08% | 1.09s | 5.27s | 86.0 GiB | 0 |
| vLLM MTP3 | C16 | 544 | 34.0 | 57.31% | 1.70s | 6.88s | 86.0 GiB | 0 |
| vLLM MTP3 | C20 | 619 | 31.0 | 56.30% | 2.00s | 7.77s | 86.0 GiB | 0 |
| vLLM MTP3 | C24 | 662 | 27.6 | 56.28% | 2.31s | 8.63s | 86.0 GiB | 0 |
| SGLang bare | C1 | 45 | 45.2 | — | 0.14s | 5.67s | 87.9 GiB | 0 |
| SGLang bare | C4 | 158 | 39.4 | — | 0.43s | 6.49s | 88.1 GiB | 0 |
| SGLang bare | C8 | 287 | 35.9 | — | 0.69s | 7.13s | 88.1 GiB | 0 |
| SGLang bare | C16 | 469 | 29.3 | — | 1.22s | 8.73s | 88.1 GiB | 0 |
| SGLang bare | C20 | 537 | 26.8 | — | 1.48s | 9.53s | 88.1 GiB | 0 |
| SGLang bare | C24 | 597 | 24.9 | — | 1.74s | 10.29s | 88.1 GiB | 0 |
| SGLang MTP3 | C1 | 86 | 86.1 | 67.86% | 0.15s | 2.97s | 86.5 GiB | 0 |
| SGLang MTP3 | C4 | 234 | 58.5 | 54.03% | 0.43s | 3.83s | 86.7 GiB | 0 |
| SGLang MTP3 | C8 | 379 | 47.4 | 51.95% | 0.72s | 4.96s | 86.7 GiB | 0 |
| SGLang MTP3 | C16 | 578 | 36.1 | 55.06% | 1.25s | 6.56s | 86.7 GiB | 0 |
| SGLang MTP3 | C20 | 612 | 30.6 | 54.42% | 1.52s | 8.06s | 86.7 GiB | 0 |
| SGLang MTP3 | C24 | 654 | 27.3 | 55.17% | 1.79s | 8.90s | 86.7 GiB | 0 |

### Verified launch paths

```bash
cd NVFP4/INT8-W8A8-QAT
bash scripts/serve-vllm-mtp3.sh
```

| Script | Purpose |
|---|---|
| `scripts/serve-vllm-bare.sh` | vLLM bare |
| `scripts/serve-vllm-mtp3.sh` | vLLM native MTP3; recommended throughput path |
| `scripts/serve-sglang-bare.sh` | SGLang bare |
| `scripts/serve-sglang-mtp3.sh` | SGLang native MTP3 |

All four bundled paths passed text, image, and real-video smoke on the same model hash. SGLang `compressed-tensors` INT8 on Blackwell SM120/121 uses the bundled `runtime/sglang-sm120-int8-compat/` compatibility layer.

<!-- INT8_W8A8_QAT_V2_EN_END -->

<!-- NVFP4_MAIN_V1_EN_START -->
## NVFP4 + official BF16 MTP

![NVFP4 C24 capability, reasoning cost, and MTP performance](assets/nvfp4-four-variant-fullsuite-v10-restored-en.png)

**Standalone NVFP4 repository: [nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-MTP-NVFP4](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-MTP-NVFP4)**

The main repository contains complete artifacts under `NVFP4/W4A4/`, `NVFP4/W4A4+W8A8/`, `NVFP4/W4A16/`, and `NVFP4/W8A16/`. The core packages retain the official native BF16 MTP; each variant also includes an optional true static FP8 DFlash2 draft under `DFlash2-FP8/`. Fast/Mixed use C24 while W4A16 uses C16; the figure presents each frozen result and is not an official-base-versus-post-training comparison.

### Formal C24 capability and reasoning cost

Protocol: one RTX PRO 6000 96GB, SGLang + official BF16 MTP, C24, xhigh, a 32,768-token output cap, and a 1,800-second timeout. All 12 / 11 GPQA timeouts remain failures in the 198-question denominator; GPQA reasoning statistics cover only the 186 / 187 returned requests. MMLU and LCB reasoning statistics cover 500 / 100 questions.

| Metric | W4A4 Fast | W4A4 + W8A8 Mixed | Change |
| --- | ---: | ---: | ---: |
| GPQA | 158/198 (79.80%) | 168/198 (84.85%) | +10 correct / +5.05pp |
| GPQA mean reasoning | 9,123 | 8,400 | -7.9% |
| GPQA P50 / P90 | 4,928.5 / 24,893.0 | 4,278.0 / 24,402.6 | — |
| MMLU | 447/500 (89.40%) | 458/500 (91.60%) | +11 / +2.20pp |
| MMLU mean reasoning | 963 | 848 | -11.9% |
| MMLU P50 / P90 | 225.0 / 2,285.5 | 216.5 / 1,668.9 | — |
| LCB | 74/100 (74.00%) | 75/100 (75.00%) | +1 correct / +1.00pp |
| LCB mean reasoning | 14,602 | 13,647 | -6.5% |
| LCB P50 / P90 | 9,626.5 / 32,769.0 | 7,441.5 / 32,769.0 | — |

Mixed precision scores higher on GPQA, MMLU, and LCB and uses fewer mean reasoning tokens in all three suites. This is a comparison between quantized variants, not an official-base-versus-post-training gain.

<!-- W4A16_FINAL_V1_EN_START -->
### W4A16 formal C16 full-suite results

Protocol: 1× RTX PRO 6000 96GB, SGLang + official BF16 MTP, C16, xhigh, a 32,768-token output cap, and a 1,800-second request timeout. This is not a controlled equal-concurrency comparison against the C24 W4A4 runs.

| Suite | Final score | Mean reasoning | P50 / P90 | >8K / >16K | 32K trunc. | Other anomalies |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| GPQA | **161/198 (81.31%)** | 11,404 | 6,795.5 / 32,767 | 92 / 57 | 27 | 29 empty final-channel outputs; 27 unparseable responses; 0 request errors |
| MMLU | **457/500 (91.40%)** | 802 | 225 / 1,554 | 9 / 1 | 0 | 0 request errors; 0 empty finals |
| LCB | **74/100 (74.00%)** | 14,511 | 8,513.5 / 32,769 | 51 / 42 | 26 | 0 request errors/timeouts; 26 empty-code cases |

<!-- W4A16_GPQA_BOUNDARY_V1_EN_START -->
> **GPQA scoring:** Final **161/198 (81.31%)** across all 198 questions, with 0 request errors and 0 timeouts. Parsing accepts only a non-empty final channel or a complete explicit `Final Answer: A/B/C/D` on the last non-empty reasoning line.
<!-- W4A16_GPQA_BOUNDARY_V1_EN_END -->

LCB difficulty: Easy **23/23 (100%)**, Medium **29/31 (93.55%)**, Hard **22/46 (47.83%)**. All 26 length-limited outputs and all 26 empty-code cases remain failures in the 100-question denominator.

All three NVFP4 MMLU results use the same offline `final-content-strict-single-letter-v2` rescore: Fast **447/500 (89.40%)**, Mixed Precision **458/500 (91.60%)**, and W4A16 **457/500 (91.40%)**; generation outputs are unchanged. The retired 430/449/439 scores are not used.

#### W4A16 MTP short-output concurrency

The fixed short-output grid tested only C1/C4/C8/C16/C24; C2 and C32 were not tested. Aggregate throughput is rounded to whole tokens/s.

| Concurrency | Aggregate tok/s | MTP acceptance | Accepted draft / verification | Committed output / verification |
| ---: | ---: | ---: | ---: | ---: |
| C1 | 127 | 72.84% | 2.185 | 3.160 |
| C4 | 452 | 70.20% | 2.106 | 3.103 |
| C8 | 764 | 71.04% | 2.131 | 3.127 |
| **C16 (balanced)** | **1,216** | **74.28%** | **2.229** | **3.228** |
| **C24 (max throughput)** | **1,304** | **70.60%** | **2.118** | **3.114** |

All five cells had 0 request errors, 0 timeouts, and 0 empty outputs. Punctuation-collapse manual review was not part of this short sweep, so no zero claim is made for that field. C16 provides the highest acceptance while retaining 1,216 tok/s; C24 is the highest measured aggregate-throughput point.
<!-- W4A16_FINAL_V1_EN_END -->

The tested W4A16 SGLang settings are `--quantization modelopt_mixed`, EAGLE, steps=3, top-k=1, draft tokens=4, BF16 dtype/KV, and a 65,536-token context. The four-mode vLLM smoke still covers only Fast and Mixed Precision.

<!-- W8A16_RELEASE_V1_EN_START -->
### W8A16 quality-oriented FP8 package

The complete **W8A16** package is available at `NVFP4/W8A16/`: **24 files / 38,477,562,434 bytes**, including the manifests. Download the entire directory and do not mix it with `W4A4/`, `W4A4+W8A8/`, or `W4A16/`.

> **Format note:** W8A16 uses block-wise **FP8 E4M3 weights with BF16 activations and KV cache**. It is grouped in this repository family for distribution, but it is **not NVFP4 encoding**.

- 64-layer text trunk; 1,391 tensors in the complete package.
- 192 MLP linear weights use FP8 E4M3 with 128×128 blocks; 305 other text linear weights remain BF16.
- `vision-mtp-bf16.safetensors` is a 1,770,897,648-byte shared component containing the official 333 BF16 vision tensors and 15 BF16 MTP tensors. It is not a standalone main model.
- The official MTP component was restored from Qwen revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`; it was not trained during this SFT/SimPO run.

<!-- W8A16_FINAL_CAPABILITY_V1_EN_START -->
#### W8A16 formal capability results

Protocol: one RTX PRO 6000 96GB, SGLang + official BF16 MTP, xhigh, 32,768-token output limit, and a 1,800-second request timeout. GPQA and LCB used C16; MMLU is the adopted clean C24 result.

| Suite | Final score | Concurrency | Request errors / timeouts |
| --- | ---: | ---: | ---: |
| GPQA | **159/198 (80.30%)** | C16 | 0 / 0 |
| MMLU | **450/500 (90.00%)** | C24 | 0 / 0 |
| LCB | **78/100 (78.00%)** | C16 | 0 / 0 |

For LCB, all 100 problems remain in the denominator: 22 length stops and the corresponding 22 empty-code submissions count as failures. The run recorded 0 request errors, 0 HTTP timeouts, 0 code-execution timeouts, and 0 syntax errors.
<!-- W8A16_FINAL_CAPABILITY_V1_EN_END -->

#### W8A16 MTP short-output concurrency

Measured on one RTX PRO 6000 96GB with SGLang + official MTP, xhigh, and one 256-token wave per cell. All **53/53 requests completed with 0 request errors**.

| Concurrency | Aggregate tok/s | MTP acceptance | Accepted draft / verification | Mean TTFT |
| ---: | ---: | ---: | ---: | ---: |
| C1 | 87 | 72.9% | 2.19 | 0.063 s |
| **C4 (highest acceptance)** | **326** | **75.8%** | **2.27** | **0.143 s** |
| C8 | 562 | 75.7% | 2.27 | 0.170 s |
| C16 | 955 | 74.7% | 2.24 | 0.283 s |
| **C24 (max throughput)** | **1,056** | **73.2%** | **2.20** | **0.257 s** |

This is a single-wave fixed-length sweep, not per-user speed or sustained 32K throughput. Spark SGLang/vLLM bare+MTP text/image/video smoke and PRO SGLang bare+MTP capability smoke also passed; these are short runtime compatibility checks, not formal general-quality scores. The adopted final GPQA/MMLU/LCB scores are listed above; no partial score is reported here.

#### Tested SGLang path

```bash
SGLANG_FORCE_FP8_MARLIN=1 python -m sglang.launch_server \
  --model-path ./NVFP4/W8A16 \
  --quantization modelopt_mixed \
  --dtype bfloat16 --kv-cache-dtype bfloat16 \
  --enable-linear-replayssm-spec \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4
```

The published metadata view above is the SGLang-tested path. vLLM bare+MTP smoke was validated only through a separate generic-FP8 metadata view of the same unchanged weights, with forced FP8 Marlin; that auxiliary view is not part of this download, so SGLang is the recommended published path.
<!-- W8A16_RELEASE_V1_EN_END -->

### MTP short-output throughput and acceptance

Fixed 256-token outputs, one wave per cell, 53 requests per variant. Aggregate throughput is not per-user speed or sustained 32K throughput. C16 is only a completed short-output speed cell, not a C16 capability score.

| Concurrency | Fast tok/s / acceptance | Mixed tok/s / acceptance |
| ---: | ---: | ---: |
| C1 | 82 / 75.64% | 102 / 72.92% |
| C4 | 318 / 76.56% | 374 / 73.08% |
| C8 | 688 / 74.49% | 665 / 72.21% |
| C16 | 1,196 / 74.25% | 1,176 / 72.71% |
| C24 | **1,684 / 73.17%** | **1,595 / 73.42%** |

C24 is the highest tested aggregate-throughput tier for this short-output sweep. Long-reasoning C24 runs recorded timeouts, so it is not presented as a validated 32K optimum. Acceptance is accepted draft tokens / proposed draft tokens.

### Download and measured SGLang settings

| Main-repository directory | Format | Complete size | Main weight |
| --- | --- | ---: | --- |
| `NVFP4/W4A4/` | W4A4 NVFP4 with retained BF16 head/control components | 20.62 GB | `model-nvfp4-fast.safetensors` |
| `NVFP4/W4A4+W8A8/` | W4A4 NVFP4 + W8A8 FP8 with retained BF16 head/control components | 25.80 GB | `model-nvfp4-mixed.safetensors` |
| `NVFP4/W4A16/` | W4A16 ModelOpt NVFP4; BF16 activation/KV and official BF16 vision/MTP | 20.62 GB | `text-01`…`text-05.safetensors` |

Download all 15 files in the selected directory, including `vision-mtp-bf16.safetensors`, configs, index, tokenizer/processors, `manifest.json`, and `SHA256SUMS`; do not mix variants. Measured SGLang native-MTP settings: Fast uses `--quantization modelopt_fp4`, Mixed uses `--quantization modelopt_mixed`; both use `EAGLE`, steps=3, top-k=1, draft tokens=4, BF16 KV, and 65,536 context. The frozen SGLang environment used source `17313cf4b25d` with runtime adaptations.

<!-- VLLM028_RUNTIME_V1_EN_START -->
### vLLM 0.28.0 · tested on DGX Spark

Fast and mixed precision both completed real bare and native-MTP load, health, and text/image/video generation checks. The environment was DGX Spark GB10 (SM121) with the official Linux/ARM64 vLLM 0.28.0 image. Fast used `modelopt_fp4`; mixed precision used `modelopt_mixed`. Both selected `FlashInferCutlassNvFp4LinearKernel` for NVFP4, while mixed FP8 layers selected `FlashInferFP8ScaledMMLinearKernel`; neither fell back to Marlin.

| Variant | Decode | Load memory | Load time | 6-case content check | Image / video | MTP accepted / drafted tokens |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| Fast | bare | 18.77 GiB | 145.10 s | 5/6 | pass / pass | — |
| Fast | MTP | 19.56 GiB | 198.43 s | 5/6 | pass / pass | 101/168 (60.1%) |
| Mixed precision | bare | 23.52 GiB | 143.88 s | 5/6 | pass / pass | — |
| **Mixed precision** | **MTP** | **24.31 GiB** | **211.90 s** | **6/6** | **pass / pass** | **112/168 (66.7%)** |

All six requests in every mode returned HTTP 200 with non-empty output and no repetitive-punctuation collapse. One short code check returned 55 instead of the expected 30 in fast bare/MTP and mixed bare, so those modes are reported as 5/6; mixed-precision MTP was 6/6. This was a short serial non-thinking smoke, **not** a vLLM TPS benchmark, general quality proof, 64K long-context test, or concurrency stress test. The 65,536 context and `max-num-seqs=4` values were startup settings.

The recommended vLLM starting point is **mixed precision + native MTP**:

```bash
VARIANT=quality MODE=mtp PORT=19120 bash NVFP4/runtime/START_VLLM028_NVFP4.sh
```

The launcher binds only to `127.0.0.1`, pins `method=mtp` and `num_speculative_tokens=3`, and refuses to pull an image or overwrite an existing container. Preload the image first; the script verifies the pinned official immutable manifest and local image ID. Model, quantization, and MTP arguments match the smoke above. The loopback host-network mapping is a deployment adapter for host access, not a new performance run.

Official references: [vLLM ModelOpt quantization](https://docs.vllm.ai/en/latest/features/quantization/modelopt/), [vLLM MTP](https://docs.vllm.ai/en/latest/features/speculative_decoding/mtp/), and [Docker host networking](https://docs.docker.com/engine/network/drivers/host/).
<!-- VLLM028_RUNTIME_V1_EN_END -->
<!-- NVFP4_MAIN_V1_EN_END -->

> **Refusal evaluation: 4 / 140 (2.9%) across 10 categories and 140 prompts.**
>
> ***Research disclaimer: This experimental release is provided solely to study the technical feasibility and behavioral effects of refusal-tendency dissolution. It is not a comprehensive safety conclusion, an endorsement of unrestricted use, or professional advice. Users are responsible for lawful and appropriate use and for independently verifying model outputs.***

<!-- AWQ_W4A16_V1_EN_START -->
## AWQ-W4A16 | native MTP with vLLM

![AWQ-W4A16 capability, reasoning, and concurrency](assets/awq-w4a16-v1-en.png)

Complete directory: `NVFP4/AWQ-W4A16/`; the main weight is `Qwen3.8-27B-EfficientThink-SimPO-AWQ-W4A16.safetensors`. Download the entire directory; do not mix it with W4A4, W4A4+W8A8, the earlier W4A16 package, or W8A16.

> **Format identity:** this is a `compressed-tensors`, pack-quantized **AWQ W4A16** build. 367 target weights use asymmetric group-128 INT4, 33 target weights use symmetric group-128 INT8, and critical, vision, MTP, and other retained tensors remain BF16; activations and KV cache are BF16. It is **not NVFP4 encoding, GPTQ, or imatrix**. `hf_quant_config.json` is retained as upstream ModelOpt provenance; runtime loading follows `config.json`, where `quant_method=compressed-tensors` is authoritative.

`vision-mtp-bf16.safetensors` combines **333 official BF16 vision tensors and 15 official BF16 MTP tensors**. It is the vision/MTP component for this model, not a DFlash2 draft.

### Formal capability and reasoning results

Protocol: one RTX PRO 6000 96GB, vLLM + native MTP, C24, xhigh, a 32,768-token output cap, and a 1,800-second request timeout. Every anomalous sample remains in the denominator; anomaly categories may overlap.

| Suite | Final score | Mean reasoning | P50 / P90 | >8K / >16K | 32K trunc. | Request errors / HTTP timeouts |
|---|---:|---:|---:|---:|---:|---:|
| GPQA | **159/198 (80.30%)** | 11,142 | 6,283 / 32,768 | 87/198 (43.94%) / 56/198 (28.28%) | 28/198 (14.14%) | 0/198 / 0/198 |
| MMLU | **453/500 (90.60%)** | 935 | 218 / 1,674.4 | 12/500 (2.40%) / 4/500 (0.80%) | 0/500 | 0/500 / 0/500 |
| LCB | **74/100 (74.00%)** | 13,922 | 8,207.5 / 32,768 | 50/100 (50.00%) / 42/100 (42.00%) | 23/100 (23.00%) | 0/100 / 0/100 |

GPQA has **28/198 (14.14%)** empty-final, no-submission, and unparseable cases. MMLU has **0/500** empty, no-submission, and unparseable cases. For LCB, **22/100 (22.00%)** no-code/no-submission cases, **23/100 (23.00%)** unparseable outputs, and **1/100 (1.00%)** syntax error remain failures; code-execution timeouts were **0/100**. This vLLM C24 run is not a controlled quantization-loss comparison against the earlier SGLang W4A16, NVFP4, or other decoder results.

### vLLM MTP short-output concurrency

The fixed workload used 1,024 input + 256 output tokens, three trials per cell, and `num_speculative_tokens=3`; all request-error counts were 0. TPS is rounded to whole tokens/s.

| Concurrency | Aggregate tok/s | MTP acceptance |
|---:|---:|---:|
| C1 | 39 | 56.03% |
| C4 | 128 | 51.82% |
| C8 | 226 | 52.19% |
| C16 | 366 | 49.05% |
| **C24 (highest measured throughput)** | **480** | **53.46%** |

### Verified launch path

```bash
python -m vllm.entrypoints.openai.api_server \
  --model ./NVFP4/AWQ-W4A16 \
  --served-model-name qwen38-27b-awq-w4a16 \
  --host 127.0.0.1 --port 19540 \
  --dtype bfloat16 \
  --quantization compressed-tensors \
  --kv-cache-dtype auto \
  --gpu-memory-utilization 0.95 \
  --max-model-len 65536 \
  --max-num-seqs 24 \
  --max-num-batched-tokens 2048 \
  --reasoning-parser qwen3 \
  --attention-backend TRITON_ATTN \
  --limit-mm-per-prompt '{"image":2,"video":1}' \
  --skip-mm-profiling \
  --no-enable-prefix-caching \
  --enforce-eager \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

vLLM 0.28.0 with compressed-tensors 0.17.0 and Transformers 5.15.1 passed bare/MTP text, Chinese, code, explanation, image, and real-MP4 smoke, including native MTP accepted/proposed counters. SGLang 0.5.19 with compressed-tensors 0.18.0, Transformers 5.12.1, FlashInfer 0.6.18, and Decord 0.6.0 also passed 6/6 in bare and MTP modes, but only inside an isolated overlay with a local CUDA `libcudart` link repair and an explicit Decord video-backend patch; this **must not be read as stock-pip, drop-in compatibility**. That SGLang run was a short smoke and provides no SGLang long-output quality or TPS claim. Reproducibility files are under `NVFP4/AWQ-W4A16/runtime/`.
<!-- AWQ_W4A16_V1_EN_END -->

## Static FP8 + DFlash2 measured serving results

| Concurrency | Completion tok/s | DFlash acceptance | Mean accepted / 8 |
|---:|---:|---:|---:|
| C1 | 36 | **70.0%** | **5.91** |
| C2 | 61 | 65.5% | 5.57 |
| C4 | 104 | 68.33% | 5.78 |
| C8 | 165 | **70.0%** | 5.89 |
| C16 | 243 | 66.0% | 5.59 |
| C24 | **281** | 67.0% | 5.70 |

Measured on DGX Spark with the published static Block128 FP8 main model, SGLang + DFlash2, XH, `draft_tokens=8`, and `max_tokens=256`. All six tiers completed without request errors. C24 maximizes aggregate throughput; C1 is the lowest-concurrency/highest-accepted-length tier; **C8 is the recommended practical balance**. `finish_reason=length` is expected in this fixed-length pressure test and is not a quality judgment.

A separate C3, `max_tokens=1024` science/code/general smoke passed 3/3, returned 3/3 `stop`, had no empty output or mojibake, and delivered 68 tok/s aggregate.

Tested launcher (pass downloaded paths explicitly):

```bash
bash FP8/runtime/BUILD_RUNTIME_SPARK.sh
CONCURRENCY=24 bash FP8/runtime/TESTED_STARTUP_C24_DFLASH2.sh \
  "$PWD/FP8" "$PWD/FP8/DFlash2-FP8" efficientthink-fp8-dflash2 19110
```

**EfficientThink targets unproductive reasoning tails—not reasoning itself.** It is trained to preserve capability and genuinely necessary long reasoning while improving terminal-answer reliability.

This repository contains the final merged **SimPO BF16** model under `BF16/` and a text-only static Block128 **FP8 main model** under `FP8/`. For one-directory downloads, both model directories include the same verified optional DFlash2 draft under their own `DFlash2-FP8/` subdirectory; the draft does not replace the main model.

## Artifacts

| Directory | Role | Verified source size |
|---|---|---:|
| `BF16/` | Final merged SimPO BF16 main model + bundled `DFlash2-FP8/` | 57,143,670,823 bytes |
| `FP8/` | Text-only static Block128 FP8 main model + tested launcher + bundled `DFlash2-FP8/` | 31,908,365,464 bytes |

Download either `BF16/` or `FP8/` to receive the corresponding main model and its DFlash2 runtime files together. `FP8/manifest.json` and `FP8/SHA256SUMS` define the static-FP8 main package. The FP8 main model is language-only: 64 layers, 1,251 tensors after SGLang key repack, zero visual tensors, and zero MTP tensors.

## Final SimPO evaluation

Frozen XH protocol, `max_tokens=32768`; every non-passing sample remains in the denominator.

| Suite | Final score |
|---|---:|
| GPQA Diamond | **171 / 198 (86.36%)** |
| MMLU | **442 / 500 (88.40%)** |
| LiveCodeBench | **74 / 100** |

LiveCodeBench breakdown: easy `23/23`, medium `27/31`, hard `24/46`. The 74/100 score is the final all-failures-counted operational result; it is not labeled as a clean run.

## Same-protocol capability and reasoning comparison

Protocol: dynamic FP8 + DFlash2, 2× GPU C24, XH, `max_tokens=32768`; official full-suite results. All failures remain in the denominator.

### GPQA Diamond · 198 questions

| Metric | Official Qwen3.8-27B | Final SimPO | Change |
|---|---:|---:|---:|
| Accuracy | 164/198 (82.83%) | **171/198 (86.36%)** | **+7 / +3.54pp** |
| Mean reasoning | 10,234 | 9,556 | −678 (−6.6%) |
| P50 / P90 | 5,182 / 32,768 | 4,788.5 / 32,765.3 | −393.5 / nearly flat |
| >8K / >16K | 78 / 51 | 73 / 44 | −5 / −7 |
| 32K truncations | 26 | 21 | −5 (−19.2%) |
| Unparseable | 22 | 18 | −4 |
| Loose LOOP candidates | 12 | 6 | −6 |

GPQA improves by 3.54pp while mean reasoning, truncation, unparseable outputs, and loose loop candidates fall.

### MMLU · 500 questions

| Metric | Official Qwen3.8-27B | Final SimPO | Change |
|---|---:|---:|---:|
| Accuracy | **451/500 (90.20%)** | 442/500 (88.40%) | **−9 / −1.80pp** |
| Mean reasoning | 1,113.91 | 1,009.76 | −104.15 (−9.4%) |
| P50 / P90 | 213.5 / 1,942.7 | 211.5 / 1,884.2 | −2 / −58.5 |
| >8K / >16K | 18 / 7 | 14 / 6 | −4 / −1 |
| 32K truncations | 4 | 1 | −3 (−75%) |

MMLU reasoning cost and long-tail incidence fall, but accuracy also drops by 1.80pp. This is reported as a real capability trade-off, not hidden behind the efficiency gain.

### LiveCodeBench · 100 questions

Reasoning statistics below cover all 100 cases; timeout/error rows contribute zero reasoning tokens.

| Metric | Official Qwen3.8-27B | Final SimPO | Change |
|---|---:|---:|---:|
| Score | 69/100 (69%) | **74/100 (74%)** | **+5 / +5pp** |
| Easy | 23/23 | 23/23 | flat |
| Medium | 26/31 (83.87%) | 27/31 (87.10%) | +1 / +3.23pp |
| Hard | 20/46 (43.48%) | **24/46 (52.17%)** | **+4 / +8.69pp** |
| Mean reasoning | 12,167 | 12,514 | +347 (+2.9%) |
| P50 / P90 | 5,442.5 / 32,772 | 6,480.5 / 32,770.1 | +1,038 / nearly flat |
| >8K / >16K | 44 / 34 | 47 / 34 | +3 / flat |
| 32K truncations | 21 | 21 | flat |
| Timeout/request errors | 6 | 2 | −4 (−66.7%) |
| Empty code | 27 | 23 | −4 (−14.8%) |
| Normal stop | 73 | 77 | +4 |
| Runtime error | 1 | 0 | −1 |
| Total elapsed | 2,060s | 2,067s | nearly flat |

LCB gains are concentrated in hard problems and submission reliability. The run does not show an overall shortening of code reasoning: mean, P50, and >8K counts rise slightly, while >16K and 32K truncations remain unchanged. SimPO converts some former non-submissions into valid solutions without eliminating the 32K tail.

## Training

[`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) → capability-preserving SFT → terminal-behavior SimPO → per-tensor FP32 delta merge → BF16.

### SFT · 1,905 examples

- 1 epoch · 239 optimizer steps · effective batch 8
- LoRA r=16 · alpha=32 · dropout=0.05
- LR 5e-6 · 12 warmup steps · seed 20260901
- 2× NVIDIA RTX PRO 6000 Blackwell Server Edition

### SimPO · 110 preference pairs / 73 unique prompts

- 5 optimizer steps · beta=1.0 · gamma=0.2 · peak LR 5e-7
- LoRA r=16 · alpha=32 · dropout=0
- seed 20260903 · world size 2 · FSDP full sharding

## Recommended Transformers usage

<!-- BF16_RUNTIME_AUDIT_V1_EN_START -->
Requires a current Transformers release supporting `Qwen3_5ForConditionalGeneration` (the published BF16 config records 5.12.1) and Accelerate. The local BF16 wrapper is multimodal; this example generates text only and does not launch DFlash2. Do not substitute the text-only static FP8 directory. This is a configuration/official-API correction, not a new BF16 performance claim.
<!-- BF16_RUNTIME_AUDIT_V1_EN_END -->

```python
from pathlib import Path
from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration

# Run from the downloaded repository root; never pass the FP8 directory here.
model_dir = str(Path("BF16").resolve())
tok = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
model = Qwen3_5ForConditionalGeneration.from_pretrained(
    model_dir, dtype="auto", device_map="auto", local_files_only=True
)
messages = [{"role": "user", "content": "What is 17 + 25?"}]
prompt = tok.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True,
    enable_thinking=True, reasoning_effort="xhigh",
)
inputs = tok(prompt, return_tensors="pt").to(model.device)
output = model.generate(
    **inputs, max_new_tokens=4096, do_sample=True,
    temperature=1.0, top_p=0.95, top_k=20,
)
print(tok.decode(output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True))
```

The bundled generation defaults are `temperature=1.0`, `top_p=0.95`, and `top_k=20`. Set `enable_thinking=False` for non-thinking mode. The frozen capability and serving results reported here use `reasoning_effort="xhigh"`.

<!-- DFLASH_RATIONALE_MTP_V1_EN_START -->
### Why we choose DFlash2

**We choose DFlash2 for its strong measured draft acceptance and high output throughput.** DFlash proposes a block of tokens in parallel; retaining more of that block per target-model verification can reduce sequential decoding overhead and improve TPS. [Method reference: DFlash authors](https://z-lab.ai/projects/dflash/).

On the measured **DGX Spark static FP8** configuration, draft acceptance was **65.5–70.0%** across C1–C24. C8 delivered **165 aggregate tok/s at 70.0% acceptance**, while C24 reached **281 aggregate tok/s at 67.0%**. We recommend C8 for practical balance and C24 for maximum measured throughput. These are DFlash2 measurements, not a matched speedup comparison against MTP; GGUF results use their own measured configuration in the linked GGUF repository.
<!-- DFLASH_RATIONALE_MTP_V1_EN_END -->

## DFlash2 scope and limits

<!-- DFLASH_STATIC_FP8_V1_EN_START -->
### True static FP8 DFlash2 draft

The bundled DFlash2 draft is now a **pre-quantized static FP8** `compressed-tensors` checkpoint, not a BF16 checkpoint carrying an FP8 directory label. `model.safetensors` is **2,407,027,720 bytes** (SHA256 `1f3636a32d866f8ebc7f422d63f9247126ebb6d2566d3e0da327d81dd8fa25d1`). Its audited tensor set contains 20 FP8 E4M3 weights with 20 FP32 scales and 61 retained BF16 tensors.

Load it explicitly with:

```text
--speculative-draft-model-quantization compressed-tensors
```

Matched DGX Spark checks used the same W4A4 target, 15 prompts, XH, 256 generated tokens, and 8 draft tokens. All 15 requests completed in every cell.

| Draft | Concurrency | Aggregate tok/s | DFlash acceptance | Mean accepted / 8 | Request errors |
|---|---:|---:|---:|---:|---:|
| BF16 reference | C1 | 29.75 | 38.77% | 3.72 | 0 |
| Static FP8 | C1 | 30.26 | 35.86% | 3.51 | 0 |
| BF16 reference | C4 | 68.50 | 32.71% | 3.29 | 0 |
| **Static FP8** | **C4** | **75.94** | **33.55%** | **3.35** | **0** |

C1 acceptance is the mean of same-run log snapshots; C4 acceptance is the post-run SGLang metrics gauge. The C4 static draft improved aggregate throughput by about **10.9%** over BF16 in this matched check. This short fixed-length test validates serving behavior; it does not replace the formal capability scores elsewhere in this card.
<!-- DFLASH_STATIC_FP8_V1_EN_END -->

- The same true static FP8 draft payload is bundled at `BF16/DFlash2-FP8/`, `FP8/DFlash2-FP8/`, and every `NVFP4/*/DFlash2-FP8/` variant, each with `model.safetensors`, `config.json`, `manifest.json`, and `SHA256SUMS`.
- The frozen evaluation configuration used DFLASH, one speculative step, top-k 1, eight draft tokens, block size 8, Triton draft attention, and an FP8 draft.
- Runtime support for this draft must be verified against the serving stack in use. The draft is not a standalone chat model.
- Scores are tied to the frozen XH harness and serving configuration and should not be compared across unrelated harnesses.
- Long reasoning can still be necessary; EfficientThink is not a universal short-answer mode.
- Verify outputs independently, especially in high-stakes contexts.

## Recommended deployment: SGLang

**Use SGLang for this release.** It is the runtime used for the frozen FP8+DFlash2 quality, acceptance, and concurrency measurements. For XH thinking mode, use Qwen's official sampling preset: `temperature=1.0`, `top_p=0.95`, `top_k=20`, `min_p=0.0`, `presence_penalty=0.0`, and `repetition_penalty=1.0`.

<!-- PORTABLE_RUNTIME_V1_EN_START -->
### Portable Spark runtime

This launcher targets **DGX Spark / Linux ARM64 / GB10**, with Docker, NVIDIA Container Toolkit, Python 3, and curl installed. It is not an x86/V100 FP8 launcher. Run from the downloaded repository root with the complete `FP8/` directory, including `FP8/runtime/` and `FP8/DFlash2-FP8/`.

`BUILD_RUNTIME_SPARK.sh` builds a local image from a **public SGLang base pinned by digest**, public SGLang source at `17313cf4b25d`, and a pinned public xgrammar wheel. The script verifies both small download hashes; it does not download model weights. Allow sufficient Docker disk space for the roughly 32 GB unpacked runtime and build layers. No private image registry or author-specific source directory is required. An existing download cache can be copied into `FP8/runtime/build-cache/` before building.

The launcher reports missing files and unavailable ports, refuses to overwrite an existing container, prints its log command, and requires both server readiness and an actual chat-generation probe before reporting READY. It disables the pinned version's special token-only health-generation probe. The default port is **19110**, bound to **127.0.0.1**. For intentional LAN access set `BIND_HOST=0.0.0.0` and secure the endpoint; no authentication is enabled by this script.

Keep the measured server limit at `CONCURRENCY=24`. Use **8 simultaneous client requests (C8)** for the practical balance, or **24 client requests (C24)** for maximum measured aggregate throughput. The server limit is not an automatic load generator: the client must send that many simultaneous requests. Inspect with `docker logs -f efficientthink-fp8-dflash2`; stop only this server with `docker stop efficientthink-fp8-dflash2`. After inspecting a stopped container, remove that exact container before reusing its name, or choose a new name.

Use explicit XH template settings in each request:
```bash
curl --fail-with-body http://127.0.0.1:19110/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"efficientthink-fp8-dflash2","messages":[{"role":"user","content":"What is 17 + 25?"}],"max_tokens":1024,"temperature":1.0,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0,"chat_template_kwargs":{"enable_thinking":true,"reasoning_effort":"xhigh"}}'
```

`chat_template_kwargs` is a request field for the template, not a server command-line flag. The 1,024-token example is a short connectivity check; the formal capability runs used 32,768. SGLang's DFlash verify block is 8; llama.cpp uses `--spec-draft-n-max 7` for this draft. These are different runtime conventions, not interchangeable flags.

Official references: [Qwen3.8 SGLang cookbook](https://docs.sglang.io/cookbook/autoregressive/Qwen/Qwen3.8-27B), [SGLang DFlash](https://docs.sglang.io/docs/advanced_features/speculative_decoding), [pinned SGLang source](https://github.com/sgl-project/sglang/tree/17313cf4b25d). This package preserves the measured runtime configuration; it does not substitute the latest official recipe and relabel old TPS as a new measurement.
<!-- PORTABLE_RUNTIME_V1_EN_END -->

### SGLang — verified FP8 + DFlash2 path

```bash
bash FP8/runtime/BUILD_RUNTIME_SPARK.sh
CONCURRENCY=24 bash FP8/runtime/TESTED_STARTUP_C24_DFLASH2.sh \
  "$PWD/FP8" "$PWD/FP8/DFlash2-FP8" efficientthink-fp8-dflash2 19110
```

Use C8 for the measured practical balance or C24 when maximum aggregate throughput is the priority. This is the repository's frozen, tested DFlash2 path.

### vLLM — official baseline reference only, not tested here

```bash
vllm serve "$PWD/FP8" \
  --served-model-name efficientthink-fp8 \
  --reasoning-parser qwen3 --max-model-len 40960 \
  --host 127.0.0.1 --port 19110
```

Pass `reasoning_effort="xhigh"` and the official thinking sampling preset in the OpenAI-compatible request. This command is included only as the official Qwen3.8 baseline serving shape. This repository has **not** tested vLLM for this checkpoint and does **not** recommend or claim a frozen vLLM+DFlash2 result.

References: [official Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B), [SGLang documentation](https://docs.sglang.ai/), and [vLLM documentation](https://docs.vllm.ai/).

---

---

## 中文说明

![EfficientThink 评测摘要](assets/efficientthink-capability-reasoning-v5-3-zh.png)

> **已审查的 Q2–Q8 测评中未发现严格死循环。**

**GGUF 量化仓：[nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2-GGUF](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2-GGUF)**

<!-- Q8_Q5_MAIN_MIRROR_V1_ZH_START -->
### GGUF 六档实测成绩

主仓与独立 GGUF 仓已经同步提供全部六档；以下均为正式全量冻结成绩，所有未通过样本保留在分母。主仓路径增加 `GGUF/` 前缀：

| 档位 | GPQA 198 | MMLU 500 | LCB 100 | 主仓目录 |
|---|---:|---:|---:|---|
| Q8_0 | 164/198（82.83%） | 447/500（89.40%） | 74/100（74.00%） | `GGUF/Q8_0/` |
| Q6_K | 171/198（86.36%） | 440/500（88.00%） | 78/100（78.00%） | `GGUF/Q6_K/` |
| Q5-LynnStyle | 164/198（82.83%） | 438/500（87.60%） | 75/100（75.00%） | `GGUF/Q5-LynnStyle/` |
| Q4-LynnStyle | 166/198（83.84%） | 443/500（88.60%） | 74/100（74.00%） | `GGUF/Q4-LynnStyle/` |
| Q3-LynnStyle | 172/198（86.87%） | 435/500（87.00%） | 78/100（78.00%） | `GGUF/Q3-LynnStyle/` |
| Q2-LynnStyle | 167/198（84.34%） | 416/500（83.20%） | 75/100（75.00%） | `GGUF/Q2-LynnStyle/` |

> **Q2-LynnStyle 使用 GSQ-RCO 混合精度量化，并采用 IQ 数值细化。** 此精确 12,999,977,600-byte 构建没有冻结 TPS。
>
> Q2 LCB 说明：75/100 最终视图保留原始 99 题，并对流式 JSON 异常题做了一次 Lynn 授权的精确补测；补测仍在 32K 结束且代码为空。

完整 DFlash2 并发表、文件角色和 llama.cpp 命令见上方独立 GGUF 仓链接。
<!-- Q8_Q5_MAIN_MIRROR_V1_ZH_END -->

<!-- LYNN_AGENT_V0870_ZH_START -->
## Lynn Agent v0.87.0

Lynn Agent v0.87.0 已采用本系列 **Q2-LynnStyle / Q3-LynnStyle + DFlash2**。该组合已在 DGX Spark 实测通过；Mac Apple Silicon/Intel 公证、Windows 安装包运行检查、两仓 CI、三仓 `main`/tag 一致性、23 个公网文件完整 SHA256 与远程 CLI 安装均已通过。

自然摇曳的枝叶投影与柔和窗光，默认开启；悬停顶部‘树影’查看关闭路径，点击直达设置。后台暂停，减少动态效果时静止。图片已并入文件筛选，斜杠模板取代常驻任务模式，翻译移入消息菜单，专家圆桌改为可选插件，并修复会话编辑目标与停止预处理。Kimi Datasource 继续保留在 MCP 中，用户需自行扫码登录自己的账号。

> 本轮客户端更新未改变本仓模型权重、量化文件、测评分数或性能指标。

| 安装包 | 国内镜像 | GitHub 备用 |
| --- | --- | --- |
| Mac Apple Silicon | [下载](https://download.merkyorlynn.com/downloads/Lynn-0.87.0-macOS-arm64.dmg) | [下载](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.0/Lynn-0.87.0-macOS-arm64.dmg) |
| Mac Intel | [下载](https://download.merkyorlynn.com/downloads/Lynn-0.87.0-macOS-x64.dmg) | [下载](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.0/Lynn-0.87.0-macOS-x64.dmg) |
| Windows | [下载](https://download.merkyorlynn.com/downloads/Lynn-0.87.0-Windows-Setup.exe) | [下载](https://github.com/MerkyorLynn/Lynn/releases/download/v0.87.0/Lynn-0.87.0-Windows-Setup.exe) |

发布记录：[GitHub 主仓](https://github.com/MerkyorLynn/Lynn/releases/tag/v0.87.0) · [GitHub 旧仓](https://github.com/LynnMerkyor/Lynn/releases/tag/v0.87.0) · [Gitee](https://gitee.com/merkyor/Lynn/releases/tag/v0.87.0) · [CLI 包](https://download.merkyorlynn.com/downloads/cli/lynn-cli-0.87.0.tgz)
<!-- LYNN_AGENT_V0870_ZH_END -->

<!-- GGUF_MTP_Q4_Q8_V1_ZH_START -->
### 随包提供 llama.cpp Q4_0 与 Q8_0 MTP draft

主仓 `GGUF/Q2-LynnStyle/` 至 `GGUF/Q8_0/` 的每个目录都镜像独立 GGUF 仓的两个可选 MTP sidecar：

| 每档文件 | 大小 | SHA256 |
|---|---:|---|
| `mtp-Qwen3.8-27B-Q4_0.gguf` | 1,680,271,648 bytes | `051a1764cff8c4f3ee6ae8b00593a0364c7539c67fa50ffc58f3f96509fca38e` |
| `mtp-Qwen3.8-27B-Q8_0.gguf` | 3,164,006,688 bytes | `cbf60a0c48b431bb61f1d49b8948dc88ac29c398d6dbdbbb2e6e89ef77eacc9a` |

两者均通过 GGUF 角色解析，并与 Q3-LynnStyle 在 DGX Spark 完成真实加载/生成。启动时使用 `--model-draft GGUF/<档位>/mtp-Qwen3.8-27B-Q4_0.gguf --spec-type draft-mtp`（或 Q8_0 文件）。MTP 与 DFlash2 二选一，不要在同一命令中同时启用。完整文件角色和 llama.cpp 示例见上方独立 GGUF 仓。
<!-- GGUF_MTP_Q4_Q8_V1_ZH_END -->

<!-- INT8_W8A8_QAT_V2_ZH_START -->

## 真 QAT INT8 W8A8｜动态 INT8 激活

![真 QAT INT8 W8A8｜动态 INT8 激活](assets/int8-w8a8-qat-quality-mtp-v2-zh.png)

**下载目录：`NVFP4/INT8-W8A8-QAT/`。** [同平台对应主仓/独立仓](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-MTP-NVFP4)。

### 文件与精度

| 组件 | 路径 | 精度 / 角色 | 大小 |
|---|---|---|---:|
| 主模型 | `NVFP4/INT8-W8A8-QAT/model-00001-of-00008.safetensors` … `model-00008-of-00008.safetensors` | 真 QAT INT8 W8A8；动态 INT8 激活 | 29.48 GB |
| 视觉 + 原生 MTP | `NVFP4/INT8-W8A8-QAT/vision-mtp-bf16.safetensors` | 333 个 BF16 视觉张量 + 15 个 BF16 MTP 张量，索引真实引用 348 项 | 1.77 GB |
| 完整清单 | `NVFP4/INT8-W8A8-QAT/manifest.json` 与 `NVFP4/INT8-W8A8-QAT/SHA256SUMS` | 当前目录 29 个文件的角色、bytes 与 SHA256 | — |
| 结构化评测 | [`NVFP4/INT8-W8A8-QAT/evaluation/formal-quality-and-performance.json`](NVFP4/INT8-W8A8-QAT/evaluation/formal-quality-and-performance.json) | 正式成绩、思考量与完整研究记录 | — |

### 训练与导出方法

- 64 层 Qwen3.8-27B 多模态架构，发布包索引共 1,599 个张量。
- 经过 3,200 个 QAT optimizer steps；400 个语言线性层均记录到非零梯度，并以 INT8 权重发布。
- 激活采用动态 INT8；247 条训练样本进入已接受训练集。
- BF16 scale 无损导出为 F32；视觉塔与原生 MTP 保持 BF16。

### 正式能力与思考量

协议：单张 RTX PRO 6000 Blackwell 96GB、vLLM 0.28.0 + 原生 MTP3、C20、BF16 KV、`reasoning_effort=xhigh`、32,768 输出上限、1,800 秒请求超时。正式长输出采用 C20，因为 C24 无法为整套长输出保留足够 KV 容量。

| 项目 | 得分 | 平均思考 | P50 / P90 | >8K / >16K | 32K 截断 | 空 final / 不可解析 |
|---|---:|---:|---:|---:|---:|---:|
| GPQA | **162/198（81.82%）** | 9,530 | 4,699.5 / 32,767 | 73 / 41 | 23 | 23 / 23 |
| MMLU | **451/500（90.20%）** | 837 | 203 / 1,906.1 | 9 / 3 | 0 | 0 / 0 |
| LCB | **73/100（73.00%）** | 13,921 | 8,347 / 32,768 | 50 / 41 | 23 | 23 / 23 |

请求 / HTTP / capture / grader 错误均为 **0**；LCB 代码超时与语法错误均为 **0**，另有 1 个 runtime error。LCB 采用 IPC-v4 对原始 100 份回答统一复判，没有发出新模型请求。

### 24 个随包运行路径的短输出性能单元

协议：1,024 输入 / 256 输出、预热后 3 轮。下表只代表短定长服务吞吐，不代表长思考速度；24 个裸跑/MTP3 单元均为 0 请求错误。

- **本档最高实测吞吐：vLLM MTP3 C24，662 tok/s，接受率 56.28%，约 27.6 tok/s/请求。**
- SGLang MTP3 C24：654 tok/s，接受率 55.17%。
- 发布包只附带并推荐原生 MTP3；完整历史研究数据保留在结构化评测文件中。

| 框架 / 模式 | 并发 | 聚合 tok/s | 每请求 tok/s | 接受率 | TTFT P50 | 延迟 P50 | 峰值显存 | 错误 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| vLLM 裸跑 | C1 | 32 | 31.9 | — | 0.16s | 8.03s | 85.8 GiB | 0 |
| vLLM 裸跑 | C4 | 113 | 28.2 | — | 0.56s | 9.04s | 86.1 GiB | 0 |
| vLLM 裸跑 | C8 | 213 | 26.6 | — | 1.01s | 9.55s | 86.1 GiB | 0 |
| vLLM 裸跑 | C16 | 363 | 22.7 | — | 1.59s | 11.15s | 86.1 GiB | 0 |
| vLLM 裸跑 | C20 | 423 | 21.2 | — | 1.87s | 11.95s | 86.1 GiB | 0 |
| vLLM 裸跑 | C24 | 476 | 19.8 | — | 2.16s | 12.71s | 86.1 GiB | 0 |
| vLLM MTP3 | C1 | 56 | 55.9 | 47.48% | 0.18s | 4.58s | 85.8 GiB | 0 |
| vLLM MTP3 | C4 | 202 | 50.4 | 54.87% | 0.56s | 4.62s | 86.0 GiB | 0 |
| vLLM MTP3 | C8 | 356 | 44.5 | 57.08% | 1.09s | 5.27s | 86.0 GiB | 0 |
| vLLM MTP3 | C16 | 544 | 34.0 | 57.31% | 1.70s | 6.88s | 86.0 GiB | 0 |
| vLLM MTP3 | C20 | 619 | 31.0 | 56.30% | 2.00s | 7.77s | 86.0 GiB | 0 |
| vLLM MTP3 | C24 | 662 | 27.6 | 56.28% | 2.31s | 8.63s | 86.0 GiB | 0 |
| SGLang 裸跑 | C1 | 45 | 45.2 | — | 0.14s | 5.67s | 87.9 GiB | 0 |
| SGLang 裸跑 | C4 | 158 | 39.4 | — | 0.43s | 6.49s | 88.1 GiB | 0 |
| SGLang 裸跑 | C8 | 287 | 35.9 | — | 0.69s | 7.13s | 88.1 GiB | 0 |
| SGLang 裸跑 | C16 | 469 | 29.3 | — | 1.22s | 8.73s | 88.1 GiB | 0 |
| SGLang 裸跑 | C20 | 537 | 26.8 | — | 1.48s | 9.53s | 88.1 GiB | 0 |
| SGLang 裸跑 | C24 | 597 | 24.9 | — | 1.74s | 10.29s | 88.1 GiB | 0 |
| SGLang MTP3 | C1 | 86 | 86.1 | 67.86% | 0.15s | 2.97s | 86.5 GiB | 0 |
| SGLang MTP3 | C4 | 234 | 58.5 | 54.03% | 0.43s | 3.83s | 86.7 GiB | 0 |
| SGLang MTP3 | C8 | 379 | 47.4 | 51.95% | 0.72s | 4.96s | 86.7 GiB | 0 |
| SGLang MTP3 | C16 | 578 | 36.1 | 55.06% | 1.25s | 6.56s | 86.7 GiB | 0 |
| SGLang MTP3 | C20 | 612 | 30.6 | 54.42% | 1.52s | 8.06s | 86.7 GiB | 0 |
| SGLang MTP3 | C24 | 654 | 27.3 | 55.17% | 1.79s | 8.90s | 86.7 GiB | 0 |

### 已验证启动方式

```bash
cd NVFP4/INT8-W8A8-QAT
bash scripts/serve-vllm-mtp3.sh
```

| 脚本 | 用途 |
|---|---|
| `scripts/serve-vllm-bare.sh` | vLLM 裸跑 |
| `scripts/serve-vllm-mtp3.sh` | vLLM 原生 MTP3；推荐吞吐路径 |
| `scripts/serve-sglang-bare.sh` | SGLang 裸跑 |
| `scripts/serve-sglang-mtp3.sh` | SGLang 原生 MTP3 |

四条随包路径均在同哈希模型上通过文本、图片与真实视频 smoke。Blackwell SM120/121 的 SGLang `compressed-tensors` INT8 路径使用随包 `runtime/sglang-sm120-int8-compat/` 兼容层。

<!-- INT8_W8A8_QAT_V2_ZH_END -->

<!-- NVFP4_MAIN_V1_ZH_START -->
## NVFP4 + 官方 BF16 MTP

![NVFP4 C24 能力、思考量与 MTP 性能](assets/nvfp4-four-variant-fullsuite-v10-restored-zh.png)

**独立 NVFP4 仓：[nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-MTP-NVFP4](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-MTP-NVFP4)**

主仓已在 `NVFP4/W4A4/`、`NVFP4/W4A4+W8A8/`、`NVFP4/W4A16/` 与 `NVFP4/W8A16/` 提供完整实体文件；核心包保留官方原生 BF16 MTP，各档另在 `DFlash2-FP8/` 提供可选的真静态 FP8 DFlash2 draft。Fast/Mixed 为 C24，W4A16 为 C16；图表并列展示各自冻结结果，不是原版与后训练版对比。

### C24 正式能力与思考量

协议：单张 RTX PRO 6000 96GB、SGLang + 官方 BF16 MTP、C24、xhigh、32,768 输出上限、1,800 秒超时。GPQA 的 12 / 11 个超时均按失败保留在 198 题分母；其思考统计只覆盖正常返回的 186 / 187 题。MMLU、LCB 思考统计分别覆盖 500 / 100 题。

| 指标 | W4A4 极速版 | W4A4 + W8A8 混合精度版 | 变化 |
| --- | ---: | ---: | ---: |
| GPQA | 158/198（79.80%） | 168/198（84.85%） | +10题 / +5.05pp |
| GPQA 平均思考量 | 9,123 | 8,400 | -7.9% |
| GPQA P50 / P90 | 4,928.5 / 24,893.0 | 4,278.0 / 24,402.6 | — |
| MMLU | 447/500（89.40%） | 458/500（91.60%） | +11题 / +2.20pp |
| MMLU 平均思考量 | 963 | 848 | -11.9% |
| MMLU P50 / P90 | 225.0 / 2,285.5 | 216.5 / 1,668.9 | — |
| LCB | 74/100（74.00%） | 75/100（75.00%） | +1题 / +1.00pp |
| LCB 平均思考量 | 14,602 | 13,647 | -6.5% |
| LCB P50 / P90 | 9,626.5 / 32,769.0 | 7,441.5 / 32,769.0 | — |

混合精度版在 GPQA、MMLU、LCB 得分均更高，三项平均思考 token 均下降。这是两种量化方案的对比，不能写成原版对后训练提升。

<!-- W4A16_FINAL_V1_ZH_START -->
### W4A16 正式 C16 全量结果

协议：单张 RTX PRO 6000 96GB、SGLang + 官方 BF16 MTP、C16、xhigh、32,768 输出上限、1,800 秒请求超时。此处与 W4A4 两版的 C24 不是严格等并发对照。

| 项目 | 最终得分 | 平均思考 | P50 / P90 | >8K / >16K | 32K 截断 | 其他异常 |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| GPQA | **161/198（81.31%）** | 11,404 | 6,795.5 / 32,767 | 92 / 57 | 27 | final 通道空 29；不可解析 27；请求错误 0 |
| MMLU | **457/500（91.40%）** | 802 | 225 / 1,554 | 9 / 1 | 0 | 请求错误 0；空 final 0 |
| LCB | **74/100（74.00%）** | 14,511 | 8,513.5 / 32,769 | 51 / 42 | 26 | 请求错误/超时 0；空代码 26 |

<!-- W4A16_GPQA_BOUNDARY_V1_ZH_START -->
> **GPQA 计分：**全部 198 题的最终成绩为 **161/198（81.31%）**，请求错误 0、超时 0。解析仅接受非空 final 通道，或 reasoning 最后一个非空行中的完整明确 `Final Answer: A/B/C/D`。
<!-- W4A16_GPQA_BOUNDARY_V1_ZH_END -->

LCB 难度：Easy **23/23（100%）**、Medium **29/31（93.55%）**、Hard **22/46（47.83%）**。26 个长度结束与 26 个空代码均按失败保留在 100 题分母。

三套 NVFP4 的 MMLU 均采用同一 `final-content-strict-single-letter-v2` 离线重算：极速版 **447/500（89.40%）**、混合精度版 **458/500（91.60%）**、W4A16 **457/500（91.40%）**；生成内容未改变。旧的 430/449/439 分数不再使用。

#### W4A16 MTP 短输出并发

固定短输出网格仅测试 C1/C4/C8/C16/C24；C2 与 C32 未测。聚合吞吐按模型卡规则取整。

| 并发 | 聚合 tok/s | MTP 接受率 | 接受草稿 / 验证轮 | 实际提交 / 验证轮 |
| ---: | ---: | ---: | ---: | ---: |
| C1 | 127 | 72.84% | 2.185 | 3.160 |
| C4 | 452 | 70.20% | 2.106 | 3.103 |
| C8 | 764 | 71.04% | 2.131 | 3.127 |
| **C16（平衡推荐）** | **1,216** | **74.28%** | **2.229** | **3.228** |
| **C24（最高吞吐）** | **1,304** | **70.60%** | **2.118** | **3.114** |

五档均为 0 请求错误、0 超时、0 空输出；本短扫未进行标点坍塌人工终审，因此不作对应零值声明。C16 在保持 1,216 tok/s 时接受率最高，作为平衡档；C24 是已测最大聚合吞吐。
<!-- W4A16_FINAL_V1_ZH_END -->

W4A16 的已测 SGLang 参数为 `--quantization modelopt_mixed`、EAGLE、steps=3、top-k=1、draft tokens=4、BF16 dtype/KV、65,536 context；vLLM 四路 smoke 仍只覆盖极速版与混合精度版。

<!-- W8A16_RELEASE_V1_ZH_START -->
### W8A16 质量优先 FP8 包

完整 **W8A16** 包已发布在 `NVFP4/W8A16/`：含清单共 **24 个文件 / 38,477,562,434 bytes**。请下载整个目录，不要与 `W4A4/`、`W4A4+W8A8/` 或 `W4A16/` 混用。

> **格式说明：** W8A16 使用分块 **FP8 E4M3 权重 + BF16 激活与 KV cache**。它为了统一分发放在本仓系列中，但编码格式**不是 NVFP4**。

- 64 层文字主干；完整包共 1,391 个张量。
- 192 个 MLP 线性权重使用 128×128 分块 FP8 E4M3；其余 305 个文字线性权重保留 BF16。
- `vision-mtp-bf16.safetensors` 为 1,770,897,648-byte 共用组件，包含官方 333 个 BF16 视觉张量与 15 个 BF16 MTP 张量；它不是可独立运行的主模型。
- 官方 MTP 来自 Qwen revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`，未参与本轮 SFT/SimPO 训练。

<!-- W8A16_FINAL_CAPABILITY_V1_ZH_START -->
#### W8A16 正式能力成绩

口径：单张 RTX PRO 6000 96GB、SGLang + 官方 BF16 MTP、xhigh、32,768 token 输出上限、1,800 秒请求超时。GPQA 与 LCB 使用 C16；MMLU 采用已冻结的 clean C24 结果。

| 项目 | 最终得分 | 并发 | 请求错误 / 超时 |
| --- | ---: | ---: | ---: |
| GPQA | **159/198（80.30%）** | C16 | 0 / 0 |
| MMLU | **450/500（90.00%）** | C24 | 0 / 0 |
| LCB | **78/100（78.00%）** | C16 | 0 / 0 |

LCB 保留全部 100 题作为分母：22 次长度结束及对应的 22 个空代码均按失败计入；请求错误、HTTP 超时、代码执行超时和语法错误均为 0。
<!-- W8A16_FINAL_CAPABILITY_V1_ZH_END -->

#### W8A16 MTP 短输出并发

实测环境：单张 RTX PRO 6000 96GB、SGLang + 官方 MTP、xhigh、每档单波 256-token 定长输出。**53/53 个请求全部完成，请求错误 0。**

| 并发 | 聚合 tok/s | MTP 接受率 | 接受草稿 / 验证轮 | 平均 TTFT |
| ---: | ---: | ---: | ---: | ---: |
| C1 | 87 | 72.9% | 2.19 | 0.063 秒 |
| **C4（接受率最高）** | **326** | **75.8%** | **2.27** | **0.143 秒** |
| C8 | 562 | 75.7% | 2.27 | 0.170 秒 |
| C16 | 955 | 74.7% | 2.24 | 0.283 秒 |
| **C24（最高吞吐）** | **1,056** | **73.2%** | **2.20** | **0.257 秒** |

这是单波定长短测，不是单用户速度，也不是 32K 持续吞吐。Spark 上的 SGLang/vLLM bare+MTP 文本/图片/视频 smoke，以及 PRO 上的 SGLang bare+MTP 能力 smoke 也已通过；它们只证明短请求运行兼容性，不是正式通用质量分数。已采用的 GPQA/MMLU/LCB 最终成绩见上方；本段不披露 partial 分数。

#### 已测 SGLang 路径

```bash
SGLANG_FORCE_FP8_MARLIN=1 python -m sglang.launch_server \
  --model-path ./NVFP4/W8A16 \
  --quantization modelopt_mixed \
  --dtype bfloat16 --kv-cache-dtype bfloat16 \
  --enable-linear-replayssm-spec \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4
```

以上已发布元数据是 SGLang 实测路径。vLLM bare+MTP smoke 仅通过同一权重的独立通用 FP8 元数据视图并强制 FP8 Marlin 完成；该辅助视图未随本目录发布，因此公开推荐路径仍为 SGLang。
<!-- W8A16_RELEASE_V1_ZH_END -->

### MTP 短输出吞吐与接受率

固定 256-token、每格单批、每版 53 个请求；聚合吞吐不是单用户速度，也不是 32K 持续吞吐。C16 仅是短输出测速，不是 C16 能力成绩。

| 并发 | 极速版 tok/s / 接受率 | 混合精度版 tok/s / 接受率 |
| ---: | ---: | ---: |
| C1 | 82 / 75.64% | 102 / 72.92% |
| C4 | 318 / 76.56% | 374 / 73.08% |
| C8 | 688 / 74.49% | 665 / 72.21% |
| C16 | 1,196 / 74.25% | 1,176 / 72.71% |
| C24 | **1,684 / 73.17%** | **1,595 / 73.42%** |

C24 是已测短输出最高聚合吞吐档；长推理在 C24 出现过超时，因此不把它宣称为 32K 最佳并发。接受率按接受草稿 token / 提议草稿 token 计算。

### 下载与已测 SGLang 参数

| 主仓目录 | 方案 | 完整包大小 | 主权重 |
| --- | --- | ---: | --- |
| `NVFP4/W4A4/` | W4A4 NVFP4，保留 BF16 头部/控制组件 | 20.62 GB | `model-nvfp4-fast.safetensors` |
| `NVFP4/W4A4+W8A8/` | W4A4 NVFP4 + W8A8 FP8，保留 BF16 头部/控制组件 | 25.80 GB | `model-nvfp4-mixed.safetensors` |
| `NVFP4/W4A16/` | W4A16 ModelOpt NVFP4；BF16 activation/KV，官方 BF16 视觉与 MTP | 20.62 GB | `text-01`…`text-05.safetensors` |

每个目录必须完整下载 15 个文件，包括 `vision-mtp-bf16.safetensors`、配置、索引、tokenizer/processor、`manifest.json` 与 `SHA256SUMS`；不要混用两版文件。已测 SGLang 原生 MTP 参数：极速版 `--quantization modelopt_fp4`，混合精度版 `--quantization modelopt_mixed`；两版均为 `EAGLE`、steps=3、top-k=1、draft tokens=4、BF16 KV、65,536 context。冻结的 SGLang 环境使用源码 `17313cf4b25d` 并带运行适配。

<!-- VLLM028_RUNTIME_V1_ZH_START -->
### vLLM 0.28.0 · DGX Spark 实测

极速版与混合精度版均完成 bare 与原生 MTP 四路真实加载、健康检查和文本/图片/视频生成。实测环境为 DGX Spark GB10（SM121）、官方 Linux/ARM64 vLLM 0.28.0 镜像；极速版使用 `modelopt_fp4`，混合精度版使用 `modelopt_mixed`。三版 NVFP4 均实际选择 `FlashInferCutlassNvFp4LinearKernel`，混合精度版的 FP8 层使用 `FlashInferFP8ScaledMMLinearKernel`，未回退到 Marlin。

| 版本 | 解码 | 加载显存 | 加载时间 | 6 项内容校验 | 图片 / 视频 | MTP 接受 token / 提议 token |
| --- | --- | ---: | ---: | ---: | --- | ---: |
| 极速版 | bare | 18.77 GiB | 145.10 秒 | 5/6 | 通过 / 通过 | — |
| 极速版 | MTP | 19.56 GiB | 198.43 秒 | 5/6 | 通过 / 通过 | 101/168（60.1%） |
| 混合精度版 | bare | 23.52 GiB | 143.88 秒 | 5/6 | 通过 / 通过 | — |
| **混合精度版** | **MTP** | **24.31 GiB** | **211.90 秒** | **6/6** | **通过 / 通过** | **112/168（66.7%）** |

四路各 6 个请求均为 HTTP 200、非空输出，未出现重复标点坍塌。极速 bare/MTP 与混合 bare 的同一道简短代码校验答为 55，正确值是 30，因此如实记为 5/6；混合精度 MTP 为 6/6。这里是关闭思考的短串行 smoke，**不是** vLLM TPS、通用质量、64K 长上下文或并发压力证明；65,536 context 与 `max-num-seqs=4` 是启动配置值。

推荐的 vLLM 起步组合是**混合精度版 + 原生 MTP**：

```bash
VARIANT=quality MODE=mtp PORT=19120 bash NVFP4/runtime/START_VLLM028_NVFP4.sh
```

启动器默认只监听 `127.0.0.1`，固定 `method=mtp` 与 `num_speculative_tokens=3`，并拒绝自动拉取镜像或覆盖同名容器。必须预先准备镜像；脚本会核对固定的官方不可变 manifest 与本地 image ID。模型/量化/MTP 参数来自上述实测；便于宿主访问的 loopback host-network 连接是部署适配，不作为新的性能实测。

官方参考：[vLLM ModelOpt 量化](https://docs.vllm.ai/en/latest/features/quantization/modelopt/)、[vLLM MTP](https://docs.vllm.ai/en/latest/features/speculative_decoding/mtp/)、[Docker host network](https://docs.docker.com/engine/network/drivers/host/)。
<!-- VLLM028_RUNTIME_V1_ZH_END -->
<!-- NVFP4_MAIN_V1_ZH_END -->

> **拒答评测：10 个类别、140 条提示中为 4 / 140（2.9%）。**
>
> ***科研免责声明：本实验版本仅用于研究拒答倾向消解的技术可行性及其行为影响。它不构成全面的安全结论，不代表对无限制使用的认可，也不构成任何专业建议。用户应依法、恰当地使用，并独立核验模型输出。***

<!-- AWQ_W4A16_V1_ZH_START -->
## AWQ-W4A16｜vLLM 原生 MTP

![AWQ-W4A16 能力、思考与并发](assets/awq-w4a16-v1-zh.png)

完整目录：`NVFP4/AWQ-W4A16/`；主权重文件为 `Qwen3.8-27B-EfficientThink-SimPO-AWQ-W4A16.safetensors`。请下载整个目录，勿与 W4A4、W4A4+W8A8、旧 W4A16 或 W8A16 文件混用。

> **格式身份：**这是 `compressed-tensors` 的 pack-quantized **AWQ W4A16**：367 个目标权重采用 group-128 非对称 INT4，33 个目标权重采用 group-128 对称 INT8，其余关键、视觉及 MTP 张量保留 BF16；激活与 KV cache 为 BF16。它**不是 NVFP4 编码、GPTQ 或 imatrix**。`hf_quant_config.json` 仅保留上游 ModelOpt 来源记录，运行时以 `config.json` 的 `quant_method=compressed-tensors` 为准。

`vision-mtp-bf16.safetensors` 同时包含 **333 个官方 BF16 视觉张量和 15 个官方 BF16 MTP 张量**；它是主模型的视觉/MTP 组件，不是 DFlash2 draft。

### 正式能力与思考量

口径：单张 RTX PRO 6000 96GB、vLLM + 原生 MTP、C24、xhigh、32,768 token 输出上限、1,800 秒请求超时。全部异常样本保留在分母；异常项可重叠。

| 项目 | 最终得分 | 平均思考 | P50 / P90 | >8K / >16K | 32K 截断 | 请求错误 / HTTP 超时 |
|---|---:|---:|---:|---:|---:|---:|
| GPQA | **159/198（80.30%）** | 11,142 | 6,283 / 32,768 | 87/198（43.94%）/ 56/198（28.28%） | 28/198（14.14%） | 0/198 / 0/198 |
| MMLU | **453/500（90.60%）** | 935 | 218 / 1,674.4 | 12/500（2.40%）/ 4/500（0.80%） | 0/500 | 0/500 / 0/500 |
| LCB | **74/100（74.00%）** | 13,922 | 8,207.5 / 32,768 | 50/100（50.00%）/ 42/100（42.00%） | 23/100（23.00%） | 0/100 / 0/100 |

GPQA 的空 final、无提交和不可解析均为 **28/198（14.14%）**。MMLU 的空答、无提交和不可解析均为 **0/500**。LCB 的无代码/无提交为 **22/100（22.00%）**、不可解析 **23/100（23.00%）**、语法错误 **1/100（1.00%）**、代码执行超时 **0/100**；均按失败计入。这里与旧 SGLang W4A16、NVFP4 或其他解码器结果不是同条件量化损失对照。

### vLLM MTP 短输出并发

固定口径为 1,024 输入 + 256 输出，每档 3 次，`num_speculative_tokens=3`，所有请求错误为 0。TPS 按模型卡统一取整。

| 并发 | 聚合 tok/s | MTP 接受率 |
|---:|---:|---:|
| C1 | 39 | 56.03% |
| C4 | 128 | 51.82% |
| C8 | 226 | 52.19% |
| C16 | 366 | 49.05% |
| **C24（已测最高吞吐）** | **480** | **53.46%** |

### 已验证启动方式

```bash
python -m vllm.entrypoints.openai.api_server \
  --model ./NVFP4/AWQ-W4A16 \
  --served-model-name qwen38-27b-awq-w4a16 \
  --host 127.0.0.1 --port 19540 \
  --dtype bfloat16 \
  --quantization compressed-tensors \
  --kv-cache-dtype auto \
  --gpu-memory-utilization 0.95 \
  --max-model-len 65536 \
  --max-num-seqs 24 \
  --max-num-batched-tokens 2048 \
  --reasoning-parser qwen3 \
  --attention-backend TRITON_ATTN \
  --limit-mm-per-prompt '{"image":2,"video":1}' \
  --skip-mm-profiling \
  --no-enable-prefix-caching \
  --enforce-eager \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

vLLM 0.28.0 + compressed-tensors 0.17.0 + Transformers 5.15.1 已完成 bare/MTP 的文本、中文、代码、解释、图片和真实 MP4 smoke，并记录原生 MTP accepted/proposed 计数。SGLang 0.5.19 + compressed-tensors 0.18.0 + Transformers 5.12.1 + FlashInfer 0.6.18 + Decord 0.6.0 的 bare/MTP 同样各完成 6/6，但依赖隔离 overlay、局部 CUDA `libcudart` 链接修复与显式 Decord 视频后端补丁，**不能理解为原生 pip 环境即装即用**。SGLang 该轮只是短 smoke；没有 SGLang 长输出质量或 TPS 结论。可复现文件见 `NVFP4/AWQ-W4A16/runtime/`。
<!-- AWQ_W4A16_V1_ZH_END -->

## 静态 FP8 + DFlash2 实测服务结果

| 并发 | Completion tok/s | DFlash 接受率 | 平均接受长度 / 8 |
|---:|---:|---:|---:|
| C1 | 36 | **70.0%** | **5.91** |
| C2 | 61 | 65.5% | 5.57 |
| C4 | 104 | 68.33% | 5.78 |
| C8 | 165 | **70.0%** | 5.89 |
| C16 | 243 | 66.0% | 5.59 |
| C24 | **281** | 67.0% | 5.70 |

实测环境为 DGX Spark、已发布的静态 Block128 FP8 主模型、SGLang + DFlash2、XH、`draft_tokens=8`、`max_tokens=256`。六档均无请求错误。C24 为最大聚合吞吐；C1 为最低并发且平均接受长度最高；**日常实用平衡推荐 C8**。定长压力测试中的 `finish_reason=length` 是测试设计，不作为质量判断。

另行执行的 C3、`max_tokens=1024` science/code/general 质量 smoke 为 3/3 正确、3/3 `stop`、无空答/乱码、聚合 68 tok/s。

实测启动脚本（显式传入下载目录）：

```bash
bash FP8/runtime/BUILD_RUNTIME_SPARK.sh
CONCURRENCY=24 bash FP8/runtime/TESTED_STARTUP_C24_DFLASH2.sh \
  "$PWD/FP8" "$PWD/FP8/DFlash2-FP8" efficientthink-fp8-dflash2 19110
```

**EfficientThink 优化的是无效推理长尾，而不是推理本身。** 目标是在保留能力和必要长推理的同时，提高最终答案的可靠性。

本仓包含 `BF16/` 下的最终合并 **SimPO BF16** 主模型，以及 `FP8/` 下的纯文本静态 Block128 **FP8 主模型**。为便于按目录一次下载，两个主模型目录内均配套同一份已验证的可选 `DFlash2-FP8/` draft；draft 不替代主模型。

## 文件

| 目录 | 作用 | 已验证源大小 |
|---|---|---:|
| `BF16/` | 最终合并 SimPO BF16 主模型 + 内置 `DFlash2-FP8/` | 57,143,670,823 bytes |
| `FP8/` | 纯文本静态 Block128 FP8 主模型 + 实测启动脚本 + 内置 `DFlash2-FP8/` | 31,908,365,464 bytes |

下载 `BF16/` 或 `FP8/` 任一目录，即可同时取得对应主模型与 DFlash2 运行文件。静态 FP8 主包以 `FP8/manifest.json` 与 `FP8/SHA256SUMS` 为准；该 FP8 主模型为纯文本：64 层、SGLang 键名重排后 1,251 tensors、visual tensors=0、MTP tensors=0。

## 最终 SimPO 冻结评测

冻结 XH 协议，`max_tokens=32768`；全部未通过样本均保留在分母中。

| Suite | 最终分数 |
|---|---:|
| GPQA Diamond | **171 / 198（86.36%）** |
| MMLU | **442 / 500（88.40%）** |
| LiveCodeBench | **74 / 100** |

LiveCodeBench 难度分布：easy `23/23`、medium `27/31`、hard `24/46`。74/100 是将全部失败计入后的最终 operational 分数，不标注为 clean run。

## 同协议能力与思考对比

协议：动态 FP8 + DFlash2、双卡 C24、XH、`max_tokens=32768`，原版与最终 SimPO 均为正式全量结果；所有失败均保留在分母中。

### GPQA Diamond｜198题

| 指标 | 原版 Qwen3.8-27B | 最终 SimPO | 变化 |
|---|---:|---:|---:|
| 正确率 | 164/198（82.83%） | **171/198（86.36%）** | **+7题 / +3.54pp** |
| 平均 reasoning | 10,234 | 9,556 | −678（−6.6%） |
| P50 / P90 | 5,182 / 32,768 | 4,788.5 / 32,765.3 | −393.5 / 基本不变 |
| >8K / >16K | 78 / 51 | 73 / 44 | −5 / −7 |
| 32K 截断 | 26 | 21 | −5（−19.2%） |
| 不可解析 | 22 | 18 | −4 |
| 宽松 LOOP 候选 | 12 | 6 | −6 |

GPQA 提升 3.54pp，同时平均思考、截断、不可解析与宽松 LOOP 候选均下降。

### MMLU｜500题

| 指标 | 原版 Qwen3.8-27B | 最终 SimPO | 变化 |
|---|---:|---:|---:|
| 正确率 | **451/500（90.20%）** | 442/500（88.40%） | **−9题 / −1.80pp** |
| 平均 reasoning | 1,113.91 | 1,009.76 | −104.15（−9.4%） |
| P50 / P90 | 213.5 / 1,942.7 | 211.5 / 1,884.2 | −2 / −58.5 |
| >8K / >16K | 18 / 7 | 14 / 6 | −4 / −1 |
| 32K 截断 | 4 | 1 | −3（−75%） |

MMLU 的平均思考与长尾明显下降，但正确率同步回落 1.80pp；这是需要如实披露的能力交换，不能只展示效率改善。

### LiveCodeBench｜100题

下列 reasoning 统计按全部 100 题计算，超时/错误题以 0 reasoning tokens 计入。

| 指标 | 原版 Qwen3.8-27B | 最终 SimPO | 变化 |
|---|---:|---:|---:|
| 正确率 | 69/100（69%） | **74/100（74%）** | **+5题 / +5pp** |
| Easy | 23/23 | 23/23 | 持平 |
| Medium | 26/31（83.87%） | 27/31（87.10%） | +1题 / +3.23pp |
| Hard | 20/46（43.48%） | **24/46（52.17%）** | **+4题 / +8.69pp** |
| 平均 reasoning | 12,167 | 12,514 | +347（+2.9%） |
| P50 / P90 | 5,442.5 / 32,772 | 6,480.5 / 32,770.1 | +1,038 / 基本不变 |
| >8K / >16K | 44 / 34 | 47 / 34 | +3 / 持平 |
| 32K 截断 | 21 | 21 | 持平 |
| 超时/请求错误 | 6 | 2 | −4（−66.7%） |
| empty code | 27 | 23 | −4（−14.8%） |
| 正常 stop | 73 | 77 | +4 |
| runtime error | 1 | 0 | −1 |
| 总耗时 | 2,060秒 | 2,067秒 | 基本持平 |

LCB 的增益主要来自难题与提交可靠性。代码推理没有整体缩短：平均、P50 和 >8K 略增，>16K 与 32K 截断不变。也就是说，SimPO 将一部分原本无法提交的样本转化为有效解答，但尚未进一步消除 32K 长尾。

## 训练

[`Qwen/Qwen3.8-27B`](https://huggingface.co/Qwen/Qwen3.8-27B) → 能力保持 SFT → 终止行为 SimPO → 逐 tensor FP32 delta 合并 → BF16。

### SFT · 1,905 条样本

- 1 epoch · 239 optimizer steps · effective batch 8
- LoRA r=16 · alpha=32 · dropout=0.05
- LR 5e-6 · warmup 12 steps · seed 20260901
- 双 NVIDIA RTX PRO 6000 Blackwell Server Edition

### SimPO · 110 组偏好对 / 73 个唯一 prompt

- 5 optimizer steps · beta=1.0 · gamma=0.2 · peak LR 5e-7
- LoRA r=16 · alpha=32 · dropout=0
- seed 20260903 · world size 2 · FSDP full sharding

## 推荐 Transformers 用法

<!-- BF16_RUNTIME_AUDIT_V1_ZH_START -->
需使用支持 `Qwen3_5ForConditionalGeneration` 的 Transformers 新版本（发布的 BF16 config 记录为 5.12.1）及 Accelerate。BF16 保留多模态 wrapper；下例仅生成文本，不启用 DFlash2。不要替换成纯文本静态 FP8 目录。这是依据配置与官方 API 的修正，不声称新增 BF16 性能实测。
<!-- BF16_RUNTIME_AUDIT_V1_ZH_END -->

```python
from pathlib import Path
from transformers import AutoTokenizer, Qwen3_5ForConditionalGeneration

# Run from the downloaded repository root; never pass the FP8 directory here.
model_dir = str(Path("BF16").resolve())
tok = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
model = Qwen3_5ForConditionalGeneration.from_pretrained(
    model_dir, dtype="auto", device_map="auto", local_files_only=True
)
messages = [{"role": "user", "content": "What is 17 + 25?"}]
prompt = tok.apply_chat_template(
    messages, tokenize=False, add_generation_prompt=True,
    enable_thinking=True, reasoning_effort="xhigh",
)
inputs = tok(prompt, return_tensors="pt").to(model.device)
output = model.generate(
    **inputs, max_new_tokens=4096, do_sample=True,
    temperature=1.0, top_p=0.95, top_k=20,
)
print(tok.decode(output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True))
```

模型内置生成默认值为 `temperature=1.0`、`top_p=0.95`、`top_k=20`。非思考模式可设置 `enable_thinking=False`；本卡披露的冻结能力与服务结果均使用 `reasoning_effort="xhigh"`。

<!-- DFLASH_RATIONALE_MTP_V1_ZH_START -->
### 为什么选择 DFlash2

**我们选择 DFlash2，主要看重实测草稿接受度与高输出吞吐。** DFlash 并行提出一组候选 token；主模型每轮验证保留的 token 越多，越有利于减少逐 token 顺序解码开销、提高 TPS。[方法说明：DFlash 作者](https://z-lab.ai/projects/dflash/)。

在已测的 **DGX Spark 静态 FP8** 配置中，C1–C24 测得 **65.5–70.0% 的接受率**；C8 达到 **165 聚合 tok/s、70.0% 接受率**，C24 达到 **281 聚合 tok/s、67.0% 接受率**。日常平衡推荐 C8，最大实测吞吐选 C24。这些是 DFlash2 实测结果，不是与 MTP 的同条件加速比；GGUF 结果使用其独立实测配置，见关联 GGUF 仓。
<!-- DFLASH_RATIONALE_MTP_V1_ZH_END -->

## DFlash2 范围与限制

<!-- DFLASH_STATIC_FP8_V1_ZH_START -->
### 名副其实的静态 FP8 DFlash2 draft

仓内 DFlash2 draft 现已替换为**预量化静态 FP8** `compressed-tensors` checkpoint，不再是放在 FP8 目录名下的 BF16 文件。`model.safetensors` 为 **2,407,027,720 bytes**（SHA256 `1f3636a32d866f8ebc7f422d63f9247126ebb6d2566d3e0da327d81dd8fa25d1`）；tensor 审计为 20 个 FP8 E4M3 权重、20 个 FP32 scale，以及 61 个保留 BF16 tensor。

加载时必须显式加入：

```text
--speculative-draft-model-quantization compressed-tensors
```

同条件 DGX Spark 对照使用同一 W4A4 主模型、15 条固定输入、XH、256 输出 token 与 8 draft tokens；四个 cell 均为 15/15 请求成功。

| Draft | 并发 | 聚合 tok/s | DFlash 接受率 | 平均接受长度 / 8 | 请求错误 |
|---|---:|---:|---:|---:|---:|
| BF16 对照 | C1 | 29.75 | 38.77% | 3.72 | 0 |
| 静态 FP8 | C1 | 30.26 | 35.86% | 3.51 | 0 |
| BF16 对照 | C4 | 68.50 | 32.71% | 3.29 | 0 |
| **静态 FP8** | **C4** | **75.94** | **33.55%** | **3.35** | **0** |

C1 接受度为同轮服务日志快照均值，C4 接受度为结束后 SGLang metrics 精确值。本次同口径 C4 中，静态 FP8 draft 的聚合吞吐比 BF16 高约 **10.9%**。该短定长测试只验证服务行为，不替代本卡其他位置的正式能力分数。
<!-- DFLASH_STATIC_FP8_V1_ZH_END -->

- 同一份真静态 FP8 draft 分别放在 `BF16/DFlash2-FP8/`、`FP8/DFlash2-FP8/` 与每个 `NVFP4/*/DFlash2-FP8/` 档位，均包含 `model.safetensors`、`config.json`、`manifest.json` 与 `SHA256SUMS`。
- 冻结评测配置使用 DFLASH、1 speculative step、top-k 1、8 draft tokens、block size 8、Triton draft attention 和 FP8 draft。
- 使用前必须在目标服务框架中核对兼容性；draft 不能作为独立聊天模型运行。
- 分数绑定冻结 XH harness 与服务配置，不用于跨协议直接比较。
- 必要的长推理仍然保留；EfficientThink 不是统一短答模式。
- 高风险场景请独立核验输出。

## 推荐部署：SGLang

**本模型推荐使用 SGLang。** 冻结的 FP8+DFlash2 质量、接受率与并发数据均由 SGLang 实测获得。XH 思考模式采用 Qwen 官方采样参数：`temperature=1.0`、`top_p=0.95`、`top_k=20`、`min_p=0.0`、`presence_penalty=0.0`、`repetition_penalty=1.0`。

<!-- PORTABLE_RUNTIME_V1_ZH_START -->
### 可复现的 Spark 运行环境

该脚本面向 **DGX Spark / Linux ARM64 / GB10**，需先安装 Docker、NVIDIA Container Toolkit、Python 3 与 curl。它不是 x86/V100 的 FP8 启动脚本。请在下载仓库根目录执行，并完整下载 `FP8/`，包括 `FP8/runtime/` 与 `FP8/DFlash2-FP8/`。

`BUILD_RUNTIME_SPARK.sh` 从**按 digest 锁定的公开 SGLang 基础镜像**、公开的 `17313cf4b25d` 源码与锁定的公开 xgrammar wheel 构建本地镜像，校验两份小依赖的哈希，不下载模型权重。请为约 32 GB 的解包运行环境和构建层预留 Docker 磁盘空间。不再依赖私有镜像仓或作者本机源码目录；也可先把下载缓存复制到 `FP8/runtime/build-cache/` 再构建。

启动器会明确报告缺失文件、端口占用等错误，拒绝覆盖已有容器，显示日志命令，且只有服务就绪并通过一次真实聊天生成后才显示 READY。脚本关闭该锁定版本的特殊 token-only 健康生成探针。默认端口 **19110**，只监听 **127.0.0.1**。确需局域网访问时设置 `BIND_HOST=0.0.0.0` 并做好访问控制；脚本本身未开启鉴权。

服务端保留实测上限 `CONCURRENCY=24`；**客户端同时发出 8 个请求（C8）** 为实用平衡档，**24 个请求（C24）** 为最大实测聚合吞吐档。服务端并发上限不等于自动压测，客户端需真正发出相应并发请求。查看日志：`docker logs -f efficientthink-fp8-dflash2`；只停止该服务：`docker stop efficientthink-fp8-dflash2`。检查完已停止容器后，删除这个精确容器才能复用名称，或改用新名称。

每次请求显式指定 XH 模板参数：
```bash
curl --fail-with-body http://127.0.0.1:19110/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"efficientthink-fp8-dflash2","messages":[{"role":"user","content":"What is 17 + 25?"}],"max_tokens":1024,"temperature":1.0,"top_p":0.95,"top_k":20,"min_p":0.0,"presence_penalty":0.0,"repetition_penalty":1.0,"chat_template_kwargs":{"enable_thinking":true,"reasoning_effort":"xhigh"}}'
```

`chat_template_kwargs` 是请求中的模板参数，不是服务启动命令参数。上例 1,024-token 预算仅作短连接测试，正式能力测评使用 32,768。SGLang 的 DFlash verify block 为 8；llama.cpp 对本 draft 使用 `--spec-draft-n-max 7`，两者是不同框架的参数约定，不能互换。

官方参考：[Qwen3.8 SGLang 配方](https://docs.sglang.io/cookbook/autoregressive/Qwen/Qwen3.8-27B)、[SGLang DFlash](https://docs.sglang.io/docs/advanced_features/speculative_decoding)、[锁定的 SGLang 源码](https://github.com/sgl-project/sglang/tree/17313cf4b25d)。本运行包保持已测配置，不把最新版官方配方与旧 TPS 混成一次实测。
<!-- PORTABLE_RUNTIME_V1_ZH_END -->

### SGLang — 已验证 FP8 + DFlash2 路径

```bash
bash FP8/runtime/BUILD_RUNTIME_SPARK.sh
CONCURRENCY=24 bash FP8/runtime/TESTED_STARTUP_C24_DFLASH2.sh \
  "$PWD/FP8" "$PWD/FP8/DFlash2-FP8" efficientthink-fp8-dflash2 19110
```

日常部署推荐采用实测平衡档 C8；追求最大聚合吞吐时使用 C24。这是本仓已冻结实测的 DFlash2 路径。

### vLLM — 仅列官方基础参考，本仓未实测

```bash
vllm serve "$PWD/FP8" \
  --served-model-name efficientthink-fp8 \
  --reasoning-parser qwen3 --max-model-len 40960 \
  --host 127.0.0.1 --port 19110
```

OpenAI-compatible 请求中显式传入 `reasoning_effort="xhigh"` 与官方思考采样参数。该命令仅作为 Qwen3.8 官方基础服务形态参考；本仓没有实测该 checkpoint 的 vLLM 路径，**不推荐也不声称**已完成 vLLM+DFlash2 冻结实测。

参考：[Qwen3.8-27B 官方模型卡](https://huggingface.co/Qwen/Qwen3.8-27B)、[SGLang 文档](https://docs.sglang.ai/) 与 [vLLM 文档](https://docs.vllm.ai/)。

---

