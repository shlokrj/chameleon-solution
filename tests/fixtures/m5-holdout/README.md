# Final M5 grouped-label repair holdout

Three deterministic, hand-authored judge cases generated after the builder froze its grouped-label repair (`engine/resize.py` SHA256 `a14aeaea00f1d0a0b9453bccfc7019cbcb42a2e536a05f61f8387d54bd43183f`), against baseline `34edde9`. No random seed. The builder received only the case count until independent paired evaluation and PNG inspection completed. They are now exposed development evidence, not a reusable sealed holdout.

All sources are valid schema v0.9 designs with ordinary text/backing relationships and no external or fabricated assets. Gray rendered panels reflect the existing converter behavior for these shape fields. Each source was actually rendered and inspected for semantic validity.

| Case | Purpose | Result |
|---|---|---|
| `01-rotated-styled-groups` | Separate backed labels rotated ±12 degrees, mixed bold runs | Labels improve from 7.272px to 9.719/10.375px; rotation/style/containment preserved; no glyph collision. |
| `02-shared-group-overlapping-boxes` | Two distinct glyph blocks whose text boxes overlap inside a common backing | Guard leaves output exactly unchanged at 5.488px. No new collision, but conservative guard leaves a known tiny-label quality limitation. |
| `03-multiline-group-hierarchy` | Three cards with bold headings, italic body runs, letter spacing and explicit newlines | Headings 5.76→7.20px; bodies 4.32→6px. Text complete, hierarchy and backing preserved; small size remains a quality limitation. |

Reproduce from repository root in the verified image:

```sh
docker run --rm --platform linux/amd64 --network none -v "$PWD:/app" --entrypoint python chameleon-verify -m evaluation.regressions --fixtures tests/fixtures/m5-holdout --output artifacts/m5-holdout
```

Independent paired artifacts/report: `artifacts/m5-review-judge/holdout/` and `artifacts/m5-review-judge/repair-report.json`. See `agent-kit/runs/m5-fresh-review-judge.md` for acceptance boundaries. All three outputs pass independent contracts; the holdout does not establish universal readability or official scorer performance.
