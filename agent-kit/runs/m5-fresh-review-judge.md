# M5 fresh review: independent judge

Frozen engine revision: `34edde9` (2026-10-22). White-box, one six-case challenger round. Judge used an isolated agent context; exact model/version was not exposed, so this is role separation, not a verified cross-model comparison. The initial review had no holdout; the final repair phase below adds three fresh judge-held cases.

## Environment and reproduction

Image `chameleon-verify`, ID `sha256:cb1ceac4328879f60e75a77d52d1ee459dd2875df5666ad948e1aa30e088bc1f`, Linux/amd64, networking disabled. Root confirmed synchronized revision; judge verified HEAD and did not pull, commit, or edit production. Independent harness calls `resize_with_diagnostics`, full Draft202012 source validation, `evaluation.contract.check_contract`, and the real renderer directly. It compares nested inputs and hashes every brand file before/after. Raw fixture hashes, diagnostics, timings and rendering warnings are in `artifacts/m5-review-judge/report.json`; all twelve PNGs were visually inspected.

From repository root, rerun saved local harness:

```sh
docker run --rm --platform linux/amd64 --network none -e PYTHONPATH=/app -v "$PWD:/app" --entrypoint python chameleon-verify artifacts/m5-review-judge/reproduce.py
docker run --rm --platform linux/amd64 --network none -e PYTHONPATH=/app -v "$PWD:/app" --entrypoint python chameleon-verify artifacts/m5-review-judge/witness.py
```

The initial harness attempt omitted PYTHONPATH and failed before importing the engine. The corrected invocation above completed. Artifacts are ignored local evidence; tracked fixtures plus `python -m evaluation.regressions --fixtures tests/fixtures/m5-review --output artifacts/m5-review` reproduce the source/output pairs. No timing benchmark claim: individual engine measurements ranged 0.0025–0.0577 seconds in one serial pass; cold/warm resource profiling was not run.

## Adjudication

All six sources validate; all six outputs have zero contract findings, zero measured text overflow and zero support violations. Nested inputs and all brand files remain unchanged. No malformed-input case or missing-asset exception was needed.

| Fixture | Verdict | Source/output visual evidence |
|---|---|---|
| `01-alpha-rotated` | No new failure accepted | Rotation survives; title/detail fit. White logo lettering has weak contrast in source and output, and becomes small; no new solver-induced contrast failure established. |
| `02-pill-labels` | **Accepted M5-R1: avoidably tiny grouped labels (quality)** | Three labels shrink to 6.26399898px beside a much larger headline. Same-box 9px witness fits and visibly improves them. |
| `03-mixed-unit-scale` | No new failure accepted | Product/logo, headline, legal copy and button remain present and separated; legal copy and label are small but fit. |
| `04-final-floor-styled` | No new failure accepted | Styled title, spaced subtitle and explicit-newline detail remain complete; low-contrast logo inherited from source. |
| `05-stroked-frame` | Reject as solver styling failure | Gray shape and absent expected colored stroke already occur in source rendering. Output preserves the enclosing relationship. This is renderer/source behavior, not evidence of a resize regression. |
| `06-two-buttons-alpha` | No new failure accepted | Both labels remain contained; logo/title/buttons separated. 9.09px labels remain a quality limit but no distinct failure class was established. |

## M5-R1 feasible witness

Judge independently reconstructed the witness from its own baseline output, changing **only** `font_size` of `label0`, `label1`, `label2` to 9. All boxes, content, source font family/style, backing shapes, headline and other properties stay exactly unchanged. Contract validation remains clean. Renderer text extents are respectively 82/83/66px wide by 12.5999997px high inside 151.379975px by 13.0499979px boxes. All three are one line. The direct real-rendered witness was visually compared with the baseline and is visibly more readable, without overlap or lost hierarchy.

Local evidence: `02-pill-labels-output.json/png`, `02-pill-labels-witness.json/png`, `witness-report.json` under `artifacts/m5-review-judge/`. The 9px value is a feasible improvement witness, not an official readability threshold or a claim that 9px is ideal. A compact reproduction of the witness is to load the saved baseline JSON, change those three label font sizes to 9, call `check_contract` against the unchanged fixture and `text_extent` per label, then directly render.

This is a quality failure under SPEC quality objective 1, not a C1–C7 hard-constraint violation. It deduplicates with the existing small-group typography limitation; the new evidence demonstrates available room, rather than irreducible density. Builder may attempt a general grouped-label fitting repair, with original layout/group relationships preserved. Judge must compare any repair on identical fixtures plus prior regressions; at this initial checkpoint no repair had yet been judged; the final verdict follows below. Zero hard failures here is not a universal correctness or release-ready claim.

## Frozen repair and final fresh check

The builder froze one repair in `engine/resize.py` (SHA256 `a14aeaea00f1d0a0b9453bccfc7019cbcb42a2e536a05f61f8387d54bd43183f`, baseline HEAD still `34edde9`). It enlarges explicit grouped labels in their existing boxes with source-size/12px caps and guards for overlapping text boxes, measured fit, loss and hierarchy. Judge evaluated this exact file independently, using `git show 34edde9:engine/resize.py` loaded as the paired baseline and current unchanged layout/typography helpers. The root's wider test/catalogue/parity checks are separate evidence, not claimed as judge executions.

**Verdict: accept this bounded repair.** All six exposed review cases and three fresh holdouts validate at source and output; no contract failures, measured overflows, support violations, input mutations, new overlap or hierarchy inversion. Actual source/baseline/candidate PNGs were inspected. JSON comparisons confirm that all candidate differences are font sizes alone. No new glyph collisions, clipped styled text, changed rotations or lost backing relationships were observed. Ordering was not anonymized; contract checks, measured extents and actual paired PNGs support the decision rather than a numerical vision score.

Exposed M5-R1 pill labels improve from 6.263999px to 9.321419px, without changing their boxes or title. The mixed-unit case label improves 9.813→11.766px; both labels in the two-button case improve 9.090→12px. The other three exposed outputs remain exactly unchanged.

After the repair freeze, the judge authored three deterministic fixtures in `tests/fixtures/m5-holdout/`, withheld details until evaluation completed, and then disclosed all results:

| Fresh fixture | Evidence and interpretation |
|---|---|
| `01-rotated-styled-groups` | ±12-degree mixed-bold labels improve from 7.272px to 9.719/10.375px. Source and target glyphs remain within their backings; no rotation/style regression. |
| `02-shared-group-overlapping-boxes` | Deliberately overlapping text boxes contain separate visible text blocks. Output is exactly unchanged: guard safely declines growth. 5.488px text is still tiny; this is the existing conservative-fit quality limitation, not a new regression or a fully solved case. |
| `03-multiline-group-hierarchy` | Bold headings, italic body runs, letter spacing and explicit newlines survive. Headings improve 5.76→7.20px and two-line bodies 4.32→6px. They remain small, but fit and preserve hierarchy without collision. |

These three cases are now exposed and retired as sealed holdout evidence. This finishes the bounded cycle; no further holdout generation or repair iteration is implied. Small grouped text in tight or overlapping boxes and low-contrast/small logos remain unresolved quality limitations.

Paired local evidence is in `artifacts/m5-review-judge/repair/`, `holdout/`, and `repair-report.json` (fixture hashes, engine hash, full checks, text extents and diagnostics). The saved `verify_repair.py` is reproducible with the same offline invocation and PYTHONPATH used above; its baseline module is saved as `baseline_resize.py`. Tracked holdout README documents a direct source/output reproduction via the evaluation helper. No new performance/resource acceptance claim was made in this judge pass.
