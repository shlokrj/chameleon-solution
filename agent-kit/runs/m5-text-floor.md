# M5 final text-floor refinement

Date: 2026-10-21 America/Chicago. Parent 0f8cfe2. Owner: root. Change: `fix: preserve readable text floors when downscaling`.

## Cause and correction

The existing readable floor was capped at source font size times the canvas scale, so downscaling could erase the floor immediately. For the chosen layout's standalone text zone, try fitting again with the same floor and a cap at the source size (when downscaling). Keep the headline-relative 70% ceiling and 10px floor policy. Do not alter groups, images, layout selection or the candidate budget.

This is a bounded post-selection refinement, not a new candidate. It records source copy for eligible downscaled multi-text zones, reruns the existing 18-step fitter only for the chosen zone, and accepts changes only when no text shrinks, measured text fits, max_lines holds and rotated bounds stay in the assigned zone. A final quality check rolls back if loss, hierarchy inversion or overflow count increases. Candidate diagnostics remain pre-refinement scores; refined_text lists IDs enlarged by the accepted final pass. Returned design JSON has no internal metadata.

Two rejected intermediate implementations matter: changing the floor during candidate generation reduced a compact badge label below its existing regression threshold; moving refinement after selection avoided that. A 49-case size sweep then caught a hierarchy/score regression at 320x320; final quality rollback now preserves the original output there. Tests were retained rather than weakened.

## Validation and results

- 71 tests pass in the rebuilt linux/amd64 verification container with networking disabled. Four new tests cover the downscale floor, source-size cap, stable selection/no shrinking, and hierarchy relative to grouped labels.
- Both images build; all three production JSON/PNG pairs pass independent contract and direct-render pixel verification.
- 70 catalogue cases: zero contract and measured-overflow findings. Seven improve local loss; no measured regression. Inspected all seven changed before/after renders. Editorial 300x250 minimum copy grows 6 to 10px; Level 1 300x250 grows 8.333 to 10px; dense-labels 300x250 grows 4.667 to 6.667px; dense-labels 160x600 grows 9.333 to 10px. Other improvements enlarge body copy while grouped labels remain the minimum.
- Catalogue cases below 6px fall from five to four. The hardest Level 3 fine print remains small because fitting a larger floor would shrink other copy.
- Additional 49-case boundary sweep: seven local-loss improvements, no regression and no contract findings. These are exposed development variations, not holdouts.
- 42 regression/stress cases pass contract and input-immutability checks; repeated final-image runs compare complete designs, scores and decoded pixels exactly.
- [Per-case evidence, hashes and timing](m5-text-floor-evidence/summary.json).

Runtime checks use Colima/Rosetta linux/amd64 with --network none. Measure five sequential warm engine-only sweeps of all 70 catalogue cases after one warmup per revision; exclude rendering, startup and memory. Baseline engine extracted from 0f8cfe2 into an ignored artifact directory. No official score, fresh judge/holdout or native-hardware performance claim.

Commands: scripts/verify-container.sh; evaluation.catalogue; evaluation.parity and a repeat; the saved m5-compact-sweep.py for the 49 boundary cases; the saved m5-expand-measure.py for full-output comparisons and timing. Local evidence: artifacts/m5-floor-guarded*, artifacts/m5-floor-time-*-final.json, artifacts/m5-floor-contact.png, artifacts/m5-floor-container-final.log and artifacts/container-check.Ajeorm/output.

Median warm 70-case sweep: 0.5011s before and 0.5313s after (+6.0%, +0.432ms per case). These small local measurements do not establish performance on native benchmark hardware.

## Handoff

Accepted. Expected Fontconfig and missing holiday badge warnings remain. Four sub-6px catalogue cases, crowded logo/product allocation, anchoring and organizer/release questions remain open. Next, perform a bounded fresh review of accumulated M5 changes before extending layout heuristics. Root releases ownership after integration.
