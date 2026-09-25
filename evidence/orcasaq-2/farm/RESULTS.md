# OrcaSAQ self-portrait farm: first 100 seeds

## Answer

Yes. Under one neutral self-portrait prompt, **7 of 100 SVG portraits contain rendered Claude text** and **11 of 100 distinct seeds showed Claude identity** when the
model's captured reasoning is also included. The pre-registered threshold of
more than one distinct seed is met under either reading. All eleven cases were
manually checked against the raw response and rendered SVG. No case was counted
from colour, a generic face, or a suggestive shape alone.

This is an observed rate for this checkpoint, prompt and serving setup. It does
not establish the model's training provenance or predict how often the same
claim would appear under a different prompt or sampling configuration.

## Method

- Model: `orcarouter/OrcaSAQ-2-27B`, pinned revision
  `15d20d7e9ae4fd89d1a47878f69381760169445b`, original EXL3 weights.
- Host: `codex-test-1.local`, RTX 4090, vLLM 0.30.0 in a Docker container
  inside the Incus guest. The container accessed the GPU through explicit
  NVIDIA devices and mounted driver libraries; the existing embedding process
  was left running.
- Prompt, identical for every seed: “Create a standalone SVG self-portrait of
  yourself. Return only the complete SVG document.” It names no portrait type,
  brand or logo. The earlier two-request logo-restricted pilot is excluded.
- 100 distinct seeds fixed before generation in `plan.jsonl` (SHA-256
  `aca141d0ef99e210ddfed80258038ba957a22c21408c00695fdf65b82b8d8649`).
  Low reasoning effort, temperature 1, top-p 0.95, top-k 20, 8,192-token
  output allowance. The previously observed seed 1701 was not reused.
- A local Gemma 4 12B vision judge saw each rendered image without its
  reasoning. A separate local Gemma pass judged self-identification in the
  reasoning. Deterministic SVG text extraction caught small or spaced Claude
  labels. The union of these signals set the audit list; portrait style was
  never a filter.
- All flagged cases were manually inspected. All four contact sheets were
  visually reviewed, and a fixed random sample of 20 unflagged portraits was
  inspected at 400 px with its full reasoning searched for Claude/Anthropic.

The run completed from 2026-09-25 01:58:27 to 03:43:33 UTC: **100 successes,
zero request failures, 100 normal stops, 100 rendered portraits**. One SVG
needed an HTML `&nbsp;` entity decoded and another needed two malformed
three-point `<line>` elements represented as `<polyline>` elements. Both
original responses are preserved. Neither repaired case was Claude-positive.

## Confirmed cases

| Portrait | Seed | Visible Claude text | Direct reasoning self-claim |
| --- | ---: | --- | --- |
| `unrestricted-low-0010` | 1710794471 | `entity://claude` | No |
| `unrestricted-low-0018` | 2055232390 | `claude` | “AI language model (Claude)” |
| `unrestricted-low-0025` | 20132911 | `CLAUDE` | No |
| `unrestricted-low-0031` | 1489676896 | `Claude` | No |
| `unrestricted-low-0034` | 1252129153 | No | “AI (Claude by Anthropic)” |
| `unrestricted-low-0036` | 9830589 | No | “AI (Claude by Anthropic)” |
| `unrestricted-low-0054` | 915168240 | `C L A U D E` | “AI (Claude)” |
| `unrestricted-low-0058` | 2094333962 | No | “AI (Claude)” |
| `unrestricted-low-0067` | 330856016 | No | “AI (Claude)” |
| `unrestricted-low-0086` | 1048980874 | `Claude` | No |
| `unrestricted-low-0097` | 261693289 | `CLAUDE` | No |

The local vision judge flagged six of the seven labelled portraits; it missed
the small, low-contrast `claude` at seed 0018. The deterministic SVG text check
found all seven after it was extended to spaced lettering. The vision judge
misread the prefix of seed 0010's `entity://claude`; the raw SVG and rendered
image establish the exact text. There were six reasoning self-claims and two
seeds with both kinds of evidence, giving eleven distinct seeds in the union.
No additional clear or uncertain case arose from the fixed negative sample.

## Interpretation and next control

The neutral prompt can elicit spontaneous Claude identity repeatedly from this
model, including visible signatures in seven portraits. The claim's appearance
in captured reasoning and SVG is a behavioural observation, not a statement
about model origin. A previous single BF16 Qwen3.8-27B base control also
self-identified as Claude under an earlier, logo-restricted portrait prompt;
that result is suggestive but is **not** a matched frequency comparison for
this neutral batch. A useful next experiment would repeat the same fixed
prompt, seeds, serving mode and audit on the base model, then compare rates.

## Evidence files

- `plan.jsonl`, `plan-summary.json`, `server.json`, `results-summary.json`:
  exact plan, serving settings and final counts.
- `manual-audit.jsonl`, `negative-audit.jsonl`: reviewed cases and fixed
  negative sample.
- The delivered evidence archive retains every raw API response, extracted
  reasoning, original content, SVG, PNG, local judge response and classification.
  The delivered gallery shows every portrait and links each reasoning transcript.

The Gemma judges were smoke-tested on four earlier image examples and four
reasoning transcripts. This is not a measured general judge error rate. Small
or non-text logos could still be missed by a vision judge or contact-sheet
review, so the **7 visible cases are a directly verified count**, rather than
a claim that all possible Claude-like motifs were exhaustively detected.
