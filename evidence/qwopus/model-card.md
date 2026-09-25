---
library_name: transformers
base_model:
- Qwen/Qwen3.8-27B
tags:
- gguf
- llama.cpp
- image-text-to-text
- vision
- multimodal
- text-generation-inference
- transformers
- unsloth
- conversational
- text-generation
- qwen3_8
- qwen3
- qwen
- 27b
- fine-tuned
- instruction-tuned
- reasoning
- agent
- agentic
- tool-use
- function-calling
- code-generation
- mtp
- speculative-decoding
- local-inference
- safetensors
license: apache-2.0
language:
- en
- zh
- es
- ru
- ja
pipeline_tag: image-text-to-text
---

# 🪐 Qwopus3.8-27B-Flash

<div align="center">
<img src="https://cdn-uploads.huggingface.co/production/uploads/66309bd090589b7c65950665/GvN4SANiFepBuWcsoWbOX.jpeg" alt="IMG_7359" width="82%"/>
</div>

> [!NOTE]
> **Qwopus3.8-27B-Flash** is a fine-tuned model built on [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B). It is designed to retain strong general capability while substantially lowering reasoning cost and response time for practical, long-running agent workloads.

> [!TIP]
> **12.8% Faster Decoding · 80.7% MTP Acceptance · Less Runaway Reasoning · More Efficient Agent Completion**

## 💡 1. Fine-Tuning Philosophy — Preserve Capability, Collapse Cost

Qwopus3.8-27B-Flash starts from a simple premise: a useful Flash model should preserve enough capability to complete demanding work while driving down the cost and latency of reasoning.

An agent amplifies reasoning cost. A normal chat may call a model once, but one agent task can call it dozens or hundreds of times through a repeated loop:

```text
Read → Think → Tool Call → Observe → Edit → Test
```

> [!IMPORTANT]
> **Wall-clock time is what users feel.** If a model adds five seconds to each turn, a 50-turn task adds 250 seconds of waiting. In the agent era, every-token speed, reasoning length, and completion efficiency are as important as a single-turn benchmark result.

Inference cost is also a central commercialization constraint. Every generated token consumes GPU time, electricity, memory capacity, and concurrency budget. Flash models are intended to give users with constrained resources a more practical experience, not merely to produce a higher throughput number on paper.

The goal of Qwopus3.8-27B-Flash is therefore to reduce ineffective computation and reach a clean completion more quickly and consistently. The benchmark results below show that this optimization has an explicit trade-off: it improves inference efficiency, while the reported MMLU-Pro mixed-set score is lower than the base comparison.




### Five-Story Pagoda Garden — Visual Output Comparison

> [!NOTE]
> These visuals are qualitative model outputs. They complement the measured benchmark results below and are not a quantitative capability score on their own.

#### Original Base Model — Qwen3.8-27B

![Original model — Five-Story Pagoda test](https://cdn-uploads.huggingface.co/production/uploads/66309bd090589b7c65950665/r2jq2T2BEdtQJMYCMaMzR.png)

#### Fine-Tuned Model — Qwopus3.8-27B-Flash

![Fine-tuned model — Five-Story Pagoda test](https://cdn-uploads.huggingface.co/production/uploads/66309bd090589b7c65950665/xI9kuvJwKjYHBi1Chuq19.png)



## 🧪 2. Fine-Tuning Cookbook

### 2.1 Base Model and Training Goal

Qwopus3.8-27B-Flash is fine-tuned from the Qwen3.8-27B foundation model. The training objective is not simply to maximize visible reasoning length or claim a universal benchmark gain. It is to retain practical problem-solving ability while making the model faster, less prone to pathological long-tail reasoning, and better suited to iterative agent workflows.

### 2.2 Stage 1 — Data Preparation and Quality SFT

Data preparation is the foundation of the SFT stage. The first stage began with approximately **1.5 million** teacher-model SFT examples. After extensive cleaning and filtering, the highest-quality **10%** was retained for the initial fine-tuning stage.

Each example was evaluated across its three main components—**question**, **chain of thought**, and **answer**—with criteria tailored to a 27B model:

- Semantic relevance and usefulness.
- Problem difficulty.
- Chain-of-thought quality.
- Answer consistency.

The evaluation ensemble used reasoning models including **Qwen3.7-Max**, **GLM-5**, **GPT-OSS-120B-High**, and **Gemma4-27B**. Their scores were combined through a weighted calculation, after which only high-quality examples were retained.

> [!NOTE]
> The training mix also includes agent-trajectory data and reconstructed trace data derived from closed models such as Claude and GPT. Detailed examples cannot currently be disclosed. The dataset will be further organized and released after preparation is complete.

### 2.3 Stage 2 — NeMo-RL + GSPO Reasoning Reinforcement

Stage 2 consolidates and strengthens the chain-of-thought and reasoning behaviors learned during SFT. This stage follows an **NVIDIA NeMo-RL + GSPO** route for reasoning reinforcement.

The training process uses repeated sampling and reward comparison, then updates the model with a sequence-level importance ratio. The intent is to reinforce useful reasoning trajectories and completion behavior rather than reward longer reasoning traces by default.

> [!TIP]
> The two stages serve different roles: Stage 1 builds a high-quality reasoning and instruction-following foundation; Stage 2 consolidates it through reward-guided reasoning reinforcement.

## 🙏 3. Training Stack, Testing, and Collaboration

### Unsloth

Special thanks to [Unsloth](https://unsloth.ai/) for its efficient, memory-optimized fine-tuning framework. Its tooling made the large-model training workflow more practical and accessible.

### Kyle Hessling

Special thanks to [**Kyle Hessling**](https://x.com/KyleHessling1) for completing the testing work and providing essential evaluation support for this release.

> [!TIP]
> If you have any questions or suggestions about the model, please feel free to reach out to [Kyle Hessling](https://x.com/KyleHessling1) on [X](https://x.com/KyleHessling1) and share your feedback. Thank you so much for all your support! 🙏

> [!NOTE]
> The training and test results in this card are author-provided local results. The sections below describe the measured scope and do not claim universal behavior across all hardware, prompts, or agent environments.

## 📊 4. Benchmark Results

| Reported signal | Qwopus3.8-27B-Flash | Qwen3.8 base comparison | Interpretation |
| --- | ---: | ---: | --- |
| MMLU-Pro mixed-question accuracy (2,500 questions) | 91.28% | **92.73%** | **−1.45 pp** |
| Decoder-only throughput across Math, Physics, and Chemistry | **9.347 tok/s** | 8.284 tok/s | **+12.8%** |
| Weighted MTP draft acceptance | **80.7%** | 66.1% | **+14.6 pp** |
| Aggregate `raw_output` characters across three subjects | **7,949,546** | 8,824,213 | **−9.9%** |
| End-to-end batch evaluation throughput | **~8% higher** | — | Separate, approximate measurement |
| Agentic software-engineering battery, strict one-run result | **13 / 14 (93%)** | — | 26.0 min on one RTX 5090 |

### 4.1 Evaluation Scope

The reported local tests used inference environments that included NVIDIA GeForce RTX 5090, NVIDIA V100, and NVIDIA GB10 hardware. The current test brief does not map every table or case study to a particular device.

For the MMLU-Pro decoder-only comparison, both models used the same Q5_K_M + MTP configuration:

```text
draft_n_max = 2
-c 327680
-np 10
```

The agentic software-engineering battery in Section 4.6 is a separate run explicitly reported on one RTX 5090 and uses its own configuration, listed with that battery.

### 4.2 MMLU-Pro Accuracy Reference and Five-Layer Tower Renders

> [!WARNING]
> **Accuracy–efficiency trade-off:** The fine-tuned model improves reasoning efficiency, but its reported score on the 2,500-question MMLU-Pro mixed set is **91.28%**, compared with **92.73%** for the Qwen3.8 base comparison—a decrease of **1.45 percentage points**. The decoder-only throughput results below measure speed, not answer accuracy.


### 4.3 MMLU-Pro Decoder-Only Throughput

This table measures isolated generated-token throughput rather than answer accuracy. Evaluation time is in seconds; throughput is generated tokens per second.

| Subject | Qwopus generated | Qwopus eval (s) | Qwopus tok/s | Qwen generated | Qwen eval (s) | Qwen tok/s | Gain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Math | 753,406 | 81,212.1 | **9.277** | 804,071 | 96,614.0 | 8.323 | **+11.5%** |
| Physics | 1,055,509 | 111,465.3 | **9.469** | 1,021,881 | 125,039.7 | 8.173 | **+15.9%** |
| Chemistry | 1,428,542 | 153,685.2 | **9.295** | 1,372,810 | 164,461.4 | 8.347 | **+11.4%** |
| **Three-subject total** | **3,237,457** | **346,362.6** | **9.347** | **3,198,762** | **386,115.2** | **8.284** | **+12.8%** |

Across the three reported subjects, Qwopus reaches **9.35 tok/s** versus **8.28 tok/s** when rounded to two decimals. Every reported subject shows a double-digit decoder-only throughput gain. The separately reported ~8% end-to-end batch-throughput result includes the full evaluation path and should not be combined with this decoder-only measurement.

### 4.4 MTP Draft Acceptance

Draft acceptance is an internal llama.cpp/MTP implementation metric. The reported aggregate is a weighted calculation, rather than an average of subject-level percentages:

```text
sum(accepted) / sum(generated)
```

| Subject | Qwopus3.8-27B-Flash | Qwen3.8 base comparison | Difference |
| --- | ---: | ---: | ---: |
| Math | **81.1%** | 66.3% | **+14.8 pp** |
| Physics | **79.2%** | 64.6% | **+14.5 pp** |
| Chemistry | **81.7%** | 67.1% | **+14.6 pp** |
| **Three-subject weighted total** | **80.7%** | **66.1%** | **+14.6 pp** |

| Three-subject raw counts | Accepted | Generated |
| --- | ---: | ---: |
| Qwopus3.8-27B-Flash | 1,998,599 | 2,476,486 |
| Qwen3.8 base comparison | 1,821,083 | 2,755,425 |

> [!TIP]
> The **+14.6 pp** result is an absolute difference in percentage points. It is not a +14.6% relative-improvement claim.

### 4.5 Reasoning-Efficiency Findings

The following values are `raw_output` **character counts**, not token counts. Mean, P95, and median describe different parts of the output-length distribution.

| Subject | Mean Qwen | Mean Qwopus | Mean change |
| --- | ---: | ---: | ---: |
| Math | 4,614.2 | 3,798.7 | **−17.7%** |
| Physics | 5,995.0 | 5,469.6 | **−8.8%** |
| Chemistry | 7,039.2 | 6,630.8 | **−5.8%** |

| Aggregate `raw_output` characters | Qwen3.8 base comparison | Qwopus3.8-27B-Flash | Change |
| --- | ---: | ---: | ---: |
| Math + Physics + Chemistry | 8,824,213 | **7,949,546** | **−9.9%** |

The reported data suggests that Qwopus reduces pathological long-tail reasoning while retaining sufficient reasoning depth on typical samples. P95 output length falls by 13–40% depending on subject, while median output length increases in all three subjects. This pattern suggests less runaway reasoning rather than uniform suppression of reasoning.


### 4.6 Agentic Software-Engineering Battery

This held-out battery evaluates **14 agentic software-engineering tasks** with deterministic hidden-test verifiers. There is no LLM-as-judge and no partial credit: a task passes only when its complete hidden suite passes. Before evaluation, every task was checked with negative and positive controls—the untouched starting state had to fail, and a reference solution had to pass. Hidden tests remain outside the agent workspace and are SHA-256 hashed before and after each run to detect tampering.

> [!IMPORTANT]
> **Strict result: 13 / 14 passed (93%).** The 95% Wilson confidence interval is **69%–99%**. Total wall-clock time was **26.0 minutes** on one RTX 5090. A task counts only if the agent both passes its hidden suite and finishes within its per-task wall-clock budget.

| # | Capability | What it tests | Result | Turns | Wall |
| --- | --- | --- | --- | ---: | ---: |
| T01 | Multi-bug repair | Diagnose and fix 3 distinct bugs from a failing suite | ✅ pass | 10 | 55s |
| T02 | Runtime debugging | Run a crashing script, read the traceback, and fix the root cause | ✅ pass | 8 | 57s |
| T03 | Cross-file refactor | Rename a symbol and parameter across 4 files with zero stragglers | ✅ pass | 12 | 40s |
| T04 | Build CLI to spec | New CLI with an exact stdout contract, verified by execution | ✅ pass | 15 | 124s |
| T05 | Algorithm from spec | Bidirectional Roman numerals with full 1–3,999 round-trip | ✅ pass | 3 | 29s |
| T06 | Performance optimization | O(n²) to sub-second on 20k inputs with identical results | ✅ pass | 15 | 129s |
| T07 | Parser / interpreter | Recursive-descent expression evaluator without `eval()` | ⚠️ over budget | — | 420s |
| T08 | Self-correction | Recover correctly from a `UnicodeDecodeError` | ✅ pass | 6 | 38s |
| T09 | Exact output contract | Strict schema, rounding, multi-key sort, and no mutation | ✅ pass | 3 | 24s |
| T10 | Negative constraint | Hand-rolled CSV parser without the `csv` module | ✅ pass | 22 | 224s |
| T11 | Test authoring | Write tests that catch 4 unseen buggy implementations | ✅ pass | 19 | 269s |
| T12 | Messy-input parsing | Log parsing with continuations, junk lines, and nested brackets | ✅ pass | 7 | 60s |
| T13 | Stateful persistence | KV store that survives a real process restart | ✅ pass | 4 | 36s |
| T14 | Regression-safe fix | Fix an LRU-recency bug without breaking existing behavior | ✅ pass | 7 | 47s |

#### Inference Characteristics

| Metric | Value |
| --- | --- |
| Generation speed | 99.0 tok/s mean across tasks |
| MTP draft acceptance | 88.8% mean |
| Agent turns per task | 10.1 mean; 3–22 range |
| Output tokens per task | 2,340 mean; 30,414 total |
| Integrity violations | 0; hidden tests remained untampered after every task |

The battery used **Qwopus 3.8 27B** in Q5_K_M GGUF format with a bundled NextN/MTP head, self-speculative decoding (`--spec-type draft-mtp`), q8_0 KV cache, and thinking disabled. It was run through headless Claude Code against a local llama.cpp server with real file and shell tools.

#### Scoring, Failure Analysis, and Repeat Sampling

T07 left a file that passed its hidden suite (`7 passed in 0.01s`), but the agent kept iterating and did not return before the 420-second limit. It is therefore correctly scored as a strict failure: completing the task includes knowing when to stop. This was a termination and verbosity failure, not necessarily an inability to implement the parser.

| Task | Attempts | Passed | Rate | Observed failure modes |
| --- | ---: | ---: | ---: | --- |
| T01 Multi-bug repair | 2 | 2 | 100% | — |
| T07 Parser / interpreter | 7 | 5 | 71% | Incorrect output; non-termination loop |

> [!WARNING]
> Sampling is stochastic. Only T07, the failing task, was resampled; the other 13 tasks are single-sample passes. The 13/14 headline is therefore a one-draw capability demonstration, not a stable leaderboard number, and is more likely optimistic than pessimistic. A stable estimate requires multiple seeds for every task.

### 4.7 Reported Agent and Practical Workload Case Studies

These are individual reported workload case studies, not aggregate success rates or universal behavior claims.

#### Case Study A — Agent Workload Comparison

| Metric | Qwopus3.8-27B-Flash | Qwen3.8 base comparison |
| --- | --- | --- |
| Wall-clock | **640.2 s (10.7 min)** | 1,389.8 s (23.2 min) |
| Turns | **20, completed** | 48, crashed |
| Early-turn behavior | Normal | First turns hit 32K cap |
| Generated tokens | **27,975** | 109,337 |
| Average MTP acceptance | **80.1%** | 72.7% |
| Final status | **Completed** | 500 API error |
| Output | **40 KB / 1,319 lines** | 33 KB / 1,001 lines, partial state |

In this reported workload, the base comparison generated more tokens and spent more time but did not complete, while Qwopus completed with fewer turns and fewer generated tokens.

#### Case Study B — Long Code / Web-Generation Workload

| Metric | Qwopus3.8-27B-Flash | Qwen3.8 base comparison |
| --- | --- | --- |
| Completion tokens | **14,379** | 60,000 ceiling |
| Finish reason | **stop (complete)** | length (incomplete) |
| Thinking | **2,959 chars / 21 s** | 98,452 chars / 15.5 min |
| Answer | **51,844 chars, complete** | 70,116 chars, truncated |
| Wall time | **4.8 min** | 24.4 min |
| HTML | **All balanced** | Invalid / unclosed |

This case illustrates a reported valid long-form completion without hitting the token ceiling and with less reported internal reasoning. It does not establish that every web- or code-generation task will show the same ratio.

#### Case Study C — Long-Horizon Agent Workload

| Reported Qwopus3.8-27B-Flash result | Value |
| --- | --- |
| Test outcome | **22 / 22 tests passed** |
| Wall time | 22.7 min |
| API time | 1,061 s |
| Turns | 56 |
| Tool calls | 55 |
| Tool-call mix | Bash 20 · Write 17 · Edit 11 · Read 7 |
| Tool errors | 5, all self-recovered |
| Input tokens | ~101K |
| Cumulative cache-read tokens | ~4.17M |
| Estimated emitted tokens | ~34.9K |

> [!IMPORTANT]
> These case studies are workload-specific evidence. They must not be converted into a general pass rate, API reliability guarantee, or claim that Qwopus is universally faster or more capable.

## 🎯 5. Recommended Use Cases

- Local MTP speculative decoding where decoder throughput and draft acceptance matter.
- Long-running agent workflows with repeated tool calls and iterative edits.
- Resource-conscious workloads where wall-clock time and generated-token cost are operational constraints.

## ⚠️ 6. Limitations

- **Accuracy–Efficiency Trade-off:** The Flash fine-tuning objective prioritizes practical inference efficiency. On the reported 2,500-question MMLU-Pro mixed set, Qwopus scores 91.28% versus 92.73% for the Qwen3.8 base comparison.
- **Reasoning Stability:** Although the long-tail behavior is improved in the reported evaluation, edge cases may still exhibit reasoning drift, loops, or inefficient trajectories.
- **Agent Dependence:** Tool-use quality and task completion remain dependent on the prompt, tool environment, orchestration layer, and feedback loop.
- **Experimental Release:** This is an independent experimental release for research, local evaluation, and technical exploration. It has not undergone broad safety evaluation or universal agent-reliability testing.

## 🙏 Acknowledgements

Special thanks to:

- **Qwen** for the Qwen3.8-27B base-model foundation.
- **Unsloth** for practical, efficient large-model fine-tuning tooling.
- [**Kyle Hessling**](https://x.com/KyleHessling1) for completing testing and evaluation support.
- The open-source community for training tools, evaluation methods, and technical discussion.
