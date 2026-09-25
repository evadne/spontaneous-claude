# Consolidation verification — 25 September 2026

- **2,101 original files**, 68,640,729 bytes, copied and SHA-256 checked against
  source. The manifest covers originally ignored raw farm outputs as well as
  tracked reports/scripts. Originals were not edited.
- Orca's original Git bundle passes `git bundle verify` and contains its full
  retained history, including the final farm commit.
- All 100 farm raw responses and 100 classifications are present. Offline recount:
  7 SVG text candidates, 6 image flags, 6 reasoning self-claims, 11 distinct flagged
  seeds. The ID set exactly matches the final report and eleven positive manual
  audit records. The plan hash matches the recorded pre-registration.
- All 300 local gallery links resolve in the new location.
- **Seven tests passed** on Python 3.9.6. They verify archive hashes, unchanged
  detector/judge code, final-count/audit agreement, spaced-text matching and
  metadata exclusion, incomplete-SVG/repair handling, duplicate-seed rejection,
  and a local HTTP generation/judging/resume round trip. The synthetic HTTP test
  verifies image requests contain no generator reasoning and reasoning requests
  contain no image. Configuration changes refuse to reuse a run directory.

## Live local judge smoke test

The CLI was exercised against the existing local `gemma-4-12B-it-Q4_0` endpoint
on port 8090, using three retained raw responses, not new generated portraits:

| ID | Image flag | Reasoning self-claim | SVG text candidate |
| --- | --- | --- | --- |
| `unrestricted-low-0002` | No | No | No |
| `unrestricted-low-0018` | No | Yes | Yes |
| `unrestricted-low-0010` | Yes | No | Yes |

This reproduced two known limitations: the image judge missed the small label
in 0018 and described 0010's `entity://claude` as `anthropic://claude`. Its positive
classification is usable as a flag, but its quoted text/branding explanation
needs checking. The raw SVG text is preserved and the historical manual audit
already records the correct interpretation. These checks do not estimate judge
accuracy or prove byte-identical inference.

The renderer was librsvg 2.62.3, Cairo 1.18.4, Pango 1.58.2, HarfBuzz 14.4.0,
fontconfig 2.18.3. The exact runner manifests, generated rendering derivatives,
judge answers and logs are in `validation/`. Their implementation hashes and
source-response hashes are recorded. The model alias was verified available;
this consolidation did not independently rehash the judge weights or establish
that every serving binary/weight matches the earlier investigation.

No new 100-seed run was performed. No existing model service was reconfigured,
restarted or stopped. No Athanor application changes or remote Git pushes were
made. All empirical claims above are limited to the archived batch and these
three judge smoke cases.
