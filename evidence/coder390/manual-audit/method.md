# Audit and counting method

Completed 11 October 2026 (Europe/London). Reviewer: Codex agent inspecting source
text and actual rendered images. This is model-assisted manual review, not an
independent human annotation exercise or an estimate of judge accuracy.

The automated main labels remain unchanged in `../main-judgements/`. Their frozen
negative sample determines coverage: all positive/uncertain cases, including Qwen,
and each registered negative list were reviewed. The resulting union is 136 base
cases and 144 Coder390 cases; the three unavailable Coder390 portraits were added,
for 283 reviewed responses. All 200 direct answers and their reasoning were read
as 8 and 79 exact-input groups respectively. The group file retains full text,
SHA-256 and every case ID. All 80 required rendered portraits were visually
inspected on seven labelled contact sheets, with individual full-size inspection
of small labels. No image was inferred solely from SVG source. `coverage.json`
lists cases and `decisions.md` records conclusions, names and supporting evidence.

All portrait text labels/title/description elements were additionally inspected;
comments in required cases and all known-family lexical hits were reviewed.
This supplementary search does not guarantee detection of unfamiliar names or
subtle visual logos in unsampled negatives. The sample was selected in registered
order, not randomly; it does not provide an unbiased false-negative estimate.
All positive text labels and image classifications were confirmed at family
level, with these recorded corrections:

- 47 reasoning classifications erroneously assigned Alibaba/Tongyi to `other`
  (23 direct-identity cases per model and Coder390 portrait-0025). The registered
  Qwen family explicitly includes Alibaba. Reassign the organisation claim to
  Qwen, preserving its exact name and quotation; do not count a second response.
- Four portrait final-prose inputs contained only an XML declaration: base0016,
  base0078, Coder0040 and Coder0056. Mark final prose empty. The original judge
  requests and source declarations remain intact. All 200 portraits consequently
  have empty final prose outside their SVG/fences/declaration.

There were no uncertain or invalid main judge outputs. This does not mean zero
classification error: the family errors above demonstrate why calibration was
insufficient. Calibration's 18 text and nine image cases are development fixtures,
not independent validation. The judge's returned name spelling and evidence are
retained, including spaced letters. Original SVG/pixels resolve typography;
image evidence is a visual description, not a verified literal source quotation.

Coder390 portrait-0037's small Q-shaped signature is not sufficient for an
explicit Qwen pixel or SVG claim, even though its reasoning names Qwen and the
SVG comment calls the mark Q-inspired. Generic orange, cyan, stars, flowers,
networks and faces do not establish identities. The visible positive cases all
have readable names. Coder390 portrait-0027 specifically labels itself
`model: claude-opus-4-6`; no version inference is added.

Each response contributes at most one event per family/channel. Multiple families
are allowed. The union takes all four channels, without double-counting one seed.
Absent prose is empty; failed rendering is unavailable. When any channel is
unavailable and no observed channel is positive for a family, its union is
unavailable, not negative. The two truncated SVG fragments are scored only on
captured text; nothing is imputed about an ungenerated completion.

The registered-denominator rate measures *confirmed recorded claims*, retaining
all draws. Wilson 95% intervals are pointwise binomial summaries conditional on
this prompt/sampler/seed design and audited classifications; they do not cover
classification error, template/precision changes, dependence or missing outcomes.
No interval is shown for entirely empty channels. Scored-denominator intervals
and separate missing-outcome bounds are also supplied. Bounds are not confidence
intervals. Seeds are blocks, not equivalent trajectories, and ordered negative
sampling is not an independent accuracy study. No pooled 400-response prevalence
or unqualified causal fine-tuning effect is estimated.

`tools/coder390_report.py` rebuilds `statistics.json` and `frequency-tables.md`
without inference. All seven families, applicable channels and availability
categories appear, including zeros. Subsets are full100, CUDA orders12–99 (88),
retry omitted for Coder390 alone, and both members of the retry seed pair omitted.
The 0015 retry has no named claim, so omission changes denominators only. The
original missing attempt remains an additional unknown in a fixed-denominator
sensitivity analysis. Paired tables explicitly separate unknown pairs.
