# M4 final local efficiency and delivery review

2026-10-22; frozen revision `04c8358`, production engine unchanged since `a411461`. **Local efficiency and packaging checks complete; full M4 exit remains blocked on unresolved organizer requirements.** Dense typography is tracked as M5 quality debt, not a Docker blocker. No submission or viewer was published.

## Current verification

Rebuilt production and verification images with cached layers using `scripts/verify-container.sh`. All 73 tests pass offline Linux/amd64; production generates all three supplied JSON/PNG pairs; independent schema/contract and direct-render pixel validation reports no findings. All three actual outputs were inspected. Level 3 still has tiny copy and the deliberate missing holiday badge. This is a fresh cached build, not a new no-cache build claim; clean-build evidence remains in the earlier packaging record.

Prior unchanged-engine evidence remains applicable: 70 catalogue layouts, 42 exact repeated parity cases, and nine M5 challenger/judge cases. Candidate-slot experiments did not change production. Existing bounded search, preserved assets and fonts, input immutability and no runtime network dependency remain covered by tests and prior review. Generalization evidence is finite; no claim of hidden-set success or universal readability.

## Current performance

Offline Linux/amd64 under Colima/Rosetta on Apple Silicon, four VM CPUs and approximately 4GiB memory. Nine cases, each with separate fresh cold and warm workers (18 processes). Warm workers perform one warmup then five timed repetitions. Cold wall includes startup/imports, schema validation, engine, rendering and report I/O; OS caches are not cleared. RSS includes the entire worker and validation before profiler instrumentation, not engine-only allocations. Every worker exits zero, contract findings are empty, repeated designs agree and code hashes remain unchanged.

| Case | Cold worker wall (s) | Warm engine median / max (ms) | Warm render median (ms) | Peak worker MiB |
|---|---:|---:|---:|---:|
| chameleon_sample_level1_warmup | 1.760 | 0.50 / 0.52 | 154.25 | 254.5 |
| chameleon_sample_level2_core | 1.506 | 1.44 / 1.78 | 129.25 | 276.9 |
| chameleon_sample_level3_advanced | 1.571 | 40.68 / 43.15 | 67.41 | 251.1 |
| scale-12-wide | 1.378 | 1.53 / 1.55 | 14.41 | 227.1 |
| scale-12-portrait | 1.316 | 3.16 / 3.28 | 14.01 | 227.3 |
| scale-48-wide | 1.400 | 64.67 / 67.59 | 21.50 | 239.7 |
| scale-48-portrait | 1.545 | 65.54 / 69.35 | 21.72 | 239.6 |
| scale-120-wide | 1.674 | 269.64 / 270.82 | 36.34 | 264.9 |
| scale-120-portrait | 1.589 | 177.36 / 209.45 | 37.62 | 264.8 |

Five additional fresh production-entrypoint processes each handled all three supplied tasks: 1.904, 1.657, 1.711, 1.844 and 1.718 seconds. Peak child RSS 271.24MiB; container memory peak 213.64MiB. These are different accounting methods, not interchangeable measurements. No crash or full-render fallback occurred. The known Fontconfig warning and intentional missing-asset placeholder remain. Five warm samples are too few for a stable tail estimate; raw values and maxima are retained rather than claiming precise p95 performance.

These results support finishing local efficiency work without further optimization. For future local regression monitoring, use provisional investigation thresholds of 1s maximum warm engine time, 5s cold worker wall and 512MiB worker RSS on this suite/environment. These are post-measurement engineering thresholds with headroom, not organizer limits or guarantees. All current measurements fall below them. Rebaseline when environment or workload changes; inspect quality before accepting speed changes.

[Profile and environment](m4-final-evidence/profile.json), [production resource runs](m4-final-evidence/resources.json), [delivery validation](m4-final-evidence/delivery.json). Image IDs and Docker Size fields are retained; Size is the engine-reported value and not a portable download/storage estimate.

## Release boundary and next action

The PDF was reread at pages 7, 8 and 14: engine/container/README for stage one, full add-on in finale, and submission channel announced separately. Local FAQ Q5 contradicts viewer timing. Public organizer/partner research did not resolve that conflict or exact hardware/submission requirements; see the dated update in [SOURCES](../SOURCES.md). No runtime model is used, so model approval/weight limits do not currently constrain this implementation.

M4 technical work is ready for handoff, but the original milestone requires the release checklist, including applicable submission requirements. Keep M4 blocked rather than marking an unmet exit complete. Next: obtain the participant announcement/code-freeze instructions, confirm viewer timing, submission mechanism and execution limits, then close the last release gate. M5 dense-copy improvements can proceed independently.

## Reproduce

```sh
./scripts/verify-container.sh
docker run --rm --platform linux/amd64 --network none -v "$PWD:/app" --entrypoint python chameleon-verify -m evaluation.profile --output artifacts/m4-final-profile
```

Run the saved `m4-container-evidence/measure.py` in the production image with input read-only, an isolated writable output directory, and networking disabled for the five full-pipeline runs. The profile command mounts the checkout for Git revision metadata; it is validation tooling, not a runtime requirement. Original logs are under `artifacts/m4-final-*` and `artifacts/container-check.Cy2kNI`.
