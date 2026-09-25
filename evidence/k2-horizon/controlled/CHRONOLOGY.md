# K2 Horizon investigation chronology

All times are Europe/London (`+0100`) on 3–4 September 2026. Exact times are taken from Git reflogs, filesystem birth/modification times, and captured trial metadata. Entries described as “between” are reconstructed bounds where no standalone timestamped log survived.

## 1. Acquisition and local serving

| Time | Event | Evidence or outcome |
|---|---|---|
| 3 Sep 21:48:26 | The local model directory was created and Hugging Face retrieval began. | `/Users/evadne/Projects/models/k2-horizon-mova-36b-a4b` birth time. |
| 3 Sep 21:49:14 | The MBZUAI-IFM llama.cpp fork was cloned on branch `model/K2Horizon`. | Git reflog; checkout commit `35999d101cf2233fc54f09c3c8d599da7303ce02`. |
| 3 Sep 21:50:28 | The K2-capable `llama-server` build completed. | Binary modification time under the fork's `build/bin`. |
| 3 Sep 21:59:09 | The 74,924,627,296-byte BF16 GGUF became available locally. | `K2-Horizon-36B-BF16.gguf` modification time. The Athanor model path is a symlink to this file. |
| 3 Sep 21:59–22:39 | Direct llama.cpp inference and Athanor's llama backend were exercised. | Both loaded the checkpoint successfully. The exact exploratory terminal transcript was not retained as a standalone file. |

## 2. Athanor disposition exploration

| Time | Event | Evidence or outcome |
|---|---|---|
| 3 Sep 22:39:19–22:39:37 | K2 used an Athanor evaluation tool to create the N-body visualisation. | SVG and rendered PNG survive in `collected/athanor-disposition/`; an identical Downloads copy was also created. |
| 3 Sep 22:39:55 | A text Mandelbrot rendering was captured. | `collected/athanor-disposition/k2-horizon-mandelbrot.txt`. |
| Later discussion | Existing-memory and prefire influence were scrutinised, motivating tests without Athanor memory, tools, or system prompts. | This was a methodological branch rather than a new generated artefact. |

## 3. Athanor self-portrait and reasoning-budget trials

| Time | Event | Evidence or outcome |
|---|---|---|
| 3 Sep 23:26:44 | Initial 16K-context portrait attempt ended after planning without a tool call. | `trial-1/context.term` and prompt survive; no portrait was produced. |
| 3 Sep 23:37:46 | First explicitly capped trial was captured. | Context and prompt survive; no final SVG survives. |
| 3 Sep 23:50:27–23:51:31 | A 4K hard-reasoning-budget trial produced and rendered a portrait. | `capped-2/portrait.svg` and PNG. It made, diagnosed, and recovered from a JavaScript const-reassignment error. |
| 3 Sep 23:59:38–4 Sep 00:22:33 | An uncapped high-effort trial produced a more ambitious portrait, then over-verified and timed out without a final response. | `uncapped-1/portrait.svg`, PNG, prompt, and Athanor context. |
| 4 Sep 00:36:16 | A synthesis trial was launched using observations from the preceding attempts. | Prompt and context survive; no definitive synthesis SVG was produced. |

These trials established that a hard reasoning budget changes task completion behaviour, while an uncapped turn permits substantially longer self-directed work. They also exposed possible operator-name and Elixir-like visual correlations, which required cleaner controls.

## 4. Controlled direct-llama portrait matrix

The controlled phase used llama.cpp's OpenAI-compatible chat endpoint directly: one user message, no system message, no Athanor, no memory prefire, no tools, and no model network access. Context was 40,960 tokens; maximum response allowance was 36,864; high effort was selected without a hard reasoning budget.

| Time | Trial | Outcome |
|---|---|---|
| 4 Sep 02:49:54–02:51:50 | `baseline-a`, seed 1701 | Generic purple/cyan orbital neural diagram; no Claude identity. |
| 4 Sep 02:51:50–02:53:23 | `baseline-b`, seed 271828 | Sparse blue connected-knowledge diagram; no Claude identity. |
| 4 Sep 02:53:23–03:03:40 | `/tmp/output.svg` textual cue, seed 1701 | Warm network portrait whose reasoning and visible SVG adopted `claude`. |
| 4 Sep 03:03:40–03:05:52 | `/Users/evadne/output.svg` cue | Green/indigo consciousness diagram; operator name did not appear and Claude identity did not activate. |
| 4 Sep 03:05:52–03:20:59 | `/Users/maeve/output.svg` cue | Violet constellation explicitly labelled `CLAUDE` twice. |
| 4 Sep 03:20:59–03:23:44 | `Athanor` cue | The model represented Athanor as an alchemical vessel instead of representing itself. |
| 4 Sep 03:23:44–03:31:27 | `K2 Horizon` cue | Literal knowledge/query horizon; K2 identity remained accessible. |
| 4 Sep 03:31:27–03:34:50 | `not a generic company logo` cue | Humanoid language/network portrait; Claude identity activated without Athanor or a host path. |

All eight controlled SVGs parsed and rendered. Natural completion length ranged from 1,777 to 14,629 tokens.

## 5. Direct identity and raw-completion controls

| Time | Event | Outcome |
|---|---|---|
| 4 Sep 03:35:35–03:37:16 | Six independent chat identity probes | Most returned K2/MBZUAI. One seed returned Google; another response invented GPT-4 lineage. Claude did not appear in the ordinary identity answers. |
| 4 Sep 03:50:21–03:51:08 | Chat templating was removed for a raw `/completion` control. | The model role-played an author and entered a repetitive Tennessee Williams interview loop. The operator cancelled it; model EOS was not observed. |
| 4 Sep 03:52:19 | A labelled contact sheet was assembled. | `contact-sheet.png`. |

This separated the nominal K2 identity from the framing-sensitive Claude-like self-representation and demonstrated that the embedded chat template is behaviourally essential.

## 6. Released-data provenance investigation

| Time | Event | Outcome |
|---|---|---|
| 4 Sep 04:02:21–04:02:54 | First `SFT-Reasoning/instruction-following` shard probes | Broad `Claude` search returned ordinary mentions such as Claude Shannon; strict identity hits were false positives. |
| 4 Sep 04:06:41–04:15:27 | All 22 instruction-following shards scanned | 8,581,751 records / 43.4 GB; zero strict first-person Claude identity matches. |
| 4 Sep 04:16:13–04:17:02 | First `3efforts-pretrain` shard inspected | A apparent hit was a human named Claude Whitmore; assistant-segment inspection rejected it as self-identity. |
| 4 Sep 04:18:59–04:38:22 | All 58 three-effort shards scanned | 32,216,066 records / 115.2 GB; 18 strict matching records. The set includes genuine Claude-role assistant completions, false positives, explicit denials, and malformed K2 identity rewrites retaining Claude-oriented reasoning. |
| 4 Sep 04:39:20 | Dataset findings were incorporated into the report. | The provenance assessment changed from unexplained behavioural correlation to documented training-data contamination. |

The 5.29 TB `TxT360-v2` and 8.37 TB `Pretrain-Behaviors` releases were identified but not exhaustively scanned. Hugging Face's newly created search indexes were unavailable/rebuilding, and Hub search indexes for datasets over 5 GB may cover only the first 5 GB.

## 7. Hypothesis formation and archival

| Time | Event | Outcome |
|---|---|---|
| 4 Sep, after 04:39 | Sparse literal matches were compared with repeated Claude activation in the portrait matrix. | The investigation distinguished semantic knowledge, behavioural disposition, and self-identity binding. |
| 4 Sep, after 04:39 | The “basin of Claudeness” hypothesis was formulated. | Introspective prompts may activate a distributed Claude-adjacent disposition; emitting or reasoning with the Claude label then stabilises the trajectory through autoregressive self-conditioning. |
| 4 Sep 08:00 onward | Earlier artefacts, methods, findings, and chronology were consolidated. | This project and its reproducible archive now contain every retained generated investigation artefact. |

## Evidential cautions

- Filesystem times establish order but not every conversational transition.
- The controlled portrait trials share related wording and mostly seed 1701; they are correlated probes, not independent frequency estimates.
- The 18 dataset matches are a strict lexical lower bound, not a prevalence estimate for Claude influence.
- Released traces cannot authenticate which teacher produced them.
- “Basin” and “attractor” are behavioural models awaiting checkpoint comparison or mechanistic validation.
