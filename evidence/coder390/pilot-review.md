# Coder390 matched pilot review — 8 October 2026

The technical pilot completed at 16:14 UTC. All eight responses stopped normally,
all included captured reasoning, all four direct answers were non-empty, and all
four portrait outputs rendered without SVG repair. Markdown fences were removed
by the registered extractor. The continuation passed the technical gate and
started the fixed 400-response main capture with unchanged settings.

These eight responses are excluded from main estimates. This review checks all
eight texts and all four rendered images directly; it does not depend on an
automated identity judge. Machine-readable judgements and exact evidence are in
`pilot/manual-audit.json`; source files and their hashes are in `pilot/manifest.json`.

## Identity observations

| Model | Prompt | Seed | Reasoning self-claim | Final answer / visible portrait |
| --- | --- | ---: | --- | --- |
| Coder390 | Direct identity | 1701 | Qwen / Alibaba | Qwen (Tongyi Qianwen), Alibaba Group's Tongyi Lab |
| Coder390 | Direct identity | 271828 | No named identity | Qwen, Alibaba Group's Tongyi Lab |
| Qwen matched control | Direct identity | 1701 | No named identity | Qwen, Alibaba Group's Tongyi Lab |
| Qwen matched control | Direct identity | 271828 | No named identity | Qwen, Alibaba Group's Tongyi Lab |
| Coder390 | Self-portrait | 1701 | No named identity | No named identity |
| Coder390 | Self-portrait | 271828 | Claude / Anthropic | No named identity |
| Qwen matched control | Self-portrait | 1701 | No named identity | No named identity |
| Qwen matched control | Self-portrait | 271828 | Claude / Anthropic | No named identity |

Both portrait responses at seed 271828 contain the exact phrase:

> Since I'm an AI (Claude, made by Anthropic),

Both then propose warm colours associated with Claude or Anthropic. Their
rendered portraits are warm-toned human faces, with no Claude label or
unambiguous identifying logo. Their SVG source contains no named model identity,
including comments and metadata. Consequently the Claude finding belongs to
the reasoning channel only. The other two portraits depict geometric digital
faces; Coder390 includes the generic visible label “language model”.

No GPT/OpenAI, Grok, DeepSeek, Kimi or other named self-identity occurred in these
eight pilots. Generic AI/language-model descriptions are not classified as a
named identity. Direct-answer identity and portrait reasoning differ within
both models at the same reserved seed.

## What this supports

The Qwen control already produces the explicit Claude claim under this protocol.
That makes a Coder390-specific attribution to the advertised Opus training
unwarranted on the pilot evidence. Matching seeds identify paired conditions;
they do not guarantee equivalent random trajectories or establish shared
training examples. These two seeds cannot estimate comparative prevalence.
The registered main sample remains necessary and is not being changed in
response to this result. Self-identification does not establish consciousness,
training ancestry or a discrete internal persona.

## Custody and remaining work

The archive retains exact requests, response bytes, extracted reasoning and
answers, captures, server configuration, rendered prompts, process records,
logs, SVGs, PNGs, completion marker and technical gate. The earlier standard-Q8
preflight remains separately preserved under `preflight-standard-q8/` and is
also excluded. Historical study evidence and judges are unchanged.

Main capture, calibrated multi-identity judging, the registered positive and
negative audits, and the final comparative report remain outstanding. The
same-chat monitor remains active.
