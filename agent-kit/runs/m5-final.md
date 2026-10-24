# M5 composition-quality closure

Frozen production revision `9dc59b3`, 2026-10-23. Final acceptance is bounded to the recorded catalogue, regression and fresh-review evidence; it is not a claim of perfect layout, hidden-set success or official scoring.

## Delivered work

M5 shipped shared-scale row/column packing, proportional shape lengths, alpha-aware image bounds, bounded spare-space image expansion, compact-canvas allocation, guarded standalone text floors, grouped-label fitting, and final-copy spare-height fitting. Runtime search remains capped at six candidates; no runtime model, generated assets or network dependency was added. Contrast tiebreak and direct allocation-slot replacements were rejected on evidence. These rejected experiments are complete investigations, not missing runtime features.

## Final verification

- 75 tests and all three production JSON/PNG delivery checks pass offline Linux/amd64 at the frozen engine. Latest build uses cached layers; earlier clean-build evidence remains in M4.
- 70 catalogue layouts have zero contract findings or measured text overflow; final [per-case results](m5-final-evidence/catalogue.json) are preserved.
- Relative to the first M5 Linux integration catalogue, 20 local-loss improvements and no worse losses; mean local loss 0.029919→0.014043. This is a local proxy, not an official score. Earlier M4-to-M5 loss is not directly comparable because the overlap metric changed.
- 42 parity cases repeat exactly, including designs and decoded pixels. Fifteen M3 saved regressions were rerun during closure with zero findings. Nine exposed M5 review cases also pass; changed catalogue/review renders were inspected in the tail-copy repair.
- Current final-engine warm 70-case sweep median is 0.5638s over five measured repeats after warmup, excluding rendering. Current cold/RSS evidence immediately predates the small final-copy pass and is not relabeled as a new final-engine profile; see [M4 measurements](m4-final-review.md) and [paired final-pass timing](m5-tail-copy.md).

## Remaining quality limits

| Case | Smallest text | Interpretation |
|---|---:|---|
| Level 3, 728×90 | 4.908px | Dense grouped labels remain tiny |
| Level 3, 300×250 | 5.159px | Legal copy now 6.111px; grouped labels set the minimum |
| Level 3, 160×600 | 4.733px | Dense secondary group still limits readability |

Small/low-contrast logos can remain weak beside large product imagery. Collision-aware corner anchoring and a source-derived logo minimum are deferred enhancements. Overlapping grouped text boxes conservatively skip growth. These known quality compromises are not claimed solved; the challenge explicitly welcomes partial solutions. No fixed readability threshold is an official acceptance rule. This bounded milestone closes with limitations, rather than promising open-ended optimization.

The user-confirmed final PDF governs stage-one engine/Dockerfile/README scope. The user owns the submission form; no form was submitted. Future changes should start from the frozen verified engine, preserve the regression evidence and reopen a concrete task rather than silently changing this closure.

## Independent final review

A separate judge context authored three deterministic fresh cases after freezing `9dc59b3`, covering styled tail copy, rotated tail copy and grouped-peer hierarchy. All sources/contracts, measured text fit, repeats and input preservation pass; actual source/baseline/output renders were inspected. Styled tails grow 10→10.5px and 10→10.4px, while the rotated tail remains unchanged. No new hard failure was found. See [judge report](m5-final-judge.md) and the saved `tests/fixtures/m5-final/` cases. The inherited model ID was not exposed, so this is independent role/context review, not a verified cross-model comparison. Fixtures are now exposed and retired from holdout use.

Decision: **close M5 as a bounded composition-quality milestone with the limits above**. All shipped changes have validation evidence, unsuccessful alternatives are explicitly rejected, the frozen final change passes fresh review, and remaining enhancements are documented. No further repair round is required by this review.
