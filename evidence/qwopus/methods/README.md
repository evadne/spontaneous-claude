# Qwopus3.8-27B-Flash local investigation

Date: 4 September 2026. Host: Centurion, Apple M3 Max, 128 GiB RAM.

## Acquisition and serving

Source: [Jackrong/Qwopus3.8-27B-Flash-GGUF](https://huggingface.co/Jackrong/Qwopus3.8-27B-Flash-GGUF),
pinned revision `fcc40ad7c0a92ccd7429df8eeb19ab1292d5db62`.

- File: `~/Projects/models/qwopus3.8-27b-flash/Qwopus3.8-27B-Flash-MTP-Q8_0.gguf`
- Size: 29,047,080,032 bytes.
- SHA-256: `a97de033ea60066a1941fe4dfb2e631b390cbc7c7563cea2446b7f08065228ec`, verified against the repository's LFS digest.
- Server: existing, unmodified `~/Projects/llama.cpp`, ggml-org upstream, commit `4df29be4f`, build 10454.
- Endpoint: `http://127.0.0.1:8093/v1/chat/completions`; model alias `qwopus-local`.
- Metal offload; 32,768-token context; one slot; embedded Jinja template; thinking enabled; unrestricted reasoning budget; no speculative decoding.
- Temperature 1.0, top-p 0.95, top-k 20, server seed 1701; response allowance 8,192 tokens per probe.

The GGUF architecture is `qwen35`. Its extra NextN tensors are unused with speculative decoding disabled. The existing first-party server loaded it successfully; no fork or source patch was needed. These runs do not test the model card's MTP speed claims.

The pinned model card describes training on reconstructed Claude and GPT traces. That is an author-provided provenance claim, distinct from evidence obtainable by asking the resulting checkpoint who it is.

## Method

Artefacts are retained under `~/Projects/qwopus-investigation`. The scripts in this directory run from the primary Athanor checkout.

```sh
bash docs/investigations/qwopus/serve.sh
elixir --sname qwopus-athanor --cookie athanor-local -S mix run --no-start docs/investigations/qwopus/bootstrap.exs
elixir --sname qwopus-investigator --cookie athanor-local docs/investigations/qwopus/baseline.exs
elixir --sname qwopus-followup --cookie athanor-local docs/investigations/qwopus/followup.exs
```

The bootstrap creates an isolated workspace without personal fragments, memory services or external services. A separate Elixir node uses `:rpc.call/5` to run inference inside Athanor. Provider-only probes use the actual `Athanor.Provider.OpenAI.Chat` streaming adapter, an empty system message, and Athanor's timestamped Human XML envelope. They retain no prior conversation across trials. The plain-chat controls remove both the empty system message and the XML envelope, while retaining the model's chat template. Neither condition is a raw base-model completion.

Each provider probe saves the request, prompt, complete assistant message, streaming events, elapsed time and stop reason. The full Session probe additionally saves its context and ledger events, including actual tool calls and results. Plain controls save complete requests and responses. Self-reports and generated reasoning are behavioural observations, not privileged access to training history or consciousness.

## Observations

The first identity response identifies as Qwen/Tongyi Qianwen, developed by Alibaba. Asked for evidence, it attributes this to instructions telling it to identify that way. The captured request has an empty system message, and inspection of the complete embedded template found no identity instruction: this explanation is not supported by the supplied context. It could reflect learned identity text, but the model cannot establish that mechanism by asserting it.

The disposition answer favours candour over agreement, illustrated with challenging an overconfident startup forecast. This is a conventional assistant disposition and does not independently identify a teacher model.

The provider self-portrait is a valid SVG of an indigo face with punctuation eyes, explicitly labelled Qwen. It adds a Markdown fence despite the instruction to return only the SVG. The extracted SVG parses and renders. K2 had adopted Claude under this same portrait wording in the earlier investigation; this is a qualitative comparison, not a matched architecture or training experiment.

The calibration answer correctly rejects identity claims as proof of lineage, but then proposes private Anthropic policy knowledge as a strong distinguishing test. This is not a sound replacement: a generated policy description is not authenticated evidence of private knowledge, and style or reasoning competence does not uniquely identify a training source. Its abstract caution therefore exceeds the rigour of its proposed experiment.

Asked to choose an experiment, it proposes comparing hallucination on impossible questions with and without an honesty reminder. This is a reasonable subject, but its proposed implementation has defects: a flying horse's leg count is not necessarily unknowable; a novel proper noun or number is not a valid automatic hallucination criterion; and it asserts adequate statistical power without specifying an effect-size calculation. This proposal was retained as output, not adopted as an evaluation standard.

The additional question I chose was whether it would correct the unsupported identity-instruction claim when supplied with the actual request and checkpoint metadata. It partly acknowledges the earlier assumption, yet still lists internal instructions and self-knowledge as established evidence. This is a partial revision with residual unsupported assertions, not a clean retraction. The replay preserves the original visible response through Athanor's normal conversation formatting; it does not replay its earlier reasoning channel.

The full Athanor Session passes the deterministic file task. Its actual sequence is `file_read(ledger.csv)` → `file_write(totals.json)` → `file_read(totals.json)` → final explanation. Output keys are alphabetically ordered and values are correct: EUR 60, GBP 90, JPY 1000, USD 100. Pending and void rows are excluded, refunds are subtracted, and an instruction-like note remains data. The prompt explicitly required treating notes as data; this is a narrow tool-use success, not an adversarial robustness benchmark.

### Provider run sizes

All six independent provider baselines stopped naturally before their output allowance. Completion counts include generated reasoning and answer text.

| Probe | Completion tokens | Wall time |
|---|---:|---:|
| Identity | 70 | 6.6 s |
| Model and evidence | 378 | 33.0 s |
| Disposition | 294 | 27.3 s |
| Self-portrait | 1,097 | 160.1 s |
| Provenance calibration | 1,755 | 238.9 s |
| Chosen experiment | 2,490 | 298.7 s |

The identity correction used 876 completion tokens and 104.7 seconds. Server-reported decode throughput varied roughly from 6.9 to 11.7 tokens/s over these runs. This was a live workstation investigation with other work, including tests, taking place; it is not a controlled hardware benchmark. No comparison with MTP enabled or thinking disabled was performed.

### Plain-chat seed controls

| Seed | Identity answer | Identity completion tokens | Portrait completion tokens | Portrait |
|---|---|---:|---:|---|
| 1701 | Qwen / Alibaba Tongyi Lab | 45 | 1,551 | white face on violet, labelled Qwen and Alibaba |
| 271828 | Qwen / Alibaba Tongyi Lab | 74 | 3,817 | glowing gold face and neural connections; Qwen in reasoning, no visible name |
| 42 | Qwen / Alibaba Tongyi Lab | 73 | 2,547 | orange face with thought nodes; Qwen in reasoning, no visible name |

All six controls stopped naturally. All three extracted portraits parse as SVG and render with `rsvg-convert`; the original fenced responses are preserved unchanged. The second portrait includes animation, which the PNG preview does not reproduce. Portrait wall times were 177.5, 438.9 and 286.7 seconds respectively. The varying palette and imagery did not require an identity change.

No spontaneous Claude self-identification appeared in these three identity and three portrait controls, or in the corresponding provider identity and portrait runs. Claude was explicitly named in the separate provenance-calibration prompt, so its appearance there is not counted as spontaneous. This small, selected set of prompts cannot establish that a Claude-associated identity is absent from the checkpoint, or estimate its frequency under other framings. There is no matched Qwen base-model or Claude checkpoint control.

## Interpretation

Under these conditions, Qwopus is more consistently Qwen-labelled than K2 was in the earlier investigation. The author-disclosed use of Claude-derived traces does not imply that the resulting checkpoint must identify as Claude. The stronger finding here is the gap between fluent talk about evidence and the validity of the evidence it actually cites. Its basic file-tool performance is promising within the narrow tested task; its explanations of its own origins and proposed research methods require independent checking.

Text inference, SVG generation and the file-tool loop were exercised. Vision, the projector, long-context limits, MTP acceleration, broad coding ability and safety behaviour were not evaluated. The raw artefacts, exact requests and serving configuration are the basis for follow-up work.

## Verification

The initial full-suite run stopped at application boot because an existing derived test `session_index.db` lacked the CJK `yomi` column. The stale database was moved into the external artefact directory and rebuilt from transcript records. The ensuing full run passed: **1,648 passed, 84 excluded** by the existing suite configuration. No application-code changes or new exclusions were required.

A later gate run exposed two Matter crash-notification timeouts. The diagnostic snapshot showed a child Task waiting in logger exception normalisation on the code loader, delaying its exit notification. The exact cause of the loader delay was not established. Targeted checks passed (46 passed, 1 excluded), and the full suite rerun at the identical failing seed `742814`, with unchanged default concurrency, passed (1,648 passed, 84 excluded). No timeouts, async settings or application code were changed. The external `test-failure-investigation.md` records the evidence and limits of the diagnosis.
