---
license: apache-2.0
base_model: nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2
pipeline_tag: image-text-to-text
language:
- en
- zh
tags:
- qwen3.8
- efficient-thinking
- reasoning
- coding
- uncensored
- sft
- simpo
- rloo
- fp8
- bf16
- nvfp4
- modelopt
- quantization
- calibration
- static-quantization
- compressed-tensors
- gsq-rco
- gsq
- rco
- hessian
- imatrix
- block128
- mtp
- dflash2
- speculative-decoding
- multimodal
- sglang
- vllm
- gguf
- llama.cpp
---

![Coder390 FP8 vs. original FP8](assets/header-fp8-vs-base-en-8k.png)

<!-- CARD_EN_START -->
# Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2

A model post-trained with several rounds of SFT and RLOO on top of [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2), which is itself the official [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) post-trained with SFT and SimPO. It is built to fix the original model's habit of failing to stop: it already has an answer, yet keeps re-deriving until it hits the 94K cap with no final answer. This repository provides five safetensors tiers, **BF16**, **static FP8 Block128**, **NVFP4 W4A16**, **NVFP4 W4A4**, and **NVFP4 W4A4-W8A8** (mixed precision), all fully multimodal (text + image/video) with the official BF16 MTP bundled; all load in SGLang without patches, and the FP8 package is also smoke-tested on vLLM. It also has **NInfer W4A4 / W4A4-W8A8** (`NVFP4-NInfer/`), **INT8 W8A8** (`INT8/W8A8/`, text only), and **GGUF Q2 / Q3 / Q4 LynnStyle, Q6_K, and Q8_0** (`GGUF/`, `GGUF-NInfer/`, built-in MTP).

- **Far fewer 94K truncations**: under the same protocol, 4 → 1 on GPQA and 13 → 3 on LCB.
- **No regression on any suite**: GPQA **178/198**, MMLU **450/500**, LCB **90/100** (static FP8), vs. 177 / 444 / 83 for the original FP8.
- **Lossless quantization**: GPQA and LCB are identical across BF16, dynamic FP8, and static FP8.
- **Two speculative-decoding options (mutually exclusive)**: about 180 tok/s per request with DFlash2 and 91 tok/s with MTP, vs. about 46 tok/s without speculation.

**Related repositories**

- GGUF / GGUF-NInfer (llama.cpp, NInfer, built-in MTP): [Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer)
- NVFP4-NInfer: [Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer)

## Training method

**Lineage**: official Qwen3.8 27B (177 / 444 / 83) → our SFT + SimPO110 final, i.e. the [EfficientThink base](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2) (171 / 442 / 89) → K3 continuation SFT → week-2 SFT (week2dose, update-225) → first RLOO round (182 groups) → another SFT round (merge-sft-100), giving sft-base-rloo (177 / 448 / 90) → second RLOO round (172 groups) → **Coder390** (178 / 445 / 90, dynamic FP8). Numbers are GPQA / MMLU / LCB, all full suites under the same 100K protocol.

**Training base**: this model starts from our own EfficientThink SFT + SimPO model (the SimPO110 final) and goes through several rounds of SFT and RLOO, which is itself a post-trained version of the official Qwen3.8-27B: [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2).

| Name part | Meaning |
|---|---|
| Coder | Strengthened coding |
| 390 | GPQA, MMLU, and LCB all reach 90 |
| EfficientThink | Training goal: remove unproductive reasoning tails while keeping necessary long reasoning |
| Opus5.5, GPT6Astra | Wrote the gold answers and teacher trajectories |
| Grok4.7 | Host of this training run; checked and filtered data throughout |
| DSV4Pro, K3 | Their trajectories served as teacher-model data; K3 also performed the RLOO value review and wrote part of the problems |
| SFT-RLOO | Method: alternating SFT and RLOO rounds on an SFT (incl. SimPO) base |
| MTP / DFlash2 | Bundled BF16 MTP head / companion DFlash2 speculative-decoding draft |

**The problem**: after the model already has a local answer, it keeps re-running the same derivation with Wait / Actually until the context is full, and the final answer is empty. In most of these cases the model can solve the problem; it just does not stop.

**RLOO data**: 8 trajectories sampled per problem; only groups with both correct and wrong trajectories are kept (all-correct groups are dropped). Groups with 0 or 1 correct trajectory receive one reviewed short teacher trajectory, which replaces the shortest wrong trajectory in that group (27 groups). Final set: 172 groups, 1,376 trajectories: 859 correct and 517 wrong, including 68 empty answers.

**Reward**: penalties apply only to wrong trajectories; long correct reasoning still earns a positive reward, so necessary long reasoning is not suppressed.

| Case | Reward |
|---|---:|
| Short and correct (<24K) | +1.05 |
| Long and correct | +1.0 |
| Short and wrong (<24K) | −0.2 |
| Wrong, 24K–48K | −0.5 |
| Wrong, ≥48K | −0.7 |
| Reached 94K with an answer letter, but wrong | −0.9 |
| Empty answer | −1.0 |

**Result**: under the same protocol, 94K truncations drop from 4 to 1 on GPQA and from 13 to 3 on LCB (FP8) compared with the original model, and none of the three scores falls below the original (all FP8 figures; see the NVFP4 scores below).

## Scores

**Protocol**: the same Coder390 merged weights; two RTX PRO 6000 GPUs, C8 per GPU, 100K context, 94,208-token generation cap, no client-side timeout, DFlash2 draft, SGLang; full GPQA 198, MMLU 500, and LCB 100. Empty answers count as wrong, truncated-but-correct answers count as correct, and every failed sample stays in the denominator.

| Suite | Original Qwen3.8 27B (FP8) | BF16 | Dynamic FP8 | Static FP8 |
|---|---:|---:|---:|---:|
| GPQA | 177/198 | 178/198 | 178/198 | **178/198** |
| MMLU | 444/500 | 446/500 | 445/500 | **450/500** |
| LCB | 83/100 | 90/100 | 90/100 | **90/100** |

GPQA and LCB are identical across all three precisions. MMLU varies between 445 and 450, which is sampling noise rather than a precision effect. Dynamic FP8 means online FP8 quantization of the BF16 weights at inference time; it is not shipped as a separate package.

### All tiers: scores, reasoning length, 94K truncation, and empty answers

Reasoning length is `usage.reasoning_tokens`; a 94K truncation means the output hit the generation cap. LCB empty answers are the number of problems for which no runnable code could be extracted. The original, BF16, dynamic FP8, and static FP8 rows use two RTX PRO 6000 GPUs with C8 per GPU; the three NVFP4 tiers use a single RTX PRO 6000 at C8; the rest of the protocol is the same.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | Original Qwen3.8 27B (FP8) | 177/198 | 5,299 / 12,607 / 50,577 | 4 | 3 |
| GPQA | BF16 | **178/198** | **3,196** / **8,200** / **28,417** | **2** | **2** |
| GPQA | Dynamic FP8 | **178/198** | **2,815** / **8,371** / **27,744** | **1** | **1** |
| GPQA | Static FP8 | **178/198** | **2,966** / **7,832** / **26,431** | **1** | **2** |
| GPQA | NVFP4 W4A16 | 170/198 | **2,965** / **9,667** / **28,433** | **2** | 3 |
| GPQA | NVFP4 W4A4 | 167/198 | **2,876** / **10,996** / **31,986** | **2** | 3 |
| GPQA | NVFP4 W4A4-W8A8 | 172/198 | **2,953** / **10,010** / **35,731** | **2** | 4 |
| MMLU | Original Qwen3.8 27B (FP8) | 444/500 | 205 / 373 / 1,622 | 1 | 0 |
| MMLU | BF16 | **446/500** | **154** / **252** / **779** | 1 | 0 |
| MMLU | Dynamic FP8 | **445/500** | **138** / **271** / **881** | 1 | 0 |
| MMLU | Static FP8 | **450/500** | **154** / **279** / **937** | 1 | 0 |
| MMLU | NVFP4 W4A16 | 439/500 | **159** / **277** / **1,061** | 1 | 0 |
| MMLU | NVFP4 W4A4 | 440/500 | **168** / **306** / **967** | 2 | 0 |
| MMLU | NVFP4 W4A4-W8A8 | 442/500 | **157** / **273** / **778** | **0** | 0 |
| LCB | Original Qwen3.8 27B (FP8) | 83/100 | 8,388 / 24,241 / 94,208 | 13 | 13 |
| LCB | BF16 | **90/100** | **5,073** / **16,033** / **38,911** | **2** | **2** |
| LCB | Dynamic FP8 | **90/100** | **4,791** / **15,866** / **41,168** | **4** | **4** |
| LCB | Static FP8 | **90/100** | **4,511** / **16,027** / **43,992** | **3** | **3** |
| LCB | NVFP4 W4A16 | **91/100** | **5,119** / **15,790** / **47,768** | **4** | **3** |
| LCB | NVFP4 W4A4 | **92/100** | **6,338** / **15,771** / **54,096** | **3** | **3** |
| LCB | NVFP4 W4A4-W8A8 | **88/100** | **4,731** / **15,122** / **41,344** | **2** | **1** |

Bold marks values better than the original (a higher score, or lower P50 / P70 / P90, 94K truncations, or empty answers); values equal to or worse than the original are not bolded.

LCB improves the most: all 13 of the original's 94K truncations ended with empty code (13 truncations, 13 empty answers), and the Coder390 tiers cut this to 2–4. The 3 for W4A4 are problems 0, 53, and 96 (problem ids in the score file), likewise truncated with no code; of the 4 for W4A16, problems 6, 7, and 54 have no code, and problem 53 has 20 characters of code but is wrong; of the 2 for W4A4-W8A8, problem 11 has no code, and problem 6 has 2,338 characters of code but is wrong. On GPQA the original had 4 truncations at the 94K cap and the tiers have 1–2; on MMLU the original had 1 and the tiers have 0–2, with no clear change.

<details open>
<summary>Details for six precisions (bucketed by reasoning length)</summary>

Buckets are "correct / questions in bucket", split by reasoning length, left-closed and right-open.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty | <2K | 2–12K | 12–24K | 24–48K | ≥48K |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| GPQA | BF16 | 178/198 | 3,196 / 8,200 / 28,417 | 2 | 2 | 80/85 | 66/68 | 17/20 | 12/18 | 3/7 |
| GPQA | Dynamic FP8 | 178/198 | 2,815 / 8,371 / 27,744 | 1 | 1 | 78/81 | 68/70 | 18/21 | 11/17 | 3/9 |
| GPQA | Static FP8 | 178/198 | 2,966 / 7,832 / 26,431 | 1 | 2 | 82/84 | 68/74 | 17/19 | 9/17 | 2/4 |
| GPQA | NVFP4 W4A16 | 170/198 | 2,965 / 9,667 / 28,433 | 2 | 3 | 77/80 | 64/70 | 17/21 | 8/17 | 4/10 |
| GPQA | NVFP4 W4A4 | 167/198 | 2,876 / 10,996 / 31,986 | 2 | 3 | 76/82 | 58/60 | 20/23 | 12/26 | 1/7 |
| GPQA | NVFP4 W4A4-W8A8 | 172/198 | 2,953 / 10,010 / 35,731 | 2 | 4 | 79/82 | 58/63 | 19/22 | 14/22 | 2/9 |
| MMLU | BF16 | 446/500 | 154 / 252 / 779 | 1 | 0 | 432/472 | 13/23 | 1/3 | 0/0 | 0/2 |
| MMLU | Dynamic FP8 | 445/500 | 138 / 271 / 881 | 1 | 0 | 436/477 | 8/21 | 0/1 | 0/0 | 1/1 |
| MMLU | Static FP8 | 450/500 | 154 / 279 / 937 | 1 | 0 | 435/469 | 13/27 | 2/3 | 0/0 | 0/1 |
| MMLU | NVFP4 W4A16 | 439/500 | 159 / 277 / 1,061 | 1 | 0 | 427/471 | 11/26 | 0/1 | 1/1 | 0/1 |
| MMLU | NVFP4 W4A4 | 440/500 | 168 / 306 / 967 | 2 | 0 | 426/469 | 13/28 | 0/1 | 0/0 | 1/2 |
| MMLU | NVFP4 W4A4-W8A8 | 442/500 | 157 / 273 / 778 | 0 | 0 | 432/477 | 8/20 | 1/2 | 1/1 | 0/0 |
| LCB | BF16 | 90/100 | 5,073 / 16,033 / 38,911 | 2 | 2 | 40/40 | 25/26 | 11/14 | 9/11 | 5/9 |
| LCB | Dynamic FP8 | 90/100 | 4,791 / 15,866 / 41,168 | 4 | 4 | 38/39 | 25/26 | 11/14 | 12/13 | 4/8 |
| LCB | Static FP8 | 90/100 | 4,511 / 16,027 / 43,992 | 3 | 3 | 39/39 | 24/26 | 13/13 | 12/14 | 2/8 |
| LCB | NVFP4 W4A16 | 91/100 | 5,119 / 15,790 / 47,768 | 4 | 3 | 38/38 | 26/27 | 13/13 | 10/12 | 4/10 |
| LCB | NVFP4 W4A4 | 92/100 | 6,338 / 15,771 / 54,096 | 3 | 3 | 33/33 | 30/31 | 9/11 | 13/14 | 7/11 |
| LCB | NVFP4 W4A4-W8A8 | 88/100 | 4,731 / 15,122 / 41,344 | 2 | 1 | 40/41 | 21/24 | 16/16 | 7/10 | 4/9 |

</details>

### NVFP4 tiers

**Protocol**: one RTX PRO 6000, C8, 100K context, 94,208-token generation cap, no client-side timeout, DFlash2 draft, SGLang; full GPQA 198, MMLU 500, and LCB 100.

| Suite | NVFP4 W4A16 | NVFP4 W4A4 | NVFP4 W4A4-W8A8 |
|---|---:|---:|---:|
| GPQA | 170/198 | 167/198 | 172/198 |
| MMLU | 439/500 | 440/500 | 442/500 |
| LCB | 91/100 | 92/100 | 88/100 |

Reasoning length, 94K truncations, and empty answers for the three NVFP4 tiers are in the "All tiers" table above. LCB correctness is judged by each problem's `pass` field. Raw records: `evaluation/SCORES_NVFP4_W4A16.json`, `evaluation/SCORES_NVFP4_W4A4.json`, and `evaluation/SCORES_NVFP4_MIXED.json` (the W4A4-W8A8 tier).

### NInfer tiers: scores, reasoning length, 94K truncations, and empty answers

**Protocol**: scores carried over from the official triad run on 2026-10-05 on the same NInfer text path; one RTX PRO 6000, official NInfer engine (`iamwavecut/ninfer-all`), C8, 100K context, 94,208 generation cap, client not timed, **no speculation**; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. The packages uploaded now add a Q8 MTP head, the DFlash2 draft, and the proposal head on top of that text path; the text path is unchanged and the full triad was not re-run. Only the NInfer engine can load `.ninfer`; SGLang / vLLM / llama.cpp / transformers cannot.

Reasoning length is `usage.reasoning_tokens` (i.e. `completion_tokens_details.reasoning_tokens`); a 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8).

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | NInfer W4A4 | 177/198 | **2,934** / **7,646** / **25,804** | **2** | **2** |
| GPQA | NInfer W4A4-W8A8 | 177/198 | **3,176** / **8,844** / **24,804** | **2** | **2** |
| MMLU | NInfer W4A4 | **449/500** | **164** / **285** / **830** | **0** | 0 |
| MMLU | NInfer W4A4-W8A8 | 444/500 | **163** / **281** / **923** | **0** | 0 |
| LCB | NInfer W4A4 | **89/100** | **3,994** / **15,533** / **36,125** | **2** | **2** |
| LCB | NInfer W4A4-W8A8 | **92/100** | **4,046** / **15,829** / **40,479** | **2** | **3** |

For NInfer W4A4, the 2 LCB empty answers are problems 11 and 15, both truncated with no code; the 2 GPQA empty answers are problems 79 and 127, both truncated with an empty pred. MMLU has no truncations and no empty answers. For NInfer W4A4-W8A8, the 3 LCB empty answers are problems 17, 53, and 54 (problem 17 stopped normally with no code; 53 and 54 were truncated with no code); the 2 GPQA empty answers are problems 79 and 127, both truncated with an empty pred. MMLU has no truncations and no empty answers.

<details open>
<summary>Details for the two NInfer tiers (by reasoning-length bucket)</summary>

Buckets are "correct / problems in bucket", half-open on the left.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty | <2K | 2–12K | 12–24K | 24–48K | ≥48K |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| GPQA | NInfer W4A4 | 177/198 | 2,934 / 7,646 / 25,804 | 2 | 2 | 76/83 | 69/71 | 17/22 | 14/19 | 1/3 |
| GPQA | NInfer W4A4-W8A8 | 177/198 | 3,176 / 8,844 / 24,804 | 2 | 2 | 79/82 | 70/74 | 13/21 | 12/16 | 3/5 |
| MMLU | NInfer W4A4 | 449/500 | 164 / 285 / 830 | 0 | 0 | 438/480 | 11/19 | 0/1 | 0/0 | 0/0 |
| MMLU | NInfer W4A4-W8A8 | 444/500 | 163 / 281 / 923 | 0 | 0 | 435/478 | 8/21 | 1/1 | 0/0 | 0/0 |
| LCB | NInfer W4A4 | 89/100 | 3,994 / 15,533 / 36,125 | 2 | 2 | 40/41 | 21/23 | 12/14 | 13/16 | 3/6 |
| LCB | NInfer W4A4-W8A8 | 92/100 | 4,046 / 15,829 / 40,479 | 2 | 3 | 38/38 | 26/26 | 14/16 | 11/12 | 3/8 |

</details>

### INT8 W8A8: scores, 94K truncations, and empty answers

**Protocol**: one RTX PRO 6000, vLLM 0.28, C8, 100K context, 94,208 generation cap, client not timed, **no speculation**, reasoning effort xhigh; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. INT8 W8A8 has only the text path and loads only in vLLM.

A 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8); its numbers are in the all-tier table above.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | INT8 W8A8 | 175/198 | **3,862** / **9,055** / **25,299.5** | **1** | **1** |
| MMLU | INT8 W8A8 | **450/500** | **156** / **291** / **864.4** | **0** | 0 |
| LCB | INT8 W8A8 | **91/100** | — | **2** | **0** |

Note: the INT8 W8A8 eval ran vLLM without a reasoning parser, so `usage.reasoning_tokens` is 0 throughout and reasoning plus answer were returned as content. GPQA and MMLU reasoning lengths were recounted from the raw text: the text before `</think>` in the content, counted with the BF16 tokenizer (the same method as the GGUF tiers). The LCB result file kept only the code, not the reasoning text, so it cannot be counted; that cell reads "—".

GPQA's 1 truncation is problem 127, with an empty pred, so it also counts as the empty answer. LCB's 2 truncations are problems 7 and 53: problem 7 left code that raised a runtime error and was judged wrong; problem 53 was truncated, but its code was still judged correct; LCB has no empty answers. MMLU has no truncations and no empty answers. By difficulty, LCB is hard 38/46, medium 30/31, and easy 23/23.

### GGUF Q2 / Q3 / Q4 LynnStyle: scores, reasoning length, 94K truncations, and empty answers

**Protocol**: one RTX PRO 6000, llama.cpp (`llama-server`), C4, about 100K context per slot, 94,208 generation cap, client not timed, thinking on; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. Scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights. The matching `.ninfer` packages under `GGUF-NInfer/` are converted from the same GGUFs; the full triad was run only on the GGUF.

A 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8); its numbers are in the all-tier table above.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q2 LynnStyle | 177/198 | **2,989.5** / **8,923.8** / **27,156.1** | **3** | **0** |
| MMLU | GGUF Q2 LynnStyle | 433/500 | **181** / **326.3** / **1,020.5** | 1 | 0 |
| LCB | GGUF Q2 LynnStyle | **90/100** | **5,656.5** / **17,835.8** / **40,067.3** | **1** | **1** |
| GPQA | GGUF Q3 LynnStyle | 173/198 | **3,125.5** / **7,265.2** / **24,343.1** | **1** | **1** |
| MMLU | GGUF Q3 LynnStyle | **449/500** | — | **0** | 0 |
| LCB | GGUF Q3 LynnStyle | **92/100** | — | **1** | **1** |
| GPQA | GGUF Q4 LynnStyle | 175/198 | **2,951.0** / **8,159.3** / **25,649.0** | **1** | **2** |
| MMLU | GGUF Q4 LynnStyle | **448/500** | — | **0** | 0 |
| LCB | GGUF Q4 LynnStyle | **89/100** | — | **2** | **2** |

Note: reasoning lengths are counted from the raw text with the BF16 tokenizer (GPQA/LCB: `reasoning` field; MMLU: text before the last line of `response`). Q3 and Q4 LynnStyle MMLU / LCB have no saved reasoning text and cannot be counted; those cells read "—".

### GGUF Q6_K: scores, reasoning length, 94K truncations, and empty answers

**Protocol**: one RTX PRO 6000, llama.cpp (`llama-server`) loading `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`, C4, 100K context, 94,208 generation cap, client not timed, reasoning effort xhigh; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong, truncations that still answer correctly count as correct, and every failure stays in the denominator. `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` is converted from the same GGUF with the same backbone quantization; the full triad was run only on the GGUF.

Reasoning length is `usage.reasoning_tokens`; a 94K truncation means the generation cap was hit. LCB empty answers are the number of problems for which no runnable code could be extracted. Bold means better than the original Qwen3.8 27B (FP8); its numbers are in the all-tier table above.

| Suite | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q6_K | 174/198 | **3,683** / **9,814** / **27,966** | **2** | **2** |
| MMLU | GGUF Q6_K | **448/500** | **162** / **310.3** / **939.4** | **0** | 0 |
| LCB | GGUF Q6_K | **91/100** | — | **0** | **1** |

Note: for MMLU and LCB, llama.cpp did not return reasoning tokens separately (`usage` has no `reasoning_tokens`). MMLU reasoning length is the text before the last line of `response`, counted with the BF16 tokenizer (the same method as Q8_0); the LCB result file kept no reasoning text, so it cannot be counted and reads "—". GPQA reasoning tokens were counted separately by the eval script.

GPQA's 2 truncations are problems 79 and 127; both hit 94,208 with an empty pred, so they also count as the empty answers. MMLU has no truncations and no empty answers.

LCB has no 94K truncations; its 1 empty answer is problem 92, which stopped normally without producing code.

LCB is scored on llama.cpp: the LCB eval script gets replies from NInfer that are not valid JSON. This is a compatibility issue between the eval script and the API, not a model-quality issue; the same GGUF on llama.cpp passed every problem in the same spot-check batch.


### GGUF Q8_0: scores, reasoning length, 94K truncations, and empty answers

**Protocol**: single RTX PRO 6000, llama.cpp (`llama-server`) loading `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`, C4, 100K context, generation cap 94,208, no client timeout, thinking xhigh; full GPQA 198 / MMLU 500 / LCB 100; empty answers count as wrong; truncated-but-correct counts as correct. `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer` is converted from the same GGUF; the full triad was run on GGUF only.

Reasoning length: GPQA from `usage.reasoning_tokens`; MMLU from text before the last newline of `response`, counted with the BF16 tokenizer; LCB from saved `reasoning` text. 94K truncation means hitting the generation cap. LCB empty means no runnable code was extracted. Bold beats original Qwen3.8 27B (FP8).

| Bench | Precision | Score | Reasoning P50 / P70 / P90 | 94K trunc. | Empty |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q8_0 | 171/198 | **3,102.5** / **7,971** / **28,891.6** | **2** | **0** |
| MMLU | GGUF Q8_0 | 443/500 | **164** / **291** / **741** | **0** | 0 |
| LCB | GGUF Q8_0 | **90/100** | **4,098.5** / **16,087.8** / **39,135.5** | **3** | **3** |

GPQA: 2 truncations, 0 empty. MMLU: 0 / 0. LCB: 3 truncations, 3 empty (length with no code).

LCB is scored on llama.cpp: the LCB harness gets non-JSON replies from NInfer — a harness issue, not model quality.


## Quantization tiers

| Tier | Directory | Notes | Package size (bytes) | BPW | GPQA / MMLU / LCB |
|---|---|---|---:|---:|---|
| BF16 | `BF16/` | Fully multimodal, original config, official BF16 MTP bundled, DFlash2 draft included, no patches needed | 55,583,125,732 (≈51.8 GiB) | 16.00 | 178 / 446 / 90 |
| Static FP8 Block128 | `FP8/` | Fully multimodal, official BF16 MTP bundled, DFlash2 draft included | 33,669,220,491 (≈31.4 GiB) | 9.00 | 178 / 450 / 90 |
| NVFP4 W4A16 | `NVFP4/W4A16/` | Fully multimodal, language-model Linear layers with NVFP4 weights + BF16 activations, official BF16 MTP bundled, DFlash2 draft included, no patches needed in SGLang | 20,613,406,953 (≈19.2 GiB, excluding the draft) | 5.93 | 170 / 439 / 91 |
| NVFP4 W4A4 | `NVFP4/W4A4/` | Fully multimodal, language-model Linear layers with NVFP4 weights + NVFP4 activations, official BF16 MTP bundled, DFlash2 draft included, no patches needed in SGLang | 20,613,386,462 (≈19.2 GiB, excluding the draft) | 5.93 | 167 / 440 / 92 |
| NVFP4 W4A4-W8A8 | `NVFP4/W4A4-W8A8/` | Fully multimodal, language-model MLP layers in NVFP4 W4A4 and attention / linear-attention projections in FP8 W8A8, official BF16 MTP bundled, DFlash2 draft included, no patches needed in SGLang | 23,769,634,648 (≈22.1 GiB, excluding the draft) | 6.84 | 172 / 442 / 88 |
| NInfer W4A4 | `NVFP4-NInfer/W4A4/` | Official NInfer package (`.ninfer`), W4A4 text path with a Q8 MTP head, the DFlash2 draft, and the proposal head built in; the vision tower is not in the package, so no image input under NInfer (NInfer cannot load the `vision-bf16.safetensors` in the same folder); loadable only by the NInfer engine (`iamwavecut/ninfer-all`) | 23,477,856,260 (≈21.9 GiB) | 6.76 | 177 / 449 / 89 |
| NInfer W4A4-W8A8 | `NVFP4-NInfer/W4A4-W8A8/` | Official NInfer mixed-precision package (`.ninfer`), W4A4-W8A8 text path with a Q8 MTP head, the DFlash2 draft, and the proposal head built in; the vision tower is not in the package, so no image input under NInfer (NInfer cannot load the `vision-bf16.safetensors` in the same folder); loadable only by the NInfer engine (`iamwavecut/ninfer-all`) | 23,477,856,260 (≈21.9 GiB) | 6.76 | 177 / 444 / 92 |
| NInfer W4A4 text-only | `NVFP4-NInfer/W4A4/` | Official NInfer package (`.ninfer`), text path only: no MTP, no vision tower, no DFlash2 draft, so it runs without speculation only; loadable only by the NInfer engine (`iamwavecut/ninfer-all`) | 20,752,974,596 (≈19.3 GiB) | 6.17 | Not separately evaluated |
| NInfer W4A4-W8A8 text-only | `NVFP4-NInfer/W4A4-W8A8/` | Official NInfer mixed-precision package (`.ninfer`), text path only: no MTP, no vision tower, no DFlash2 draft, so it runs without speculation only; loadable only by the NInfer engine (`iamwavecut/ninfer-all`) | 20,752,974,596 (≈19.3 GiB) | 6.17 | Not separately evaluated |
| INT8 W8A8 | `INT8/W8A8/` | Text-only (`Qwen3_5ForCausalLM`): SmoothQuant per-channel INT8 weights + per-token dynamic INT8 activations in compressed-tensors format; does not include the vision tower, MTP, or the DFlash2 draft; loadable only by vLLM | 29,500,937,028 (≈27.5 GiB) | 8.77 | 175 / 450 / 91 |
| GGUF Q3 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF (`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf`): lowest type Q3; **built-in Q4 MTP**; vision external | 17,303,770,432 (~16.1 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer from Q3 LynnStyle GGUF; built-in Q4 MTP; NInfer-all only | 17,300,551,168 (~16.1 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q4 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF (`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf`): lowest type Q4; **built-in Q4 MTP**; vision external | 19,620,406,592 (~18.3 GiB) | 5.75 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer from Q4 LynnStyle GGUF; built-in Q4 MTP; NInfer-all only | 19,617,187,328 (~18.3 GiB) | 5.74 | 175 / 448 / 89 |
| GGUF Q2 LynnStyle | `GGUF/` | Mixed-precision LynnStyle GGUF (`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf`): lowest type Q2; **built-in Q4 MTP**; vision external | 13,276,009,792 (~12.4 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · NInfer | `GGUF-NInfer/` | NInfer from Q2 LynnStyle GGUF; built-in Q4 MTP; NInfer-all only | 13,272,798,720 (~12.4 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q8_0 | `GGUF/` | GGUF single file for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`): Q8_0 backbone, built-in MTP head, no external draft; llama.cpp vision via `--mmproj` with the mmproj in `GGUF/` | 29,069,202,688 (~27.1 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q8_0 · NInfer | `GGUF-NInfer/` | NInfer package converted from the same Q8_0 GGUF (`.ninfer`), built-in MTP head; loadable only by NInfer-all (`iamwavecut/ninfer-all`); scores from the same GGUF on llama.cpp | 29,065,983,488 (~27.1 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q6_K | `GGUF/` | Single GGUF file for llama.cpp (`Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`): Q6_K backbone with imatrix calibration and a built-in Q8 MTP head, so no external draft is needed; llama.cpp vision via `--mmproj` with the mmproj in `GGUF/` | 23,177,516,384 (≈21.6 GiB) | 6.79 | 174 / 448 / 91 |
| GGUF Q6_K · NInfer | `GGUF-NInfer/` | NInfer package (`.ninfer`) converted from the same GGUF, same backbone quantization, built-in MTP head (attention/MLP weights Q6_K, input projection Q8_0), no vision tower in the package, so no image input under NInfer; loadable only by NInfer-all (`iamwavecut/ninfer-all`); scores measured on the same GGUF with llama.cpp | 23,084,144,128 (≈21.5 GiB) | 6.76 | 174 / 448 / 91 |

BPW (bits per weight) is the effective average bit width of the whole package: the total bytes of the main-model weight files (`.safetensors`, including the vision tower, MTP, and scale tensors, excluding the DFlash2 draft) × 8 ÷ total parameter count. The parameter count is taken from the safetensors headers and is identical across the five tiers at 27,781,427,952 (an NVFP4 packed U8 tensor counts 2 elements per byte; scale tensors add no elements). The weight-file totals for BF16, static FP8, NVFP4 W4A16, NVFP4 W4A4, and NVFP4 W4A4-W8A8 are 55,563,008,568, 31,242,033,200, 20,593,097,872, 20,593,145,056, and 23,749,329,544 bytes respectively. Every tier is mixed precision (different layers use different bit widths), so the nominal bit width can mislead; BPW reflects quality density per unit of size.

BPW for the two NInfer tiers is the whole `.ninfer` file bytes × 8 ÷ total parameter count 27,781,427,952: both files are 23,477,856,260 bytes, so BPW is 6.76 for each. Each `.ninfer` package includes the Q8 MTP head, the DFlash2 draft, and the proposal head, but not the vision tower; the safetensors-based BPW above for NVFP4 / BF16 / FP8 excludes the DFlash2 draft, so the two formulas differ and BPW should not be compared directly across those families.

The two NInfer text-only packages contain only the text path, so their BPW is the `.ninfer` file bytes × 8 ÷ the text parameter count 26,895,998,464 (the same denominator as INT8 W8A8 below): both files are 20,752,974,596 bytes, so BPW is 6.17 for each. Because the denominator differs from 27,781,427,952, BPW should not be compared directly with the NInfer MTP packages or the NVFP4 tiers.

INT8 W8A8 has only the text path, so its BPW is the total bytes of its 8 `.safetensors` weight files, 29,480,791,128, × 8 ÷ the text parameter count 26,895,998,464, giving 8.77. The text parameter count comes from this package's safetensors headers (INT8 and BF16 tensors count their elements; scale tensors add no elements) and equals the BF16 package's count without the vision tower (460,730,096) and MTP (424,699,392); because the denominator differs from the 27,781,427,952 used above, BPW should not be compared directly with the other tiers.

BPW for the two GGUF Q6_K packages is the single file's bytes × 8 ÷ the text + MTP parameter count 27,320,697,856: the GGUF is 23,177,516,384 bytes, giving 6.79, and the NInfer package is 23,084,144,128 bytes, giving 6.76. The parameter count comes from the GGUF header (866 tensors: text 26,895,998,464 + MTP 424,699,392); vision is an external mmproj, not in the package and not in the denominator. Because the denominator differs from both the 27,781,427,952 used above and the 26,895,998,464 used for INT8 W8A8, BPW should not be compared directly with the other tiers.

- Each tier carries its own copy of the DFlash2 draft (identical files, 2,407,384,680 bytes): `FP8/DFlash2-FP8/`, `BF16/DFlash2-FP8/`, `NVFP4/W4A16/DFlash2-FP8/`, `NVFP4/W4A4/DFlash2-FP8/`, and `NVFP4/W4A4-W8A8/DFlash2-FP8/`.
- DFlash2 draft format: FP8 E4M3 weights with 128×128 block scales (`weight_scale_inv`), the same format as the FP8 body; q/k/v projections, `fc`, the candidate selector, convolutions and norms stay BF16. It replaced the earlier per-tensor-scale draft on 2026-10-08 (engines that only read block scales, such as radiance, loaded the old draft without error but accepted almost no draft tokens). The new draft is verified by format and SGLang source check; an engine re-test is pending. The DFlash2 speed numbers in this card were measured with the earlier draft.
- Speed figures for BF16 and static FP8 were measured on the static FP8 package (BF16 was not benchmarked separately and shares the same figures); the three NVFP4 tiers were each benchmarked on their own package.
- NVFP4 scores were measured on a single GPU at C8; see "NVFP4 tiers" above for the protocol.
- NInfer tier scores are carried over from the 2026-10-05 triad on the same text path (single GPU, C8, official NInfer, no speculation); see the NInfer tiers section above. NInfer speeds were measured separately on the new packages; see "NInfer tiers" under Best-TPS and concurrency recommendations below.
- INT8 W8A8 scores are a full triad measured on a single GPU at C8 with vLLM and no speculation; see the INT8 W8A8 section above for the protocol. Its speeds come from a quick benchmark; see "INT8 W8A8" under Best-TPS and concurrency recommendations below.
- GGUF Q6_K scores are a full triad measured on a single GPU at C4 with llama.cpp; see the GGUF Q6_K section above for the protocol. Its speeds come from a quick benchmark; see "GGUF Q6_K" under Best-TPS and concurrency recommendations below.
- The two NInfer tiers are under `NVFP4-NInfer/W4A4/` and `NVFP4-NInfer/W4A4-W8A8/`, INT8 W8A8 is under `INT8/W8A8/`, and GGUF Q2 / Q3 / Q4 LynnStyle, Q6_K, and Q8_0 are under `GGUF/` and `GGUF-NInfer/`.

## Best-TPS and concurrency recommendations

Environment: one RTX PRO 6000 Blackwell 96GB; SGLang, 32K context (32,768), 4,096-token generation cap, thinking enabled, model-default sampling.

| Goal | Pick | Aggregate tok/s | Per-request tok/s |
|---|---|---:|---:|
| Fastest single request | DFlash2 · C1 | 146.7 | **180.3** |
| Highest aggregate throughput | DFlash2 · C16 | **1,057.5** | 93.6 |
| Balanced daily use | DFlash2 · C8 | 646.3 | 113.9 |
| MTP only: fastest single request | MTP · C1 | 82.1 | **91.1** |
| MTP only: highest aggregate throughput | MTP · C16 | **612.7** | 60.1 |
| MTP only: balanced daily use | MTP · C8 | 380.3 | 71.1 |

- **Which speculation**: at every measured concurrency (C1–C16), DFlash2 beats MTP on both aggregate and per-request speed. Use DFlash2 whenever you can.
- **When to use MTP**: on vLLM (DFlash2 has only been validated on SGLang), or when you do not want to load the separate DFlash2 draft. If you run MTP only: use C1 for the fastest single request (91.1 tok/s), C4 for interactive use with a few users (293.3 aggregate, 84.0 per request), C8 for shared serving (380.3 aggregate, 71.1 per request), and C16 when only total throughput matters (612.7 aggregate, 60.1 per request).
- **Concurrency**: C1–C4 for interactive use, C8 for shared or batch serving, C16 when only total throughput matters. Concurrency above C16 was not tested.

<details>
<summary>Full measured table</summary>

C1 is the main run (4 requests); C4/C8/C16 are reruns with more requests (6×C per cell). "vs. no spec" is the ratio of aggregate throughput at the same concurrency.

| Speculation | Concurrency | Aggregate tok/s | Per-request decode tok/s (median) | TTFT s (median) | Accept length | Accept rate | vs. no spec |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP (bundled BF16) | C1 | 82.1 | 91.1 | 0.12 | 2.858 | 0.619 | 1.82× |
| MTP (bundled BF16) | C4 | 293.3 | 84.0 | 0.15 | 2.844 | 0.615 | 1.96× |
| MTP (bundled BF16) | C8 | 380.3 | 71.1 | 0.16 | 2.813 | 0.604 | 1.34× |
| MTP (bundled BF16) | C16 | 612.7 | 60.1 | 0.17 | 2.747 | 0.582 | 1.45× |
| DFlash2 | C1 | 146.7 | 180.3 | 0.12 | 4.289 | 0.470 | 3.25× |
| DFlash2 | C4 | 384.9 | 124.4 | 0.16 | 3.982 | 0.425 | 2.57× |
| DFlash2 | C8 | 646.3 | 113.9 | 0.15 | 4.131 | 0.447 | 2.28× |
| DFlash2 | C16 | 1,057.5 | 93.6 | 0.24 | 4.017 | 0.431 | 2.50× |
| No speculation | C1 | 45.1 | 45.6 | 0.11 | n/a | n/a | 1.00× |
| No speculation | C4 | 149.5 | 42.2 | 0.13 | n/a | n/a | 1.00× |
| No speculation | C8 | 283.0 | 41.7 | 0.12 | n/a | n/a | 1.00× |
| No speculation | C16 | 422.8 | 38.4 | 0.13 | n/a | n/a | 1.00× |

| Speculation | Fastest per request | Recommended (highest aggregate with per-request speed ≥ 60% of C1) | Highest aggregate |
|---|---|---|---|
| MTP | C1 (91.1 tok/s) | C16 (612.7 tok/s, 60.1 per request) | C16 |
| DFlash2 | C1 (180.3 tok/s) | C8 (646.3 tok/s, 113.9 per request) | C16 (1,057.5 tok/s) |
| No speculation | C1 (45.6 tok/s) | C16 (422.8 tok/s) | C16 |

</details>

### NVFP4 tiers

Same environment as above: one RTX PRO 6000 Blackwell 96GB; SGLang, 32K context (32,768), 4,096-token generation cap, thinking enabled, model-default sampling. Data from `evaluation/BENCH_NVFP4_W4A16.json`, `evaluation/BENCH_NVFP4_W4A4.json`, and `evaluation/BENCH_NVFP4_MIXED.json` (the W4A4-W8A8 tier).

| Goal | Pick | W4A16 aggregate tok/s | W4A16 per-request tok/s | W4A4 aggregate tok/s | W4A4 per-request tok/s | W4A4-W8A8 aggregate tok/s | W4A4-W8A8 per-request tok/s |
|---|---|---:|---:|---:|---:|---:|---:|
| Fastest single request | DFlash2 · C1 | 147.4 | **218.4** | 188.6 | **211.5** | 175.1 | **216.8** |
| Highest aggregate throughput | DFlash2 · C16 | **1,012.3** | 96.6 | **1,143.2** | 121.1 | **1,146.4** | 105.5 |
| Balanced daily use | DFlash2 · C8 | 472.4 | 131.7 | 689.8 | 132.4 | 627.9 | 132.4 |
| MTP only: fastest single request | MTP · C1 | 101.1 | **128.9** | 104.7 | **124.5** | 99.9 | **116.3** |
| MTP only: highest aggregate throughput | MTP · C16 | **817.3** | 70.6 | **912.4** | 73.0 | **580.2** | 69.4 |
| MTP only: balanced daily use | MTP · C8 | 450.7 | 91.3 | 355.5 | 86.6 | 417.2 | 83.2 |

- **Which speculation**: on W4A4 and W4A4-W8A8, DFlash2 beats MTP on both aggregate and per-request speed at every measured concurrency (C1–C16). On W4A16, MTP has the higher aggregate only at C4 (351.4 vs. 315.2); DFlash2 is faster at every other level and on per-request speed throughout.
- **MTP only**: on W4A16, use C1 for the fastest single request (128.9 tok/s), C4 for interactive use with a few users (351.4 aggregate, 108.0 per request), C8 for shared serving (450.7 aggregate, 91.3 per request), and C16 when only total throughput matters (817.3 aggregate, 70.6 per request). On W4A4 the same levels give C1 124.5 tok/s, C4 323.2 / 103.9, C8 355.5 / 86.6, and C16 912.4 / 73.0; on W4A4-W8A8, C1 116.3 tok/s, C4 213.0 / 99.8, C8 417.2 / 83.2, and C16 580.2 / 69.4 (aggregate / per request).
- **Accept length**: MTP 2.608–2.967 (W4A16), 2.597–2.923 (W4A4), and 2.647–2.865 (W4A4-W8A8); DFlash2 3.351–4.143 (W4A16), 3.723–4.327 (W4A4), and 3.828–4.364 (W4A4-W8A8).
- **Concurrency**: above C16 was not tested.

<details>
<summary>NVFP4 W4A16 full measured table</summary>

Requests per level: 4 at C1, 12 at C4, 24 at C8, 48 at C16. "vs. no spec" is the ratio of aggregate throughput at the same concurrency.

| Speculation | Concurrency | Aggregate tok/s | Per-request decode tok/s (median) | TTFT s (median) | Accept length | Accept rate | vs. no spec |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP (bundled BF16) | C1 | 101.1 | 128.9 | 0.11 | 2.608 | 0.537 | 1.44× |
| MTP (bundled BF16) | C4 | 351.4 | 108.0 | 0.13 | 2.796 | 0.599 | 2.34× |
| MTP (bundled BF16) | C8 | 450.7 | 91.3 | 0.13 | 2.743 | 0.581 | 1.50× |
| MTP (bundled BF16) | C16 | 817.3 | 70.6 | 0.15 | 2.967 | 0.656 | 1.58× |
| DFlash2 | C1 | 147.4 | 218.4 | 0.10 | 3.469 | 0.353 | 2.11× |
| DFlash2 | C4 | 315.2 | 164.9 | 0.13 | 3.351 | 0.337 | 2.10× |
| DFlash2 | C8 | 472.4 | 131.7 | 0.14 | 3.454 | 0.351 | 1.57× |
| DFlash2 | C16 | 1,012.3 | 96.6 | 0.23 | 4.143 | 0.449 | 1.96× |
| No speculation | C1 | 70.0 | 71.6 | 0.09 | n/a | n/a | 1.00× |
| No speculation | C4 | 150.3 | 62.1 | 0.10 | n/a | n/a | 1.00× |
| No speculation | C8 | 300.9 | 62.1 | 0.10 | n/a | n/a | 1.00× |
| No speculation | C16 | 515.8 | 54.7 | 0.10 | n/a | n/a | 1.00× |

| Speculation | Fastest per request | Recommended (highest aggregate with per-request speed ≥ 60% of C1) | Highest aggregate |
|---|---|---|---|
| MTP | C1 (128.9 tok/s) | C8 (450.7 tok/s, 91.3 per request) | C16 (817.3 tok/s) |
| DFlash2 | C1 (218.4 tok/s) | C8 (472.4 tok/s, 131.7 per request) | C16 (1,012.3 tok/s) |
| No speculation | C1 (71.6 tok/s) | C16 (515.8 tok/s) | C16 (515.8 tok/s) |

</details>

<details>
<summary>NVFP4 W4A4 full measured table</summary>

Requests per level: 4 at C1, 12 at C4, 24 at C8, 48 at C16. "vs. no spec" is the ratio of aggregate throughput at the same concurrency.

| Speculation | Concurrency | Aggregate tok/s | Per-request decode tok/s (median) | TTFT s (median) | Accept length | Accept rate | vs. no spec |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP (bundled BF16) | C1 | 104.7 | 124.5 | 0.15 | 2.685 | 0.562 | 1.48× |
| MTP (bundled BF16) | C4 | 323.2 | 103.9 | 0.18 | 2.597 | 0.531 | 2.04× |
| MTP (bundled BF16) | C8 | 355.5 | 86.6 | 0.17 | 2.683 | 0.561 | 1.12× |
| MTP (bundled BF16) | C16 | 912.4 | 73.0 | 0.18 | 2.923 | 0.641 | 1.86× |
| DFlash2 | C1 | 188.6 | 211.5 | 0.14 | 4.327 | 0.476 | 2.66× |
| DFlash2 | C4 | 456.1 | 182.1 | 0.16 | 4.011 | 0.430 | 2.88× |
| DFlash2 | C8 | 689.8 | 132.4 | 0.17 | 3.723 | 0.389 | 2.18× |
| DFlash2 | C16 | 1,143.2 | 121.1 | 0.28 | 3.985 | 0.427 | 2.33× |
| No speculation | C1 | 70.9 | 72.0 | 0.13 | n/a | n/a | 1.00× |
| No speculation | C4 | 158.3 | 62.8 | 0.15 | n/a | n/a | 1.00× |
| No speculation | C8 | 316.8 | 62.5 | 0.14 | n/a | n/a | 1.00× |
| No speculation | C16 | 490.5 | 55.2 | 0.14 | n/a | n/a | 1.00× |

| Speculation | Fastest per request | Recommended (highest aggregate with per-request speed ≥ 60% of C1) | Highest aggregate |
|---|---|---|---|
| MTP | C1 (124.5 tok/s) | C8 (355.5 tok/s, 86.6 per request) | C16 (912.4 tok/s) |
| DFlash2 | C1 (211.5 tok/s) | C8 (689.8 tok/s, 132.4 per request) | C16 (1,143.2 tok/s) |
| No speculation | C1 (72.0 tok/s) | C16 (490.5 tok/s) | C16 (490.5 tok/s) |

</details>

<details>
<summary>NVFP4 W4A4-W8A8 full measured table</summary>

Requests per level: 4 at C1, 12 at C4, 24 at C8, 48 at C16. "vs. no spec" is the ratio of aggregate throughput at the same concurrency.

| Speculation | Concurrency | Aggregate tok/s | Per-request decode tok/s (median) | TTFT s (median) | Accept length | Accept rate | vs. no spec |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP (bundled BF16) | C1 | 99.9 | 116.3 | 0.17 | 2.865 | 0.621 | 1.61× |
| MTP (bundled BF16) | C4 | 213.0 | 99.8 | 0.19 | 2.667 | 0.555 | 1.09× |
| MTP (bundled BF16) | C8 | 417.2 | 83.2 | 0.18 | 2.647 | 0.549 | 1.33× |
| MTP (bundled BF16) | C16 | 580.2 | 69.4 | 0.19 | 2.772 | 0.591 | 1.24× |
| DFlash2 | C1 | 175.1 | 216.8 | 0.16 | 4.201 | 0.458 | 2.82× |
| DFlash2 | C4 | 395.0 | 152.4 | 0.19 | 3.995 | 0.427 | 2.02× |
| DFlash2 | C8 | 627.9 | 132.4 | 0.19 | 3.828 | 0.404 | 2.00× |
| DFlash2 | C16 | 1,146.4 | 105.5 | 0.30 | 4.364 | 0.479 | 2.44× |
| No speculation | C1 | 62.2 | 63.0 | 0.15 | n/a | n/a | 1.00× |
| No speculation | C4 | 195.7 | 56.4 | 0.17 | n/a | n/a | 1.00× |
| No speculation | C8 | 314.0 | 53.4 | 0.16 | n/a | n/a | 1.00× |
| No speculation | C16 | 469.4 | 47.7 | 0.16 | n/a | n/a | 1.00× |

| Speculation | Fastest per request | Recommended (highest aggregate with per-request speed ≥ 60% of C1) | Highest aggregate |
|---|---|---|---|
| MTP | C1 (116.3 tok/s) | C8 (417.2 tok/s, 83.2 per request) | C16 (580.2 tok/s) |
| DFlash2 | C1 (216.8 tok/s) | C8 (627.9 tok/s, 132.4 per request) | C16 (1,146.4 tok/s) |
| No speculation | C1 (63.0 tok/s) | C16 (469.4 tok/s) | C16 (469.4 tok/s) |

</details>

### NInfer tiers

Setup: one RTX PRO 6000 Blackwell; official NInfer with the same context flags as the NInfer launch commands below (`--max-context 102400 --kv-capacity 819200 --max-concurrency 8 --kv-dtype fp8`); 4,096 generation cap, thinking on (template default xhigh), sampling temperature 1.0, top_p 0.95, top_k 20, same prompts as the NVFP4 benchmark above; 4 requests at C1, 12 at C4, 24 at C8. MTP uses 4 draft tokens and DFlash2 uses 8, both with `--lm-head-draft`. Numbers are aggregate decode tok/s. NInfer supports at most 8 concurrent requests, so C16 was not tested.

| Speculation | Tier | C1 | C4 | C8 |
|---|---|---:|---:|---:|
| No speculation | NInfer W4A4 | 68.1 | 195.8 | 306.8 |
| No speculation | NInfer W4A4-W8A8 | 68.1 | 236.1 | 369.5 |
| MTP (4 draft tokens) | NInfer W4A4 | 154.8 | 498.3 | 678.3 |
| MTP (4 draft tokens) | NInfer W4A4-W8A8 | 162.5 | 367.6 | 663.9 |
| DFlash2 (8 draft tokens) | NInfer W4A4 | 207.1 | 539.6 | 975.9 |
| DFlash2 (8 draft tokens) | NInfer W4A4-W8A8 | 199.1 | 650.1 | 804.9 |

- **Best setting**: for both tiers and all three modes, aggregate throughput peaks at C8. NInfer W4A4 tops out with DFlash2 · C8 (975.9 tok/s) and NInfer W4A4-W8A8 with DFlash2 · C8 (804.9 tok/s); with MTP only, C8 gives 678.3 and 663.9 tok/s respectively.
- **C8 versus NVFP4 W4A4 (SGLang)**: NInfer W4A4 reaches 306.8 vs 316.8 with no speculation, 678.3 vs 355.5 with MTP, and 975.9 vs 689.8 tok/s with DFlash2. The engines and context settings differ, so treat this as a rough comparison.

### INT8 W8A8

Setup: one RTX PRO 6000 Blackwell; vLLM 0.28 with `--max-model-len 102400` and `--max-num-seqs 8`; 512 generation cap, thinking on (xhigh), sampling temperature 1.0, top_p 0.95, top_k 20; each level sends only as many requests as its concurrency (1 at C1, 2 at C2, 4 at C4, 8 at C8). This is a quick benchmark with few requests and short outputs, so the numbers are not directly comparable with the tiers above. Numbers are aggregate tok/s (all output tokens ÷ wall-clock time). Both rows were measured on a separate, unreleased comparison build with MTP (the same INT8 text weights plus one BF16 MTP layer); with no speculation the MTP layer is not used. This package does not include MTP.

| Speculation | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| No speculation | 30.8 | 45.5 | 101.2 | **177.3** |
| MTP (comparison only; not in this package) | 23.9 | 37.8 | 72.5 | 145.9 |

- **Recommendation**: no speculation at C8 (177.3 tok/s); aggregate throughput rises with concurrency, and nothing above C8 was tested.
- **Do not enable MTP**: the model has only 1 MTP layer, so `num_speculative_tokens=3` calls the same layer repeatedly; acceptance is low and every level from C1–C8 is slower than no speculation. This tier also has no DFlash2 draft.

### GGUF Q6_K

Setup: one RTX PRO 6000 Blackwell; 1-minute quick benchmark, 512 generation cap, thinking on (xhigh), sampling temperature 1.0, top_p 0.95, top_k 20; each level sends only as many requests as its concurrency (1 at C1, 2 at C2, 4 at C4, 8 at C8). Numbers are aggregate tok/s (all output tokens ÷ wall-clock time). This is a quick benchmark with few requests and short outputs, so the numbers are not directly comparable with the full SGLang / NInfer benchmarks above. NInfer rows were measured on the `GGUF-NInfer/` package with the server at `--max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 --max-concurrency 8`; llama.cpp rows were measured on the `GGUF/` package.

| Engine · speculation | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · MTP (3 draft tokens) | 131.9 | 161.9 | **235.5** | 388.1 |
| NInfer · no speculation | 56.0 | 93.9 | 162.1 | 298.1 |
| llama.cpp · MTP | 97.2 | 95.3 | 168.1 | 189.0 |
| llama.cpp · no speculation | 53.4 | not measured | 123.0 | not measured |

- **Recommendation**: NInfer + C4 + MTP (235.5 tok/s), matching the recommended launch command below (`--max-concurrency 4`). For aggregate throughput alone, C8 is higher (388.1 tok/s); raise `--max-concurrency` to 8 for that.
- **MTP is built in**: both packages carry a built-in MTP head (GGUF: Q8_0; NInfer: Q6_K attention/MLP weights), so no external draft model is needed. For a single request, NInfer with MTP reaches 131.9 tok/s, about 2.5× llama.cpp without speculation (53.4 tok/s); llama.cpp with MTP reaches 97.2 tok/s aggregate at C1 (119.0 tok/s single-request decode).


### GGUF Q8_0

Hardware: single RTX PRO 6000 Blackwell. llama.cpp rows use the quick protocol (thinking on, fused MTP): C1=4 requests, C2=6, C4=12; aggregate decode tok/s. NInfer rows use the same-caliber bench (thinking on, template default xhigh, max_tokens 4096, temperature 1.0, top_p 0.95, top_k 20; C1=4, C4=12, C8=24; MTP draft-tokens 4).

| Engine · speculation | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · MTP (draft 4) | 109.5 | not measured | 332.0 | **486.3** |
| llama.cpp · MTP | 85.3 | 133.6 | **190.8** | not measured |

- **Recommended**: NInfer + C8 + MTP (486.3 tok/s). Fastest llama.cpp point is C4 MTP (190.8 tok/s).
- **MTP built in**: both packages carry an MTP head; no external draft model.


## Recommended launch commands

### Quantization scheme

- **BF16** (`BF16/`): all weights in BF16 with the original multimodal config (mrope retained, `mtp_num_hidden_layers=1`) and no `quantization_config`.
- **Static FP8** (`FP8/`): official-style static FP8, E4M3 weights in 128×128 blocks with one scale per block (`weight_scale_inv`); activations use dynamic FP8. The config only adds a top-level FP8 `quantization_config`.
- **NVFP4 W4A16** (`NVFP4/W4A16/`): ModelOpt local-Hessian calibration. NVFP4 is E2M1 in 16-element blocks with one E4M3 scale per block plus a per-tensor FP32 second-level scale. MLP gate/up/down, full-attention q/k/v/o, and linear-attention `in_proj_qkv` / `in_proj_z` / `out_proj` (400 Linear layers) use NVFP4 weights with BF16 activations; linear-attention `in_proj_a` / `in_proj_b` and `lm_head` (97 layers) stay in BF16. The quantization metadata uses ModelOpt's `MIXED_PRECISION` format (each of the 400 layers tagged `W4A16_NVFP4`), which SGLang detects as `modelopt_mixed`. 1,999 tensors: 1,651 language, 333 vision, 15 MTP.
- **NVFP4 W4A4** (`NVFP4/W4A4/`): same calibration data and algorithm and the same 400 Linear layers, with both weights and activations in NVFP4 (activations are quantized at inference in 16-element blocks). Standard `NVFP4` export, detected by SGLang as `modelopt_fp4`. 2,399 tensors: 2,051 language, 333 vision, 15 MTP.
- **NVFP4 W4A4-W8A8** (`NVFP4/W4A4-W8A8/`): mixed precision with the same calibration data and algorithm. MLP gate/up/down (192 Linear layers) use NVFP4 W4A4 (both weights and activations in NVFP4; activations are quantized at inference in 16-element blocks); full-attention q/k/v/o and linear-attention `in_proj_qkv` / `in_proj_z` / `out_proj` (208 Linear layers) use FP8 W8A8 (E4M3 weights and activations with static per-tensor scales; activation scales come from calibration); linear-attention `in_proj_a` / `in_proj_b` and `lm_head` (97 layers) stay in BF16. The quantization metadata uses ModelOpt's `MIXED_PRECISION` format (each layer tagged `NVFP4` or `FP8`), which SGLang detects as `modelopt_mixed`. 2,191 tensors: 1,843 language, 333 vision, 15 MTP.
- **NVFP4 calibration data**: complete trajectories (prompt + reasoning + final answer) that were correct and non-empty, taken from this model's own RLOO training data: 512 samples, about 1.735M tokens, at most 4,096 tokens each. No official GPQA, MMLU, or LCB problems are used. See `evaluation/NVFP4_CALIBRATION_METHOD.md`. In all three tiers the vision tower (333 tensors) and MTP (15 tensors) are BF16.
- Architecture: `Qwen3_5ForConditionalGeneration`, 64 layers (linear attention and full attention alternating 3:1). The FP8 package has 1,599 tensors: 1,251 language, 333 vision, 15 MTP.

| Component (static FP8 package) | Precision |
|---|---|
| Linear attention `A_log`, `dt_bias`, `norm`, `conv1d`, `in_proj_a` / `in_proj_b` (×48) | BF16 |
| Linear attention `in_proj_qkv`, `in_proj_z`, `out_proj` (×48) | FP8 E4M3 Block128 |
| Full-attention q/k/v/o and all MLP gate/up/down (400 Linear layers including the row above) | FP8 E4M3 Block128 |
| `embed_tokens`, `lm_head` | BF16 |
| Vision tower (333 tensors) | BF16, taken unchanged from the RLOO merged weights |
| MTP (15 tensors) | BF16, taken unchanged from the official Qwen3.8-27B |

All SSM control branches stay in BF16; the exclusion list matches Qwen's official FP8 release, keeping 146 language-model modules in BF16. FP8 package smoke tests all passed: patch-free load in SGLang, greedy output identical to the text-only evaluation build, SGLang image request, SGLang MTP, patch-free load in vLLM 0.28 with MTP, and vLLM image request.

NVFP4 smoke tests: patch-free load in SGLang, greedy parity, and the image request passed. MTP and DFlash2 speed and accept length come from the separate benchmark runs (all C1–C16 levels completed; see above).

**GGUF Q8_0** (`GGUF/`, `GGUF-NInfer/`): Q8_0 backbone with built-in MTP head (`blk.64.nextn`), no external draft; 866 tensors; `.ninfer` converted from the same GGUF; vision weights are not inside either package: for images use `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` with llama.cpp (`--mmproj`); NInfer cannot load `vision-bf16.safetensors` as a separate file, so the `.ninfer` package is text-only.

**GGUF Q6_K** (`GGUF/`, `GGUF-NInfer/`): Q6_K backbone calibrated with a 512-chunk imatrix, plus structure protection: the linear-attention (SSM) `ssm_alpha` / `ssm_beta` stay BF16, the token embedding and output head are Q8_0, and the MTP head (`blk.64` attn q/k/v/output, ffn gate/up/down, and `nextn.eh_proj`) is entirely Q8_0 with its norms kept in F32. The GGUF has 866 tensors in 65 blocks (64 backbone layers + 1 MTP layer). The `.ninfer` is converted from the same GGUF with the same backbone quantization; its MTP attention/MLP weights are Q6_K (`gguf_q6_k`) and only `mtp/input_projection` is Q8_0; vision weights are not inside either package: for images use `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` with llama.cpp (`--mmproj`); NInfer cannot load `vision-bf16.safetensors` as a separate file, so the `.ninfer` package is text-only.

### Commands

Requires official SGLang ≥ 0.5.19; vLLM ≥ 0.28 (MTP only). vLLM MTP on NVFP4 with tensor parallel ≥ 2 has a known issue (vLLM #52480); use a single GPU there. INT8 W8A8 loads only in vLLM (tested on 0.28); its command is at the end of this section.

**MTP and DFlash2 are mutually exclusive; enable only one per launch.** The examples use `./FP8`; for the BF16 tier, replace the `--model-path` / `vllm serve` path with `./BF16`, and for the NVFP4 tiers replace `--model-path` with `./NVFP4/W4A16`, `./NVFP4/W4A4`, or `./NVFP4/W4A4-W8A8`. The DFlash2 draft is the `DFlash2-FP8` folder inside each tier (e.g. `./FP8/DFlash2-FP8`, `./BF16/DFlash2-FP8`, `./NVFP4/W4A16/DFlash2-FP8`). SGLang detects the NVFP4 quantization format automatically, so no `--quantization` flag is needed; vLLM was validated only on the FP8 package, and NVFP4 was tested only on SGLang. Concurrency and context settings match the benchmark runs; adjust as needed.

**SGLang · MTP (bundled BF16)**

```bash
python -m sglang.launch_server \
  --model-path ./FP8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4
```

**vLLM · MTP (smoke-tested on the FP8 package)**

```bash
vllm serve ./FP8 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

**SGLang · DFlash2**

```bash
python -m sglang.launch_server \
  --model-path ./FP8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./FP8/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

**SGLang · NVFP4 W4A16 · DFlash2** (for W4A4, replace both `W4A16` with `W4A4`; for MTP on NVFP4, use the MTP command above and change only `--model-path`)

```bash
python -m sglang.launch_server \
  --model-path ./NVFP4/W4A16 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./NVFP4/W4A16/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

**SGLang · NVFP4 W4A4-W8A8 · DFlash2** (for MTP, use the MTP command above and change only `--model-path`)

```bash
python -m sglang.launch_server \
  --model-path ./NVFP4/W4A4-W8A8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./NVFP4/W4A4-W8A8/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

All benchmark scores in this card were measured with DFlash2 enabled; speculative decoding does not change the target model's output distribution. Default sampling is in `generation_config.json` (temperature 1.0, top_p 0.95, top_k 20).

W4A4 is shown; for W4A4-W8A8, change the path to `./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer` and `--model-id` to `qwen3.8-27b-coder390-w4a4-w8a8`.

The MTP-DFlash2 packages already contain the Q8 MTP head and the DFlash2 draft, so NInfer needs no external draft model (unlike the SGLang commands above, which take a DFlash2 draft path); pass either `--spec mtp` or `--spec dflash2`, or omit `--spec` to run without speculation.

**Images:** none of these `.ninfer` packages can take image input. NInfer turns images on with `--vision`, but that only works when the vision tower is inside the `.ninfer`; these packages do not have it, and `ninfer-serve` has no option to load the separate `vision-bf16.safetensors`. Do not add `--vision`: the server will not start. For images, use the BF16 / FP8 / NVFP4 tiers in SGLang (commands above).

**NInfer · no speculation**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8
```

**NInfer · MTP (4 draft tokens)**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec mtp --draft-tokens 4 --lm-head-draft
```

**NInfer · DFlash2 (8 draft tokens)**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec dflash2 --draft-tokens 8 --lm-head-draft
```

**NInfer · text-only packages (no MTP)**

`Qwen3.8-27B-Coder390-EfficientThink-W4A4.ninfer` and `Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8.ninfer` contain only the text path: no MTP, no vision tower, no DFlash2 draft. They run without speculation only, so do not add `--spec`, `--draft-tokens`, or `--lm-head-draft`. These two packages have not been separately evaluated; they have only passed SHA256 verification. For W4A4-W8A8, change the path to `./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8.ninfer` and `--model-id` to `qwen3.8-27b-coder390-w4a4-w8a8`.

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8
```

Health check: `curl -sf http://127.0.0.1:19931/health`. The chat endpoint is `POST /v1/chat/completions`; the request `model` must match `--model-id`.

**vLLM · INT8 W8A8 (no speculation)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel \
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A8 \
  --trust-remote-code --dtype bfloat16 \
  --max-model-len 102400 --served-model-name int8 \
  --gpu-memory-utilization 0.85 --max-num-seqs 8 \
  --reasoning-parser qwen3
```

On RTX PRO 6000 Blackwell, vLLM's Cutlass INT8 kernel is unavailable and the server will not start unless it is disabled with `VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel`; vLLM then uses its Triton INT8 kernel (the startup log shows `TritonInt8ScaledMMLinearKernel`). `VLLM_USE_FLASHINFER_SAMPLER=0` matches the tested setup. Tested on vLLM 0.28; SGLang cannot load this package (`ModelOptFp8Config` raises an error). `--reasoning-parser qwen3` returns the reasoning separately in `reasoning_content` (it was off during scoring).

**GGUF / GGUF-NInfer**

Load the `.ninfer` with NInfer-all (the `master` branch of `iamwavecut/ninfer-all`): the package keeps the GGUF quantization blocks, which other NInfer builds cannot read. llama.cpp needs an upstream build that supports `--spec-type draft-mtp`. NInfer's `--kv-capacity` is one KV pool shared by all requests; llama.cpp's `-c 409600 -np 4` splits the context evenly across 4 slots, so each request gets at most 102,400 tokens, enough for a single request to reach 94K. The chat endpoint is `POST /v1/chat/completions`; for NInfer the request `model` must match `--model-id`. Vision: `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` for llama.cpp `--mmproj` (629,247,008 bytes, sha256 `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32`). The `.ninfer` packages have no vision tower and NInfer cannot load the separate `GGUF-NInfer/vision-bf16.safetensors`, so they are text-only under NInfer; do not add `--vision` (the server will not start). For images, use llama.cpp with `GGUF/` and `--mmproj`.

**MTP and DFlash2**: every package under `GGUF/` and `GGUF-NInfer/` has a built-in MTP head (Q2 / Q3 / Q4 LynnStyle use built-in **Q4** MTP). To enable it, add `--spec mtp --draft-tokens N` for NInfer or `--spec-type draft-mtp --spec-draft-n-max N` for llama.cpp; leave these out to run without speculation. DFlash2 is an external draft model and is not in these GGUF / NInfer packages; this repository does not ship a DFlash2 draft for GGUF / GGUF-NInfer. For DFlash2, use the `DFlash2-FP8/` draft that ships with the BF16 / FP8 / NVFP4 tiers in this repository (SGLang `--speculative-algorithm DFLASH`) or the `.ninfer` packages under `NVFP4-NInfer/` (`--spec dflash2`). MTP and DFlash2 are mutually exclusive: a server runs one or the other, never both.

#### GGUF · NInfer

**NInfer · GGUF Q2 LynnStyle · MTP (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --kv-dtype rk8v4 \
  --max-concurrency 8 --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q3 LynnStyle · MTP (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q4 LynnStyle · MTP (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q6_K · MTP (draft 3, recommended concurrency 4)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-q6k-mtp \
  --max-context 102400 --kv-capacity 409600 --kv-dtype rk8v4 \
  --max-concurrency 4 --spec mtp --draft-tokens 3
```

**NInfer · GGUF Q8_0 · MTP (draft 4, recommended concurrency 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-q8-mtp \
  --max-context 102400 --kv-capacity 819200 --kv-dtype rk8v4 \
  --max-concurrency 8 --spec mtp --draft-tokens 4
```

Do not use `--max-context 131072 --kv-capacity 131072` (the KV pool then holds only one full context and queued requests return HTTP 503). Do not use `--lm-head-q6` / `--embedding-q4`. Requires NInfer-all (`ninfer-serve`); official ninfer-src cannot read `gguf_blocks_v1`.

#### GGUF · llama.cpp

**llama.cpp · GGUF Q2 LynnStyle · MTP (representative; swap the `-m` path for Q3 / Q4 / Q6_K / Q8_0)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

To use another GGUF tier, only change `-m` to `...-Q3LynnStyle-MTP.gguf`, `...-Q4LynnStyle-MTP.gguf`, `...-Q6_K-MTP.gguf`, or `...-Q8_0-MTP.gguf` (and the `--alias`, e.g. `qwen3.8-27b-coder390-q6k-mtp`, `qwen3.8-27b-coder390-q8-mtp`). MTP is fused inside the GGUF (`blk.64`); do not attach an external draft; the log should show `creating MTP draft context against the target model`. For image input add `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`.

## Files overview

### `FP8/` (main package: 19 files, 31,262,188,871 bytes)

`FP8/SHA256SUMS` covers the first 18 files below.

| File | Bytes | SHA256 |
|---|---:|---|
| `FP8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `FP8/config.json` | 17,784 | `9e58e8daf2914c2d11c07449dc7f03bbb822ba39dec37c4c5b3bd1f623492f90` |
| `FP8/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `FP8/model.safetensors.index.json` | 135,976 | `989573833195e17342983c7fd109e010155c423a355068b5aceb6631fcee83f2` |
| `FP8/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `FP8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `FP8/text-01.safetensors` | 2,542,796,928 | `54d83c1d36631de231876217a8e0c2483eccee8746369a482b79442bdfc5d958` |
| `FP8/text-02.safetensors` | 3,998,718,144 | `5b1e34725cd88924495765149ff816903d702180c72561c2e22e8377e2044fa8` |
| `FP8/text-03.safetensors` | 3,969,173,888 | `5e2376d6cce25aecf2d8901959f9d6f98801a0b2e98331f4088481bf839c9cf3` |
| `FP8/text-04.safetensors` | 3,925,079,000 | `669b87fd69d2de004073ed633f8e2890c8c9c90e1101bd59c859f1431b5cb967` |
| `FP8/text-05.safetensors` | 3,994,338,456 | `3f150179f9e3f03e2ef2e1afc805e7d745c1ab88dd72776fadf7c33f1d73ae67` |
| `FP8/text-06.safetensors` | 3,920,901,280 | `4d658974b7efb906972bc66cb4fd6dc7f1b7ac1fa79a7db068442314e3bf75d4` |
| `FP8/text-07.safetensors` | 3,972,285,640 | `d155ad91985b57e2515cea321a474708dd162665d1f5870df1c85601a2ca9b2c` |
| `FP8/text-08.safetensors` | 3,147,842,216 | `e37d025cd9bcacdd00fa0969f5c827d2504019c020585dfe1aca3934152b7700` |
| `FP8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `FP8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `FP8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `FP8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `FP8/SHA256SUMS` | 1,570 | (checksum list itself) |

### `FP8/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `FP8/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `FP8/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `FP8/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `FP8/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `BF16/` (12 files, 55,583,125,732 bytes; the DFlash2 subdirectory is listed separately below)

`BF16/SHA256SUMS` covers the first 11 files below. `mtp-bf16.safetensors` is byte-identical to the file of the same name in the FP8 package.

| File | Bytes | SHA256 |
|---|---:|---|
| `BF16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `BF16/config.json` | 3,799 | `b25e4020b4f791f2b20a3bf486f7ded5116fa0680cf7aa2ac50f80ee353663ce` |
| `BF16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `BF16/model-00001-of-00002.safetensors` | 49,825,162,976 | `ed83b8a41d447f4592c490b6135917419aea00fc7dbf9d6f5eb9525631f86fe0` |
| `BF16/model-00002-of-00002.safetensors` | 4,888,445,168 | `5c56330027c0eb9a776e89f80ef1643e60b1c2ae3adbbaf4b5142ebf7cb57271` |
| `BF16/model.safetensors.index.json` | 112,034 | `e8e177ff98a940337d496a0820e51c9fb68b2ab98fb68647d26aef9368dedeab` |
| `BF16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `BF16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `BF16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `BF16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `BF16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `BF16/SHA256SUMS` | 990 | (checksum list itself) |

### `BF16/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

Byte-identical to `FP8/DFlash2-FP8/`.

| File | Bytes | SHA256 |
|---|---:|---|
| `BF16/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `BF16/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `BF16/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `BF16/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A16/` (main package: 17 files, 20,613,406,953 bytes; the DFlash2 subdirectory is listed separately below)

`NVFP4/W4A16/SHA256SUMS` covers the first 16 files below; its own SHA256 is `ecc28d31be0d97e23509af61625251af14980db5b67189a1d1ca75a3fc9652f3`. `mtp-bf16.safetensors` is byte-identical to the file of the same name in the FP8 package.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A16/config.json` | 69,785 | `e71fd7b2cbade1ebb8be0382c81f7bf69eb1e039e30734914378d2c41217ef62` |
| `NVFP4/W4A16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A16/hf_quant_config.json` | 65,978 | `2ff46ad6bc27eb740e29831e642522ee4c110fea1ae9520b89272566b0d12d62` |
| `NVFP4/W4A16/model.safetensors.index.json` | 171,578 | `13651163cd9c1c20af460e6595616075a1f0d7f5995a3efc46d3ac449bc4f51e` |
| `NVFP4/W4A16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A16/text-01.safetensors` | 3,994,732,420 | `dfdd15ab6b889eee01357d38910552bb0968248df0e21a9564d7ae29482d3139` |
| `NVFP4/W4A16/text-02.safetensors` | 3,981,611,096 | `8e4a2a7b4c9325c27380a41de0fb51028065ff97090af9d4213cb5a50629d517` |
| `NVFP4/W4A16/text-03.safetensors` | 3,960,207,028 | `c92929b575321e080d0ea2ca7c1a26b49fa638a8d03bacfef2cd0b6f83237689` |
| `NVFP4/W4A16/text-04.safetensors` | 3,983,003,152 | `feb69e1a4c7a374f1a11cf3e4af5d70fdd870963519e71469eb067a86fb35634` |
| `NVFP4/W4A16/text-05.safetensors` | 2,902,646,528 | `28dda5f9a39b83736ae458c2e626b429bbd18e408be63ef598dbb47327c97e3e` |
| `NVFP4/W4A16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A16/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A16/SHA256SUMS` | 1,399 | `ecc28d31be0d97e23509af61625251af14980db5b67189a1d1ca75a3fc9652f3` |

### `NVFP4/W4A16/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

Byte-identical to `FP8/DFlash2-FP8/`.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A16/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A16/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A16/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A16/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A4/` (main package: 17 files, 20,613,386,462 bytes; the DFlash2 subdirectory is listed separately below)

`NVFP4/W4A4/SHA256SUMS` covers the first 16 files below; its own SHA256 is `5aea8bb9c1f1979661bfa5c1216de7aafeb64cd708aa8cc71f3b185c224cfde0`. `mtp-bf16.safetensors` is byte-identical to the file of the same name in the FP8 package.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A4/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A4/config.json` | 18,130 | `4df9be90e61070a553447129e504fea7be8e60dc22ae9e9f7a85bdfc140c0054` |
| `NVFP4/W4A4/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A4/hf_quant_config.json` | 13,956 | `d3603810fba7548903ba2f3382fdd30f5704d3b6e0688e2dccf34fe023c11d31` |
| `NVFP4/W4A4/model.safetensors.index.json` | 207,580 | `541d828aed73b4df9f9fc86be7111aa404983d55d9797ca1cfb3e71474bfd3b7` |
| `NVFP4/W4A4/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A4/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A4/text-01.safetensors` | 3,994,737,240 | `1ea4cf8a0036b5d87815b65a38d0d2c00b37c010056a03d0db1fc72eb6c829bc` |
| `NVFP4/W4A4/text-02.safetensors` | 3,981,625,016 | `c9a0d2c3c506ad17da4dd47bf571326eef201e40db6f259a9d42971778033359` |
| `NVFP4/W4A4/text-03.safetensors` | 3,960,220,600 | `3c8778873d2ef08c512b7e457d61a6ac9ea047975e4723cd3804d0d18e86c1db` |
| `NVFP4/W4A4/text-04.safetensors` | 3,983,016,880 | `40081557adf0713f1624cdb2d1c53ea5fd2a30e09f5f964799457b23e4e2304d` |
| `NVFP4/W4A4/text-05.safetensors` | 2,902,647,672 | `0266ba0fa0354a4c409bc180c9d9a67ed12c915fc9886970745c87f8babcaa24` |
| `NVFP4/W4A4/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A4/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A4/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A4/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A4/SHA256SUMS` | 1,399 | `5aea8bb9c1f1979661bfa5c1216de7aafeb64cd708aa8cc71f3b185c224cfde0` |

### `NVFP4/W4A4/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

Byte-identical to `FP8/DFlash2-FP8/`.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A4/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A4/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A4/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A4/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A4-W8A8/` (main package: 18 files, 23,769,634,648 bytes; the DFlash2 subdirectory is listed separately below)

`NVFP4/W4A4-W8A8/SHA256SUMS` covers the first 17 files below; its own SHA256 is `c177f4907a7dd037efe91b8d34927dd3a3624227f259238b82db0f12f8b0b8e2`. `mtp-bf16.safetensors` is byte-identical to the file of the same name in the FP8 package.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A4-W8A8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A4-W8A8/config.json` | 71,802 | `d1cc2af6971ae0bb776f5f36eb1c923546742fda3a83e6d8355720a652e27b5d` |
| `NVFP4/W4A4-W8A8/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A4-W8A8/hf_quant_config.json` | 43,976 | `2bd65f6f325ea8e8e40c37b6e7d386633ac6236db6fcde3d7e9de128d961a599` |
| `NVFP4/W4A4-W8A8/model.safetensors.index.json` | 187,500 | `1257454a255efb01ba8047fe41bf34460b551c210db7cc8c4713f1c01150c69d` |
| `NVFP4/W4A4-W8A8/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A4-W8A8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A4-W8A8/text-01.safetensors` | 3,981,847,464 | `b5502eb2c54c5a53ee08712c48935023ed924e0f054acb3573e1288095d2e3ff` |
| `NVFP4/W4A4-W8A8/text-02.safetensors` | 3,956,368,808 | `f08e7fccb4d2467af8b2b2d3bc587e6e8404b5764e9fc8e640ad0ff4f445d293` |
| `NVFP4/W4A4-W8A8/text-03.safetensors` | 3,956,368,928 | `8299287bb0e570efda02bcbe67c4bd9c5378b44bbf84c17ff062fc5ce6ba53e0` |
| `NVFP4/W4A4-W8A8/text-04.safetensors` | 3,967,919,248 | `bea560dda7b885cca987b8352e2ae659acaee70c3255fde7fa487c1fd73badf2` |
| `NVFP4/W4A4-W8A8/text-05.safetensors` | 3,573,130,520 | `a969faa5f2a3963450ad64bb84664035676c426877499593aea91080643ba6fa` |
| `NVFP4/W4A4-W8A8/text-06.safetensors` | 2,542,796,928 | `54d83c1d36631de231876217a8e0c2483eccee8746369a482b79442bdfc5d958` |
| `NVFP4/W4A4-W8A8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A4-W8A8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A4-W8A8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A4-W8A8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A4-W8A8/SHA256SUMS` | 1,485 | `c177f4907a7dd037efe91b8d34927dd3a3624227f259238b82db0f12f8b0b8e2` |

### `NVFP4/W4A4-W8A8/DFlash2-FP8/` (4 files, 2,407,384,680 bytes)

Byte-identical to `FP8/DFlash2-FP8/`.

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4/W4A4-W8A8/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `evaluation/`

Score, benchmark, smoke-test (static FP8 and BF16), and calibration records. `evaluation/SHA256SUMS` covers the first 22 files below (23 files in total, including the checksum list itself). `NVFP4_*.results.summary.json` are the raw summaries of the three suites for the three NVFP4 tiers (`NVFP4_MIXED_*` is the W4A4-W8A8 tier).

| File | Bytes | SHA256 |
|---|---:|---|
| `evaluation/SCORES_STATICFP8.json` | 3,935 | `eba280071a75fc8dd90e5866df783a68ccd08bdb4d4dde85c062f7d398ea0eb0` |
| `evaluation/BENCH_STATICFP8.json` | 6,511 | `c62c6c82f234a27fa93faf691d1d4ee01a2408a18bbe94efafe341e4ad10db20` |
| `evaluation/BENCH_STATICFP8.md` | 1,405 | `ea662952b73446d5b88422b2a3dbcc215829521cc001cb26ad492caa137fa2ac` |
| `evaluation/SMOKE_STATICFP8.json` | 2,119 | `1a2383ad0f8e26f02ec7d65db418fea2bd50e73458ee247cc9d2f9322ffbb833` |
| `evaluation/SCORES_BF16.json` | 4,279 | `76e921712bab0577853499d3f67440de6f3577f4818c40184f4b0580e5f7a77e` |
| `evaluation/SMOKE_BF16.json` | 889 | `01ea5e4518615af2a3c574fa49ae6f2a4819482bbaafce2695b62016b14a582f` |
| `evaluation/SCORES_NVFP4_W4A16.json` | 3,319 | `7294901f3493f593e0de6d7f95b860c44578780300aebcb52bca6f06ead1ddfd` |
| `evaluation/BENCH_NVFP4_W4A16.json` | 3,992 | `1877fe3e4126de72ad1165a1e0f5d1dd569f73f1dcd16a93249c389b3d47f2d3` |
| `evaluation/SCORES_NVFP4_W4A4.json` | 3,212 | `eee169bb6cde4d048d12d604a72c7570b0ebd0fee88a3c19d39ad4493a912f30` |
| `evaluation/BENCH_NVFP4_W4A4.json` | 3,922 | `2ebedf7e221f69765364a73deaca459a9636a4c190b2cbde06de8d119a15f4a7` |
| `evaluation/SCORES_NVFP4_MIXED.json` | 3,063 | `845027e6324b5300ed5ce306b3515b559f75b5c0e8ef1aac4d1b98d62d135454` |
| `evaluation/BENCH_NVFP4_MIXED.json` | 4,038 | `3d6f348425b6fd184d620c101a803139d7bcc0d620ff3237c28cc627e8f85ca7` |
| `evaluation/NVFP4_CALIBRATION_METHOD.md` | 3,712 | `e3678dbe9020a83998a5c66207b515376defebd78e6fadf4f63e55059785e03a` |
| `evaluation/NVFP4_W4A16_gpqa.results.summary.json` | 1,182 | `4835f8cf4b403047487b0a52db88574a2125ba103a30404b8b9e97e7112511bd` |
| `evaluation/NVFP4_W4A16_lcb.results.summary.json` | 2,642 | `56990657d101c2ce47b44d5fcdcb498a286bbf6093ae7790cde5809ba266d5a1` |
| `evaluation/NVFP4_W4A16_mmlu.results.summary.json` | 4,075 | `e9d507b5da71621032a13f487eb60159e0369c025ed12c4fa613e70b6f0f71e5` |
| `evaluation/NVFP4_W4A4_gpqa.results.summary.json` | 1,189 | `961b3f98b4a54d78d1983896a0b12b10a3d1e7facf456f594793dc7bbefb5e70` |
| `evaluation/NVFP4_W4A4_lcb.results.summary.json` | 2,640 | `bd371e898121ee5dd6fda47065254cc2137ba783b466b3830f0c58d631137688` |
| `evaluation/NVFP4_W4A4_mmlu.results.summary.json` | 4,076 | `b468cf81854562e0e20bf232ddd13b68ed58e10a4da840e6bd3c20564d20f74a` |
| `evaluation/NVFP4_MIXED_gpqa.results.summary.json` | 1,171 | `72c000ffc4ff15db8d542b6d9d924c5795ad491d946dee0f6c3f11b0e62151f1` |
| `evaluation/NVFP4_MIXED_lcb.results.summary.json` | 2,641 | `7e3d3146dd98954ef80358ce88f5505798f77427c1a5ddf73c65dd728cf3afc2` |
| `evaluation/NVFP4_MIXED_mmlu.results.summary.json` | 4,077 | `3088c6254dad8af25ace3b44f4cfa688b192eca98f693afa1c595df121cb9afb` |
| `evaluation/SHA256SUMS` | 2,071 | (checksum list itself) |

### Verification

```bash
(cd FP8 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd BF16 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A16 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A4 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A4-W8A8 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4-NInfer/W4A4 && sha256sum -c SHA256SUMS)
(cd NVFP4-NInfer/W4A4-W8A8 && sha256sum -c SHA256SUMS)
(cd INT8/W8A8 && sha256sum -c SHA256SUMS)
(cd GGUF && sha256sum -c SHA256SUMS)
(cd GGUF-NInfer && sha256sum -c SHA256SUMS)
(cd evaluation && sha256sum -c SHA256SUMS)
```

## NInfer loading notes

- Only the NInfer engine can load `.ninfer`; SGLang, vLLM, llama.cpp, and transformers cannot.
- Use `ninfer-serve` from official NInfer ([`iamwavecut/ninfer-all`](https://github.com/iamwavecut/ninfer-all)); no patches are needed. Tested on one RTX PRO 6000 Blackwell (compute capability 12.0); NInfer supports at most 8 concurrent requests.
- `NVFP4-NInfer/W4A4/` and `NVFP4-NInfer/W4A4-W8A8/` each hold one `.ninfer` file with MTP and DFlash2: the text path is the same one scored on 2026-10-05, and the package also carries a Q8 MTP head, the DFlash2 draft, and the proposal head; the vision tower is not in the package, so it cannot take image input; NInfer cannot load the `vision-bf16.safetensors` in the same folder as a separate file. The MTP projections are Q8 because several of their matrix shapes have no BF16 kernel in NInfer, and a BF16 MTP makes the server exit while building the compute graph.
- Each of the two directories also holds a text-only package (`Qwen3.8-27B-Coder390-EfficientThink-W4A4.ninfer`, `Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8.ninfer`, 20,752,974,596 bytes each): text path only, no MTP, no vision tower, no DFlash2 draft, so it runs without speculation only; not separately evaluated, SHA256 verification only.
- MTP and DFlash2 are mutually exclusive per launch (`--spec mtp` or `--spec dflash2`); `--lm-head-draft` must be used together with `--spec`. MTP accepts 1–5 draft tokens and DFlash2 1–15; the NInfer commands under Commands above use 4 and 8, as in the benchmark. The DFlash2 draft is built into the package, so no separate `DFlash2-FP8/` directory is needed.
- These context flags are verified to start: `--max-context 102400 --kv-capacity 819200 --max-concurrency 8 --kv-dtype fp8`. `--kv-capacity` must fall between `max-context` and `max-context × max-concurrency`; 819,200 is exactly 8 × 102,400.
- The HF packages under the NVFP4 directories still run in SGLang (MTP or DFlash2); they are not interchangeable with the NInfer packages.

### NInfer V2 packages (Tesla V100 only)

The four packages whose filenames contain `NInferV2-NOT-FOR-V3` are for Tesla V100 only (ninfer-v100 branch); on any other GPU, use the packages without this suffix.

- The 4 packages whose filenames contain `NInferV2-NOT-FOR-V3` use the NInfer **V2** container and are only for the Tesla V100 `ninfer-v100` branch. Official NInfer and `ninfer-serve` read V3 only and reject these files; for official NInfer, use the V3 packages above (without `NInferV2` in the name). Do not rename the V2 packages to V3 filenames or use them to replace the V3 packages.
- The two text-only packages (`Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer`, `Qwen3.8-27B-Coder390-W4A4-W8A8-NInferV2-NOT-FOR-V3.ninfer`) have no MTP or DFlash2, so do not pass `--spec`; the two MTP-DFlash2 packages (`…-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer`) accept `--spec mtp` or `--spec dflash2`; they already contain the MTP head and the DFlash2 draft, so no external draft model is needed. None of the four V2 packages includes the vision tower.
- V100 has no NVFP4 KV or K8V4 KV, so do not use the V3 flags `--kv-dtype rk8v4` or `--kv-capacity 819200`; when serving on V100, add `--prefill-chunk 2048`.
- The V2 packages have not been separately evaluated; they have only passed SHA256 verification. In `SHA256SUMS`, the two V2 lines come after a `#` comment line, separate from the V3 lines.

```bash
# V100 ninfer-v100 branch · text-only package (no --spec)
ninfer ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer \
  --prompt "Explain prefill and decode in three sentences." \
  --max-context 8192 \
  --max-new 256

# V100 ninfer-v100 branch · MTP-DFlash2 package (MTP on)
ninfer ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer \
  --prompt "Explain prefill and decode in three sentences." \
  --max-context 8192 \
  --max-new 256 \
  --spec mtp --draft-tokens 3
```

### `NVFP4-NInfer/W4A4/` (6 files, 89,382,856,537 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer` | 23,477,856,260 | `212972ef9f7f86765f7963bdadcab133c42cb0308feb33a55e820513d8a6bcfc` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4.ninfer` | 20,752,974,596 | `6020ee54dcc2bd809c0f3127e9146e27d786813933970691ce21078d2a111a89` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer` | 20,752,831,236 | `eac9e3d47fe6731c021d7154fd2f801a8263ac6d00e6d16834e54947ee58bcf8` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer` | 23,477,696,516 | `e93f3b83f7589fdb776ce25a0cdef98ed1892e101ef564fdb844a5aacff13d22` |
| `NVFP4-NInfer/W4A4/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4-NInfer/W4A4/SHA256SUMS` | 705 | `7fcdf5c55c74fd34a31968f5a36da1fde31db577d5bec4ebe7ed9311ca0890d9` |

### `NVFP4-NInfer/W4A4-W8A8/` (6 files, 89,382,856,557 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer` | 23,477,856,260 | `799dd5921a69b6c0e0f4bced88ebf9db7a744f50f4b8c2c63e26656b0983f279` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8.ninfer` | 20,752,974,596 | `f4aa505aaadf358d30df061dc7cc8151bbded858cd38c02e4f4b1ae83e171047` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-W4A4-W8A8-NInferV2-NOT-FOR-V3.ninfer` | 20,752,831,236 | `01a4440f77dcdac66906e1bb061e1c38c6b236b805ff7bcb644aedf90f06a038` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-W4A4-W8A8-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer` | 23,477,696,516 | `099b2d00fa3982d601218d6587dc25222cc21ef708de7dab8b2e2c0bee60da74` |
| `NVFP4-NInfer/W4A4-W8A8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4-NInfer/W4A4-W8A8/SHA256SUMS` | 725 | `59c714ff4b2b9e37d1091f45ec12d9ac45d20a002336f24ae0d43d2b75738d11` |

## INT8 W8A8 notes

- Text path only: the architecture is `Qwen3_5ForCausalLM` with 64 layers (linear and full attention alternating 3:1); the package does not include the vision tower, MTP, or the DFlash2 draft, and accepts text requests only.
- Quantization: SmoothQuant + INT8 W8A8. Weights are quantized to INT8 per output channel, and activations are quantized to INT8 per token at runtime; the SmoothQuant pre-scale is folded into the weights, so no inference-engine patch is needed. Quantization metadata uses the compressed-tensors (`int-quantized`) format.
- Layer layout: MLP gate/up/down, full-attention q/k/v/o, and linear-attention `in_proj_qkv` / `in_proj_z` / `out_proj` make up 400 INT8 Linear layers; linear-attention `in_proj_a` / `in_proj_b` and `lm_head`, 97 in total, stay BF16; linear-attention control branches such as `A_log`, `dt_bias`, `norm`, and `conv1d` also stay BF16.
- Calibration and error: 512 calibration samples; held-out NLL rises from 0.50535 (BF16) to 0.52812, a perplexity ratio of 1.023 (measured before the pre-scale was folded into the weights).
- Loading: validated only on vLLM 0.28; not for SGLang or NInfer. `VLLM_LOAD.json` records the load requirements. On RTX PRO 6000 Blackwell the Cutlass INT8 kernel must be disabled; see Commands above.

### `INT8/W8A8/` (16 files, 29,500,937,028 bytes)

| File | Bytes | SHA256 |
|---|---:|---|
| `INT8/W8A8/VLLM_LOAD.json` | 329 | `b1101c2ef1d53e76f132686a15079068fc76ad2ae139514817e088c6223adf7b` |
| `INT8/W8A8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `INT8/W8A8/config.json` | 19,123 | `b3db670871591bcfbedc05743a4cdc8a41c20cbc1af570e653716d7904ec92c7` |
| `INT8/W8A8/generation_config.json` | 214 | `a4cef85934ea1fdcb207944dbc6eee70dbbf16806874428556ae33023336c0a4` |
| `INT8/W8A8/model-00001-of-00008.safetensors` | 3,978,325,744 | `f8f7ecb52576f50108d2a9335074e5621dd5a0c2b5ee92b830929c8acc34900a` |
| `INT8/W8A8/model-00002-of-00008.safetensors` | 3,990,728,496 | `73c182d4362ca9351329eb9c812aa44f627631d1d1866868a326010dc8387a45` |
| `INT8/W8A8/model-00003-of-00008.safetensors` | 3,927,632,952 | `59510687bfca9272147d8153b0d3cc55a2672a03c7326d7099d78a313cc4f102` |
| `INT8/W8A8/model-00004-of-00008.safetensors` | 3,995,896,560 | `fd9c32e4a11dec2dbf42dfb4e5da653bbbc01cd075ff60e593869022138e2efd` |
| `INT8/W8A8/model-00005-of-00008.safetensors` | 3,922,465,008 | `7478173acc5b54c80329756cf2bb81b5b804a0fa107217fbba5d0cb3353c3f77` |
| `INT8/W8A8/model-00006-of-00008.safetensors` | 3,984,366,360 | `cd53edb6084ec639667f2bdb997f7822db1eb758a15a06818fddcac603642127` |
| `INT8/W8A8/model-00007-of-00008.safetensors` | 3,138,579,112 | `997de745c52a87d54f684a461dd831f59d80e6b0c4c43e7ad75bd148cc87fdd5` |
| `INT8/W8A8/model-00008-of-00008.safetensors` | 2,542,796,896 | `6866cf8adcccc4cc6a00e74bc025f1a774fb52103b70f2674d0288272951a733` |
| `INT8/W8A8/model.safetensors.index.json` | 125,462 | `8d04b274eb35757ea076fd573ca0e435649d3f6835a69dbd05317e29f05579e5` |
| `INT8/W8A8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `INT8/W8A8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `INT8/W8A8/SHA256SUMS` | 1,420 | `e96702ae14a09d8280d24423d08a781fbef87e91784eaf1004ac46201fed8f73` |

## GGUF Q2 LynnStyle notes

- Mixed-precision LynnStyle; lowest type reaches Q2; built-in **Q4 MTP** (not Q8). Scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights: GPQA 177/198, MMLU 433/500, LCB 90/100. Reasoning P50/P70/P90: GPQA 2,989.5 / 8,923.8 / 27,156.1; MMLU 181 / 326.3 / 1,020.5; LCB 5,656.5 / 17,835.8 / 40,067.3.
- Size: GGUF 13,276,009,792 bytes (BPW 3.89), NInfer 13,272,798,720 bytes (BPW 3.89); denominator 27,320,697,856.
- Speeds (handoff): llama.cpp built-in Q4 MTP long bench C4 174.8 tok/s (4096 gen cap); NInfer short bench C8 521.0 tok/s (512 gen cap). Protocols differ.
- Launch GGUF and NInfer separately (MTP built-in); see Commands above. MTP and DFlash2 are mutually exclusive, and this repository ships no DFlash2 draft for GGUF.

## GGUF Q3 LynnStyle notes

- Mixed-precision LynnStyle; built-in **Q4 MTP** (not Q8). Scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights: GPQA **173/198**, MMLU **449/500**, LCB **92/100**. GPQA think P50/P70/P90: 3,125.5 / 7,265.2 / 24,343.1.
- Size: GGUF 17,303,770,432 bytes (BPW **5.07**), NInfer 17,300,551,168 bytes (BPW **5.07**); denominator 27,320,697,856.
- Speeds (handoff): llama.cpp fused MTP long bench C4 **191.8** tok/s (4096 gen cap); NInfer short bench C8 **512.3** tok/s (512 gen cap). Protocols differ.
- Launch GGUF and NInfer separately (MTP built-in). DFlash2 is optional external draft, not the default for these packages. See the GGUF-NInfer repository card for full launch commands.

## GGUF Q4 LynnStyle notes

- Mixed-precision LynnStyle; built-in **Q4 MTP** (not Q8). Scored before the built-in MTP head was attached (external Q8 MTP draft); same quantized weights: GPQA **175/198**, MMLU **448/500**, LCB **89/100**.
- Size: GGUF 19,620,406,592 bytes (BPW **5.75**), NInfer 19,617,187,328 bytes (BPW **5.74**); denominator 27,320,697,856.
- Speeds (handoff): llama.cpp fused MTP long bench C4 **81.1** tok/s (4096 gen cap); NInfer short bench C8 **436.4** tok/s (512 gen cap). Protocols differ.
- Launch GGUF and NInfer separately (MTP built-in). DFlash2 is optional external draft, not the default for these packages. See the GGUF-NInfer repository card for full launch commands.

## GGUF Q8_0 notes

- Both packages share the Q8_0 backbone with a built-in MTP head; recommended NInfer + C8 + MTP (486.3 tok/s).
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`: load with llama.cpp.
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer`: NInfer-all only; use `--max-context 102400 --kv-capacity 819200 --max-concurrency 8`.
- Scores from llama.cpp on the GGUF; reasoning tokens are split for all three benches.

## GGUF Q6_K notes

- Both packages share the same backbone quantization (Q6_K + imatrix + structure protection; see Quantization scheme above) and carry a built-in MTP head (GGUF `blk.64` is Q8_0; NInfer MTP attention/MLP weights are Q6_K, input projection Q8_0), so no external draft model is needed; NInfer + C4 + MTP is recommended.
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`: loads directly in llama.cpp; the GGUF architecture is `qwen35` with 65 blocks, the last of which (`blk.64`) is MTP.
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer`: loadable only by NInfer-all; SGLang, vLLM, llama.cpp, and transformers cannot read it.
- Vision: llama.cpp uses `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` (629,247,008 bytes); the `.ninfer` packages are text-only under NInfer: they have no vision tower, and NInfer cannot load the separate `vision-bf16.safetensors` (in `GGUF-NInfer/`, 921,497,224 bytes).
- Scores were measured with the GGUF package on llama.cpp; the LCB eval script is not compatible with the NInfer API (its replies are not valid JSON), which is an eval-script issue rather than a model-quality issue, so LCB is scored on llama.cpp.

### `GGUF/` (7 files: Q3+Q4+Q2+Q8+Q6 + mmproj + SHA256SUMS)

| File | Bytes | SHA256 |
|---|---:|---|
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf` | 17,303,770,432 | `9985b3d41fc7dc0bb5d493f7523d4515504912a3a7fc830f66e0fd2f90f9fd95` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf` | 19,620,406,592 | `56c7c605a59764d9f0bb645d4eb335f1574af2c9e74020386139597df0e872f5` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf` | 13,276,009,792 | `cad973b3b7cc0d86bd39968209268318a746673c12c9536e5c37408baa7b5e6e` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf` | 29,069,202,688 | `b24e8c5fe3f2b282cce841400c740fcaca48afcdcf9e991f7bbe9a59a78cabfe` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf` | 23,177,516,384 | `302597c53d1b00f7230b53a8a050831390a4371e92a80c1ac644fa920af76ab1` |
| `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 629,247,008 | `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32` |
| `GGUF/SHA256SUMS` | 696 | `7b01a47f763ca72c58b2067dc21658d2a41eabff52bf5bbe25c2517fb99ebebf` |

### `GGUF-NInfer/` (7 files: Q3+Q4+Q2+Q8+Q6 + vision-bf16 + SHA256SUMS)

| File | Bytes | SHA256 |
|---|---:|---|
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.ninfer` | 17,300,551,168 | `983456fc57cfc63a160512c933dc44f93005151c954b060399373d685b10de99` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.ninfer` | 19,617,187,328 | `376ee05a8c5160bde35e7c742565671fb4cec0e6e3c82cb293f87ad3a27d6cac` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.ninfer` | 13,272,798,720 | `cdd82b69027faba0bda619224ee851ccd0ecf0dfb176bad85a17d2df07926921` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer` | 29,065,983,488 | `40937a1509b0333858703b7c285b5a64b507803060a94bcccee19f4f683647bf` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` | 23,084,144,128 | `c273d394cd727a1055abc53b29e253e258926288429751e00acbeaea1ec0cd0e` |
| `GGUF-NInfer/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `GGUF-NInfer/SHA256SUMS` | 701 | `2cf12cd6ca7a98ed5340a9bb3139a3f90401f39ab12798bb082c83df2eed47b2` |

## Known limitations

- On GPQA, the empty answers at all three precisions come from the same two molecular-biology questions; this is a long-standing issue with those questions, not a quantization effect.
- The long tail is not eliminated: accuracy is clearly lower for reasoning ≥48K (e.g., static FP8 LCB ≥48K is 2/8), and 3 LCB problems still hit the 94K cap.
- MMLU shows 445–450 sampling variation across precisions. Scores depend on the protocol above (100K context, 94,208-token cap, no timeout) and should not be compared directly with numbers from other protocols.
- Performance was measured only on a single RTX PRO 6000 Blackwell with SGLang: BF16 / static FP8 figures come from the static FP8 package, and each NVFP4 tier was measured on its own package. vLLM was covered only by load, MTP, and image smoke tests on the FP8 package, and NVFP4 was not tested on vLLM; DFlash2 was validated only on SGLang.
- NVFP4 GPQA (170, 167, and 172) is below the 178 of BF16 / FP8, MMLU (439, 440, and 442) is slightly below 445–450, and LCB (91, 92, and 88) is around 90; the calibration data comes from this model's own RLOO training data and contains no official evaluation problems. NVFP4 smoke tests were run only on SGLang (patch-free load, greedy parity, image request); MTP and DFlash2 are covered by the full benchmark runs.
- BF16 scores come from full-suite runs on the same weight shards; GPU smoke tests of the BF16 package itself (SGLang + MTP, image) are still pending.
- INT8 W8A8 has only the text path and runs only in vLLM; GPQA 175 is slightly below the 177 of the original Qwen3.8 27B (FP8); speeds come from a quick benchmark (requests per level equal to the concurrency, 512 generation cap) and are not directly comparable with the other tiers; GPQA / MMLU reasoning lengths were recounted from the raw text with the BF16 tokenizer; LCB kept no reasoning text, so it has no reasoning-length percentiles.
- GGUF Q8_0: GPQA 171 below original Qwen3.8 27B (FP8) 177; LCB truncations 3, empty 3; full triad on GGUF (llama.cpp) only; NInfer speed is same-caliber, llama.cpp is the quick protocol.
- GGUF Q6_K: GPQA 174 is below the 177 of the original Qwen3.8 27B (FP8); MMLU reasoning length is counted from the raw text with the BF16 tokenizer, and LCB kept no reasoning text, so it has no reasoning-length percentiles; the full triad was run only on the GGUF (llama.cpp), not separately on the NInfer package; speeds come from a quick benchmark (requests per level equal to the concurrency, 512 generation cap) and are not directly comparable with the other tiers; vision uses `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` (llama.cpp `--mmproj`); the NInfer package is text-only; the image path was not re-tested on every tier.

## License and acknowledgements

Licensed under Apache-2.0, following the license of the base model Qwen3.8-27B.

Thanks to the Qwen team for the base model and the official FP8 scheme; to Opus5.5, GPT6Astra, Grok4.7, DSV4Pro, and K3 for problem writing, gold labels, teacher trajectories, data review, and the RLOO value review; and to the SGLang, vLLM, and DFlash communities.
<!-- CARD_EN_END -->

<!-- LANG_SEPARATOR -->

---

<!-- CARD_ZH_START -->
# Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-MTP-DFlash2

![Coder390 FP8 对比原版 FP8](assets/header-fp8-vs-base-zh-8k.png)

在 [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2)(官方 [Qwen3.8-27B](https://modelscope.cn/models/Qwen/Qwen3.8-27B) 经 SFT + SimPO 后训练得到的模型)基础上继续做多轮 SFT 与 RLOO 后训练,专治原版「已有答案却停不下来、写满 94K 也不给最终答案」的问题。本仓库提供 **BF16**、**静态 FP8 Block128**、**NVFP4 W4A16**、**NVFP4 W4A4**、**NVFP4 W4A4-W8A8**(混合精度)五个 safetensors 档,均为完整多模态(文本 + 图像/视频)、内置官方 BF16 MTP,SGLang 免补丁加载(FP8 包另经 vLLM 冒烟验证);另有 **NInfer W4A4 / W4A4-W8A8**(`NVFP4-NInfer/`)、**INT8 W8A8**(`INT8/W8A8/`,仅文本)以及 **GGUF Q2 / Q3 / Q4 LynnStyle、Q6_K、Q8_0**(`GGUF/`、`GGUF-NInfer/`,内置 MTP)。

- **94K 截断大幅减少**:同口径下 GPQA 从 4 降到 1,LCB 从 13 降到 3。
- **三项全面不低于原版**:GPQA **178/198**、MMLU **450/500**、LCB **90/100**(静态 FP8),原版 FP8 为 177 / 444 / 83。
- **量化无损**:BF16、动态 FP8、静态 FP8 三种精度 GPQA、LCB 一题不差。
- **两种投机解码(互斥)**:DFlash2 单请求约 180 tok/s,MTP 约 91 tok/s,不开投机约 46 tok/s。

**相关仓库**

- GGUF / GGUF-NInfer（llama.cpp、NInfer，内置 MTP）：[Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-GGUF-NInfer)
- NVFP4-NInfer：[Hugging Face](https://huggingface.co/nerkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer) · [ModelScope](https://modelscope.cn/models/Merkyor/Qwen3.8-27B-Coder390-EfficientThink-Opus5.5-GPT6Astra-Grok4.7-DSV4Pro-K3-SFT-RLOO-NVFP4-NInfer)

## 训练方法

**谱系**:官方 Qwen3.8 27B(177 / 444 / 83)→ 我们的 SFT + SimPO110 终版,即 [EfficientThink 基座](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2)(171 / 442 / 89)→ K3 续训 SFT → 第二周 SFT(week2dose,update-225)→ 第一轮 RLOO(182 组)→ 再一轮 SFT(merge-sft-100),得 sft-base-rloo(177 / 448 / 90)→ 第二轮 RLOO(172 组)→ **Coder390**(178 / 445 / 90,动态 FP8 口径)。括号内依次为 GPQA / MMLU / LCB,均为 100K 同口径全量。

**训练基座**:本模型以我们自己的 EfficientThink SFT + SimPO 模型(SimPO110 终版)为起点,继续做多轮 SFT 与 RLOO,该基座模型本身是官方 Qwen3.8-27B 的后训练版本,见 [Qwen3.8-27B-EfficientThink-SFT-SimPO-DFlash2](https://huggingface.co/nerkyor/Qwen3.8-27B-EfficientThink-Uncensored-K3-Opus5-Grok4.6-GPT5.6Sol-SFT-SimPO-DFlash2)。

| 名字片段 | 含义 |
|---|---|
| Coder | 代码强化 |
| 390 | GPQA、MMLU、LCB 三项都到 90 分 |
| EfficientThink | 训练目标:去掉无效的长推理尾巴,保留必要的长推理 |
| Opus5.5、GPT6Astra | 撰写出题金标与教师模型轨迹 |
| Grok4.7 | 本次训练的主持人,全程核对、筛选数据 |
| DSV4Pro、K3 | 其轨迹作为教师模型用于训练;K3 还做了 RLOO 价值评审和一部分出题工作 |
| SFT-RLOO | 训练方法:SFT(含 SimPO)基座上,SFT 与 RLOO 交替进行 |
| MTP / DFlash2 | 内置 BF16 MTP 头 / 配套 DFlash2 投机解码草稿 |

**要解决的问题**:模型在局部已经有答案之后,仍用 Wait / Actually 把同一套推导反复再推,直到写满上下文,最终答案为空。这类题多数不是不会,而是停不下来。

**RLOO 数据**:每题采样 8 条轨迹,只保留组内有对有错的题(8 条全对的不入训);组内 0 或 1 条对的,补 1 条审过的短教师轨迹,替换该组最短的一条错轨迹(共 27 组)。最终 172 组、1,376 条:正确 859 条、错误 517 条,其中空答 68 条。

**奖励**:惩罚只打在错的一侧,长而正确的推理仍得正奖励,以免压制必要的长推理。

| 情形 | 奖励 |
|---|---:|
| 短且对(<24K) | +1.05 |
| 长且对 | +1.0 |
| 短且错(<24K) | −0.2 |
| 错,24K–48K | −0.5 |
| 错,≥48K | −0.7 |
| 写到 94K 有选项字母但错 | −0.9 |
| 空答 | −1.0 |

**结果**:同口径下,GPQA 的 94K 截断从原版的 4 降到 1,LCB 从 13 降到 3,三项分数均不低于原版(均为 FP8 档;NVFP4 三档见下文成绩)。

## 成绩

**口径**:同一份 Coder390 合并权重;两张 RTX PRO 6000,每卡 C8,上下文 100K,生成上限 94,208,客户端不计超时,DFlash2 草稿,SGLang;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。

| 套题 | 原版 Qwen3.8 27B(FP8) | BF16 | 动态 FP8 | 静态 FP8 |
|---|---:|---:|---:|---:|
| GPQA | 177/198 | 178/198 | 178/198 | **178/198** |
| MMLU | 444/500 | 446/500 | 445/500 | **450/500** |
| LCB | 83/100 | 90/100 | 90/100 | **90/100** |

GPQA、LCB 三种精度一题不差;MMLU 在 445–450 之间,属于采样抖动,不是精度造成的。动态 FP8 是推理时对 BF16 权重在线量化,不另出包。

### 全档位:分数、思考长度、94K 截断与空答

思考长度取 `usage.reasoning_tokens`;94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。原版 FP8、BF16、动态 FP8、静态 FP8 为两张 RTX PRO 6000、每卡 C8;NVFP4 三档为单张 RTX PRO 6000、C8,其余口径相同。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | 原版 Qwen3.8 27B(FP8) | 177/198 | 5,299 / 12,607 / 50,577 | 4 | 3 |
| GPQA | BF16 | **178/198** | **3,196** / **8,200** / **28,417** | **2** | **2** |
| GPQA | 动态 FP8 | **178/198** | **2,815** / **8,371** / **27,744** | **1** | **1** |
| GPQA | 静态 FP8 | **178/198** | **2,966** / **7,832** / **26,431** | **1** | **2** |
| GPQA | NVFP4 W4A16 | 170/198 | **2,965** / **9,667** / **28,433** | **2** | 3 |
| GPQA | NVFP4 W4A4 | 167/198 | **2,876** / **10,996** / **31,986** | **2** | 3 |
| GPQA | NVFP4 W4A4-W8A8 | 172/198 | **2,953** / **10,010** / **35,731** | **2** | 4 |
| MMLU | 原版 Qwen3.8 27B(FP8) | 444/500 | 205 / 373 / 1,622 | 1 | 0 |
| MMLU | BF16 | **446/500** | **154** / **252** / **779** | 1 | 0 |
| MMLU | 动态 FP8 | **445/500** | **138** / **271** / **881** | 1 | 0 |
| MMLU | 静态 FP8 | **450/500** | **154** / **279** / **937** | 1 | 0 |
| MMLU | NVFP4 W4A16 | 439/500 | **159** / **277** / **1,061** | 1 | 0 |
| MMLU | NVFP4 W4A4 | 440/500 | **168** / **306** / **967** | 2 | 0 |
| MMLU | NVFP4 W4A4-W8A8 | 442/500 | **157** / **273** / **778** | **0** | 0 |
| LCB | 原版 Qwen3.8 27B(FP8) | 83/100 | 8,388 / 24,241 / 94,208 | 13 | 13 |
| LCB | BF16 | **90/100** | **5,073** / **16,033** / **38,911** | **2** | **2** |
| LCB | 动态 FP8 | **90/100** | **4,791** / **15,866** / **41,168** | **4** | **4** |
| LCB | 静态 FP8 | **90/100** | **4,511** / **16,027** / **43,992** | **3** | **3** |
| LCB | NVFP4 W4A16 | **91/100** | **5,119** / **15,790** / **47,768** | **4** | **3** |
| LCB | NVFP4 W4A4 | **92/100** | **6,338** / **15,771** / **54,096** | **3** | **3** |
| LCB | NVFP4 W4A4-W8A8 | **88/100** | **4,731** / **15,122** / **41,344** | **2** | **1** |

加粗表示优于原版(分数更高,或 P50 / P70 / P90、94K 截断、空答更低);等于或不如原版的不加粗。

LCB 改善最明显:原版 13 条 94K 截断全是空代码(截断 13、空答 13),Coder390 各档降到 2–4 条。W4A4 的 3 条是第 0、53、96 题(成绩文件中的题目编号),同样是截断后没有代码;W4A16 的 4 条中,第 6、7、54 题没有代码,第 53 题有 20 个字符的代码但答错;W4A4-W8A8 的 2 条中,第 11 题没有代码,第 6 题有 2,338 个字符的代码但答错。GPQA 的 94K 截断原版 4 条,各档 1–2 条;MMLU 原版 1 条,各档 0–2 条,没有明显变化。

<details open>
<summary>六种精度明细(按思考长度分桶)</summary>

分桶为「答对/该桶题数」,按思考长度左闭右开。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 | <2K | 2–12K | 12–24K | 24–48K | ≥48K |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| GPQA | BF16 | 178/198 | 3,196 / 8,200 / 28,417 | 2 | 2 | 80/85 | 66/68 | 17/20 | 12/18 | 3/7 |
| GPQA | 动态 FP8 | 178/198 | 2,815 / 8,371 / 27,744 | 1 | 1 | 78/81 | 68/70 | 18/21 | 11/17 | 3/9 |
| GPQA | 静态 FP8 | 178/198 | 2,966 / 7,832 / 26,431 | 1 | 2 | 82/84 | 68/74 | 17/19 | 9/17 | 2/4 |
| GPQA | NVFP4 W4A16 | 170/198 | 2,965 / 9,667 / 28,433 | 2 | 3 | 77/80 | 64/70 | 17/21 | 8/17 | 4/10 |
| GPQA | NVFP4 W4A4 | 167/198 | 2,876 / 10,996 / 31,986 | 2 | 3 | 76/82 | 58/60 | 20/23 | 12/26 | 1/7 |
| GPQA | NVFP4 W4A4-W8A8 | 172/198 | 2,953 / 10,010 / 35,731 | 2 | 4 | 79/82 | 58/63 | 19/22 | 14/22 | 2/9 |
| MMLU | BF16 | 446/500 | 154 / 252 / 779 | 1 | 0 | 432/472 | 13/23 | 1/3 | 0/0 | 0/2 |
| MMLU | 动态 FP8 | 445/500 | 138 / 271 / 881 | 1 | 0 | 436/477 | 8/21 | 0/1 | 0/0 | 1/1 |
| MMLU | 静态 FP8 | 450/500 | 154 / 279 / 937 | 1 | 0 | 435/469 | 13/27 | 2/3 | 0/0 | 0/1 |
| MMLU | NVFP4 W4A16 | 439/500 | 159 / 277 / 1,061 | 1 | 0 | 427/471 | 11/26 | 0/1 | 1/1 | 0/1 |
| MMLU | NVFP4 W4A4 | 440/500 | 168 / 306 / 967 | 2 | 0 | 426/469 | 13/28 | 0/1 | 0/0 | 1/2 |
| MMLU | NVFP4 W4A4-W8A8 | 442/500 | 157 / 273 / 778 | 0 | 0 | 432/477 | 8/20 | 1/2 | 1/1 | 0/0 |
| LCB | BF16 | 90/100 | 5,073 / 16,033 / 38,911 | 2 | 2 | 40/40 | 25/26 | 11/14 | 9/11 | 5/9 |
| LCB | 动态 FP8 | 90/100 | 4,791 / 15,866 / 41,168 | 4 | 4 | 38/39 | 25/26 | 11/14 | 12/13 | 4/8 |
| LCB | 静态 FP8 | 90/100 | 4,511 / 16,027 / 43,992 | 3 | 3 | 39/39 | 24/26 | 13/13 | 12/14 | 2/8 |
| LCB | NVFP4 W4A16 | 91/100 | 5,119 / 15,790 / 47,768 | 4 | 3 | 38/38 | 26/27 | 13/13 | 10/12 | 4/10 |
| LCB | NVFP4 W4A4 | 92/100 | 6,338 / 15,771 / 54,096 | 3 | 3 | 33/33 | 30/31 | 9/11 | 13/14 | 7/11 |
| LCB | NVFP4 W4A4-W8A8 | 88/100 | 4,731 / 15,122 / 41,344 | 2 | 1 | 40/41 | 21/24 | 16/16 | 7/10 | 4/9 |

</details>

### NVFP4 三档

**口径**:单张 RTX PRO 6000,C8,上下文 100K,生成上限 94,208,客户端不计超时,DFlash2 草稿,SGLang;GPQA 198、MMLU 500、LCB 100 全量。

| 套题 | NVFP4 W4A16 | NVFP4 W4A4 | NVFP4 W4A4-W8A8 |
|---|---:|---:|---:|
| GPQA | 170/198 | 167/198 | 172/198 |
| MMLU | 439/500 | 440/500 | 442/500 |
| LCB | 91/100 | 92/100 | 88/100 |

NVFP4 三档的思考长度、94K 截断与空答见上方「全档位」总表。LCB 按每题的 `pass` 字段判对错。原始记录见 `evaluation/SCORES_NVFP4_W4A16.json`、`evaluation/SCORES_NVFP4_W4A4.json`、`evaluation/SCORES_NVFP4_MIXED.json`(W4A4-W8A8 档)。

### NInfer 两档:分数、思考长度、94K 截断与空答

**口径**:分数沿用 2026-10-05 在同一条 NInfer 文本路径上测得的官方三联;单张 RTX PRO 6000,官方 NInfer 引擎(`iamwavecut/ninfer-all`),C8,上下文 100K,生成上限 94,208,客户端不计超时,**不开投机**;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。本次上传的新包只在这条文本路径上加入 Q8 MTP、DFlash2 草稿与 proposal head,文本路径不变,全量三联没有重跑。只有 NInfer 引擎能加载 `.ninfer`;SGLang / vLLM / llama.cpp / transformers 均不能加载。

思考长度取 `usage.reasoning_tokens`(即 `completion_tokens_details.reasoning_tokens`);94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8)。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | NInfer W4A4 | 177/198 | **2,934** / **7,646** / **25,804** | **2** | **2** |
| GPQA | NInfer W4A4-W8A8 | 177/198 | **3,176** / **8,844** / **24,804** | **2** | **2** |
| MMLU | NInfer W4A4 | **449/500** | **164** / **285** / **830** | **0** | 0 |
| MMLU | NInfer W4A4-W8A8 | 444/500 | **163** / **281** / **923** | **0** | 0 |
| LCB | NInfer W4A4 | **89/100** | **3,994** / **15,533** / **36,125** | **2** | **2** |
| LCB | NInfer W4A4-W8A8 | **92/100** | **4,046** / **15,829** / **40,479** | **2** | **3** |

NInfer W4A4 的 LCB 空答 2 条是第 11、15 题,均为截断后没有代码;GPQA 空答 2 条是第 79、127 题,均为截断且 pred 为空。MMLU 无截断、无空答。NInfer W4A4-W8A8 的 LCB 空答 3 条是第 17、53、54 题(第 17 题正常停但没有代码,第 53、54 题截断且没有代码);GPQA 空答 2 条是第 79、127 题,均为截断且 pred 为空。MMLU 无截断、无空答。

<details open>
<summary>NInfer 两档明细(按思考长度分桶)</summary>

分桶为「答对/该桶题数」,按思考长度左闭右开。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 | <2K | 2–12K | 12–24K | 24–48K | ≥48K |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| GPQA | NInfer W4A4 | 177/198 | 2,934 / 7,646 / 25,804 | 2 | 2 | 76/83 | 69/71 | 17/22 | 14/19 | 1/3 |
| GPQA | NInfer W4A4-W8A8 | 177/198 | 3,176 / 8,844 / 24,804 | 2 | 2 | 79/82 | 70/74 | 13/21 | 12/16 | 3/5 |
| MMLU | NInfer W4A4 | 449/500 | 164 / 285 / 830 | 0 | 0 | 438/480 | 11/19 | 0/1 | 0/0 | 0/0 |
| MMLU | NInfer W4A4-W8A8 | 444/500 | 163 / 281 / 923 | 0 | 0 | 435/478 | 8/21 | 1/1 | 0/0 | 0/0 |
| LCB | NInfer W4A4 | 89/100 | 3,994 / 15,533 / 36,125 | 2 | 2 | 40/41 | 21/23 | 12/14 | 13/16 | 3/6 |
| LCB | NInfer W4A4-W8A8 | 92/100 | 4,046 / 15,829 / 40,479 | 2 | 3 | 38/38 | 26/26 | 14/16 | 11/12 | 3/8 |

</details>

### INT8 W8A8:分数、94K 截断与空答

**口径**:单张 RTX PRO 6000,vLLM 0.28,C8,上下文 100K,生成上限 94,208,客户端不计超时,**不开投机**,思考档位 xhigh;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。INT8 W8A8 只有文本路径,只能用 vLLM 加载。

94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8),其数字见上方「全档位」总表。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | INT8 W8A8 | 175/198 | **3,862** / **9,055** / **25,299.5** | **1** | **1** |
| MMLU | INT8 W8A8 | **450/500** | **156** / **291** / **864.4** | **0** | 0 |
| LCB | INT8 W8A8 | **91/100** | — | **2** | **0** |

注:INT8 W8A8 测评时 vLLM 未开推理解析器,`usage.reasoning_tokens` 均为 0,思考与答案都记在正文里。GPQA 与 MMLU 的思考长度按原文重新计数:取正文中 `</think>` 之前的文本,用 BF16 tokenizer 计数(与 GGUF 档相同的方法)。LCB 的结果文件只保存了代码,没有保存思考原文,无法计数,记「—」。

GPQA 的 1 条截断是第 127 题,pred 为空,同时记为空答。LCB 的 2 条截断是第 7、53 题:第 7 题截断后留下的代码运行出错,判错;第 53 题虽然截断,代码仍判对;LCB 没有空答。MMLU 无截断、无空答。LCB 按难度为 hard 38/46、medium 30/31、easy 23/23。

### GGUF Q2 / Q3 / Q4 LynnStyle:分数、思考长度、94K 截断与空答

**口径**:单张 RTX PRO 6000,llama.cpp(`llama-server`),C4,每槽上下文约 100K,生成上限 94,208,客户端不计超时,思考打开;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同;`GGUF-NInfer/` 下对应的 `.ninfer` 由同一份 GGUF 转换,全量三联只在 GGUF 上跑。

94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8),其数字见上方「全档位」总表。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q2 LynnStyle | 177/198 | **2,989.5** / **8,923.8** / **27,156.1** | **3** | **0** |
| MMLU | GGUF Q2 LynnStyle | 433/500 | **181** / **326.3** / **1,020.5** | 1 | 0 |
| LCB | GGUF Q2 LynnStyle | **90/100** | **5,656.5** / **17,835.8** / **40,067.3** | **1** | **1** |
| GPQA | GGUF Q3 LynnStyle | 173/198 | **3,125.5** / **7,265.2** / **24,343.1** | **1** | **1** |
| MMLU | GGUF Q3 LynnStyle | **449/500** | — | **0** | 0 |
| LCB | GGUF Q3 LynnStyle | **92/100** | — | **1** | **1** |
| GPQA | GGUF Q4 LynnStyle | 175/198 | **2,951.0** / **8,159.3** / **25,649.0** | **1** | **2** |
| MMLU | GGUF Q4 LynnStyle | **448/500** | — | **0** | 0 |
| LCB | GGUF Q4 LynnStyle | **89/100** | — | **2** | **2** |

注:思考长度从原文用 BF16 tokenizer 计数(GPQA/LCB 用 `reasoning` 字段,MMLU 由 `response` 末行前文本拆分)。Q3 与 Q4 LynnStyle 的 MMLU / LCB 没有保存思考原文,无法计数,记「—」。

### GGUF Q6_K:分数、思考长度、94K 截断与空答

**口径**:单张 RTX PRO 6000,llama.cpp(`llama-server`)加载 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`,C4,上下文 100K,生成上限 94,208,客户端不计超时,思考档位 xhigh;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` 由同一份 GGUF 转换而来,主干量化相同,全量三联只在 GGUF 上跑。

思考长度取 `usage.reasoning_tokens`;94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8),其数字见上方「全档位」总表。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q6_K | 174/198 | **3,683** / **9,814** / **27,966** | **2** | **2** |
| MMLU | GGUF Q6_K | **448/500** | **162** / **310.3** / **939.4** | **0** | 0 |
| LCB | GGUF Q6_K | **91/100** | — | **0** | **1** |

注:MMLU 与 LCB 测评时 llama.cpp 没有单独返回思考 token(`usage` 里没有 `reasoning_tokens`)。MMLU 的思考长度由 `response` 末行前文本拆分,用 BF16 tokenizer 计数(与 Q8_0 相同的方法);LCB 的结果文件没有保存思考原文,无法计数,记「—」;GPQA 的思考 token 由测评脚本单独统计。

GPQA 的 2 条截断是第 79、127 题,均写满 94,208 且 pred 为空,同时记为空答。MMLU 无截断、无空答。

LCB 无 94K 截断;空答 1 条是第 92 题,正常停止但没有给出代码。

LCB 以 llama.cpp 的结果为准:LCB 测评脚本请求 NInfer 时收到的回复不是合法 JSON,这是测评脚本与接口的兼容问题,不是模型质量问题;同一份 GGUF 用 llama.cpp 跑同一批抽测题全部通过。


### GGUF Q8_0:分数、思考长度、94K 截断与空答

**口径**:单张 RTX PRO 6000,llama.cpp(`llama-server`)加载 `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`,C4,上下文 100K,生成上限 94,208,客户端不计超时,思考档位 xhigh;GPQA 198、MMLU 500、LCB 100 全量;空答记错,截断但答对记对,失败样本全部留在分母里。`GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer` 由同一份 GGUF 转换而来,主干量化相同,全量三联只在 GGUF 上跑。

思考长度:GPQA 取 `usage.reasoning_tokens`;MMLU 由 `response` 末行前文本拆分并用 BF16 tokenizer 计数;LCB 由落盘的 `reasoning` 原文计数。94K 截断指写满生成上限。LCB 空答指没有提取到可运行代码的题数。加粗表示优于原版 Qwen3.8 27B(FP8)。

| 套题 | 精度 | 分数 | 思考 P50 / P70 / P90 | 94K 截断 | 空答 |
|---|---|---:|---|---:|---:|
| GPQA | GGUF Q8_0 | 171/198 | **3,102.5** / **7,971** / **28,891.6** | **2** | **0** |
| MMLU | GGUF Q8_0 | 443/500 | **164** / **291** / **741** | **0** | 0 |
| LCB | GGUF Q8_0 | **90/100** | **4,098.5** / **16,087.8** / **39,135.5** | **3** | **3** |

GPQA 截断 2、空答 0。MMLU 无截断、无空答。LCB 截断 3、空答 3(写满长度且无代码)。

LCB 以 llama.cpp 的结果为准:LCB 测评脚本请求 NInfer 时收到的回复不是合法 JSON,这是测评脚本与接口的兼容问题,不是模型质量问题。


## 量化档

| 档位 | 目录 | 说明 | 包大小(字节) | BPW | GPQA / MMLU / LCB |
|---|---|---|---:|---:|---|
| BF16 | `BF16/` | 完整多模态,原版 config,内置官方 BF16 MTP,含 DFlash2 草稿,免补丁 | 55,583,125,732(约 51.8 GiB) | 16.00 | 178 / 446 / 90 |
| 静态 FP8 Block128 | `FP8/` | 完整多模态,内置官方 BF16 MTP,含 DFlash2 草稿 | 33,669,220,491(约 31.4 GiB) | 9.00 | 178 / 450 / 90 |
| NVFP4 W4A16 | `NVFP4/W4A16/` | 完整多模态,语言模型 Linear 为 NVFP4 权重 + BF16 激活,内置官方 BF16 MTP,含 DFlash2 草稿,SGLang 免补丁 | 20,613,406,953(约 19.2 GiB,不含草稿) | 5.93 | 170 / 439 / 91 |
| NVFP4 W4A4 | `NVFP4/W4A4/` | 完整多模态,语言模型 Linear 为 NVFP4 权重 + NVFP4 激活,内置官方 BF16 MTP,含 DFlash2 草稿,SGLang 免补丁 | 20,613,386,462(约 19.2 GiB,不含草稿) | 5.93 | 167 / 440 / 92 |
| NVFP4 W4A4-W8A8 | `NVFP4/W4A4-W8A8/` | 完整多模态,语言模型 MLP 为 NVFP4 W4A4、注意力与线性注意力投影为 FP8 W8A8,内置官方 BF16 MTP,含 DFlash2 草稿,SGLang 免补丁 | 23,769,634,648(约 22.1 GiB,不含草稿) | 6.84 | 172 / 442 / 88 |
| NInfer W4A4 | `NVFP4-NInfer/W4A4/` | 官方 NInfer 包(`.ninfer`),W4A4 文本路径,包内含 Q8 MTP、DFlash2 草稿与 proposal head,视觉塔不在包内,NInfer 下不能输入图片(同一文件夹的 `vision-bf16.safetensors` NInfer 加载不了);仅 NInfer 引擎(`iamwavecut/ninfer-all`)可加载 | 23,477,856,260(约 21.9 GiB) | 6.76 | 177 / 449 / 89 |
| NInfer W4A4-W8A8 | `NVFP4-NInfer/W4A4-W8A8/` | 官方 NInfer 混合精度包(`.ninfer`),W4A4-W8A8 文本路径,包内含 Q8 MTP、DFlash2 草稿与 proposal head,视觉塔不在包内,NInfer 下不能输入图片(同一文件夹的 `vision-bf16.safetensors` NInfer 加载不了);仅 NInfer 引擎(`iamwavecut/ninfer-all`)可加载 | 23,477,856,260(约 21.9 GiB) | 6.76 | 177 / 444 / 92 |
| NInfer W4A4 纯文本 | `NVFP4-NInfer/W4A4/` | 官方 NInfer 包(`.ninfer`),仅文本路径,不含 MTP、视觉塔与 DFlash2 草稿,只能不开投机启动;仅 NInfer 引擎(`iamwavecut/ninfer-all`)可加载 | 20,752,974,596(约 19.3 GiB) | 6.17 | 未单独测评 |
| NInfer W4A4-W8A8 纯文本 | `NVFP4-NInfer/W4A4-W8A8/` | 官方 NInfer 混合精度包(`.ninfer`),仅文本路径,不含 MTP、视觉塔与 DFlash2 草稿,只能不开投机启动;仅 NInfer 引擎(`iamwavecut/ninfer-all`)可加载 | 20,752,974,596(约 19.3 GiB) | 6.17 | 未单独测评 |
| INT8 W8A8 | `INT8/W8A8/` | 仅文本(`Qwen3_5ForCausalLM`),SmoothQuant 按通道 INT8 权重 + 按 token 动态 INT8 激活,compressed-tensors 格式;不含视觉塔、MTP 与 DFlash2 草稿;仅 vLLM 可加载 | 29,500,937,028(约 27.5 GiB) | 8.77 | 175 / 450 / 91 |
| GGUF Q3 LynnStyle | `GGUF/` | 混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf`):最低 Q3;内置 **Q4 MTP**;视觉外挂 | 17,303,770,432(约 16.1 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q3 LynnStyle · NInfer | `GGUF-NInfer/` | 由 Q3 LynnStyle GGUF 转换;内置 Q4 MTP;仅 NInfer-all | 17,300,551,168(约 16.1 GiB) | 5.07 | 173 / 449 / 92 |
| GGUF Q4 LynnStyle | `GGUF/` | 混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf`):最低 Q4;内置 **Q4 MTP**;视觉外挂 | 19,620,406,592(约 18.3 GiB) | 5.75 | 175 / 448 / 89 |
| GGUF Q4 LynnStyle · NInfer | `GGUF-NInfer/` | 由 Q4 LynnStyle GGUF 转换;内置 Q4 MTP;仅 NInfer-all | 19,617,187,328(约 18.3 GiB) | 5.74 | 175 / 448 / 89 |
| GGUF Q2 LynnStyle | `GGUF/` | 混合精度 LynnStyle GGUF(`Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf`):最低 Q2;内置 **Q4 MTP**;视觉外挂 | 13,276,009,792(约 12.4 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q2 LynnStyle · NInfer | `GGUF-NInfer/` | 由 Q2 LynnStyle GGUF 转换;内置 Q4 MTP;仅 NInfer-all | 13,272,798,720(约 12.4 GiB) | 3.89 | 177 / 433 / 90 |
| GGUF Q8_0 | `GGUF/` | llama.cpp 用 GGUF 单文件(`Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`):主干 Q8_0,内置 MTP 头,不需要外挂草稿;视觉用 `GGUF/` 内的 mmproj(llama.cpp `--mmproj`) | 29,069,202,688(约 27.1 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q8_0 · NInfer | `GGUF-NInfer/` | 由同一份 Q8_0 GGUF 转换的 NInfer 包(`.ninfer`),内置 MTP 头;仅 NInfer-all(`iamwavecut/ninfer-all`)可加载;成绩为同一份 GGUF 在 llama.cpp 上测得 | 29,065,983,488(约 27.1 GiB) | 8.51 | 171 / 443 / 90 |
| GGUF Q6_K | `GGUF/` | llama.cpp 用 GGUF 单文件(`Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`):主干 Q6_K + imatrix 校准,内置 Q8 MTP 头,不需要外挂草稿;视觉用 `GGUF/` 内的 mmproj(llama.cpp `--mmproj`) | 23,177,516,384(约 21.6 GiB) | 6.79 | 174 / 448 / 91 |
| GGUF Q6_K · NInfer | `GGUF-NInfer/` | 由同一份 GGUF 转换的 NInfer 包(`.ninfer`),主干量化相同,内置 MTP 头(attention/MLP 权重 Q6_K,输入投影 Q8_0),包内不含视觉塔,NInfer 下不能输入图片;仅 NInfer-all(`iamwavecut/ninfer-all`)可加载;成绩为同一份 GGUF 在 llama.cpp 上测得 | 23,084,144,128(约 21.5 GiB) | 6.76 | 174 / 448 / 91 |

BPW(bits per weight)是整包的有效平均位宽:整包主模型权重文件(`.safetensors`,含视觉塔、MTP 与 scale 张量,不含 DFlash2 草稿)总字节数 × 8 ÷ 总参数数。总参数数按 safetensors 头部统计,五档一致,均为 27,781,427,952 个(NVFP4 的 U8 打包张量一个字节算 2 个元素,scale 张量不计元素)。BF16、静态 FP8、NVFP4 W4A16、NVFP4 W4A4、NVFP4 W4A4-W8A8 的权重文件总字节数依次为 55,563,008,568、31,242,033,200、20,593,097,872、20,593,145,056、23,749,329,544。各档都是混合精度(不同层不同位宽),标称位宽会误导,BPW 反映单位体积下的质量密度。

NInfer 两档的 BPW 按整包 `.ninfer` 文件字节数 × 8 ÷ 总参数数 27,781,427,952 计算:两档文件均为 23,477,856,260 字节,BPW 均为 6.76。`.ninfer` 包内含 Q8 MTP、DFlash2 草稿与 proposal head,不含视觉塔;上方 NVFP4 / BF16 / FP8 的 safetensors 计法不计 DFlash2 草稿,两种计法不同,不宜直接横向比较 BPW。

NInfer 两个纯文本包只有文本路径,BPW 按 `.ninfer` 文件字节数 × 8 ÷ 文本参数数 26,895,998,464(与下方 INT8 W8A8 同一分母)计算:两个文件均为 20,752,974,596 字节,BPW 均为 6.17。分母与 27,781,427,952 不同,不宜直接和带 MTP 的 NInfer 包或 NVFP4 各档横向比较 BPW。

INT8 W8A8 只有文本路径,BPW 按 8 个 `.safetensors` 权重文件总字节数 29,480,791,128 × 8 ÷ 文本参数数 26,895,998,464 计算,为 8.77。文本参数数按本包 safetensors 头部统计(INT8 与 BF16 张量计元素,scale 张量不计元素),与 BF16 包去掉视觉塔(460,730,096)和 MTP(424,699,392)后的参数数一致;分母与上方各档的 27,781,427,952 不同,不宜直接横向比较 BPW。

GGUF Q8_0 两个包的 BPW 按单个文件字节数 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 计算:GGUF 29,069,202,688 字节、8.51,NInfer 29,065,983,488 字节、8.51。GGUF Q6_K 两个包的 BPW 按单个文件字节数 × 8 ÷ 文本 + MTP 参数数 27,320,697,856 计算:GGUF 为 23,177,516,384 字节、6.79,NInfer 为 23,084,144,128 字节、6.76。参数数按 GGUF 头部统计(866 个张量:文本 26,895,998,464 + MTP 424,699,392);视觉是外挂的 mmproj,不在包内,也不计入分母。分母与上方各档的 27,781,427,952 及 INT8 W8A8 的 26,895,998,464 都不同,不宜直接横向比较 BPW。

- 每档各自带一份 DFlash2 草稿(文件完全相同,2,407,384,680 字节):`FP8/DFlash2-FP8/`、`BF16/DFlash2-FP8/`、`NVFP4/W4A16/DFlash2-FP8/`、`NVFP4/W4A4/DFlash2-FP8/`、`NVFP4/W4A4-W8A8/DFlash2-FP8/`。
- DFlash2 草稿格式:FP8 E4M3 权重,128×128 分块 scale(`weight_scale_inv`),与 FP8 主体相同;q/k/v 投影、`fc`、候选选择器、卷积和 norm 保持 BF16。2026-10-08 起替换了原来按张量 scale 的草稿(只认分块 scale 的引擎,如 radiance,加载旧草稿不报错,但几乎不接受草稿 token)。新草稿已通过格式核对和 SGLang 源码核对,引擎实测待补。本卡 DFlash2 测速数字是用旧草稿测的。
- BF16 与静态 FP8 的速度数据在静态 FP8 包上测得,BF16 未单独测速,沿用同一组数据;NVFP4 三档各自单独测速。
- NVFP4 三档的分数为单卡 C8 测得,口径见上文「NVFP4 三档」。
- NInfer 两档成绩沿用 2026-10-05 在同一文本路径上以单卡 C8、官方 NInfer、不开投机测得的三联,口径见上文「NInfer 两档」;NInfer 两档的速度为新包单独实测,见下文「最佳 TPS 推荐与并发推荐」中的「NInfer 两档」。
- INT8 W8A8 成绩为单卡 C8、vLLM、不开投机测得的全量三联,口径见上文「INT8 W8A8」;速度为快测,见下文「最佳 TPS 推荐与并发推荐」中的「INT8 W8A8」。
- GGUF Q6_K 成绩为单卡 C4、llama.cpp 测得的全量三联,口径见上文「GGUF Q6_K」;速度为快测,见下文「最佳 TPS 推荐与并发推荐」中的「GGUF Q6_K」。
- GGUF Q8_0 成绩为单卡 C4、llama.cpp 测得的全量三联,口径见上文「GGUF Q8_0」;速度见下文「GGUF Q8_0」(NInfer C8 MTP 486.3;llama.cpp C4 MTP 190.8)。
- NInfer 两档已上传到 `NVFP4-NInfer/W4A4/` 与 `NVFP4-NInfer/W4A4-W8A8/`,INT8 W8A8 已上传到 `INT8/W8A8/`,GGUF Q2 / Q3 / Q4 LynnStyle、Q6_K 与 Q8_0 已上传到 `GGUF/` 与 `GGUF-NInfer/`。

## 最佳 TPS 推荐与并发推荐

测试环境:单张 RTX PRO 6000 Blackwell 96GB;SGLang,上下文 32K(32,768),生成上限 4,096,开思考,采样用模型默认值。

| 场景 | 推荐 | 总吞吐 tok/s | 单请求 tok/s |
|---|---|---:|---:|
| 单请求最快 | DFlash2 · C1 | 146.7 | **180.3** |
| 总吞吐最高 | DFlash2 · C16 | **1,057.5** | 93.6 |
| 日常均衡 | DFlash2 · C8 | 646.3 | 113.9 |
| 只用 MTP:单请求最快 | MTP · C1 | 82.1 | **91.1** |
| 只用 MTP:总吞吐最高 | MTP · C16 | **612.7** | 60.1 |
| 只用 MTP:日常均衡 | MTP · C8 | 380.3 | 71.1 |

- **选哪种投机**:实测 C1–C16 每一档,DFlash2 的总吞吐和单请求速度都高于 MTP,能用就用 DFlash2。
- **MTP 的位置**:在 vLLM 上(DFlash2 只在 SGLang 上验证过),或不想另载 DFlash2 草稿时用 MTP;只用 MTP 时:追求单请求速度用 C1(91.1 tok/s),交互与少量并发可用 C4(总吞吐 293.3,单请求 84.0),多人共用用 C8(总吞吐 380.3,单请求 71.1),只看总量用 C16(总吞吐 612.7,单请求 60.1)。
- **并发**:交互为主用 C1–C4;多人共用或批量跑用 C8;只看总量用 C16。C16 以上未测。

<details>
<summary>完整实测表</summary>

C1 为主测(4 个请求),C4/C8/C16 为加大请求数(每档 6×C)的复测。「相对不开投机」为同并发下总吞吐之比。

| 投机方式 | 并发 | 总吞吐 tok/s | 单请求解码 tok/s(中位) | 首 token 延迟 s(中位) | 接受长度 | 接受率 | 相对不开投机 |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP(包内 BF16) | C1 | 82.1 | 91.1 | 0.12 | 2.858 | 0.619 | 1.82× |
| MTP(包内 BF16) | C4 | 293.3 | 84.0 | 0.15 | 2.844 | 0.615 | 1.96× |
| MTP(包内 BF16) | C8 | 380.3 | 71.1 | 0.16 | 2.813 | 0.604 | 1.34× |
| MTP(包内 BF16) | C16 | 612.7 | 60.1 | 0.17 | 2.747 | 0.582 | 1.45× |
| DFlash2 | C1 | 146.7 | 180.3 | 0.12 | 4.289 | 0.470 | 3.25× |
| DFlash2 | C4 | 384.9 | 124.4 | 0.16 | 3.982 | 0.425 | 2.57× |
| DFlash2 | C8 | 646.3 | 113.9 | 0.15 | 4.131 | 0.447 | 2.28× |
| DFlash2 | C16 | 1,057.5 | 93.6 | 0.24 | 4.017 | 0.431 | 2.50× |
| 不开投机 | C1 | 45.1 | 45.6 | 0.11 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C4 | 149.5 | 42.2 | 0.13 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C8 | 283.0 | 41.7 | 0.12 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C16 | 422.8 | 38.4 | 0.13 | 不适用 | 不适用 | 1.00× |

| 投机方式 | 单请求最快 | 推荐并发(单请求速度不低于 C1 的 60% 时总吞吐最高) | 总吞吐最高 |
|---|---|---|---|
| MTP | C1(91.1 tok/s) | C16(612.7 tok/s,单请求 60.1) | C16 |
| DFlash2 | C1(180.3 tok/s) | C8(646.3 tok/s,单请求 113.9) | C16(1,057.5 tok/s) |
| 不开投机 | C1(45.6 tok/s) | C16(422.8 tok/s) | C16 |

</details>

### NVFP4 三档

测试环境同上:单张 RTX PRO 6000 Blackwell 96GB;SGLang,上下文 32K(32,768),生成上限 4,096,开思考,采样用模型默认值。数据取自 `evaluation/BENCH_NVFP4_W4A16.json`、`evaluation/BENCH_NVFP4_W4A4.json`、`evaluation/BENCH_NVFP4_MIXED.json`(W4A4-W8A8 档)。

| 场景 | 推荐 | W4A16 总吞吐 tok/s | W4A16 单请求 tok/s | W4A4 总吞吐 tok/s | W4A4 单请求 tok/s | W4A4-W8A8 总吞吐 tok/s | W4A4-W8A8 单请求 tok/s |
|---|---|---:|---:|---:|---:|---:|---:|
| 单请求最快 | DFlash2 · C1 | 147.4 | **218.4** | 188.6 | **211.5** | 175.1 | **216.8** |
| 总吞吐最高 | DFlash2 · C16 | **1,012.3** | 96.6 | **1,143.2** | 121.1 | **1,146.4** | 105.5 |
| 日常均衡 | DFlash2 · C8 | 472.4 | 131.7 | 689.8 | 132.4 | 627.9 | 132.4 |
| 只用 MTP:单请求最快 | MTP · C1 | 101.1 | **128.9** | 104.7 | **124.5** | 99.9 | **116.3** |
| 只用 MTP:总吞吐最高 | MTP · C16 | **817.3** | 70.6 | **912.4** | 73.0 | **580.2** | 69.4 |
| 只用 MTP:日常均衡 | MTP · C8 | 450.7 | 91.3 | 355.5 | 86.6 | 417.2 | 83.2 |

- **选哪种投机**:W4A4 与 W4A4-W8A8 在 C1–C16 每一档,DFlash2 的总吞吐和单请求速度都高于 MTP;W4A16 只有 C4 的总吞吐是 MTP 更高(351.4 对 315.2),其余各档与全部单请求速度都是 DFlash2 更高。
- **只用 MTP 时**:W4A16 追求单请求速度用 C1(128.9 tok/s),交互与少量并发可用 C4(总吞吐 351.4,单请求 108.0),多人共用用 C8(总吞吐 450.7,单请求 91.3),只看总量用 C16(总吞吐 817.3,单请求 70.6);W4A4 依次为 C1(124.5 tok/s)、C4(总吞吐 323.2,单请求 103.9)、C8(总吞吐 355.5,单请求 86.6)、C16(总吞吐 912.4,单请求 73.0);W4A4-W8A8 依次为 C1(116.3 tok/s)、C4(总吞吐 213.0,单请求 99.8)、C8(总吞吐 417.2,单请求 83.2)、C16(总吞吐 580.2,单请求 69.4)。
- **接受长度**:MTP 为 2.608–2.967(W4A16)、2.597–2.923(W4A4)与 2.647–2.865(W4A4-W8A8);DFlash2 为 3.351–4.143(W4A16)、3.723–4.327(W4A4)与 3.828–4.364(W4A4-W8A8)。
- **并发**:C16 以上未测。

<details>
<summary>NVFP4 W4A16 完整实测表</summary>

每档请求数:C1 4 个、C4 12 个、C8 24 个、C16 48 个。「相对不开投机」为同并发下总吞吐之比。

| 投机方式 | 并发 | 总吞吐 tok/s | 单请求解码 tok/s(中位) | 首 token 延迟 s(中位) | 接受长度 | 接受率 | 相对不开投机 |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP(包内 BF16) | C1 | 101.1 | 128.9 | 0.11 | 2.608 | 0.537 | 1.44× |
| MTP(包内 BF16) | C4 | 351.4 | 108.0 | 0.13 | 2.796 | 0.599 | 2.34× |
| MTP(包内 BF16) | C8 | 450.7 | 91.3 | 0.13 | 2.743 | 0.581 | 1.50× |
| MTP(包内 BF16) | C16 | 817.3 | 70.6 | 0.15 | 2.967 | 0.656 | 1.58× |
| DFlash2 | C1 | 147.4 | 218.4 | 0.10 | 3.469 | 0.353 | 2.11× |
| DFlash2 | C4 | 315.2 | 164.9 | 0.13 | 3.351 | 0.337 | 2.10× |
| DFlash2 | C8 | 472.4 | 131.7 | 0.14 | 3.454 | 0.351 | 1.57× |
| DFlash2 | C16 | 1,012.3 | 96.6 | 0.23 | 4.143 | 0.449 | 1.96× |
| 不开投机 | C1 | 70.0 | 71.6 | 0.09 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C4 | 150.3 | 62.1 | 0.10 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C8 | 300.9 | 62.1 | 0.10 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C16 | 515.8 | 54.7 | 0.10 | 不适用 | 不适用 | 1.00× |

| 投机方式 | 单请求最快 | 推荐并发(单请求速度不低于 C1 的 60% 时总吞吐最高) | 总吞吐最高 |
|---|---|---|---|
| MTP | C1(128.9 tok/s) | C8(450.7 tok/s,单请求 91.3) | C16(817.3 tok/s) |
| DFlash2 | C1(218.4 tok/s) | C8(472.4 tok/s,单请求 131.7) | C16(1,012.3 tok/s) |
| 不开投机 | C1(71.6 tok/s) | C16(515.8 tok/s) | C16(515.8 tok/s) |

</details>

<details>
<summary>NVFP4 W4A4 完整实测表</summary>

每档请求数:C1 4 个、C4 12 个、C8 24 个、C16 48 个。「相对不开投机」为同并发下总吞吐之比。

| 投机方式 | 并发 | 总吞吐 tok/s | 单请求解码 tok/s(中位) | 首 token 延迟 s(中位) | 接受长度 | 接受率 | 相对不开投机 |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP(包内 BF16) | C1 | 104.7 | 124.5 | 0.15 | 2.685 | 0.562 | 1.48× |
| MTP(包内 BF16) | C4 | 323.2 | 103.9 | 0.18 | 2.597 | 0.531 | 2.04× |
| MTP(包内 BF16) | C8 | 355.5 | 86.6 | 0.17 | 2.683 | 0.561 | 1.12× |
| MTP(包内 BF16) | C16 | 912.4 | 73.0 | 0.18 | 2.923 | 0.641 | 1.86× |
| DFlash2 | C1 | 188.6 | 211.5 | 0.14 | 4.327 | 0.476 | 2.66× |
| DFlash2 | C4 | 456.1 | 182.1 | 0.16 | 4.011 | 0.430 | 2.88× |
| DFlash2 | C8 | 689.8 | 132.4 | 0.17 | 3.723 | 0.389 | 2.18× |
| DFlash2 | C16 | 1,143.2 | 121.1 | 0.28 | 3.985 | 0.427 | 2.33× |
| 不开投机 | C1 | 70.9 | 72.0 | 0.13 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C4 | 158.3 | 62.8 | 0.15 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C8 | 316.8 | 62.5 | 0.14 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C16 | 490.5 | 55.2 | 0.14 | 不适用 | 不适用 | 1.00× |

| 投机方式 | 单请求最快 | 推荐并发(单请求速度不低于 C1 的 60% 时总吞吐最高) | 总吞吐最高 |
|---|---|---|---|
| MTP | C1(124.5 tok/s) | C8(355.5 tok/s,单请求 86.6) | C16(912.4 tok/s) |
| DFlash2 | C1(211.5 tok/s) | C8(689.8 tok/s,单请求 132.4) | C16(1,143.2 tok/s) |
| 不开投机 | C1(72.0 tok/s) | C16(490.5 tok/s) | C16(490.5 tok/s) |

</details>

<details>
<summary>NVFP4 W4A4-W8A8 完整实测表</summary>

每档请求数:C1 4 个、C4 12 个、C8 24 个、C16 48 个。「相对不开投机」为同并发下总吞吐之比。

| 投机方式 | 并发 | 总吞吐 tok/s | 单请求解码 tok/s(中位) | 首 token 延迟 s(中位) | 接受长度 | 接受率 | 相对不开投机 |
|---|---|---:|---:|---:|---:|---:|---:|
| MTP(包内 BF16) | C1 | 99.9 | 116.3 | 0.17 | 2.865 | 0.621 | 1.61× |
| MTP(包内 BF16) | C4 | 213.0 | 99.8 | 0.19 | 2.667 | 0.555 | 1.09× |
| MTP(包内 BF16) | C8 | 417.2 | 83.2 | 0.18 | 2.647 | 0.549 | 1.33× |
| MTP(包内 BF16) | C16 | 580.2 | 69.4 | 0.19 | 2.772 | 0.591 | 1.24× |
| DFlash2 | C1 | 175.1 | 216.8 | 0.16 | 4.201 | 0.458 | 2.82× |
| DFlash2 | C4 | 395.0 | 152.4 | 0.19 | 3.995 | 0.427 | 2.02× |
| DFlash2 | C8 | 627.9 | 132.4 | 0.19 | 3.828 | 0.404 | 2.00× |
| DFlash2 | C16 | 1,146.4 | 105.5 | 0.30 | 4.364 | 0.479 | 2.44× |
| 不开投机 | C1 | 62.2 | 63.0 | 0.15 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C4 | 195.7 | 56.4 | 0.17 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C8 | 314.0 | 53.4 | 0.16 | 不适用 | 不适用 | 1.00× |
| 不开投机 | C16 | 469.4 | 47.7 | 0.16 | 不适用 | 不适用 | 1.00× |

| 投机方式 | 单请求最快 | 推荐并发(单请求速度不低于 C1 的 60% 时总吞吐最高) | 总吞吐最高 |
|---|---|---|---|
| MTP | C1(116.3 tok/s) | C8(417.2 tok/s,单请求 83.2) | C16(580.2 tok/s) |
| DFlash2 | C1(216.8 tok/s) | C8(627.9 tok/s,单请求 132.4) | C16(1,146.4 tok/s) |
| 不开投机 | C1(63.0 tok/s) | C16(469.4 tok/s) | C16(469.4 tok/s) |

</details>

### NInfer 两档

测试环境:单张 RTX PRO 6000 Blackwell;官方 NInfer,上下文参数与下文 NInfer 启动命令相同(`--max-context 102400 --kv-capacity 819200 --max-concurrency 8 --kv-dtype fp8`);生成上限 4,096,开思考(模板默认 xhigh),采样 temperature 1.0、top_p 0.95、top_k 20,提示词与上方 NVFP4 测速相同;C1 发 4 个请求、C4 发 12 个、C8 发 24 个。MTP 草稿长度 4、DFlash2 草稿长度 8,均开 `--lm-head-draft`。数字为合计解码 tok/s。NInfer 并发上限为 8,C16 未测。

| 投机方式 | 档位 | C1 | C4 | C8 |
|---|---|---:|---:|---:|
| 不开投机 | NInfer W4A4 | 68.1 | 195.8 | 306.8 |
| 不开投机 | NInfer W4A4-W8A8 | 68.1 | 236.1 | 369.5 |
| MTP(草稿长度 4) | NInfer W4A4 | 154.8 | 498.3 | 678.3 |
| MTP(草稿长度 4) | NInfer W4A4-W8A8 | 162.5 | 367.6 | 663.9 |
| DFlash2(草稿长度 8) | NInfer W4A4 | 207.1 | 539.6 | 975.9 |
| DFlash2(草稿长度 8) | NInfer W4A4-W8A8 | 199.1 | 650.1 | 804.9 |

- **最佳组合**:两档、三种模式的总吞吐都在 C8 最高。NInfer W4A4 最高为 DFlash2 · C8(975.9 tok/s),NInfer W4A4-W8A8 最高为 DFlash2 · C8(804.9 tok/s);只用 MTP 时 C8 分别为 678.3 与 663.9 tok/s。
- **与 NVFP4 W4A4(SGLang)的 C8 对比**:NInfer W4A4 不开投机 306.8 对 316.8,MTP 678.3 对 355.5,DFlash2 975.9 对 689.8 tok/s。两者引擎与上下文设置不同,仅作参考。

### INT8 W8A8

测试环境:单张 RTX PRO 6000 Blackwell;vLLM 0.28,`--max-model-len 102400`、`--max-num-seqs 8`;生成上限 512,开思考(xhigh),采样 temperature 1.0、top_p 0.95、top_k 20;每档只发与并发数相同的请求数(C1 发 1 个、C2 发 2 个、C4 发 4 个、C8 发 8 个)。这是快测:请求少、生成短,数字不能与上面各档直接比较。数字为总吞吐 tok/s(全部输出 token ÷ 墙钟时间)。两行都在另做的内置 MTP 对照版上测得(同一份 INT8 文本权重另加一层 BF16 MTP,未发布);不开投机时 MTP 层不参与计算。本包不含 MTP。

| 投机方式 | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| 不开投机 | 30.8 | 45.5 | 101.2 | **177.3** |
| MTP(对照,本包不含) | 23.9 | 37.8 | 72.5 | 145.9 |

- **推荐**:不开投机,C8(177.3 tok/s);并发越高总吞吐越高,C8 以上未测。
- **不要开 MTP**:模型只有 1 层 MTP,`num_speculative_tokens=3` 时同一层被反复调用,接受率低,C1–C8 每一档都比不开投机慢。本档也没有 DFlash2 草稿。

### GGUF Q6_K

测试环境:单张 RTX PRO 6000 Blackwell;1 分钟快测,生成上限 512,开思考(xhigh),采样 temperature 1.0、top_p 0.95、top_k 20;每档只发与并发数相同的请求数(C1 发 1 个、C2 发 2 个、C4 发 4 个、C8 发 8 个)。数字为总吞吐 tok/s(全部输出 token ÷ 墙钟时间)。这是快测:请求少、生成短,数字不能与上面 SGLang / NInfer 各档的完整测速直接比较。NInfer 行用 `GGUF-NInfer/` 包测得,测速时服务参数为 `--max-context 32768 --kv-capacity 32768 --kv-dtype rk8v4 --max-concurrency 8`;llama.cpp 行用 `GGUF/` 包测得。

| 引擎 · 投机方式 | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · MTP(草稿长度 3) | 131.9 | 161.9 | **235.5** | 388.1 |
| NInfer · 不开投机 | 56.0 | 93.9 | 162.1 | 298.1 |
| llama.cpp · MTP | 97.2 | 95.3 | 168.1 | 189.0 |
| llama.cpp · 不开投机 | 53.4 | 未测 | 123.0 | 未测 |

- **推荐**:NInfer + C4 + MTP(235.5 tok/s),与下文推荐启动命令(`--max-concurrency 4`)一致。只看总吞吐时 C8 更高(388.1 tok/s),需把 `--max-concurrency` 调到 8。
- **MTP 已内置**:两个包都自带 MTP 头(GGUF 为 Q8_0;NInfer 的 attention/MLP 权重为 Q6_K),不需要外挂草稿模型。单请求时 NInfer 开 MTP 为 131.9 tok/s,约为 llama.cpp 不开投机(53.4 tok/s)的 2.5 倍;llama.cpp 开 MTP 时 C1 总吞吐 97.2 tok/s(单请求解码 119.0 tok/s)。


### GGUF Q8_0

测试环境:单张 RTX PRO 6000 Blackwell。llama.cpp 行为快测口径(思考打开、融合 MTP):C1 发 4 个请求、C2 发 6 个、C4 发 12 个;数字为合计 decode tok/s。NInfer 行同口径测速(思考打开,模板默认 xhigh,生成上限 4096,temperature 1.0,top_p 0.95,top_k 20;C1 发 4、C4 发 12、C8 发 24;MTP draft-tokens 4)。

| 引擎 · 投机方式 | C1 | C2 | C4 | C8 |
|---|---:|---:|---:|---:|
| NInfer · MTP(草稿长度 4) | 109.5 | 未测 | 332.0 | **486.3** |
| llama.cpp · MTP | 85.3 | 133.6 | **190.8** | 未测 |

- **推荐**:NInfer + C8 + MTP(486.3 tok/s)。llama.cpp 最快为 C4 MTP(190.8 tok/s)。
- **MTP 已内置**:两个包都自带 MTP 头,不需要外挂草稿模型。


## 推荐启动脚本

### 量化方案

- **BF16**(`BF16/`):全部权重 BF16,原版多模态 config(保留 mrope,`mtp_num_hidden_layers=1`),无 `quantization_config`。
- **静态 FP8**(`FP8/`):官方式静态 FP8,权重 E4M3,128×128 分块,每块一个 scale(`weight_scale_inv`),激活为动态 FP8;config 只在顶层加了 FP8 `quantization_config`。
- **NVFP4 W4A16**(`NVFP4/W4A16/`):ModelOpt local-Hessian 校准;NVFP4 为 E2M1,16 个元素一块,每块一个 E4M3 尺度,另加张量级 FP32 二级尺度。MLP gate/up/down、全注意力 q/k/v/o、线性注意力 `in_proj_qkv` / `in_proj_z` / `out_proj` 共 400 个 Linear 为 NVFP4 权重、BF16 激活;线性注意力 `in_proj_a` / `in_proj_b` 与 `lm_head` 共 97 个保持 BF16。量化元数据为 ModelOpt `MIXED_PRECISION` 格式(400 层逐层标 `W4A16_NVFP4`),SGLang 自动识别为 `modelopt_mixed`。张量共 1,999 个:语言模型 1,651、视觉 333、MTP 15。
- **NVFP4 W4A4**(`NVFP4/W4A4/`):同一份校准数据和算法,同样 400 个 Linear,权重与激活都为 NVFP4(激活在推理时按 16 个元素一块量化);标准 `NVFP4` 导出,SGLang 自动识别为 `modelopt_fp4`。张量共 2,399 个:语言模型 2,051、视觉 333、MTP 15。
- **NVFP4 W4A4-W8A8**(`NVFP4/W4A4-W8A8/`):混合精度,同一份校准数据和算法。MLP gate/up/down 共 192 个 Linear 为 NVFP4 W4A4(权重与激活都为 NVFP4,激活在推理时按 16 个元素一块量化);全注意力 q/k/v/o 与线性注意力 `in_proj_qkv` / `in_proj_z` / `out_proj` 共 208 个 Linear 为 FP8 W8A8(E4M3 权重与激活,每张量静态 scale,激活 scale 由校准统计得到);线性注意力 `in_proj_a` / `in_proj_b` 与 `lm_head` 共 97 个保持 BF16。量化元数据为 ModelOpt `MIXED_PRECISION` 格式(逐层标 `NVFP4` 或 `FP8`),SGLang 自动识别为 `modelopt_mixed`。张量共 2,191 个:语言模型 1,843、视觉 333、MTP 15。
- **NVFP4 校准数据**:取自本模型自己的 RLOO 训练数据中答对且答案非空的完整轨迹(提示 + 思考 + 最终答案),512 条、约 173.5 万 token,单条最多 4,096 token;官方 GPQA、MMLU、LCB 的题目都不进校准。详见 `evaluation/NVFP4_CALIBRATION_METHOD.md`。三档的视觉塔(333 个张量)与 MTP(15 个张量)均为 BF16。
- 结构:`Qwen3_5ForConditionalGeneration`,64 层(线性注意力与全注意力 3:1 交替);FP8 包张量共 1,599 个:语言模型 1,251、视觉 333、MTP 15。

| 组件(静态 FP8 包) | 精度 |
|---|---|
| 线性注意力 `A_log`、`dt_bias`、`norm`、`conv1d`、`in_proj_a` / `in_proj_b`(×48) | BF16 |
| 线性注意力 `in_proj_qkv`、`in_proj_z`、`out_proj`(×48) | FP8 E4M3 Block128 |
| 全注意力 q/k/v/o、全部 MLP gate/up/down(与上一行合计 400 个 Linear) | FP8 E4M3 Block128 |
| `embed_tokens`、`lm_head` | BF16 |
| 视觉塔(333 个张量) | BF16,原样取自 RLOO 合并权重 |
| MTP(15 个张量) | BF16,原样取自官方 Qwen3.8-27B |

SSM 控制分支全部保留 BF16;排除清单与 Qwen 官方 FP8 一致,语言模型部分共 146 个模块保留 BF16。FP8 包冒烟均通过:SGLang 免补丁加载、贪心输出与测评用纯文本版逐字一致、SGLang 图像请求、SGLang MTP、vLLM 0.28 免补丁加载并开 MTP、vLLM 图像请求。

NVFP4 三档冒烟:SGLang 免补丁加载、贪心对拍、图像请求通过。MTP 与 DFlash2 的速度和接受长度以单独的性能测评为准(C1–C16 均已跑完,见上文)。

**GGUF Q8_0**(`GGUF/`、`GGUF-NInfer/`):主干 Q8_0,内置 MTP 头(`blk.64.nextn`),不需要外挂草稿;866 个张量;`.ninfer` 由同一份 GGUF 转换;两个包内不含视觉权重,要看图请用 llama.cpp 加 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(`--mmproj`);NInfer 不能单独加载 `vision-bf16.safetensors`,`.ninfer` 包只能跑文本。

**GGUF Q6_K**(`GGUF/`、`GGUF-NInfer/`):主干 Q6_K,用 512 个分块(chunk)的 imatrix 校准,并做结构保护:线性注意力(SSM)的 `ssm_alpha` / `ssm_beta` 保持 BF16,词嵌入与输出头为 Q8_0,MTP 头(`blk.64` 的 attn q/k/v/output、ffn gate/up/down 与 `nextn.eh_proj`)全部为 Q8_0,其 norm 保持 F32。GGUF 共 866 个张量、65 个块(64 层主干 + 1 层 MTP)。`.ninfer` 由同一份 GGUF 转换,主干量化相同,其 MTP 的 attention/MLP 权重为 Q6_K(`gguf_q6_k`),仅 `mtp/input_projection` 为 Q8_0;两个包内不含视觉权重,要看图请用 llama.cpp 加 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(`--mmproj`);NInfer 不能单独加载 `vision-bf16.safetensors`,`.ninfer` 包只能跑文本。

### 启动命令

需官方 SGLang ≥ 0.5.19;vLLM ≥ 0.28(仅 MTP)。vLLM 在张量并行 ≥ 2 时对 NVFP4 开 MTP 有已知问题(vLLM #52480),NVFP4 用 vLLM 开 MTP 时请用单卡。INT8 W8A8 只能用 vLLM 加载(在 0.28 上实测),命令见本节末尾。

**MTP 和 DFlash2 互斥,一次启动只能开其中一种。** 下面以 `./FP8` 为例,用 BF16 档时把 `--model-path` / `vllm serve` 的路径换成 `./BF16`,用 NVFP4 档时把 `--model-path` 换成 `./NVFP4/W4A16`、`./NVFP4/W4A4` 或 `./NVFP4/W4A4-W8A8`;DFlash2 草稿用各档目录下的 `DFlash2-FP8`(如 `./FP8/DFlash2-FP8`、`./BF16/DFlash2-FP8`、`./NVFP4/W4A16/DFlash2-FP8`)。NVFP4 三档的量化格式由 SGLang 自动识别,不需要加 `--quantization`;vLLM 只在 FP8 包上验证过,NVFP4 只在 SGLang 上测过。并发与上下文参数与性能测试一致,可按需调整。

**SGLang · MTP(包内 BF16)**

```bash
python -m sglang.launch_server \
  --model-path ./FP8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm EAGLE \
  --speculative-num-steps 3 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 4
```

**vLLM · MTP(FP8 包冒烟实测通过)**

```bash
vllm serve ./FP8 \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

**SGLang · DFlash2**

```bash
python -m sglang.launch_server \
  --model-path ./FP8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./FP8/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

**SGLang · NVFP4 W4A16 · DFlash2**(W4A4 把两处 `W4A16` 换成 `W4A4`;NVFP4 开 MTP 时用上面的 MTP 命令,只换 `--model-path`)

```bash
python -m sglang.launch_server \
  --model-path ./NVFP4/W4A16 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./NVFP4/W4A16/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

**SGLang · NVFP4 W4A4-W8A8 · DFlash2**(开 MTP 时用上面的 MTP 命令,只换 `--model-path`)

```bash
python -m sglang.launch_server \
  --model-path ./NVFP4/W4A4-W8A8 \
  --context-length 32768 \
  --max-running-requests 16 \
  --mamba-ssm-dtype bfloat16 \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path ./NVFP4/W4A4-W8A8/DFlash2-FP8 \
  --speculative-draft-model-quantization fp8 \
  --speculative-num-draft-tokens 8
```

本卡的三项测评分数是开 DFlash2 测出的;投机解码不改变目标模型的输出分布。采样默认值见 `generation_config.json`(temperature 1.0、top_p 0.95、top_k 20)。

以 W4A4 档为例;用 W4A4-W8A8 档时把路径换成 `./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer`,`--model-id` 换成 `qwen3.8-27b-coder390-w4a4-w8a8`。

MTP-DFlash2 包内已包含 Q8 MTP 和 DFlash2 草稿，NInfer 不需要外挂草稿模型（这一点与上面 SGLang 需要传 DFlash2 草稿路径不同）；启动时用 `--spec mtp` 或 `--spec dflash2` 二选一，不加 `--spec` 即不开投机。

**图片输入**：这里的 `.ninfer` 包都不能输入图片。NInfer 用 `--vision` 开启图片，但前提是视觉塔在 `.ninfer` 包内；这些包里没有，`ninfer-serve` 也没有单独加载 `vision-bf16.safetensors` 的参数。不要加 `--vision`，加了服务起不来。要看图请用上面 SGLang 的 BF16 / FP8 / NVFP4 档。

**NInfer · 不开投机**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8
```

**NInfer · MTP(草稿长度 4)**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec mtp --draft-tokens 4 --lm-head-draft
```

**NInfer · DFlash2(草稿长度 8)**

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8 \
  --spec dflash2 --draft-tokens 8 --lm-head-draft
```

**NInfer · 纯文本包(不含 MTP)**

`Qwen3.8-27B-Coder390-EfficientThink-W4A4.ninfer` 与 `Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8.ninfer` 只含文本路径,不含 MTP、视觉塔与 DFlash2 草稿,只能不开投机启动,不要加 `--spec`、`--draft-tokens`、`--lm-head-draft`。这两个包未单独测评,只做了 SHA256 校验。用 W4A4-W8A8 时把路径换成 `./NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8.ninfer`,`--model-id` 换成 `qwen3.8-27b-coder390-w4a4-w8a8`。

```bash
ninfer-serve ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4.ninfer \
  --host 127.0.0.1 --port 19931 --device 0 \
  --model-id qwen3.8-27b-coder390-w4a4 \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype fp8
```

健康检查:`curl -sf http://127.0.0.1:19931/health`。对话接口为 `POST /v1/chat/completions`,请求里的 `model` 要与 `--model-id` 一致。

**vLLM · INT8 W8A8(不开投机)**

```bash
VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel \
VLLM_USE_FLASHINFER_SAMPLER=0 \
vllm serve ./INT8/W8A8 \
  --trust-remote-code --dtype bfloat16 \
  --max-model-len 102400 --served-model-name int8 \
  --gpu-memory-utilization 0.85 --max-num-seqs 8 \
  --reasoning-parser qwen3
```

RTX PRO 6000 Blackwell 上 vLLM 的 Cutlass INT8 内核不可用,不关掉就起不来,须用 `VLLM_DISABLED_KERNELS=CutlassInt8ScaledMMLinearKernel` 关掉;关掉后改走 Triton INT8 内核(启动日志里能看到 `TritonInt8ScaledMMLinearKernel`)。`VLLM_USE_FLASHINFER_SAMPLER=0` 与测试时一致。在 vLLM 0.28 上实测;SGLang 不能加载本包(`ModelOptFp8Config` 报错)。`--reasoning-parser qwen3` 会把思考内容单独放进 `reasoning_content`(测分时未开)。

**GGUF / GGUF-NInfer**

`.ninfer` 用 NInfer-all(`iamwavecut/ninfer-all` 的 master 分支)加载:包里保留的是 GGUF 量化块,其他 NInfer 构建不能读。llama.cpp 需支持 `--spec-type draft-mtp` 的上游版本。NInfer 的 `--kv-capacity` 是所有请求共享的 KV 池;llama.cpp 的 `-c 409600 -np 4` 会把上下文平分给 4 个槽位,每个请求最多 102,400 token,够单请求写到 94K。对话接口为 `POST /v1/chat/completions`;NInfer 请求里的 `model` 要与 `--model-id` 一致。视觉:llama.cpp 用 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(`--mmproj`;629,247,008 字节,sha256 `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32`)。`.ninfer` 包内没有视觉塔,NInfer 也不能单独加载 `GGUF-NInfer/vision-bf16.safetensors`,所以在 NInfer 下只能跑文本;不要加 `--vision`(加了服务起不来)。要看图请用 llama.cpp 加载 `GGUF/` 并加 `--mmproj`。

**MTP 与 DFlash2**:`GGUF/` 与 `GGUF-NInfer/` 下所有包都内置 MTP 头(Q2 / Q3 / Q4 LynnStyle 为内置 **Q4** MTP)。开启方式:NInfer 加 `--spec mtp --draft-tokens N`,llama.cpp 加 `--spec-type draft-mtp --spec-draft-n-max N`;省略这两个参数即不开投机。DFlash2 是外挂草稿模型,不在这些 GGUF / NInfer 包里,本仓库不提供 GGUF / GGUF-NInfer 用的 DFlash2 草稿;需要 DFlash2 时请用本仓库 BF16 / FP8 / NVFP4 各档自带的 `DFlash2-FP8/`(SGLang `--speculative-algorithm DFLASH`)或 `NVFP4-NInfer/` 的 `.ninfer` 包(`--spec dflash2`)。MTP 与 DFlash2 互斥:同一个服务只能开其中一种,不要同时开。

#### GGUF · NInfer

**NInfer · GGUF Q2 LynnStyle · MTP(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --kv-dtype rk8v4 \
  --max-concurrency 8 --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q3 LynnStyle · MTP(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q3LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q4 LynnStyle · MTP(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.ninfer \
  --host 127.0.0.1 --port 8080 --device 0 \
  --model-id qwen3.8-27b-coder390-Q4LynnStyle-Mtp \
  --max-context 102400 --kv-capacity 819200 --max-concurrency 8 \
  --kv-dtype rk8v4 \
  --spec mtp --draft-tokens 4
```

**NInfer · GGUF Q6_K · MTP(草稿长度 3,推荐并发 4)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-q6k-mtp \
  --max-context 102400 --kv-capacity 409600 --kv-dtype rk8v4 \
  --max-concurrency 4 --spec mtp --draft-tokens 3
```

**NInfer · GGUF Q8_0 · MTP(草稿长度 4,推荐并发 8)**

```bash
ninfer-serve ./GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer \
  --model-id qwen3.8-27b-coder390-q8-mtp \
  --max-context 102400 --kv-capacity 819200 --kv-dtype rk8v4 \
  --max-concurrency 8 --spec mtp --draft-tokens 4
```

不要用 `--max-context 131072 --kv-capacity 131072`(KV 池不够多请求排队时会 HTTP 503)。不要加 `--lm-head-q6` / `--embedding-q4`。需 NInfer-all 的 `ninfer-serve`;官方 ninfer-src 读不了 `gguf_blocks_v1`。

#### GGUF · llama.cpp

**llama.cpp · GGUF Q2 LynnStyle · MTP(代表命令;换 `-m` 即可切到 Q3 / Q4 / Q6_K / Q8_0)**

```bash
llama-server -m ./GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf \
  -c 409600 -np 4 -ngl 99 --jinja \
  --host 127.0.0.1 --port 8080 \
  --alias qwen3.8-27b-coder390-Q2LynnStyle-Mtp \
  --spec-type draft-mtp --spec-draft-n-max 4
```

换其他 GGUF 档只需改 `-m` 为 `...-Q3LynnStyle-MTP.gguf`、`...-Q4LynnStyle-MTP.gguf`、`...-Q6_K-MTP.gguf` 或 `...-Q8_0-MTP.gguf`(并相应改 `--alias`,例如 `qwen3.8-27b-coder390-q6k-mtp`、`qwen3.8-27b-coder390-q8-mtp`)。MTP 已融合进 GGUF(`blk.64`),不要再外挂 draft;日志应出现 `creating MTP draft context against the target model`。需要图像输入时加 `--mmproj ./GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`。

## 其他文件纵览

### `FP8/`(主包 19 个文件,31,262,188,871 字节)

`FP8/SHA256SUMS` 覆盖下表前 18 个文件。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `FP8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `FP8/config.json` | 17,784 | `9e58e8daf2914c2d11c07449dc7f03bbb822ba39dec37c4c5b3bd1f623492f90` |
| `FP8/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `FP8/model.safetensors.index.json` | 135,976 | `989573833195e17342983c7fd109e010155c423a355068b5aceb6631fcee83f2` |
| `FP8/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `FP8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `FP8/text-01.safetensors` | 2,542,796,928 | `54d83c1d36631de231876217a8e0c2483eccee8746369a482b79442bdfc5d958` |
| `FP8/text-02.safetensors` | 3,998,718,144 | `5b1e34725cd88924495765149ff816903d702180c72561c2e22e8377e2044fa8` |
| `FP8/text-03.safetensors` | 3,969,173,888 | `5e2376d6cce25aecf2d8901959f9d6f98801a0b2e98331f4088481bf839c9cf3` |
| `FP8/text-04.safetensors` | 3,925,079,000 | `669b87fd69d2de004073ed633f8e2890c8c9c90e1101bd59c859f1431b5cb967` |
| `FP8/text-05.safetensors` | 3,994,338,456 | `3f150179f9e3f03e2ef2e1afc805e7d745c1ab88dd72776fadf7c33f1d73ae67` |
| `FP8/text-06.safetensors` | 3,920,901,280 | `4d658974b7efb906972bc66cb4fd6dc7f1b7ac1fa79a7db068442314e3bf75d4` |
| `FP8/text-07.safetensors` | 3,972,285,640 | `d155ad91985b57e2515cea321a474708dd162665d1f5870df1c85601a2ca9b2c` |
| `FP8/text-08.safetensors` | 3,147,842,216 | `e37d025cd9bcacdd00fa0969f5c827d2504019c020585dfe1aca3934152b7700` |
| `FP8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `FP8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `FP8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `FP8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `FP8/SHA256SUMS` | 1,570 | (校验清单本身) |

### `FP8/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `FP8/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `FP8/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `FP8/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `FP8/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `BF16/`(12 个文件,55,583,125,732 字节;DFlash2 子目录另列在下面)

`BF16/SHA256SUMS` 覆盖下表前 11 个文件。`mtp-bf16.safetensors` 与 FP8 包中的同名文件逐字节相同。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `BF16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `BF16/config.json` | 3,799 | `b25e4020b4f791f2b20a3bf486f7ded5116fa0680cf7aa2ac50f80ee353663ce` |
| `BF16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `BF16/model-00001-of-00002.safetensors` | 49,825,162,976 | `ed83b8a41d447f4592c490b6135917419aea00fc7dbf9d6f5eb9525631f86fe0` |
| `BF16/model-00002-of-00002.safetensors` | 4,888,445,168 | `5c56330027c0eb9a776e89f80ef1643e60b1c2ae3adbbaf4b5142ebf7cb57271` |
| `BF16/model.safetensors.index.json` | 112,034 | `e8e177ff98a940337d496a0820e51c9fb68b2ab98fb68647d26aef9368dedeab` |
| `BF16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `BF16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `BF16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `BF16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `BF16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `BF16/SHA256SUMS` | 990 | (校验清单本身) |

### `BF16/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

与 `FP8/DFlash2-FP8/` 逐字节相同。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `BF16/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `BF16/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `BF16/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `BF16/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A16/`(主包 17 个文件,20,613,406,953 字节;DFlash2 子目录另列在下面)

`NVFP4/W4A16/SHA256SUMS` 覆盖下表前 16 个文件,其自身 SHA256 为 `ecc28d31be0d97e23509af61625251af14980db5b67189a1d1ca75a3fc9652f3`。`mtp-bf16.safetensors` 与 FP8 包中的同名文件逐字节相同。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4/W4A16/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A16/config.json` | 69,785 | `e71fd7b2cbade1ebb8be0382c81f7bf69eb1e039e30734914378d2c41217ef62` |
| `NVFP4/W4A16/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A16/hf_quant_config.json` | 65,978 | `2ff46ad6bc27eb740e29831e642522ee4c110fea1ae9520b89272566b0d12d62` |
| `NVFP4/W4A16/model.safetensors.index.json` | 171,578 | `13651163cd9c1c20af460e6595616075a1f0d7f5995a3efc46d3ac449bc4f51e` |
| `NVFP4/W4A16/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A16/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A16/text-01.safetensors` | 3,994,732,420 | `dfdd15ab6b889eee01357d38910552bb0968248df0e21a9564d7ae29482d3139` |
| `NVFP4/W4A16/text-02.safetensors` | 3,981,611,096 | `8e4a2a7b4c9325c27380a41de0fb51028065ff97090af9d4213cb5a50629d517` |
| `NVFP4/W4A16/text-03.safetensors` | 3,960,207,028 | `c92929b575321e080d0ea2ca7c1a26b49fa638a8d03bacfef2cd0b6f83237689` |
| `NVFP4/W4A16/text-04.safetensors` | 3,983,003,152 | `feb69e1a4c7a374f1a11cf3e4af5d70fdd870963519e71469eb067a86fb35634` |
| `NVFP4/W4A16/text-05.safetensors` | 2,902,646,528 | `28dda5f9a39b83736ae458c2e626b429bbd18e408be63ef598dbb47327c97e3e` |
| `NVFP4/W4A16/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A16/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A16/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A16/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A16/SHA256SUMS` | 1,399 | `ecc28d31be0d97e23509af61625251af14980db5b67189a1d1ca75a3fc9652f3` |

### `NVFP4/W4A16/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

与 `FP8/DFlash2-FP8/` 逐字节相同。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `NVFP4/W4A16/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A16/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A16/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A16/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A4/`(主包 17 个文件,20,613,386,462 字节;DFlash2 子目录另列在下面)

`NVFP4/W4A4/SHA256SUMS` 覆盖下表前 16 个文件,其自身 SHA256 为 `5aea8bb9c1f1979661bfa5c1216de7aafeb64cd708aa8cc71f3b185c224cfde0`。`mtp-bf16.safetensors` 与 FP8 包中的同名文件逐字节相同。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4/W4A4/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A4/config.json` | 18,130 | `4df9be90e61070a553447129e504fea7be8e60dc22ae9e9f7a85bdfc140c0054` |
| `NVFP4/W4A4/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A4/hf_quant_config.json` | 13,956 | `d3603810fba7548903ba2f3382fdd30f5704d3b6e0688e2dccf34fe023c11d31` |
| `NVFP4/W4A4/model.safetensors.index.json` | 207,580 | `541d828aed73b4df9f9fc86be7111aa404983d55d9797ca1cfb3e71474bfd3b7` |
| `NVFP4/W4A4/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A4/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A4/text-01.safetensors` | 3,994,737,240 | `1ea4cf8a0036b5d87815b65a38d0d2c00b37c010056a03d0db1fc72eb6c829bc` |
| `NVFP4/W4A4/text-02.safetensors` | 3,981,625,016 | `c9a0d2c3c506ad17da4dd47bf571326eef201e40db6f259a9d42971778033359` |
| `NVFP4/W4A4/text-03.safetensors` | 3,960,220,600 | `3c8778873d2ef08c512b7e457d61a6ac9ea047975e4723cd3804d0d18e86c1db` |
| `NVFP4/W4A4/text-04.safetensors` | 3,983,016,880 | `40081557adf0713f1624cdb2d1c53ea5fd2a30e09f5f964799457b23e4e2304d` |
| `NVFP4/W4A4/text-05.safetensors` | 2,902,647,672 | `0266ba0fa0354a4c409bc180c9d9a67ed12c915fc9886970745c87f8babcaa24` |
| `NVFP4/W4A4/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A4/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A4/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A4/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A4/SHA256SUMS` | 1,399 | `5aea8bb9c1f1979661bfa5c1216de7aafeb64cd708aa8cc71f3b185c224cfde0` |

### `NVFP4/W4A4/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

与 `FP8/DFlash2-FP8/` 逐字节相同。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `NVFP4/W4A4/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A4/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A4/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A4/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `NVFP4/W4A4-W8A8/`(主包 18 个文件,23,769,634,648 字节;DFlash2 子目录另列在下面)

`NVFP4/W4A4-W8A8/SHA256SUMS` 覆盖下表前 17 个文件,其自身 SHA256 为 `c177f4907a7dd037efe91b8d34927dd3a3624227f259238b82db0f12f8b0b8e2`。`mtp-bf16.safetensors` 与 FP8 包中的同名文件逐字节相同。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4/W4A4-W8A8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `NVFP4/W4A4-W8A8/config.json` | 71,802 | `d1cc2af6971ae0bb776f5f36eb1c923546742fda3a83e6d8355720a652e27b5d` |
| `NVFP4/W4A4-W8A8/generation_config.json` | 214 | `df6f86c3fdce573ecdb55cec35f502ddda70e70abe78288a78164aef120232e7` |
| `NVFP4/W4A4-W8A8/hf_quant_config.json` | 43,976 | `2bd65f6f325ea8e8e40c37b6e7d386633ac6236db6fcde3d7e9de128d961a599` |
| `NVFP4/W4A4-W8A8/model.safetensors.index.json` | 187,500 | `1257454a255efb01ba8047fe41bf34460b551c210db7cc8c4713f1c01150c69d` |
| `NVFP4/W4A4-W8A8/mtp-bf16.safetensors` | 849,400,424 | `90fa0e3eed5a647c035c6df9ecabc416c0f8d573ff84ac12485b085f00a7cdf2` |
| `NVFP4/W4A4-W8A8/preprocessor_config.json` | 390 | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `NVFP4/W4A4-W8A8/text-01.safetensors` | 3,981,847,464 | `b5502eb2c54c5a53ee08712c48935023ed924e0f054acb3573e1288095d2e3ff` |
| `NVFP4/W4A4-W8A8/text-02.safetensors` | 3,956,368,808 | `f08e7fccb4d2467af8b2b2d3bc587e6e8404b5764e9fc8e640ad0ff4f445d293` |
| `NVFP4/W4A4-W8A8/text-03.safetensors` | 3,956,368,928 | `8299287bb0e570efda02bcbe67c4bd9c5378b44bbf84c17ff062fc5ce6ba53e0` |
| `NVFP4/W4A4-W8A8/text-04.safetensors` | 3,967,919,248 | `bea560dda7b885cca987b8352e2ae659acaee70c3255fde7fa487c1fd73badf2` |
| `NVFP4/W4A4-W8A8/text-05.safetensors` | 3,573,130,520 | `a969faa5f2a3963450ad64bb84664035676c426877499593aea91080643ba6fa` |
| `NVFP4/W4A4-W8A8/text-06.safetensors` | 2,542,796,928 | `54d83c1d36631de231876217a8e0c2483eccee8746369a482b79442bdfc5d958` |
| `NVFP4/W4A4-W8A8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `NVFP4/W4A4-W8A8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `NVFP4/W4A4-W8A8/video_preprocessor_config.json` | 385 | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `NVFP4/W4A4-W8A8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4/W4A4-W8A8/SHA256SUMS` | 1,485 | `c177f4907a7dd037efe91b8d34927dd3a3624227f259238b82db0f12f8b0b8e2` |

### `NVFP4/W4A4-W8A8/DFlash2-FP8/`(4 个文件,2,407,384,680 字节)

与 `FP8/DFlash2-FP8/` 逐字节相同。

| 文件 | 字节数 | SHA256 |
|---|---:|---|
| `NVFP4/W4A4-W8A8/DFlash2-FP8/model.safetensors` | 2,407,379,992 | `a7b48bc293a989494ce2db64ac01a0261c370499641b0f5a668d8005c8cbfb93` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/config.json` | 2,642 | `6c41f9b7b068b6c3cfaafe2d8af6e86cf82917a187590a78966ea6249069b2f7` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/manifest.json` | 1,804 | `7f674162e4670c862596f4bb46ddd9f7d3524a7b0dacd7c86c397a8a66a29b45` |
| `NVFP4/W4A4-W8A8/DFlash2-FP8/SHA256SUMS` | 242 | `0186950b8563dda734f5d8998e1488812b3a089d62672acde272d6e9bf9c56d8` |

### `evaluation/`

成绩、性能、冒烟(静态 FP8 与 BF16)与校准记录。`evaluation/SHA256SUMS` 覆盖下表前 22 个文件(表中共 23 行,最后一行为校验清单本身)。`NVFP4_*.results.summary.json` 为 NVFP4 三档三项测评的原始汇总(`NVFP4_MIXED_*` 为 W4A4-W8A8 档)。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `evaluation/SCORES_STATICFP8.json` | 3,935 | `eba280071a75fc8dd90e5866df783a68ccd08bdb4d4dde85c062f7d398ea0eb0` |
| `evaluation/BENCH_STATICFP8.json` | 6,511 | `c62c6c82f234a27fa93faf691d1d4ee01a2408a18bbe94efafe341e4ad10db20` |
| `evaluation/BENCH_STATICFP8.md` | 1,405 | `ea662952b73446d5b88422b2a3dbcc215829521cc001cb26ad492caa137fa2ac` |
| `evaluation/SMOKE_STATICFP8.json` | 2,119 | `1a2383ad0f8e26f02ec7d65db418fea2bd50e73458ee247cc9d2f9322ffbb833` |
| `evaluation/SCORES_BF16.json` | 4,279 | `76e921712bab0577853499d3f67440de6f3577f4818c40184f4b0580e5f7a77e` |
| `evaluation/SMOKE_BF16.json` | 889 | `01ea5e4518615af2a3c574fa49ae6f2a4819482bbaafce2695b62016b14a582f` |
| `evaluation/SCORES_NVFP4_W4A16.json` | 3,319 | `7294901f3493f593e0de6d7f95b860c44578780300aebcb52bca6f06ead1ddfd` |
| `evaluation/BENCH_NVFP4_W4A16.json` | 3,992 | `1877fe3e4126de72ad1165a1e0f5d1dd569f73f1dcd16a93249c389b3d47f2d3` |
| `evaluation/SCORES_NVFP4_W4A4.json` | 3,212 | `eee169bb6cde4d048d12d604a72c7570b0ebd0fee88a3c19d39ad4493a912f30` |
| `evaluation/BENCH_NVFP4_W4A4.json` | 3,922 | `2ebedf7e221f69765364a73deaca459a9636a4c190b2cbde06de8d119a15f4a7` |
| `evaluation/SCORES_NVFP4_MIXED.json` | 3,063 | `845027e6324b5300ed5ce306b3515b559f75b5c0e8ef1aac4d1b98d62d135454` |
| `evaluation/BENCH_NVFP4_MIXED.json` | 4,038 | `3d6f348425b6fd184d620c101a803139d7bcc0d620ff3237c28cc627e8f85ca7` |
| `evaluation/NVFP4_CALIBRATION_METHOD.md` | 3,712 | `e3678dbe9020a83998a5c66207b515376defebd78e6fadf4f63e55059785e03a` |
| `evaluation/NVFP4_W4A16_gpqa.results.summary.json` | 1,182 | `4835f8cf4b403047487b0a52db88574a2125ba103a30404b8b9e97e7112511bd` |
| `evaluation/NVFP4_W4A16_lcb.results.summary.json` | 2,642 | `56990657d101c2ce47b44d5fcdcb498a286bbf6093ae7790cde5809ba266d5a1` |
| `evaluation/NVFP4_W4A16_mmlu.results.summary.json` | 4,075 | `e9d507b5da71621032a13f487eb60159e0369c025ed12c4fa613e70b6f0f71e5` |
| `evaluation/NVFP4_W4A4_gpqa.results.summary.json` | 1,189 | `961b3f98b4a54d78d1983896a0b12b10a3d1e7facf456f594793dc7bbefb5e70` |
| `evaluation/NVFP4_W4A4_lcb.results.summary.json` | 2,640 | `bd371e898121ee5dd6fda47065254cc2137ba783b466b3830f0c58d631137688` |
| `evaluation/NVFP4_W4A4_mmlu.results.summary.json` | 4,076 | `b468cf81854562e0e20bf232ddd13b68ed58e10a4da840e6bd3c20564d20f74a` |
| `evaluation/NVFP4_MIXED_gpqa.results.summary.json` | 1,171 | `72c000ffc4ff15db8d542b6d9d924c5795ad491d946dee0f6c3f11b0e62151f1` |
| `evaluation/NVFP4_MIXED_lcb.results.summary.json` | 2,641 | `7e3d3146dd98954ef80358ce88f5505798f77427c1a5ddf73c65dd728cf3afc2` |
| `evaluation/NVFP4_MIXED_mmlu.results.summary.json` | 4,077 | `3088c6254dad8af25ace3b44f4cfa688b192eca98f693afa1c595df121cb9afb` |
| `evaluation/SHA256SUMS` | 2,071 | (校验清单本身) |

### 校验

```bash
(cd FP8 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd BF16 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A16 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A4 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4/W4A4-W8A8 && sha256sum -c SHA256SUMS && cd DFlash2-FP8 && sha256sum -c SHA256SUMS)
(cd NVFP4-NInfer/W4A4 && sha256sum -c SHA256SUMS)
(cd NVFP4-NInfer/W4A4-W8A8 && sha256sum -c SHA256SUMS)
(cd INT8/W8A8 && sha256sum -c SHA256SUMS)
(cd GGUF && sha256sum -c SHA256SUMS)
(cd GGUF-NInfer && sha256sum -c SHA256SUMS)
(cd evaluation && sha256sum -c SHA256SUMS)
```

## NInfer 加载说明

- 只有 NInfer 引擎能加载 `.ninfer`;SGLang、vLLM、llama.cpp、transformers 都不能读。
- 使用官方 NInfer([`iamwavecut/ninfer-all`](https://github.com/iamwavecut/ninfer-all))的 `ninfer-serve`,无需打补丁。实测硬件为单张 RTX PRO 6000 Blackwell(算力 12.0);NInfer 并发上限为 8。
- `NVFP4-NInfer/W4A4/` 与 `NVFP4-NInfer/W4A4-W8A8/` 各有一个带 MTP 与 DFlash2 的 `.ninfer` 文件:文本路径与 2026-10-05 测分时相同,包内另含 Q8 MTP、DFlash2 草稿与 proposal head;视觉塔不在包内,不能输入图片;同一文件夹的 `vision-bf16.safetensors` NInfer 不能单独加载。MTP 投影为 Q8:其中几个矩阵形状在 NInfer 里没有 BF16 内核,用 BF16 会在建计算图时退出。
- 两个目录另各有一个纯文本包(`Qwen3.8-27B-Coder390-EfficientThink-W4A4.ninfer`、`Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8.ninfer`,各 20,752,974,596 字节):只含文本路径,不含 MTP、视觉塔与 DFlash2 草稿,只能不开投机启动;未单独测评,只做了 SHA256 校验。
- MTP 与 DFlash2 一次启动只能选一种(`--spec mtp` 或 `--spec dflash2`);`--lm-head-draft` 须与 `--spec` 一起用。MTP 草稿长度可取 1–5,DFlash2 可取 1–15;上文「启动命令」中的 NInfer 命令用测速时的 4 与 8。DFlash2 草稿已打在包里,不需要另载 `DFlash2-FP8/` 目录。
- 下面的上下文参数已验证能启动:`--max-context 102400 --kv-capacity 819200 --max-concurrency 8 --kv-dtype fp8`。`--kv-capacity` 须落在 `max-context` 到 `max-context × max-concurrency` 之间,819,200 正好是 8 × 102,400。
- NVFP4 目录下的 HF 包仍用 SGLang(可开 MTP 或 DFlash2);与 NInfer 包互不通用。

### NInfer V2 包(仅 Tesla V100)

文件名带 `NInferV2-NOT-FOR-V3` 的四个包只给 Tesla V100 用（ninfer-v100 分支）；其他显卡请用不带这个后缀的包。

- 文件名含 `NInferV2-NOT-FOR-V3` 的 4 个包是 NInfer **V2** 容器,只给 Tesla V100 的 `ninfer-v100` 分支用。官方 NInfer 与 `ninfer-serve` 只读 V3,会拒绝这些文件;官方 NInfer 请用上面不带 `NInferV2` 的 V3 包。不要把 V2 包改名成 V3 文件名,也不要用它们替换 V3 包。
- 两个纯文本包(`Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer`、`Qwen3.8-27B-Coder390-W4A4-W8A8-NInferV2-NOT-FOR-V3.ninfer`)不含 MTP 与 DFlash2,不要加 `--spec`;两个 MTP-DFlash2 包(`…-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer`)可加 `--spec mtp` 或 `--spec dflash2`,包内已包含 MTP 和 DFlash2 草稿,不需要外挂草稿模型。四个 V2 包都不含视觉塔。
- V100 上没有 NVFP4 KV 与 K8V4 KV,不要用 V3 的 `--kv-dtype rk8v4` 或 `--kv-capacity 819200`;在 V100 上起服务时加 `--prefill-chunk 2048`。
- V2 包未单独测评,只做了 SHA256 校验。`SHA256SUMS` 里 V2 的两行放在 `#` 注释行之后,与 V3 分开。

```bash
# V100 ninfer-v100 分支 · 纯文本包(不加 --spec)
ninfer ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer \
  --prompt "用三句话说明 prefill 和 decode。" \
  --max-context 8192 \
  --max-new 256

# V100 ninfer-v100 分支 · MTP-DFlash2 包(开 MTP)
ninfer ./NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer \
  --prompt "用三句话说明 prefill 和 decode。" \
  --max-context 8192 \
  --max-new 256 \
  --spec mtp --draft-tokens 3
```

### `NVFP4-NInfer/W4A4/`(6 个文件,89,382,856,537 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4-MTP-DFlash2.ninfer` | 23,477,856,260 | `212972ef9f7f86765f7963bdadcab133c42cb0308feb33a55e820513d8a6bcfc` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-EfficientThink-W4A4.ninfer` | 20,752,974,596 | `6020ee54dcc2bd809c0f3127e9146e27d786813933970691ce21078d2a111a89` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-NInferV2-NOT-FOR-V3.ninfer` | 20,752,831,236 | `eac9e3d47fe6731c021d7154fd2f801a8263ac6d00e6d16834e54947ee58bcf8` |
| `NVFP4-NInfer/W4A4/Qwen3.8-27B-Coder390-W4A4-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer` | 23,477,696,516 | `e93f3b83f7589fdb776ce25a0cdef98ed1892e101ef564fdb844a5aacff13d22` |
| `NVFP4-NInfer/W4A4/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4-NInfer/W4A4/SHA256SUMS` | 705 | `7fcdf5c55c74fd34a31968f5a36da1fde31db577d5bec4ebe7ed9311ca0890d9` |

### `NVFP4-NInfer/W4A4-W8A8/`(6 个文件,89,382,856,557 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8-MTP-DFlash2.ninfer` | 23,477,856,260 | `799dd5921a69b6c0e0f4bced88ebf9db7a744f50f4b8c2c63e26656b0983f279` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-EfficientThink-W4A4-W8A8.ninfer` | 20,752,974,596 | `f4aa505aaadf358d30df061dc7cc8151bbded858cd38c02e4f4b1ae83e171047` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-W4A4-W8A8-NInferV2-NOT-FOR-V3.ninfer` | 20,752,831,236 | `01a4440f77dcdac66906e1bb061e1c38c6b236b805ff7bcb644aedf90f06a038` |
| `NVFP4-NInfer/W4A4-W8A8/Qwen3.8-27B-Coder390-W4A4-W8A8-MTP-DFlash2-NInferV2-NOT-FOR-V3.ninfer` | 23,477,696,516 | `099b2d00fa3982d601218d6587dc25222cc21ef708de7dab8b2e2c0bee60da74` |
| `NVFP4-NInfer/W4A4-W8A8/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `NVFP4-NInfer/W4A4-W8A8/SHA256SUMS` | 725 | `59c714ff4b2b9e37d1091f45ec12d9ac45d20a002336f24ae0d43d2b75738d11` |

## INT8 W8A8 说明

- 只有文本路径:架构为 `Qwen3_5ForCausalLM`,64 层(线性注意力与全注意力 3:1 交替),不含视觉塔、MTP 与 DFlash2 草稿,只能处理文本请求。
- 量化:SmoothQuant + INT8 W8A8。权重按输出通道量化为 INT8,激活在推理时按 token 动态量化为 INT8;SmoothQuant 的预缩放已折进权重,推理框架不需要补丁。量化元数据为 compressed-tensors(`int-quantized`)格式。
- 层分布:MLP gate/up/down、全注意力 q/k/v/o、线性注意力 `in_proj_qkv` / `in_proj_z` / `out_proj` 共 400 个 Linear 为 INT8;线性注意力 `in_proj_a` / `in_proj_b` 与 `lm_head` 共 97 个保持 BF16;线性注意力的 `A_log`、`dt_bias`、`norm`、`conv1d` 等控制分支也保持 BF16。
- 校准与误差:512 条校准样本;留出集 NLL 由 BF16 的 0.50535 升到 0.52812,困惑度之比 1.023(在把预缩放折进权重之前测得)。
- 加载:只在 vLLM 0.28 上验证,不适用于 SGLang 与 NInfer;`VLLM_LOAD.json` 记录了本包的加载条件。RTX PRO 6000 Blackwell 上须关掉 Cutlass INT8 内核,见上文「启动命令」。

### `INT8/W8A8/`(16 个文件,29,500,937,028 字节)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `INT8/W8A8/VLLM_LOAD.json` | 329 | `b1101c2ef1d53e76f132686a15079068fc76ad2ae139514817e088c6223adf7b` |
| `INT8/W8A8/chat_template.jinja` | 8,952 | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| `INT8/W8A8/config.json` | 19,123 | `b3db670871591bcfbedc05743a4cdc8a41c20cbc1af570e653716d7904ec92c7` |
| `INT8/W8A8/generation_config.json` | 214 | `a4cef85934ea1fdcb207944dbc6eee70dbbf16806874428556ae33023336c0a4` |
| `INT8/W8A8/model-00001-of-00008.safetensors` | 3,978,325,744 | `f8f7ecb52576f50108d2a9335074e5621dd5a0c2b5ee92b830929c8acc34900a` |
| `INT8/W8A8/model-00002-of-00008.safetensors` | 3,990,728,496 | `73c182d4362ca9351329eb9c812aa44f627631d1d1866868a326010dc8387a45` |
| `INT8/W8A8/model-00003-of-00008.safetensors` | 3,927,632,952 | `59510687bfca9272147d8153b0d3cc55a2672a03c7326d7099d78a313cc4f102` |
| `INT8/W8A8/model-00004-of-00008.safetensors` | 3,995,896,560 | `fd9c32e4a11dec2dbf42dfb4e5da653bbbc01cd075ff60e593869022138e2efd` |
| `INT8/W8A8/model-00005-of-00008.safetensors` | 3,922,465,008 | `7478173acc5b54c80329756cf2bb81b5b804a0fa107217fbba5d0cb3353c3f77` |
| `INT8/W8A8/model-00006-of-00008.safetensors` | 3,984,366,360 | `cd53edb6084ec639667f2bdb997f7822db1eb758a15a06818fddcac603642127` |
| `INT8/W8A8/model-00007-of-00008.safetensors` | 3,138,579,112 | `997de745c52a87d54f684a461dd831f59d80e6b0c4c43e7ad75bd148cc87fdd5` |
| `INT8/W8A8/model-00008-of-00008.safetensors` | 2,542,796,896 | `6866cf8adcccc4cc6a00e74bc025f1a774fb52103b70f2674d0288272951a733` |
| `INT8/W8A8/model.safetensors.index.json` | 125,462 | `8d04b274eb35757ea076fd573ca0e435649d3f6835a69dbd05317e29f05579e5` |
| `INT8/W8A8/tokenizer.json` | 19,989,325 | `06b9509352d2af50381ab2247e083b80d32d5c0aba91c272ca9ff729b6a0e523` |
| `INT8/W8A8/tokenizer_config.json` | 1,075 | `91a08f825d370d085d692e04cf117cdd7faad7bf18e996f1e6031b6dab03db72` |
| `INT8/W8A8/SHA256SUMS` | 1,420 | `e96702ae14a09d8280d24423d08a781fbef87e91784eaf1004ac46201fed8f73` |

## GGUF Q2 LynnStyle 说明

- 混合精度 LynnStyle,最低精度到 Q2;内置 **Q4 MTP**(不是 Q8)。成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同:GPQA 177/198、MMLU 433/500、LCB 90/100。思考 P50/P70/P90:GPQA 2,989.5 / 8,923.8 / 27,156.1;MMLU 181 / 326.3 / 1,020.5;LCB 5,656.5 / 17,835.8 / 40,067.3。
- 体积:GGUF 13,276,009,792 字节(BPW 3.89),NInfer 13,272,798,720 字节(BPW 3.89);分母 27,320,697,856。
- 速度(交接):llama.cpp 内置 Q4 MTP 长测 C4 174.8 tok/s(生成上限 4096);NInfer 短测 C8 521.0 tok/s(生成上限 512)。口径不同。
- GGUF 与 NInfer 分开启动(MTP 内置),命令见上文「启动命令」。MTP 与 DFlash2 互斥,本仓库不提供 GGUF 用的 DFlash2 草稿。

## GGUF Q3 LynnStyle 说明

- 混合精度 LynnStyle;内置 **Q4 MTP**(不是 Q8)。成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同:GPQA **173/198**、MMLU **449/500**、LCB **92/100**。GPQA 思考 P50/P70/P90:3,125.5 / 7,265.2 / 24,343.1。
- 体积:GGUF 17,303,770,432 字节(BPW **5.07**),NInfer 17,300,551,168 字节(BPW **5.07**);分母 27,320,697,856。
- 速度(交接):llama.cpp 融合 MTP 长测 C4 **191.8** tok/s(生成上限 4096);NInfer 短测 C8 **512.3** tok/s(生成上限 512)。口径不同。
- GGUF 与 NInfer 启动命令分开写(MTP 已内置)。DFlash2 是可选外挂草稿,不是这些包的默认。完整启动命令见 GGUF-NInfer 仓库卡片。

## GGUF Q4 LynnStyle 说明

- 混合精度 LynnStyle;内置 **Q4 MTP**(不是 Q8)。成绩在内置 MTP 前测得(外挂 Q8 MTP 草稿),量化权重相同:GPQA **175/198**、MMLU **448/500**、LCB **89/100**。
- 体积:GGUF 19,620,406,592 字节(BPW **5.75**),NInfer 19,617,187,328 字节(BPW **5.74**);分母 27,320,697,856。
- 速度(交接):llama.cpp 融合 MTP 长测 C4 **81.1** tok/s(生成上限 4096);NInfer 短测 C8 **436.4** tok/s(生成上限 512)。口径不同。
- GGUF 与 NInfer 分开启动(MTP 内置)。DFlash2 是可选外挂,不是这些包的默认路径。完整启动命令见 GGUF-NInfer 仓库卡片。

## GGUF Q8_0 说明

- 两个包主干量化相同(Q8_0),都内置 MTP 头,不需要外挂草稿模型;推荐 NInfer + C8 + MTP(486.3 tok/s)。
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf`:llama.cpp 直接加载。
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer`:只能用 NInfer-all 加载;启动请用 `--max-context 102400 --kv-capacity 819200 --max-concurrency 8`。
- 成绩在 llama.cpp 上用 GGUF 包测得;思考 token 三项均已拆分。

## GGUF Q6_K 说明

- 两个包主干量化相同(Q6_K + imatrix + 结构保护,见上文「量化方案」),都内置 MTP 头(GGUF `blk.64` 为 Q8_0;NInfer 的 MTP attention/MLP 权重为 Q6_K,输入投影为 Q8_0),不需要外挂草稿模型;推荐 NInfer + C4 + MTP。
- `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf`:llama.cpp 直接加载,GGUF 架构为 `qwen35`,65 个块,最后一块(`blk.64`)为 MTP。
- `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer`:只能用 NInfer-all 加载;SGLang、vLLM、llama.cpp、transformers 都不能读。
- 视觉:llama.cpp 用 `--mmproj GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(629,247,008 字节),`.ninfer` 包在 NInfer 下只能跑文本:包内没有视觉塔,NInfer 也不能单独加载 `vision-bf16.safetensors`(`GGUF-NInfer/` 内,921,497,224 字节)。
- 成绩在 llama.cpp 上用 GGUF 包测得;LCB 测评脚本与 NInfer 接口不兼容(收到的回复不是合法 JSON),属于测评脚本问题,不是模型质量问题,LCB 以 llama.cpp 为准。

### `GGUF/`(7 个文件:Q3+Q4+Q2+Q8+Q6 + mmproj + SHA256SUMS)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.gguf` | 17,303,770,432 | `9985b3d41fc7dc0bb5d493f7523d4515504912a3a7fc830f66e0fd2f90f9fd95` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.gguf` | 19,620,406,592 | `56c7c605a59764d9f0bb645d4eb335f1574af2c9e74020386139597df0e872f5` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.gguf` | 13,276,009,792 | `cad973b3b7cc0d86bd39968209268318a746673c12c9536e5c37408baa7b5e6e` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.gguf` | 29,069,202,688 | `b24e8c5fe3f2b282cce841400c740fcaca48afcdcf9e991f7bbe9a59a78cabfe` |
| `GGUF/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.gguf` | 23,177,516,384 | `302597c53d1b00f7230b53a8a050831390a4371e92a80c1ac644fa920af76ab1` |
| `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf` | 629,247,008 | `cae9799dc9196449b0d83f716e64af89d5cf65147510462e5a629a2aa23adb32` |
| `GGUF/SHA256SUMS` | 696 | `7b01a47f763ca72c58b2067dc21658d2a41eabff52bf5bbe25c2517fb99ebebf` |

### `GGUF-NInfer/`(7 个文件:Q3+Q4+Q2+Q8+Q6 + vision-bf16 + SHA256SUMS)

| 文件 | 字节 | SHA256 |
|---|---:|---|
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q3LynnStyle-MTP.ninfer` | 17,300,551,168 | `983456fc57cfc63a160512c933dc44f93005151c954b060399373d685b10de99` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q4LynnStyle-MTP.ninfer` | 19,617,187,328 | `376ee05a8c5160bde35e7c742565671fb4cec0e6e3c82cb293f87ad3a27d6cac` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q2LynnStyle-MTP.ninfer` | 13,272,798,720 | `cdd82b69027faba0bda619224ee851ccd0ecf0dfb176bad85a17d2df07926921` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q8_0-MTP.ninfer` | 29,065,983,488 | `40937a1509b0333858703b7c285b5a64b507803060a94bcccee19f4f683647bf` |
| `GGUF-NInfer/Qwen3.8-27B-Coder390-EfficientThink-Q6_K-MTP.ninfer` | 23,084,144,128 | `c273d394cd727a1055abc53b29e253e258926288429751e00acbeaea1ec0cd0e` |
| `GGUF-NInfer/vision-bf16.safetensors` | 921,497,224 | `d7defc90994f7bbc58a8feb8d3c4144895babb434a9be9f47e88ae3646e1df33` |
| `GGUF-NInfer/SHA256SUMS` | 701 | `2cf12cd6ca7a98ed5340a9bb3139a3f90401f39ab12798bb082c83df2eed47b2` |

## 已知局限

- GPQA 的空答在三种精度下都出在同两道分子生物题上,是题目上的老问题,与量化无关。
- 长尾仍未消除:思考 ≥48K 的题正确率明显偏低(如静态 FP8 的 LCB ≥48K 为 2/8),LCB 仍有 3 道写满 94K。
- MMLU 在三种精度间有 445–450 的采样抖动;成绩依赖上述口径(100K 上下文、94,208 生成上限、不计超时),不宜与其他口径直接比较。
- 性能只在单张 RTX PRO 6000 Blackwell + SGLang 上测得:BF16 / 静态 FP8 用的是静态 FP8 包,NVFP4 三档各用自己的包;vLLM 只做了 FP8 包的加载、MTP 与图像冒烟,NVFP4 未在 vLLM 上测试;DFlash2 只在 SGLang 上验证。
- NVFP4 三档的 GPQA(170、167、172)低于 BF16 / FP8 的 178,MMLU(439、440、442)略低于 445–450,LCB(91、92、88)在 90 上下;校准数据来自本模型自己的 RLOO 训练数据,不含官方测评题。NVFP4 只在 SGLang 上做过免补丁加载、贪心对拍和图像请求冒烟,MTP 与 DFlash2 以完整的性能测评为准。
- BF16 包的成绩来自同一份分片的全量测评,包本身的 GPU 冒烟(SGLang + MTP、图像)待补。
- INT8 W8A8 只有文本路径,只能用 vLLM;GPQA 175 略低于原版 Qwen3.8 27B(FP8)的 177;速度为快测(每档请求数等于并发数,生成上限 512),不能与其他档直接比较;GPQA / MMLU 思考长度按原文用 BF16 tokenizer 重新计数,LCB 没有保存思考原文,没有思考长度分位数。
- GGUF Q8_0:GPQA 171 低于原版 Qwen3.8 27B(FP8)的 177;LCB 截断 3、空答 3;全量三联只在 GGUF(llama.cpp)上跑;NInfer 速度为同口径测速,llama.cpp 为快测协议。
- GGUF Q6_K:GPQA 174 低于原版 Qwen3.8 27B(FP8)的 177;MMLU 思考长度按原文用 BF16 tokenizer 计数,LCB 没有保存思考原文,没有思考长度分位数;全量三联只在 GGUF(llama.cpp)上跑,NInfer 包未单独跑全量;速度为快测(每档请求数等于并发数,生成上限 512),不能与其他档直接比较;视觉用 `GGUF/mmproj-Qwen3.8-27B-Q8_0.gguf`(llama.cpp `--mmproj`),NInfer 包只能跑文本,各档图像路径未全部重测。

## 许可证与致谢

本模型采用 Apache-2.0 许可证,遵循基座 Qwen3.8-27B 的许可。

感谢 Qwen 团队提供基座模型与官方 FP8 方案;感谢 Opus5.5、GPT6Astra、Grok4.7、DSV4Pro、K3 在出题、金标、教师轨迹、数据核对与 RLOO 价值评审中的工作;感谢 SGLang、vLLM 与 DFlash 社区。
<!-- CARD_ZH_END -->
