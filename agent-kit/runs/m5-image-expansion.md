# M5 use spare image-zone space

Date: 2026-10-18 America/Chicago. Parent 56e30ba. Owner: root. Change: `feat: enlarge standalone images within spare zone space`.

## Approach

After choosing a layout, grow standalone unrotated contain images into unused space in their assigned image zone. Consider smaller visible images first, grow each at most 50%, and use at most 20 bisection iterations. Shift only enough to keep the full element box on canvas and visible pixels inside the assigned zone. Retain an existing separation direction and the configured gap from each neighboring image. No neighboring image is shrunk or pushed. Multi-element groups, cover images and rotated images are excluded; near-ratio layouts keep their existing behavior. No asset names or semantic logo labels drive the decision.

Layout construction records ephemeral zone references for candidate selection; only the chosen design receives expansion. No internal data appears in returned JSON and no extra layout candidate/render is needed. The per-image checks are quadratic in the number of image units overall; the six-candidate cap remains unchanged.

Rejected intermediate approaches: center-only growth improved two story layouts but could not use room near canvas edges. Growth during candidate generation changed the regression guard's baseline and made an event logo slightly smaller despite enlarging individual candidates. Moving the pass after selection prevents that interaction. Four tests cover spare-space growth, gaps/proportions, exclusions, transparent margins at canvas edges and selection stability.

## Validation

- Rebuilt production/verification images; 66 tests pass offline. All three production JSON/PNG pairs pass independent contract and direct-render pixel validation.
- 70 catalogue cases have zero contract/overflow findings. All reported selections, min/max text and quality metrics exactly match 56e30ba.
- Fifteen catalogue PNGs change; inspected all fifteen before/after pairs in a contact sheet. Fourteen are logo-only changes in Level 1/event variants; the catalogue story changes its two product images. See the per-case image evidence for exact counts and dimensions rather than treating every changed image as a logo.
- 42 regression/stress cases pass structural/input-immutability checks. A repeat in the rebuilt image exactly matches full tasks, designs, scores and decoded pixels.
- Event leaderboard logo visible width grows from 61.22 to 85.10px; Level 1 leaderboard grows from 71.06 to 101.06px. All 70 output comparisons confirm no image shrinks and all non-image fields remain exactly unchanged.
- No fresh holdout, independent judge, official scorer or new resource-memory measurement. Expected Fontconfig and missing badge warnings remain visible.

## Limitations

This improves images only where their existing zone has spare room. It does not solve the crowded Level 2 leaderboard logo, nor the five catalogue cases with text below 6px. The 50% cap is a conservative local policy, not an organizer requirement. Typography/quality proxy scores stay unchanged, so the benefit is supported by image dimensions and inspected renders rather than a claimed score gain. Logo/product hierarchy is not inferred; only standalone images qualify.

Commands: scripts/verify-container.sh; evaluation.catalogue against artifacts/m5-flow-catalogue-final/report.json; evaluation.parity and a repeat against artifacts/m5-expand-selected-parity/report.json. Measurement script and raw five-sweep timings are in [evidence](m5-image-expansion-evidence/summary.json). One full warmup precedes five engine-only sweeps of all 70 catalogue tasks, run sequentially in linux/amd64 containers on Colima/Rosetta. Median 70-case sweep: 0.4863s before, 0.4929s after (about 1.4% slower, 0.095ms additional per case). These are emulated local warm timings, excluding rendering/startup; no native-hardware claim.

Local artifacts: artifacts/m5-expand-selected, artifacts/m5-expand-selected-parity, artifacts/m5-expand-repeat, artifacts/m5-expand-contact.png; artifacts/m5-expand-container.log and artifacts/container-check.TDvJ5Z/output. Root releases its claim after integration. Next: dense small-format copy and coupled logo/product allocation; collision-aware anchoring remains deferred.
