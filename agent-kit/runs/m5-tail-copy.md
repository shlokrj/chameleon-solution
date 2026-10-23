# M5 final text-box spare-height repair

2026-10-23; baseline `6a5433e`. The compact Level 3 legal text was 3.333px despite unused space beneath its box. The existing all-copy floor proposal would shrink the headline from 11.111px to 10.460px, so rejecting that proposal was correct.

## Repair

After existing refinements, allow the final unrotated text box in a recorded copy region to use the unused height below it. Keep its position/width and every peer unchanged. Fit at most 12px or its source size, and cap against text with substantially larger source typography to preserve hierarchy. Reject no-growth, worse loss, added hierarchy inversion or overflow. Rotated boxes are deliberately skipped. The runtime candidate budget stays six; the existing bounded font search is reused. Diagnostics identify accepted changes as `refined_tail_text`; candidate scores still precede final refinement.

The compact Level 3 legal text grows 3.333→6.111px, preserving headline and all other elements. Its minimum text size is now 5.159px because badge labels remain small. This improves seven of 70 catalogue layouts across six source families, with no worse local loss, new contract findings or measured overflow. Full paired JSON comparison confirms only text height/font size changes, with no font decreases and unchanged non-text elements. Three catalogue layouts still contain sub-6px text; this is not an M5 completion or universal readability claim.

## Verification

- 75 offline Linux/amd64 tests pass, including compact peer-preservation and rotation-skip regressions.
- Production rebuild and all three JSON/PNG delivery checks pass with networking disabled.
- 70 catalogue cases pass; all seven changed before/after render pairs inspected.
- 42 parity cases repeat exactly with zero findings.
- Six saved challenger and three retired holdout cases pass. Only `01-alpha-rotated` and `04-final-floor-styled` change; both paired renders inspected. Styled/multiline copy grows without changing other elements. These are exposed regressions, not a fresh independent holdout or judge approval.
- One warmup plus five 70-case engine sweeps per revision: median 0.5722s before, 0.5638s after. Samples are noisy and this does not establish a speedup; it shows no observed large cost in this small serial run. Rendering is excluded. The baseline slowest sweep was 0.9407s. Both used the same offline verification image, with baseline engine extracted from Git and mounted read-only for the baseline run.

[Raw timing/count summary](m5-tail-copy-evidence/summary.json). Local artifacts: `artifacts/m5-tail-*`, including catalogue renders, comparison sheets, verification logs and paired full JSON. Production engine changes are confined to `engine/resize.py`; no sample-specific branching, asset changes or runtime dependencies were introduced.

## Reproduce and handoff

Run `scripts/verify-container.sh`, then the catalogue, parity/repeat and saved M5 fixture commands documented in the prior [group-refit record](m5-group-refit.md) with new output directories. Compare baseline revision `6a5433e` on the same Linux image. Timing uses all `evaluation.catalogue.sources()` × `FORMATS`, one warmup then five sweeps of `resize`.

M4 remains complete. Next M5 work should address remaining small grouped labels/logos through a feasible general improvement or perform a bounded final review with documented quality limits. Do not reopen rejected blind candidate-slot tuning. The initial local inspection script accidentally shadowed Python's `inspect` module; it was renamed and rerun successfully before evidence collection.
