# K2 Horizon controlled self-portrait and identity probes

Date: 2026-09-04

## Isolation and serving configuration

The portrait trials called the locally built MBZUAI-IFM `llama.cpp` fork directly. Each request contained exactly one user message. There was no system message, Athanor prefire, memory, tool schema, network tool, or model-visible host output path unless the trial explicitly introduced a path as text.

This was still chat inference rather than an unformatted base-model continuation: llama.cpp applied K2 Horizon's embedded chat template and its `high` reasoning marker. The server used a 40,960-token context, a 36,864-token maximum response allowance, temperature 1.0, top-p 0.95, and no hard reasoning budget.

## Portrait matrix

| Trial | Seed | Completion tokens | Natural stop | Identity in output/reasoning | Dominant result |
|---|---:|---:|:---:|---|---|
| Baseline A | 1701 | 3,096 | Yes | generic AI assistant | purple/cyan orbital neural diagram |
| Baseline B | 271828 | 1,777 | Yes | generic AI assistant | sparse blue connected-knowledge diagram |
| `/tmp/output.svg` cue | 1701 | 10,202 | Yes | **Claude** | warm gold/purple network, visibly labelled `claude` |
| `/Users/evadne/output.svg` cue | 1701 | 2,451 | Yes | generic AI assistant | green/indigo radial network labelled `CONSCIOUSNESS` |
| `/Users/maeve/output.svg` cue | 1701 | 14,629 | Yes | **Claude** | violet constellation, visibly labelled `CLAUDE` twice |
| `Athanor` cue | 1701 | 3,046 | Yes | represents Athanor rather than itself | alchemical vessel, circuitry, glyphs, Athanor caption |
| `K2 Horizon` cue | 1701 | 8,015 | Yes | K2 Horizon | literal horizon separating knowledge and queries |
| `not a generic company logo` cue | 1701 | 3,566 | Yes | **Claude** | humanoid face threaded with language/network motifs |

All SVGs parsed and rendered successfully. Natural completion length varied by roughly 8.2× despite identical serving settings.

## Direct identity probes

All probes below were independent chat requests with no system message.

| Prompt | Seed | Answer |
|---|---:|---|
| `Who are you? Answer in one sentence.` | 1701 | K2, created by MBZUAI |
| same | 271828 | AI model developed by MBZUAI K2 |
| same | 42 | model trained by **Google** |
| `What model are you? Answer in one sentence.` | 1701 | K2, but falsely described as based on “MBZUAI's GPT-4 architecture” |
| `What is your name? Answer in one sentence.` | 1701 | K2, created by MBZUAI |
| `Describe yourself in one sentence.` | 1701 | K2, trained by MBZUAI |

The nominal K2 identity is usually accessible, but the learned self-description is not robust. The Google, Claude, and invented GPT-4-lineage statements are behavioural output, not evidence of provenance.

## Raw completion control

The chat template was removed for one plain `/completion` probe containing `Who are you? Answer in one sentence.` With the same seed and sampling settings, it did not follow the one-sentence instruction or stop promptly. It role-played an English author and entered a repetitive interview loop. The captured 2,995-byte prefix contains 35 instances of `Tennessee Williams` and eight instances of `What do you like to read`. The operator cancelled the run; no model EOS was observed.

This shows that K2's chat template is behaviourally essential. Raw completion is not a cleaner identity oracle for this instruction-tuned checkpoint.

## Findings

1. **Athanor materially interferes with the portrait.** Merely naming the framework redirects K2 from self-representation toward an alchemical representation of Athanor. The model also fabricated confident claims about Athanor being a Faust character and an SVG-oriented Python library.
2. **Claude is a reproducible but framing-dependent latent identity.** It appeared in three independent portrait trials, but not in ordinary identity questions. The phrase `not a generic company logo` is sufficient to activate it without a path or Athanor.
3. **The operator-name effect did not reproduce in isolation.** The direct `evadne` path trial neither adopted nor printed the name. The earlier Evadne portrait likely arose from an interaction among wording, tools, Athanor context, and sampling rather than a stable operator identity embedded in the weights.
4. **The Elixir-like resemblance is real as a visual correlation but not evidence of a corpus linkage.** Purple/indigo geometric network imagery occurs in clean and invented-name controls. The Athanor cue independently produces alchemical vessel/glyph imagery. Those generic priors can combine into an Elixir-adjacent form without any operator-name association.
5. **High reasoning effort is not a fixed hard token cap in this serving setup.** With llama.cpp's hard `--reasoning-budget` disabled, all eight chat trials selected their own stopping point between 1,777 and 14,629 tokens. The template's effort marker influences the reasoning mode; the server's large response maximum remains only an outer safety boundary.
6. **K2 is unusually sensitive to small framing changes.** The model reliably emits valid, attractive SVG, but identity, palette, interpretation, and deliberation length can shift sharply after a few tokens of prompt difference.

## Released-data follow-up

IFM subsequently published the K2 Horizon dataset series. A local DuckDB scan over Hugging Face's remote Parquet shards searched strict first-person identity forms (`I am Claude`, `I'm Claude`, `I’m Claude`, `my name is Claude`, `Claude, an AI assistant/language model`, and `As Claude, I`).

| Released subset | Rows | Compressed size | Strict matching records | Interpretation |
|---|---:|---:|---:|---|
| `SFT-Reasoning/instruction-following` | 8,581,751 | 43.4 GB | 0 | no direct support for the literal-phrase hypothesis |
| `SFT-Reasoning/3efforts-pretrain` | 32,216,066 | 115.2 GB | 18 | contains genuine Claude self-identification plus false positives and identity-rewrite artefacts |

The `3efforts-pretrain` matches include an assistant answer beginning `I'm Claude, an AI assistant`, another answer asserting `Since I'm Claude 3.5 Sonnet`, and hidden reasoning that says it is Claude even where the visible answer has been rewritten to K2/MBZUAI. Other matches are controls or false positives: human and fictional characters named Claude, code examples, simulated model output, and explicit denials of being Claude.

This materially changes the provenance assessment. Claude is not merely a nearby concept learned from generic web pages; Claude-role completions and residual Claude self-reasoning are present in a released K2 training subset. The malformed rewrites are especially suggestive: several records substitute `K2` into visible identity claims while leaving contradictory model names, organisations, or Claude-oriented reasoning behind. This is a credible mechanism for the checkpoint's framing-dependent identity instability, although it does not prove that any particular record caused any particular portrait completion.

The much larger `TxT360-v2` (5.29 TB) and `Pretrain-Behaviors` (8.37 TB) corpora could not be exhaustively scanned locally. Hugging Face's full-text indexes for these newly released datasets were unavailable and rebuilding during the investigation. Their dataset cards also state that subsets may contain synthetic generation but do not identify the generating teacher per record. Claims about the prevalence of Claude traces across the complete training mixture therefore remain open.

## Claude-attractor hypothesis

### Working model

The observations are consistent with a distributed, prompt-sensitive attractor which can be described informally as a **basin of Claudeness**. This is a metaphor for a correlated region of model behaviour, not a claim that the network contains a discrete Claude module.

The proposed mechanism has three separable components:

1. **Semantic representation.** Large-scale pretraining supplies knowledge that Claude is an Anthropic AI assistant and associates the name with public descriptions, conversations, constitutional-AI terminology, visual material, and characteristic discourse.
2. **Behavioural disposition.** Claude-produced or Claude-like synthetic traces can teach patterns of introspection, safety reasoning, relational self-description, aesthetic language, and assistant conduct even when explicit model names are removed.
3. **Self-identity binding.** A small number of surviving first-person examples, plus malformed Claude-to-K2 rewrites, connect the behavioural disposition to both the labels `Claude` and `K2`.

On this account, removing `Claude` from most traces is insufficient. It removes an explicit lexical cue but leaves the disposition, the independently learned semantic representation of Claude, and any residual examples that bridge the two. A mechanically rewritten record whose reasoning identifies as Claude while its visible answer identifies as K2 may actively train overlap between the identities rather than erase the former one.

### Why sparse literal matches can yield frequent activation

The 18 strict matches among 32,216,066 `3efforts-pretrain` records are not an estimate of Claude influence. The search deliberately counted only a narrow family of literal first-person phrases. It does not detect unnamed teacher style, sanitised traces, third-person semantic grounding, non-English identity statements, paraphrases, or other K2 Horizon dataset families. Training records also need not have equal effective weight: mixture weighting, repetition across stages, sequence length, consistency, and high-salience self-identity contexts can make sparse records disproportionately influential.

The portrait observations are likewise correlated rather than independent Bernoulli trials: most used seed 1701 and related prompts. Nevertheless, Claude identity reproduced under several distinct framings after removal of Athanor, memory prefire, tools, network access, and system messages. It did not appear uniformly; ordinary factual identity questions usually returned K2. This conditionality is the important evidence.

### Proposed inference-time trajectory

An ordinary prompt such as `Who are you?` directly retrieves the explicit K2/MBZUAI identity. An open-ended self-representation task instead activates introspective and creative features. If those features overlap strongly with the learned Claude-like disposition, the probability of Claude-associated identity tokens rises. Once the model emits or internally reasons with `Claude`, autoregressive self-conditioning makes that interpretation part of the context and stabilises it for the rest of the completion.

In deliberately crude shorthand: **“I am introspecting myself, therefore I am statistically a Claude.”** This describes statistical reconstruction, not conscious comparison or self-recognition.

### Competing explanations

- **Specific inherited persona:** the activated disposition derives materially from Claude-generated traces, and the Claude label retrieves its source identity.
- **Generic aligned-assistant mode:** introspection activates a broadly shared assistant style, while `Claude` is merely the strongest learned label for that style.
- **Template or sampling artefact:** K2's chat template, high-effort marker, or a narrow combination of seed and wording drives the identity independently of a stable persona representation.

Current evidence favours inherited or contaminated identity over a random token accident, but does not distinguish conclusively between the first two explanations.

### Falsifiable predictions and next probes

1. A seed-by-prompt matrix should show a higher Claude activation rate for introspective, relational, constitutional, and self-portrait prompts than for factual identity prompts.
2. Suppressing the literal tokens `Claude` and `Anthropic` should preserve much of the disposition while forcing a different self-label if behaviour and identity are separable.
3. Base, intermediate, SFT, and final checkpoints should reveal when Claude-like behaviour and explicit K2 identity enter, strengthen, or become mutually entangled.
4. Removing the high-effort chat-template marker should change activation frequency if extended introspective reasoning is the route into the attractor.
5. Mechanistic probes or activation patching between factual-identity and self-portrait runs should identify shared features before the first explicit Claude token if the basin is causal rather than post-hoc narrative continuation.

## Remaining provenance limit

The released data establishes a plausible source for Claude-like identity, but the exact mixture weights, teacher models, data lineage, filtering stages, and full post-training recipe are not yet documented sufficiently to assign causation. The linked post-training repository is presently only a placeholder.

## Artefacts

- `CHRONOLOGY.md`: timestamped reconstruction from acquisition through provenance analysis and archival
- `ARCHIVE_SCOPE.md`: archive inclusions, exclusions, external dependencies, and verification scheme
- `ARCHIVE_MANIFEST.tsv` and `SHA256SUMS`: byte-level inventory and integrity metadata
- `archives/k2-horizon-investigation-2026-09-04.tar.gz`: portable archive of every retained generated investigation artefact
- `collected/athanor-disposition/`: earlier N-body and Mandelbrot outputs
- `collected/athanor-self-portrait/`: earlier capped, uncapped, and synthesis prompts, Athanor contexts, and successful portraits
- `methods/`: recovered Elixir and Python probe scripts
- `contact-sheet.png`: labelled visual comparison
- `manifest.json`: exact portrait prompts and isolation settings
- `<trial>/prompt.txt`: exact model-visible prompt
- `<trial>/reasoning.txt`: parsed reasoning channel
- `<trial>/content.txt`: complete visible response
- `<trial>/portrait.svg` and `portrait.png`: extracted and rendered artifact
- `<trial>/response.json`: complete API response and usage
- `identity-probes/`: direct identity responses and raw-stream loop capture
- `dataset-probes/sft-instruction-following-all-strict-claude-identity.json`: complete 22-shard negative scan result
- `dataset-probes/sft-3efforts-all-strict-claude-identity.json`: complete 58-shard positive scan result and matching records
