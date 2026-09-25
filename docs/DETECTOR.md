# Claudeness detector and judge

“Claudeness” is the investigation's informal name for observable Claude/Anthropic
identity signals. These tools do not detect ancestry or measure a general persona.

## Three independent signals

1. **Image judge:** `tools/judge_portrait.py` sends only the rendered PNG and the
   fixed rubric to a local vision model. It asks about clear Claude/Anthropic
   identity, allows every portrait style, and rejects colour/generic-star inference.
2. **Reasoning judge:** `tools/judge_reasoning.py` sends captured reasoning text
   in a separate request. It distinguishes direct self-claims from negation,
   hypothetical examples, quotations and discussion of other models. It also
   records explicit Qwen identity. The original implementation submits the first
   30,000 characters; the runner records whether truncation occurred and preserves
   the complete source. Audit beyond that prefix where necessary.
3. **SVG text candidate detector:** `tools/visible_svg_text.py` extracts SVG text
   elements and matches Claude/Anthropic, including spaced lettering. Despite its
   historical function name, it does not compute CSS visibility, clipping,
   occlusion, opacity or text contrast. A literal hit is an audit candidate, not
   proof the pixels visibly contain the name. It also does not understand whether
   text is a denial, quotation or identity claim.

The two judge modules and text detector are byte-identical copies of the original
Orca methods. The CLI configures their endpoint/model before use; it does not
change their prompts. `extract_svg.py` preserves the original extraction and two
recorded repair behaviours (HTML named entities and malformed three-point lines).
Every original content string is retained; repairs affect only rendering derivatives.

The CLI requires no SSH synchroniser or original workstation paths. It separates
configuration by output directory and hashes raw inputs and judging implementation
for resume checks. This is additional run bookkeeping, not a change to historical
evidence or a versioned wire protocol.

## Counting and audit

The union of image flags, reasoning self-claims and SVG text hits selects candidates.
Count distinct seeds within one condition. Preserve uncertain cases separately.
Incomplete/unrenderable SVGs remain in the denominator and can still supply
reasoning evidence; unavailable visual evidence is not evidence of absence.
No portrait is rejected for choosing a logo, face, scene, character or abstract art.

Inspect all candidates and uncertain cases, check exact quotations against raw
reasoning, and inspect rendered pixels at adequate resolution. Record corrections
without overwriting original judge outputs. Also inspect a preselected sample of
negative cases. The historical audit schema and fixed negative sample are retained
in `evidence/orcasaq-2/farm/`; new runs need their own audit.

The archived batch has seven visually verified text-bearing portraits, six direct
reasoning self-claims and two overlapping seeds: eleven distinct positives. The
vision judge alone missed one small low-contrast text label, and misread part of
another label. Four-image/four-text calibration was a smoke test, not a measured
population error rate. A model judge's confidence is not a calibrated probability.

## What repeatability means here

The archive allows byte-level verification, recounting existing outputs, rerunning
the unchanged judges and executing the original seeded plan against local servers.
Weights, kernels, templates, sampling, reasoning settings, render libraries/fonts
and hardware remain part of the experimental configuration. Same seeds alone do
not guarantee byte-identical outputs or a matched cross-model comparison.
