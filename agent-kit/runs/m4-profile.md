# M4 initial local performance evidence

Date: 2026-10-16 America/Chicago. Engine frozen at b7515b9; evaluation/profile.py added in this containing commit. No engine optimization was made in this batch. [Machine-readable measurements](m4-profile-report.json) include code hashes, package versions, renderer origin, raw repetitions, quality diagnostics, and profiler hotspots.

## Protocol and results

MacOS arm64, Python 3.12.13. Nine cases: three supplied designs, plus 12/48/120 short labels at wide and portrait target shapes. Generated labels fill rows, with a partial last row when count does not divide the inferred column count; these are exposed scaling cases, not representative hidden-distribution estimates. Each case has separate cold and warm child processes. Five warm repetitions follow a separately reported first run. Direct real rendering is required; no placeholder fallback. All 18 worker runs exited successfully, independent structural checks passed, outputs were deterministic, and inputs/code remained unchanged.

Cold wall time includes interpreter startup, imports, schema validation, engine, rendering, and report I/O. OS caches were not cleared, so this is process-cold rather than machine-cold. Warm engine/render medians exclude validation/report I/O. RSS is the whole worker's high-water mark before cProfile, including imports, renderer and evaluator; it is not engine-only memory. Units are normalized separately for Darwin and Linux. Timed-out workers are recorded as failed, rather than omitted. No container, network isolation, official benchmark, or speed improvement claim.

| Case | Cold worker wall (s) | Warm engine median (ms) | Warm render median (ms) | Warm worker peak RSS (MiB) |
|---|---:|---:|---:|---:|
| chameleon_sample_level1_warmup | 1.01 | 0.51 | 103.50 | 190.4 |
| chameleon_sample_level2_core | 0.81 | 1.16 | 91.11 | 222.4 |
| chameleon_sample_level3_advanced | 0.80 | 38.82 | 35.77 | 205.0 |
| scale-12-wide | 0.72 | 1.88 | 9.40 | 166.2 |
| scale-12-portrait | 0.73 | 11.49 | 10.66 | 191.2 |
| scale-48-wide | 1.08 | 263.05 | 12.97 | 192.9 |
| scale-48-portrait | 0.99 | 260.05 | 12.74 | 192.7 |
| scale-120-wide | 2.01 | 1203.49 | 19.97 | 194.6 |
| scale-120-portrait | 1.45 | 676.98 | 23.52 | 194.1 |

## Findings and next experiment

The largest wide case costs about 1.2 seconds in the engine despite the six-candidate cap. cProfile attributes prominent costs to repeated Skia typeface creation in glyph-width measurement and repeated geometry/overlap checks. A candidate-count limit alone does not bound per-candidate scaling cost. The profiling run is separate from the timed repetitions; its timings should not be treated as normal latency.

48/120-label outputs include very small text, down to 1px; passing structural checks is not readability success, and this run does not establish infeasibility. Keep those quality diagnostics attached to performance comparisons. Before optimizing, repair the accepted large-panel contrast defect, then compare a bounded glyph-measurement cache or reused bounds against this frozen baseline, requiring identical or independently improved output. Keep caches sensitive to text/font/style/size and bounded in memory.

Docker is absent from PATH, so linux/amd64 build, image size, network-disabled execution, and container memory remain unverified. Do not mark M4 complete.

Reproduce:

```sh
.venv/bin/python -m evaluation.profile --output artifacts/profile
.venv/bin/python -m unittest discover -s tests -v
```

Local PNGs and full reports are under artifacts/m4-profile-final. The tracked report preserves measured values; timing naturally varies between machines/runs.
