# M3 final fresh batch: two quality defects remain

Engine revision b7515b9, reviewed 2026-10-16 America/Chicago. One bounded fresh batch of six cases, independently generated and rendered by the judge after freezing production files. Four visual passes and two accepted quality failures; all six independent structural checks pass. Engine/assets stayed unchanged. Same-model separate-context review with shared filesystem/procedural isolation, not cross-model or sealed validation. No repair round was attempted in this batch.

[Independent judgment](m3-final-evidence/JUDGMENT.md) and [exact hashes/results](m3-final-evidence/report.json) preserve the detailed findings. The historical reproduction script path in the judgment is local; all six tasks and both feasible witnesses are now tracked in tests/fixtures/m3 and the tasks run with evaluation.regressions. They are exposed development evidence from now on.

| ID | Severity | Case | Accepted failure and next step |
|---|---|---|---|
| M3-R3 | P1 | large-inset-backing.json | A panel covering 87.11% of the source is excluded by the 80% support heuristic; part of white text disappears on white target. Distinguish genuine full-canvas backgrounds from large inset backing and preserve contrast. |
| M3-R4 | P2 | nested-support-panels.json | Outer/inner panels become disjoint despite clear feasible nesting. Preserve enclosing relationships without merging arbitrary unrelated shapes. |

Both have independently checked and rendered *-witness.json files demonstrating feasibility without changing immutable content/styles. Four other cases cover opposing rotations, grid plus grouped footer, full-bleed background with badge, and rotated multiline text; all passed visual expectations. The integrator inspected the six source/output render pairs too.

Full repository validation after saving fixtures: 38 tests pass; all 11 saved tasks pass structural checks and direct rendering. This does not turn R3/R4 into passing visual cases. M3 stays in progress until these defects are repaired and independently verified; subsequent fresh review must use new cases within a new bounded cycle. M4 local profiling began separately; Docker remains unavailable.

```sh
.venv/bin/python -m evaluation.regressions --output artifacts/regressions
.venv/bin/python -m unittest discover -s tests -v
```
