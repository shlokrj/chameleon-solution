# M5 compact-layout allocation

Date: 2026-10-20 America/Chicago. Parent bfac292. Owner: root. Change: `feat: allocate more group space on compact canvases`.

## Decision

For canvases with aspect ratio from 1 inclusive to 2 exclusive, replace the two side-column alternatives with bottom group zones at 40% and 50% of available height, keeping image share at 25%. Retain the baseline and other alternatives, including the grid candidate. Wide banners and portrait allocations are unchanged. This is a local geometric heuristic, not an official format catalogue or a sample-specific branch. The candidate budget remains six; no regression guard was relaxed.

Side columns are narrow at these proportions and were frequently rejected for shrinking group labels. Deeper bottom zones let those groups stay larger while existing guards protect text and image sizes. A test with opaque element IDs verifies the compact dense fixture's three badge labels retain at least 4.16px, along with the independent contract and candidate budget. That threshold prevents the reproduced regression; it does not claim readability.

## Linux checks and results

- Both images rebuilt; 67 offline tests pass; all three production JSON/PNG pairs independently validate.
- 70 catalogue cases: zero contract findings and no measured overflow or local-loss regression. Five report rows change; two change quality/font results and three change only candidate selection. Inspected the five corresponding output renders.
- Level 3 at 300x250: local loss 0.344764 to 0.321939. Three badge labels reach 4.1667px; legal copy remains 3.3333px. The five sub-6px catalogue cases remain.
- Level 3 at 1280x720: minimum type 13.2109 to 13.9421px; local loss stays zero.
- An additional 49-case sweep combines seven source families with 320x320, 400x300, 600x400, 700x400, 796x400, 800x400 and 804x400. All contracts pass; no local-loss regressions. Four Level 3 sizes improve: 320x320 (0.308037 to 0.294772), 400x300 (0.257385 to 0.201775), 600x400 (0.115609 to 0.067640), 700x400 (0.077621 to 0.044470). These are exposed development variations, not fresh holdouts.
- All 42 existing regression/stress cases preserve complete designs, quality scores and decoded pixels exactly against bfac292. A repeat in the rebuilt image also matches exactly.
- [Per-case evidence and sweep script](m5-compact-evidence/summary.json); [timing evidence](m5-compact-evidence/timing.json).

Commands: scripts/verify-container.sh; evaluation.catalogue with the prior artifacts/m5-expand-selected/report.json reference; evaluation.parity and a repeat against artifacts/m5-compact-parity/report.json; saved boundary-sweep script in both baseline and modified engines. Baseline engine was extracted from bfac292 with Git archive into an ignored artifact folder. All runtime checks use --network none, linux/amd64 via Colima/Rosetta. Five sequential warm 70-case engine sweeps per revision, after one full warmup; no rendering/startup or memory measurement in this step.

Median warm sweep: 0.4929s before and 0.5180s after (+5.1%). The measured cost is about 0.36ms per case; accepted for the quality improvements. These emulated warm timings do not establish native-hardware performance.

## Handoff

Accepted as a bounded improvement, not a resolution of dense typography. Dense fine print, crowded logo/product allocation, collision-aware anchoring and organizer/release questions remain. No new independent judge, fresh holdout or official score. The expected missing badge and Fontconfig warnings persist.

Artifacts: artifacts/m5-compact-probe, artifacts/m5-compact-parity, artifacts/m5-compact-repeat; artifacts/m5-compact-sweep-before.json and artifacts/m5-compact-sweep-after.json; artifacts/m5-compact-container.log and artifacts/container-check.w41orY/output. Root releases ownership after integration.
