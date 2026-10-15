# M3 rotation and grid repairs

Parent revision: c8de17f. Change: `fix: preserve readable rotated text and source grids`.

Rotated singleton text now measures compact text geometry and reserves its rotated and unrotated extents before fitting, avoiding a second severe shrink. Candidate six can preserve complete aligned source text rows as a grid; it replaces an allocation-only alternative and retains the six-candidate cap, original fallback, contract gates, and regression guards. Grid recognition allows alignment drift up to 1% of the smaller box dimension, sorts within each row, and rejects incomplete or overlapping rows. No runtime model or network calls were added.

## Evidence

- 36 unit tests pass, including six rotation angles, input preservation, deterministic selection, ID renaming/reordering, reading order, subpixel alignment, rejected ambiguous grids, and reduced candidate budgets.
- All five saved adversarial tasks and all 15 supplied/development comparisons pass independent structural checks. Direct real renders inspected for both repaired tasks and five changed comparison outputs. Existing extreme dense-banner readability limitations remain.
- Rotated-copy font increases from 2.819px to 42px; dense-labels from 11.518px to 42px. These are local measurements, not official scores.
- Independent judge accepted original repairs, discovered fractional alignment failure in four fresh variants, then verified its repair across all six exposed cases. [Initial review](m3-text-evidence/initial-review.md), [repair review](m3-text-evidence/repair-review.md), [exact hashes and checks](m3-text-evidence/repair-report.json).
- [Comparison timings](m3-text-evidence/comparison.json): five warm repetitions per case on macOS arm64 / Python 3.12.13; per-case candidate medians range 0.28–36.97 ms. Reference is M1 6d1dbe5, not the immediate predecessor. No cold-start/memory/container claim.

Reproduce from repository root:

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m evaluation.regressions --output artifacts/m3-text-repairs-final
.venv/bin/python -m evaluation.compare --baseline 6d1dbe5 --output artifacts/m3-text-comparison-final
```

Local ignored judge artifacts contain input/output JSON and source/output PNGs. Portable original tasks remain in tests/fixtures/m3; fractional alignment is reproduced by the new unit test. Historical review paths refer to those local artifacts.

## Remaining work

M3-R1/R2 and the newly exposed fractional-grid defect are independently verified fixed. M3 remains in progress: freeze this revision and perform a final fresh bounded review; these disclosed variants are now development cases. Judge used the same inherited model in a separate context with shared filesystem access, not cross-model or sealed isolation. Grid recognition is deliberately conservative; mixed or incomplete grids and extreme density remain limitations. M4 profiling and offline container validation remain outstanding; Docker was unavailable in prior environment checks.
