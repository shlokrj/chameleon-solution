# M5 row/column packing

Date: 2026-10-18 America/Chicago. Parent 1fc9998. Owner: root. Change: `feat: compare row and column packing for larger groups`.

## Hypothesis and implementation

Greedy wrapping rows can shrink groups unnecessarily when a column arrangement fits the same zone at a larger shared scale. Evaluate both directions, without rotating or independently resizing units; keep rows on ties. Each direction retains the bounded 24-step search and original unit order within its reading direction. Skip the second search for singletons or when rows already reach the allowed upper scale. The six-candidate engine budget is unchanged. This is a bounded heuristic, not globally optimal packing.

Added an independent feasible-layout regression: units 100x20, 20x40, 20x40 in a 140x80 slot with 5px gaps fit unshrunk in columns, while greedy rows require 85px height. The test checks retained size, bounds and pairwise non-overlap. Existing hierarchy/group tests remain unchanged.

## Linux evidence

- 62 tests pass in the rebuilt verification image with networking disabled.
- Full scripts/verify-container.sh passes: both image builds and all three independently validated production JSON/PNG pairs.
- 70 catalogue cases: zero contract findings and zero measured overflow; three changed render images, all inspected. No local loss regression. The comparison uses the same M5 quality metric.
- Level 3 at 1500x500: minimum font 11.555 to 12.594px; local loss to zero.
- Level 3 at 1600x400: minimum font 10.961 to 12.319px; local loss to zero.
- Level 3 at 300x250: local loss 0.386037 to 0.344764; minimum text only 3.321 to 3.333px, still unreadable. Larger CTA/group geometry does not solve dense small-format copy.
- 42 regression/stress cases pass structural/input-immutability checks. Repeated final-engine evaluation exactly matches the probe's tasks, output JSON, quality and decoded pixels. Three JSONs differ from the pre-change baseline (Level 3 sample, event-banner, dense-labels-banner) without quality changes; these renders were also inspected. All 15 saved adversarial cases are included.
- [Per-case comparison](m5-flow-evidence/quality.json).

Commands: scripts/verify-container.sh; evaluation.catalogue with --reference artifacts/m5-linux-catalogue/report.json; evaluation.parity; repeated evaluation.parity with --reference artifacts/m5-flow-parity/report.json. The final rebuilt image also reruns the 70-case catalogue against the probe report after skipping redundant searches.

## Efficiency

Five timed 70-case engine-only sweeps per revision, after one full warmup; sequential containers, same linux/amd64 Colima/Rosetta environment. Baseline engine was extracted from Git HEAD 1fc9998 into an ignored artifact directory. Median sweep time 0.4691 to 0.4915 seconds: about 4.8% slower, or 0.32ms additional engine time per case averaged across the sweep. Accept this bounded cost for the measured larger groups; no speedup claim. Rendering, process startup and memory were not measured in this step. Preliminary timings were superseded by the sequential final comparison, avoiding concurrent image builds. [Raw timings and script](m5-flow-evidence/timing.json).

## Limits and handoff

This addresses group packing, not semantic logo sizing. The five sub-6px catalogue cases remain; logo minimum sizing and collision-aware anchoring remain separate work. No new model, fresh holdout, independent judge or official score. Missing-asset and Fontconfig warnings remain visible. Keep M4/M5 open for remaining quality/release work.

Local artifacts: artifacts/m5-flow-probe, artifacts/m5-flow-parity, artifacts/m5-flow-final, artifacts/m5-flow-catalogue-final; build/test log artifacts/m5-flow-container.log and production pairs artifacts/container-check.8sbCSX/output. Root releases ownership after integration.
