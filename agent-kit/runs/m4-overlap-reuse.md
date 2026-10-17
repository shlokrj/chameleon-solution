# M4: reuse overlap geometry within each quality evaluation

Date: 2026-10-17 America/Chicago. Baseline 88ab64f. Change `perf: reuse bounds during overlap scoring`.

## Change and validation

Quality scoring now calculates each relevant element's rotated bounds once for the source and once for the candidate. Two local dictionaries replace repeated geometry work inside each pair comparison. Intersection formula, denominator floor, pair order, overlap allowance, explicit-group exclusions and summation order remain unchanged. No persistent geometry cache or cross-candidate state is introduced. Additional retained storage is linear in the number of relevant elements; pairwise comparisons and hierarchy checks remain quadratic.

50 tests pass. Added checks cover exact collision-score equality across rotation, degenerate boxes and groups, stale-state prevention after geometry mutation, and two bounds calculations per relevant element. The unit reference shares the unchanged overlap formula, so historical engine comparison supplies the separate numerical reference.

[42-case parity evidence](m4-overlap-evidence/parity.json) confirms exact selected-output quality dictionaries, complete JSON layouts and decoded RGBA pixel hashes against baseline. All independent structural checks pass. Cases comprise three samples, twelve development layouts, fifteen saved regressions, six scaling tasks and six typography variants. This compares selected outputs, not every rejected candidate. Existing readability limitations and intentional missing-badge warnings persist unchanged.

[Independent static review](m4-overlap-evidence/REVIEW.md) found no actionable regression. Same inherited model/separate context, shared filesystem and procedural isolation; no cross-model claim. Reviewer did not run workloads during profiling.

## Sequential paired performance

[Raw timings and whole-worker RSS](m4-overlap-evidence/profiles.json). Baseline ran from an isolated git archive of 88ab64f, with the same interpreter/dependencies/assets. Baseline profile finished before candidate profile began. Nine cases each used separate cold/warm workers and five measured warm repetitions following a first run; all 36 workers succeeded and both reports verified code stability. Parity workloads ran afterward.

| Case | Baseline warm engine median (ms) | Candidate warm engine median (ms) | Ratio |
|---|---:|---:|---:|
| chameleon_sample_level1_warmup | 0.20 | 0.18 | 1.13× |
| chameleon_sample_level2_core | 0.52 | 0.47 | 1.12× |
| chameleon_sample_level3_advanced | 16.14 | 14.80 | 1.09× |
| scale-12-wide | 0.81 | 0.49 | 1.65× |
| scale-12-portrait | 1.77 | 1.46 | 1.21× |
| scale-48-wide | 37.57 | 31.15 | 1.21× |
| scale-48-portrait | 37.85 | 31.13 | 1.22× |
| scale-120-wide | 171.19 | 132.44 | 1.29× |
| scale-120-portrait | 124.33 | 84.50 | 1.47× |

On these local cases, engine medians improve about 1.09–1.65×; the 120-label wide/portrait cases improve about 23%/32%. Tiny-case differences are fractions of a millisecond, not an application-wide latency claim. Rendering was not optimized. Whole-worker peak RSS differences are within about 0.3 MiB; these peaks include renderer/interpreter/evaluator and do not precisely quantify the small per-call dictionaries. Cold wall includes startup, imports, validation, engine/render and report I/O, with OS caches not cleared. Environment: macOS arm64, Python 3.12.13; package versions and source hashes in evidence.

## Reproduction and next step

Use evaluation/profile.py sequentially in baseline/candidate checkouts. Copy current evaluation/parity.py into the isolated baseline first: the old report format lacks quality dictionaries, and the upgraded comparison deliberately flags those as missing instead of silently passing.

```sh
# Isolated baseline checkout, same virtual-environment interpreter:
python -m evaluation.parity --output /absolute/path/overlap-before
# Candidate checkout:
python -m evaluation.parity --output artifacts/overlap-after --reference /absolute/path/overlap-before/report.json
python -m evaluation.profile --output artifacts/profile
python -m unittest discover -s tests -v
```

Local full outputs are under artifacts/m4-overlap-baseline, m4-overlap-before/after and m4-overlap-parity-before/after. Tracked compact evidence retains raw repetitions, quality values and hashes.

M4 remains in progress. Both measured optimization steps are complete; next prioritize reproducible dependency pinning and offline packaging rather than speculative further tuning. Docker remains absent from PATH, so clean linux/amd64 build, image size, network-disabled execution and container memory are still unverified. Dense-layout readability remains a separate quality limitation; this change preserves it rather than claiming improvement.
