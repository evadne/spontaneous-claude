# Archive scope and reproducibility

The archive covers every retained **generated investigation artefact** discovered during consolidation:

- Athanor disposition visualisations and text output;
- Athanor portrait prompts, serialised contexts, successful SVGs, and renders;
- the complete controlled direct-llama portrait matrix;
- direct identity probes and the cancelled raw-completion stream;
- dataset-query results, including complete matching records;
- the scripts used to run portrait, identity, raw-stream, and dataset probes;
- the report, chronology, manifest, contact sheet, archive inventory, and checksums.

The following dependencies and source inputs are deliberately referenced rather than copied:

- Model weights: `/Users/evadne/Projects/models/k2-horizon-mova-36b-a4b/K2-Horizon-36B-BF16.gguf` (74,924,627,296 bytes).
- Athanor model link: `/Users/evadne/Projects/athanor/priv/models/huggingface/IFM/K2-Horizon-MoVA-36B-A4B-GGUF/K2-Horizon-36B-BF16.gguf`.
- llama.cpp fork: `/Users/evadne/Projects/mbzuai-ifm/llama.cpp`, branch `model/K2Horizon`, commit `35999d101cf2233fc54f09c3c8d599da7303ce02`.
- Built server: `/Users/evadne/Projects/mbzuai-ifm/llama.cpp/build/bin/llama-server`.
- Athanor source and build products, which were not generated specifically as experiment outputs.

The duplicate N-body SVG and PNG under `/Volumes/Downloads/K2-Horizon-Disposition-Test` are represented by the retained copies under `collected/athanor-disposition`. Large downloaded model inputs and reproducible compiler outputs are excluded so that the evidence archive remains portable.

## Verification

`SHA256SUMS` covers every archived file except itself and archive packages. `ARCHIVE_MANIFEST.tsv` records relative path, byte size, modification time, and SHA-256 digest for the evidential files, excluding the archive bookkeeping files themselves. The compressed tar archive preserves project-relative paths beneath a single `k2-horizon-controlled/` root.
