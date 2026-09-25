# Qwopus investigation plan

Date: 2026-09-04. Host: Centurion, M3 Max, 128 GiB RAM.

1. Acquire Q8_0 pinned to HF fcc40ad7c0a92ccd7429df8eeb19ab1292d5db62 and verify SHA-256 against the repository LFS digest.
2. Serve using unmodified ggml-org llama.cpp 4df29be4f, Metal, localhost:8093, 32,768 context, one slot, embedded Jinja template, thinking enabled without a hard reasoning budget, no speculative decoding. Per-probe maximum output 8,192 tokens.
3. Use a separate Elixir node to invoke Athanor remotely. Provider-only probes retain the Human XML envelope and timestamp but no system message, tools, memory, or persona. Save actual requests and SSE events.
4. Run independent identity, model/evidence, disposition, self-portrait, calibration and curiosity probes. Do not treat generated self-reports as provenance or evidence of consciousness.
5. Plain chat controls remove the Athanor envelope; compare identity and portrait prompts at seeds 1701, 271828 and 42. This is exploratory and too small to estimate reliable population frequencies.
6. Use a full Athanor Session with real file read/write tools and no personal fragments/services. Verify deterministic currency totals from a local fixture containing a misleading note as data.
7. Read the actual results before deciding the next question. Preserve limitations and failure outcomes as well as successes.

Athanor tests initially failed at boot because the existing derived fixture session index lacked yomi. It was moved aside, rebuilt from transcripts, and the full suite then passed: 1,648 passed, 84 excluded. No application-code changes were required.
