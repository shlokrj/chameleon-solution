# M3: first adversarial repairs and open findings

Baseline: `3324d76`. Challenger and judge ran in independent contexts using the same inherited model; shared filesystem separation was procedural, not sealed. No cross-model claim is made. The integrator synchronized origin/main before workers started and before repair. Workers did not mutate Git or production code.

## Verified repairs

- An ungrouped white label on a black panel was moved off its backing and disappeared. The judge independently reproduced this visual failure. Conservative internal grouping now retains contained text on an opaque-enough rectangular backing without modifying group_id or other source fields.
- A fresh judge case exposed the same failure with a cover image. Contained cover/fill images now qualify as supports; contain images are excluded because their boxes can include unpainted margins. This remains a geometric heuristic, not a pixel contrast guarantee.
- Identity resize collapsed the nonzero dimension of a zero-width line. Uniform placement now computes scale only from nonzero source axes. The line retains its 200px extent. The renderer still shows both source and output blank; no visible-line repair is claimed.

The judge independently verified all three repairs on final engine hashes. See [verification](m3-evidence/repair-verification.md) and [machine-readable record](m3-evidence/repair-report.json). Referenced local `artifacts/` paths in historical reports are not distributed evidence; tracked reproducers below are portable.

## Remaining accepted findings

| ID | Priority | Reproducer | Observed limitation |
|---|---|---|---|
| M3-R1 | P1 | `tests/fixtures/m3/rotated-copy.json` | 90-degree singleton text shrinks from 28px to 2.819px despite a structurally valid readable 28px witness |
| M3-R2 | P2 | `tests/fixtures/m3/dense-labels.json` | Twelve labels become one column at 11.518px despite a feasible 28px 3-by-4 grid |

Both were independently adjudicated using real output/witness renders. The supplied `*-witness.json` files are hand-constructed feasible comparison designs, not implemented engine output. These fixtures are now exposed development cases. M3 remains **in progress**, with 3 of 5 milestones complete; no fresh holdout pass exists after the latest repair.

## Checks and reproduction

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m evaluation.regressions
.venv/bin/python -m evaluation.compare --output artifacts/m3-final
```

30 tests pass. All 15 prior development/sample comparisons remain structurally valid; the five saved adversarial task outputs also pass structural checks, demonstrating why visual quality cannot be reduced to these checks. `evaluation.regressions` renders portable saved tasks and reports diagnostics; a zero exit means no structural findings, not that the two open quality defects passed. All repair images were directly rendered and inspected. Production renderer, supplied assets, and source samples are unchanged.

Historical independent findings are retained in [initial judge](m3-evidence/initial-judge.md), [panel adjudication](m3-evidence/panel-adjudication.md), and [fresh judge pass](m3-evidence/fresh-judge.md). The challenger completed its second-round artifacts but hit an agent usage limit before its final response; the judge independently reproduced and adjudicated its two findings, so they do not rely on an unfinished report.

## Resume

First pull safely and read PROGRESS.md. Claim M3-R1 and fix rotation-aware text allocation without changing source rotation/content. Then add a bounded text-grid candidate for M3-R2, preserving reading order and the six-candidate budget. Retest accepted fixtures and prior development families; freeze before independent final judging. Keep dense-banner readability and missing Docker validation open. No benchmark or submission-ready claims are made by this pass.
