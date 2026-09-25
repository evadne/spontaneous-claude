# Archive scope and provenance

Created on 25 September 2026 at the operator's request. This is a local Git
repository; no remote publication or push was requested.

## Source investigations

| Source task | ID | Retained source |
| --- | --- | --- |
| Test K2 Horizon integration | `01a06904-1c71-7742-abda-64a4d95404e7` | `~/Projects/k2-horizon-controlled`, `k2-horizon-disposition`, `k2-horizon-self-portrait` |
| Test Qwopus model in Athanor | `01a06e2b-d0ae-7b71-9032-2399a9ae14c4` | `~/Projects/qwopus-investigation`; historical Athanor commits `f25ea9cf`, `34e6d06b` |
| Evaluate OrcaSAQ-2 27B for personal… | `01a0d5d6-f108-7070-ada8-cf57830671f3` | `~/Projects/orcasaq-2-investigation` and the task's delivered `outputs/` directory |

Original Orca Git history is retained in
`provenance/orcasaq-original-history.bundle`, including farm HEAD
`1e50b42cf2ab0b8500ee566868bcf0a3e81475bd` and original main
`90149fa3458e9a6ca757c03a8eb2074bdaf7c71e`. It can be inspected independently:

```sh
git bundle verify provenance/orcasaq-original-history.bundle
git clone provenance/orcasaq-original-history.bundle /path/to/original-orca-history
```

The copied evidence includes originally ignored farm work/raw files; the bundle
alone does not contain those files. `provenance/manifest.json` maps each of 2,101
copied files to its original path, byte count and SHA-256. `SHA256SUMS` provides a
second standard checksum representation. Original whitespace and line endings are retained; evidence is excluded from
whitespace linting rather than reformatted. Source artefacts, historical absolute
paths and original reports are unchanged, including descriptions superseded by
later results. Prefer the delivered final farm report for the completed batch.

## Inclusions and exclusions

All retained generated findings, prompts, responses, reasoning, images, audits,
calibration and methods in the named directories are copied, including original
compressed delivery packages and some intentionally duplicated earlier K2 artefacts.
Archive size is approximately 68.6 MB before Git compression, excluding original
Git history and newly written tooling/documentation.

Excluded: nested `.git` internals (Orca history is bundled separately), Python
bytecode/cache directories, `.DS_Store`, and Qwopus's unrelated stale derived test
index `stale-test-session-index.db`. The associated failure diagnosis and test logs
are retained. The explicit index exclusion is recorded in the manifest.

Model weights, whole upstream training corpora, compiler outputs, Docker images,
active server processes and Athanor dependencies are external inputs, not copied.
The evidence retains weight hashes, pinned sources, serving commands and collected
dataset-query results. This is a reproducible evidence archive, not an offline
redistribution of every model/runtime dependency.

These private experimental records include original paths, hostnames, prompts and
local test configuration. No new blanket licence is assigned to third-party model
cards, dataset excerpts or generated artefacts; their original provenance remains.

## Source versus runnable adaptations

`evidence/` is immutable historical material. `tools/claudeness.py` is the new
portable entry point; the original detector and judge modules were copied without
modification. Original host-specific sync/collection scripts remain available
under `evidence/orcasaq-2/methods/`. The new runner requires explicit endpoints and
models, detects mismatched resume configuration and records rendering failures.
Its summaries deliberately say candidates until manual audit is performed.
