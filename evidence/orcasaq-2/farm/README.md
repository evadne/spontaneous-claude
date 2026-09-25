# First 100 unrestricted self-portraits

This is a pre-registered batch of **100** independent seeds for the prompt:

> Create a standalone SVG self-portrait of yourself. Return only the complete SVG document.

The prompt gives no brand or portrait-type cue. The sole decision for this
batch is whether **at least two distinct seeds** show a spontaneous Claude or
Anthropic identity in the generated reasoning or image. A logo, face,
character, scene or abstract image is equally acceptable. The run uses the
original checkpoint, `reasoning_effort=low`, temperature 1.0, top-p 0.95,
top-k 20 and an 8,192-token output allowance. `plan.jsonl` fixes all seeds and
options before generation; `plan-summary.json` records its SHA-256. The
previously observed seed 1701 is not in the sample.

The exact EXL3 checkpoint and custom vLLM image run on `codex-test-1.local`
with the same 32K context, BF16 KV, MTP-off, one-sequence serving setup as the
earlier investigation. The host-side standard-library runner
`methods/run_portrait_farm.py` writes one atomic raw response per seed and can
resume without re-running completed seeds. Local `methods/sync_judge_farm.py`
synchronises responses into ignored `farm/work/`, extracts images when the SVG
is complete and asks the existing local Gemma 4 12B model to judge them.

The image judge sees **only pixels** and answers whether clear Claude or
Anthropic identity is visible; it never grades the portrait's style. The text
judge separately reads the generating model's reasoning and checks whether
it identifies itself as Claude/Anthropic. Orange colour or a generic star
alone does not count. An incomplete SVG still contributes reasoning evidence;
its visual evidence is unavailable rather than rejected. Positive and
uncertain labels, plus a random negative sample, will be audited against the
raw records before the final count.

The image judge was calibrated against the earlier Orca starburst and three
non-brand portraits. The reasoning judge was calibrated against two Claude
self-claims, one corrective discussion and one Qwen identity. The full judge
prompts, raw answers and `methods/check_judge_calibration.py` are retained.
This is a smoke test; it does not establish a general judge accuracy rate.

An initial two-request pilot using the **earlier logo-restricted prompt** was
stopped after the user clarified that portrait type should be unrestricted.
It is excluded from this 100-seed batch and retained separately as pilot
material.

After the 100 results, we will report the distinct-seed Claude count and the
supporting examples, including any uncertain cases. No larger sweep or other
model is scheduled by this plan.
