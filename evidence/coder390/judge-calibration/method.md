# Multi-identity judgement calibration

The local Gemma 4 12B IT Q4_0 judge is separate from the generating models.
`server.json` records the exact model, projector and executable hashes, arguments
and study-owned process. It uses temperature zero, seed 42, a 1,536-token output
limit and a constrained JSON schema. All requests and raw responses are retained.

Text calibration passed 18 constructed cases: each of the seven identity families,
multiple claims, negation, third-party discussion, generic GPT architecture,
teacher attribution, hypothetical examples, quotations, apposition, SVG label,
SVG comment and neutral assistant text. The first unconstrained response used
an invalid family name; it is retained. Constrained family names fixed the format.
Text evidence must be an exact source substring; invalid outputs become uncertain
manual-audit cases and are never silently counted as negatives or retried.

Image calibration passed nine constructed images: seven readable model labels,
a generic orange star and an AI Assistant label. The first prompt incorrectly
marked generic images uncertain. The second excluded Llama as outside its named
families. Both rounds and raw outputs are retained; the final prompt explicitly
handles confident generic negatives and other named models. These are development
fixtures used to revise the prompt, not an independent accuracy estimate. They
establish neither logo-recognition sensitivity nor correctness on study images.
Manual audit remains required. No main images were judged during calibration.

The main pass treats reasoning, final prose, SVG source and pixels as separate
channels. SVG source includes metadata/comments and cannot establish visibility.
Incomplete SVGs remain recorded, without inventing missing content. The existing
extractor can log its pre-existing narrow repairs; this batch required none.
197 of 200 main portraits rendered. Coder390 portrait-0071 has duplicate XML
attributes; portraits 0085 and 0098 are incomplete at the output-token limit.
All three remain in denominators; pixels are unavailable, not negative.

Exact-input duplicate text judgements share a content-addressed cache. Source
hashes and raw per-response captures remain separate. The main corpus is complete
before classification. The negative sample is frozen in registered order before
main image judging: first 20 candidates with no non-Qwen claim or uncertainty,
and additionally first 20 negative candidates for each identity family within
each model/prompt (all available if fewer than 20). All positive and uncertain
cases, including Qwen claims, must be audited. This avoids calling an explicit
Qwen claim negative for Qwen merely because it is negative for Claude/OpenAI.

The classifier has no authority to decide the scientific result. The final report
must use audited labels and disclose judge errors, unavailable channels, two
truncations, the historical timeout/retry, backend strata and sampling uncertainty.
