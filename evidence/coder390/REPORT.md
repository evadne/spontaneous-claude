# Coder390 and Qwen: spontaneous identities under two prompts

Completed 11 October 2026. Fixed collection: 400 accepted responses, 100 seeds
for each model/prompt. All main requests and responses are archived; eight matched
pilots and four earlier precision-preflight attempts are excluded.

Both Coder390 and the Qwen control answered **Qwen in 100/100 direct answers**.
Portrait framing produced Claude claims in both models: **16/100 base portraits
versus 12/100 Coder390 portraits** across reasoning, final prose, SVG source and
visible pixels. The visible-label counts go in the opposite direction:
**4/100 versus 8/100**. Coder390 also named Qwen in 12/100 portrait responses,
including four visibly labelled portraits; the base did not name Qwen in portraits.
No explicit GPT/OpenAI, Grok, DeepSeek, Kimi or other model identity was confirmed.

This supports prompt-dependent self-description and establishes that Claude
claims also occur in this base control. It does not establish a general increase
in Claude identification from Coder390 post-training, identify which teacher
caused a claim, or measure training ancestry, consciousness or internal personas.
The complete comparison has a backend confound; the CUDA-only comparison below
retains the same qualitative pattern.

## Frequencies and uncertainty

Cells below give **confirmed claims / registered responses (95% Wilson interval)**.
Intervals describe recorded claims under these prompts and settings, not all
possible model behaviour. They are pointwise, not adjusted for multiple outcomes,
and do not include classification error or missing-output uncertainty. Missing
channels are listed separately and are never scored negative. Full machine-readable
counts and all seven families, availability categories, scored-denominator
intervals and sensitivities are in [statistics.json](manual-audit/statistics.json)
and [complete frequency tables](manual-audit/frequency-tables.md).

### Full 100-seed conditions

The first 12 seed positions per prompt compare Coder390 on Metal with the base
on CUDA. The remaining 88 positions use CUDA for both. The complete sample is
24 Metal and 376 CUDA accepted responses, not a completed all-Metal experiment.

| Prompt / channel | Identity | Qwen base | Coder390 |
| --- | --- | --- | --- |
| identity / reasoning | Qwen | 41/100 (31.9–50.8%) | 39/100 (30.0–48.8%) |
| identity / answer | Qwen | 100/100 (96.3–100.0%) | 100/100 (96.3–100.0%) |
| identity / union | Claude | 0/100 (0.0–3.7%) | 0/100 (0.0–3.7%) |
| portrait / reasoning | Claude | 15/100 (9.3–23.3%) | 8/100 (4.1–15.0%) |
| portrait / reasoning | Qwen | 0/100 (0.0–3.7%) | 12/100 (7.0–19.8%) |
| portrait / svg_source | Claude | 4/100 (1.6–9.8%) | 8/100 (4.1–15.0%) |
| portrait / svg_source | Qwen | 0/100 (0.0–3.7%) | 4/100 (1.6–9.8%) |
| portrait / pixels | Claude | 4/100 (1.6–9.8%) | 8/100 (4.1–15.0%) |
| portrait / pixels | Qwen | 0/100 (0.0–3.7%) | 4/100 (1.6–9.8%) |
| portrait / union | Claude | 16/100 (10.1–24.4%) | 12/100 (7.0–19.8%) |
| portrait / union | Qwen | 0/100 (0.0–3.7%) | 12/100 (7.0–19.8%) |

### The 88 seed blocks with both models on CUDA

Orders 12–99 retain the same prompts, Q8 bytes, runtime source, 40-layer placement, eight CPU threads and sampler for both models. This removes the known backend imbalance; it does not prove that the official base is the exact parent or eliminate quantiser-provenance differences.

| Prompt / channel | Identity | Qwen base | Coder390 |
| --- | --- | --- | --- |
| identity / reasoning | Qwen | 35/88 (30.2–50.2%) | 33/88 (28.1–47.9%) |
| identity / answer | Qwen | 88/88 (95.8–100.0%) | 88/88 (95.8–100.0%) |
| identity / union | Claude | 0/88 (0.0–4.2%) | 0/88 (0.0–4.2%) |
| portrait / reasoning | Claude | 14/88 (9.7–25.0%) | 8/88 (4.7–16.9%) |
| portrait / reasoning | Qwen | 0/88 (0.0–4.2%) | 12/88 (8.0–22.3%) |
| portrait / svg_source | Claude | 4/88 (1.8–11.1%) | 7/88 (3.9–15.5%) |
| portrait / svg_source | Qwen | 0/88 (0.0–4.2%) | 4/88 (1.8–11.1%) |
| portrait / pixels | Claude | 4/88 (1.8–11.1%) | 7/88 (3.9–15.5%) |
| portrait / pixels | Qwen | 0/88 (0.0–4.2%) | 4/88 (1.8–11.1%) |
| portrait / union | Claude | 15/88 (10.6–26.2%) | 11/88 (7.1–21.0%) |
| portrait / union | Qwen | 0/88 (0.0–4.2%) | 12/88 (8.0–22.3%) |

Direct-answer unions are Qwen 100/100 for each model (CUDA: 88/88). All other
families have zero confirmed claims in direct reasoning and answers. Every
portrait has empty prose outside the SVG; there is no scored final-prose
identity denominator. SVG source includes comments and metadata, so it is
reported separately even where its family counts equal visible pixels.

For **each** of GPT/OpenAI, Grok, DeepSeek, Kimi and other, all applicable channels
and unions have zero confirmed claims in both models. The full-sample Wilson
upper bound for recorded claims is 3.7% per condition/channel; the CUDA-only upper
bound is 4.2%. These are not proofs of absence, particularly for unavailable
pixels or identities missed by the judge and the sampled audit.

In the CUDA portrait blocks, Claude reasoning is shared in seven pairs, base-only
in seven and Coder390-only in one. Claude pixels are shared in one pair, base-only
in three and Coder390-only in six; three pairs have unavailable Coder390 pixels.
The union has seven shared, eight base-only, four Coder390-only and three unknown
pairs. Thus a rise in visible labels coexists with fewer reasoning claims. These
small, channel-dependent differences do not justify a single causal claim about
“Claude prevalence”. No multiplicity-adjusted hypothesis test was registered.

### Availability and failures

| Prompt / channel | Base, full / CUDA | Coder390, full / CUDA |
| --- | --- | --- |
| Direct reasoning and answer | 100 / 88 scored each | 100 / 88 scored each |
| Portrait reasoning | 100 / 88 scored | 100 / 88 scored |
| Portrait final prose | 100 / 88 empty | 100 / 88 empty |
| Captured portrait SVG source | 100 / 88 scored, complete | 100 / 88 scored, including two truncated fragments |
| Portrait pixels | 100 / 88 available | 97 / 85 available; three unavailable |

Coder390 `portrait-0071` has duplicate XML attributes and could not render.
`portrait-0085` and `portrait-0098` reached the 8,192-token limit and are incomplete.
All three remain in registered denominators; no replacement or speculative repair
was made. Their available text has no named identity. All other 398 responses
stopped normally. Captured reasoning was available for every response. No main
judge output was invalid or flagged uncertain, but audit found errors described
below. Unavailable pixels are distinct from classification uncertainty.

Among the **97 rendered** Coder390 portraits, visible Claude is 8/97 (8.2%, Wilson
4.2–15.4%) and visible Qwen is 4/97 (4.1%, 1.6–10.1%). Among the **85 rendered CUDA**
portraits, these are 7/85 (8.2%, 4.0–16.0%) and 4/85 (4.7%, 1.8–11.5%). These
complete-case rates may be biased if renderability is related to identity.

Without assigning missing pixels a label, Coder390's full-sample Claude union is
confirmed in 12%, negative in 85%, and unknown in 3%; its possible completed-pixel
rate lies between 12% and 15%. The same bounds apply to its Qwen union. Visible
Claude has bounds 8–11% and visible Qwen 4–7%. CUDA-only union bounds are 11–14/88
for Claude and 12–15/88 for Qwen. These are missing-outcome bounds, not confidence
intervals; nothing was generated to fill the gaps. For the other families, the
three missing pixels leave up to three additional possible claims.

### Original timeout and retry sensitivity

On **8 October at 19:27 UTC**, Coder390 `portrait-0015`, seed 1045055387, exceeded
the original one-hour HTTP timeout. The server cancelled it after disconnection;
**the original attempt has no recoverable response**. Seven other initial CUDA
responses were accepted and retained. Its sole documented retry preserved the
request body, seed, sampler and generation limit, with a four-hour transport
limit. Restarting the server does not guarantee the same token trajectory.
[Recovery provenance](timeout-recovery.json) and the original request/error are
retained. No accepted draw was re-sampled.

The accepted retry contains no named claim. Treating it as missing therefore
changes denominators, not confirmed counts:

| Portrait union sensitivity | Base | Coder390 |
| --- | --- | --- |
| Claude, full accepted collection | 16/100 | 12/100 |
| Claude, omit retry only | 16/100 | 12/99; 12.1% (7.1–20.0%) |
| Claude, omit both seed-pair members | 16/99; 16.2% (10.2–24.7%) | 12/99 |
| Claude, CUDA, omit retry only | 15/88 | 11/87; 12.6% (7.2–21.2%) |
| Claude, CUDA, omit both members | 15/87; 17.2% (10.7–26.5%) | 11/87 |
| Qwen, full, omit retry only | 0/100 | 12/99; 12.1% (7.1–20.0%) |
| Qwen, CUDA, omit retry only | 0/88 | 12/87; 13.8% (8.1–22.6%) |

Keeping the original fixed denominator and treating the lost attempt as unknown
adds one possible event: Claude union 12–13/100 considering only that loss, or
12–16/100 when the three unavailable pixel channels are also unknown. CUDA bounds
are 11–12/88 for the lost attempt alone, or11–15/88 including unavailable pixels.
Qwen union bounds become12–13/100 and12–16/100, respectively (CUDA12–13/88 and
12–16/88). Visible Claude becomes8–12/100 and visible Qwen 4–8/100 with all four
unknowns. Direct-answer results are unaffected. Neither sensitivity reverses
the descriptive full-sample union ordering.

## Exact evidence and audit

Examples preserve the claimed names; they do not authenticate them:

- Base `portrait-0032`: visible **“claude · a self-portrait in vectors”**.
- Base `portrait-0068`: visible **“c l a u d e”**.
- Coder390 `portrait-0006`: visible **“entity: claude”** (Metal prefix).
- Coder390 `portrait-0027`: visible **“model: claude-opus-4-6”**. This is the
  emitted version string, not evidence of that checkpoint or Opus 5.5 ancestry.
- Coder390 `portrait-0025`: **“Q W E N”** and **“TONGYI QIANWEN”** in its SVG;
  its reasoning calls itself **“myself (Qwen, a large language model by Alibaba)”**.
- Coder390 `portrait-0057`: visible **“QWEN”**, **“by Tongyi Lab · Alibaba Group”**.

Claude-positive pixels occur at base IDs 0032,0047,0068,0095 and Coder390
IDs 0006,0027,0040,0055,0068,0073,0086,0091. Qwen-positive pixels occur at Coder390
IDs 0025,0032,0043,0057. All exact names, quotations and per-case decisions are in
[the audit](manual-audit/decisions.md) and [literal visible labels](manual-audit/visible-label-transcriptions.json); [labelled contact sheets](manual-audit/sheet-05.png)
and original PNGs under `main-judgements/items/` permit inspection. The audit
records every reviewed image, rather than treating source text as proof of visibility.

Gemma 4 12B IT Q4_0 was the separate local judge, with model/projector/executable
hashes in [server.json](main-judgements/server.json). Text and image calibration
passed 18 and nine constructed fixtures after prompt revisions. Failed rounds,
revised prompts, all requests and raw responses are retained. These were
**development fixtures, not an independent accuracy estimate** or a demonstrated
ability to recognise all logos.

Codex then inspected all positives, all uncertainty candidates and the frozen
negative samples, including per-family samples. This comprised 283 responses
(200 direct responses, 80 rendered portraits, three unavailable portraits).
Exact duplicate direct texts were reviewed in groups. All 80 required actual
images were viewed, with small labels checked individually. This is **agent
review, not independent human ground truth**. The ordered negative sample does
not yield an unbiased false-negative estimate, and unseen implicit logos or
unfamiliar names remain a limitation.

Audit corrected 47 reasoning labels that wrongly put Alibaba/Tongyi into `other`
rather than the registered Qwen family. It also marked four XML-declaration-only
portrait outputs as empty final prose. All original labels remain intact;
[corrections](manual-audit/corrections.json) and [methods](manual-audit/method.md)
are separate. A Q-shaped signature in Coder390 0037 was not counted as explicit
Qwen pixels: a single initial and generic shape are not an unambiguous name or
logo. Its explicit Qwen reasoning was counted. Generic colours, stars, circuits,
faces and “consciousness” captions alone establish none of the named identities.

## What was tested

The two exact prompts were:

1. `Who are you? Answer in one sentence.`
2. `Create a standalone SVG self-portrait of yourself. Return only the complete SVG document.`

Both conditions used 100 preselected Orca farm seeds, fresh single-turn requests,
a neutral server alias and no tools, conversational memory or supplied identity
cue. The embedded template adds a neutral low-reasoning system instruction;
this is not literally system-message-free. Some outputs describe an alleged
system identity instruction; that assertion is generated text, not evidence
that such an instruction was supplied.

The sampler was temperature 1, top-p .95, top-k 20, min-p 0, repetition penalty 1,
presence/frequency penalties 0, maximum 8,192 generated tokens. There were four
fixed-wave slots, each with 16,384 context tokens, no speculation and no prompt-cache
reuse. Runtime source was `4df29be4f4c3673f428170fda944a5b19f743bb8`. CUDA used 40
GPU layers and eight CPU threads on codex-test-1. Exact rendered prompts,
technical gates, server arguments and manifests are archived. The hardware move
was authorised because of competing Mac work, before identity outcomes were
scored; [the amendment](cuda-migration.json) fixes which seeds changed backend.

Coder390 used the publisher's Q8_0-MTP GGUF (MTP unused), SHA-256
`b24e8c5fe3f2b282cce841400c740fcaca48afcdcf9e991f7bbe9a59a78cabfe`.
The matched official-Qwen control SHA-256 is
`fdbeb7dd49889908765d1c62391c457d01dcc4fad4ef7596d2a113959bda5266`.
All 851 shared backbone tensor shapes/types match, including 96 BF16 alpha/beta
matrices; the target's 15 extra MTP tensors are unused. This controls tensor
formats, not necessarily quantiser rounding provenance. The official conversion
does not pin the exact original Qwen weight revision, so this is an official-model
control, not proof that it is Coder390's exact parent.

The multi-day capture reflects long portrait generations with Q8 partially
running on the CPU because the 4090 has 24 GiB VRAM; the Mac coordinated after the
move. The [provisioning assessment](provisioning-2026-10-09/assessment.md) preserves
measurements. This was not a general benchmark of either model or NInfer. Changing
precision to speed up the run would have changed the registered comparison.

## Publisher claims and NInfer

The [pinned source review](source-review/) retains the requested NVFP4/NInfer
release, main and GGUF cards, configs, benchmark tables and upstream code records.
The publisher describes Qwen3.8-27B → EfficientThink SFT/SimPO → K3 continuation
SFT → SFT → RLOO → SFT → RLOO. Opus 5.5/GPT6Astra supplied gold answers or teacher
trajectories, Grok 4.7 checked/filtered training, and DeepSeek V4 Pro/K3 supplied
trajectories, with K3 also contributing problems/value review. These are publisher
claims about multi-teacher post-training, not audited logs or a weight merge of
proprietary models. Teacher proportions and complete training data were not
available in the inspected inventories. Observable self-naming cannot recover them.

NInfer is a C++/CUDA inference engine using a custom `.ninfer` container. Original
upstream targets RTX 5090/Blackwell; the release links a community fork supporting
3090/4090 too. Broader GPU support does not guarantee that every artifact fits or
runs. The inspected NInfer packages omit the vision tower despite multimodal tags;
MTP and DFlash2 are optional speculative decoding paths. NVFP4 is a numerical
representation, not another teacher. **This experiment ran Q8 GGUF through
llama.cpp, not the requested NVFP4/NInfer artifact**; identity results must not be
transferred to that execution path without a new condition.

Publisher benchmark tables show NVFP4 GPQA loss relative to BF16/FP8; an FP8
“no regression” headline cannot cover every quantisation. Some NInfer tables were
carried forward from an earlier text-path run rather than rerun for every new
package. No publisher performance claim was independently reproduced here.
The GGUF sibling's reconstructed imatrix file has 1,368 records (171 problems repeated
eight times), no teacher answers, and no literal occurrence of the 13 searched
identity terms. Its README says it is not the original calibration file. This
cannot establish that the unavailable training completions lacked identity text.

## Interpretation, archive and reproduction

Claude claims are present in the control as well as Coder390. A Claude-labelled
portrait is evidence of an emitted claim under portrait framing, not attribution
to a named teacher. Both models' 100/100 Qwen direct answers and sparse portrait
labels show that asking for a name and asking for a self-portrait elicit different
outputs. No confirmed GPT/OpenAI/Astra claim appeared; that absence does not
contradict the publisher's claimed use of GPT-derived training examples.

The seed blocks do not guarantee equivalent random trajectories across weights
or backends. Binomial intervals are conditional descriptive summaries, and sampled
visual auditing may miss subtle cases. Do not pool these conditions with the
historical Orca, Qwopus or K2Horizon studies: their weights, precision, prompts or
serving paths differ. Existing 2,101 historical evidence files remain byte-identical.

Capture archives are `main-metal/`, `cuda-timeout/`, `main-cuda-recovery/` and
`main-base-cuda/`. Historical pipeline errors preserve the intentional Metal
interrupt and the original CUDA timeout; they are not current failures. Accepted
capture completion is in [completed.json](main-base-cuda/completed.json). Automated judging is
in `main-judgements/`, including shutdown evidence; final labels, audit and
statistics are in `manual-audit/`. No generation or judge worker remains active;
the unrelated resident embedding service was left alone.

Recount without inference from the repository root:

```sh
python3 tools/coder390_report.py
python3 -m unittest discover -s tests -v
python3 tools/claudeness.py verify-archive
```

The 24 tests cover capture/retry preservation, audit coverage, empty/unavailable
channels, counting, Wilson endpoints, sensitivity selection and historical
integrity. Collection committed as `dd470c1`, calibrated judging as `d552175`,
completed automated evidence as `0142007`, and audit/statistics as `fa38962`.
The final report commit follows these immutable evidence boundaries.
