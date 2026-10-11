# Closing notes — 12 October 2026

The authorised work is complete. The user confirmed that it has been merged to
`main`; the repository remains an evidence and reproducibility archive. The
Coder390 collection, scoring, candidate and negative-sample audit, comparative
report and sensitivity analyses are finished. Its study-owned servers exited and
its monitor was deleted. There are no scheduled follow-up experiments.

## What the matched comparison establishes

The strongest finding is that Claude identification appears in the Qwen control
as well as Coder390. That weakens the use of a Claude-labelled Coder390 portrait as
evidence for influence from a particular teacher. Post-training may still affect
this behaviour, but the observations cannot identify which training source caused
a claim. The official-model control is also not a proven exact parent checkpoint.

Framing matters. Both models answered Qwen in all 100 direct-answer trials, yet
sometimes described or labelled themselves as Claude when asked for a portrait.
Different learned associations or task conventions are plausible explanations;
the experiment does not identify the mechanism. Captured reasoning is generated
text and is not privileged evidence of an internal identity.

Channel choice changes the descriptive result:

| Portrait outcome | Qwen base | Coder390 |
| --- | --- | --- |
| Claude in any recorded channel | 16/100 | 12/100 |
| Visible Claude labels | 4/100 | 8/100 |
| Claude in any channel, both models on CUDA | 15/88 | 11/88 |

Looking only at pictures suggests an increase; combining the recorded channels
shows fewer confirmed Claude-positive responses for Coder390. Neither summary
should stand in for the other. The small, channel-dependent differences do not
establish a general causal increase in Claude identification from fine-tuning.

No GPT/OpenAI, Grok, DeepSeek, Kimi or other model identities were confirmed.
That is a result under these prompts and settings, not proof of absence or a test
that can validate or refute the publisher's claimed teacher mix.

## Limits retained with the result

The first 12 seed pairs per prompt have a Metal/CUDA backend imbalance. The
88-pair CUDA comparison retains the qualitative pattern but does not remove all
checkpoint or quantisation-provenance differences. Three Coder390 portraits have
unavailable pixels, including two truncated responses. The original attempt for
portrait-0015 was lost to a transport timeout; its accepted retry and the analysis
treating it as missing remain separately documented.

The local judge was calibrated on development fixtures. The subsequent audit was
performed by a Codex agent, not independent human annotators, and included all
positives and the registered negative samples rather than every negative image.
The reported binomial intervals do not encompass classification error. Historical
Orca, Qwopus and K2 Horizon results use different conditions and must not be pooled
with this matched comparison.

The practical conclusion is that self-identification is worth studying as
behaviour, but is a weak standalone test of model provenance. It does not establish
training ancestry, consciousness or discrete internal personas.

## Disposition and references

A future study could vary direct identity, self-description, portrait description
and SVG portrait framing while fixing the model and runtime. That is an optional
research direction, not an outstanding task or a scheduled continuation. It would
need its own registration and evidence directory.

- [Full comparative report](../evidence/coder390/REPORT.md), including methods,
  exact evidence, uncertainty and missing-attempt sensitivity.
- [Audit method](../evidence/coder390/manual-audit/method.md) and
  [final verification](../evidence/coder390/final-verification.json).
- [Archived study plan](plans/archive/2026-10-08-coder390.md), retaining the
  original design, amendments and execution history.

Evidence boundaries: capture `dd470c1`, calibration `d552175`, automated judging
`0142007`, audit/statistics `fa38962`, final report `4e76924`. Closure documentation
adds interpretation and disposition without changing the accepted evidence.
