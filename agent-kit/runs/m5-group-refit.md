# M5 grouped-label fitting: bounded review closure

Baseline `34edde9`, 2026-10-22. One six-case challenger round, one repair, then three fresh judge-held cases. [Independent judge verdict](m5-fresh-review-judge.md): accept the bounded repair. The roles used separate contexts and shared filesystem with the same inherited model configuration; exact model ID was unavailable. This is not verified cross-model or filesystem-sealed testing. All nine fixtures are now exposed and retired as holdouts.

## Change and evidence

The accepted quality defect was avoidably tiny grouped labels: unchanged boxes supported a 9px witness, but the engine returned 6.264px. A final pass now fits explicit group labels within their existing boxes, capped at the smaller of source font size and 12px. It skips overlapping same-group text boxes, never shrinks text, and rolls back on worse loss, hierarchy or overflow. Candidate count remains six; the existing bounded font search is reused. Candidate diagnostic scores precede final refinements; `refined_group_text` identifies accepted changes.

Pill labels reach 9.321px with no geometry changes. All 70 paired catalogue outputs differ only in font sizes, with no decreases. Sixteen local loss improvements, none worse; cases below 6px drop from four to three. Root inspected all 16 before/after catalogue render pairs; the final frozen-engine catalogue report exactly matches that reviewed run. Judge separately inspected source/baseline/candidate renders for all nine review/holdout cases, including rotated, styled and multiline labels.

Offline Linux/amd64 validation: 73 tests, three production JSON/PNG pairs, 70 catalogue cases with zero contract/overflow findings, 42 parity cases repeated without differences, 15 saved M3 cases, six fresh review cases and three judge-held cases. Missing/empty fixture-directory CLI checks return exit 2. The new `--fixtures` option preserves the default M3 directory. Frozen engine SHA256 and counts/timings are in [summary.json](m5-group-refit-evidence/summary.json).

## Efficiency

Serial engine-only measurements in the offline verification image used one full 70-case warmup followed by five 70-case sweeps per revision. Baseline engine was extracted from `34edde9`; unchanged helpers and inputs were shared. Median baseline 0.5492s, repair 0.7027s per sweep (about 28% higher, approximately 2.2ms added per case). Samples are noisy: repair sweeps range 0.571–1.300s. This is a small local warm-run observation, not a stable benchmark, cold-start/RSS measurement or official latency claim. The extra fit and two quality evaluations cost time; retained for the measured readability improvement. No concurrent review workload was intentionally run during timing.

To reproduce timing, iterate `evaluation.catalogue.sources()` × `FORMATS`, call `resize` once for every case to warm up, then time five complete sweeps with `time.perf_counter`; run baseline and repair serially in the same offline image. Raw five-sweep values are retained in the summary.

## Reproduction and handoff

```sh
./scripts/verify-container.sh
# Run these inside the verification image with /app as the working directory:
python -m evaluation.catalogue --output artifacts/catalogue
python -m evaluation.regressions --fixtures tests/fixtures/m3 --output artifacts/m3
python -m evaluation.regressions --fixtures tests/fixtures/m5-review --output artifacts/m5-review
python -m evaluation.regressions --fixtures tests/fixtures/m5-holdout --output artifacts/m5-holdout
python -m evaluation.parity --output artifacts/parity
python -m evaluation.parity --output artifacts/parity-repeat --reference artifacts/parity/report.json
```

Local ignored artifacts use `artifacts/m5-group-refit-*`, `m5-review-final`, `m5-holdout-final`, and `m5-review-judge`. Tracked fixtures and summaries preserve reproduction inputs and conclusions; raw screenshots are not committed.

This finishes the bounded review cycle. Three Level 3 catalogue layouts still contain sub-6px copy; the overlapping-box holdout remains unchanged at 5.488px. Tight groups, small/low-contrast logos and unresolved organizer requirements remain. M4/M5 stay in progress; no official score, universal readability, or submission-ready claim. Next: establish a feasible layout witness for the remaining dense Level 3 copy before changing allocation further, and resolve release questions separately.
