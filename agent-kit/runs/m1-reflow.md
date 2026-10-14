# M1: deterministic reflow

## Change and evidence

Compared with M0 engine revision `ae6e289`, the engine now preserves nearby layouts and reflows large aspect-ratio changes into horizontal or vertical arrangements. Explicit groups receive a shared uniform transform; ordinary images retain their source box proportions. Rotated bounds are included in placement. Full-canvas cover backgrounds resize to the target, while lower-layer ungrouped shapes retain proportional geometry and move in bounds.

Text sizing uses the supplied brand fonts and the vendored word wrapper. A bounded 18-step search selects a common scale for standalone text and fits group labels inside their transformed boxes. Content, fonts, styling, opacity, z-order, assets, and nested source data remain unchanged. No runtime model, external service, or sample-specific identifier branch was added.

Implementation: `engine/resize.py`, `engine/typography.py`. Evaluation changes add a separate output directory, code hashes, and explicitly labeled shared text-fit diagnostics. README now describes the implemented engine rather than the old stretch baseline. Production renderer and supplied samples are unchanged.

The exact implementation is the containing commit. [Machine-readable results](m1-reflow-report.json) include hashes of the evaluated engine/evaluation files, the parent revision, environment, all timing repetitions, text sizes, and warnings. Environment is the same Apple M3 / 16 GiB / macOS arm64 / Python 3.12 setup as [M0](m0-baseline.md). This was a single-agent implementation pass, not independent adversarial review.

## Reproduce

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m evaluation.baseline --output artifacts/m1
```

Install `requirements-dev.txt` into the local environment first if needed. Evaluation now exits 0 on these three supplied samples. Real source/output PNGs and JSON live in ignored `artifacts/m1/`; regenerate them on other machines. M0 artifacts/report remain separate.

## Results

16 tests pass, including the original eight checker tests and eight reflow tests. Reflow coverage includes all three samples at their supplied targets and two alternate targets each (nine source/target combinations), group containment, opaque ID renaming and distinct-z reordering, nested input independence, rotation/zero-area geometry, dense tiny canvases, unbreakable styled words, empty content, and explicit newlines.

All three sample outputs pass independent schema, identity, preservation, source-box proportion, and box/rotation-bound checks. Brand file hashes remain unchanged, inputs are unmodified, and repeated output is deterministic. No sample text overflow is estimated by the shared font measurement routine; this is **not** an independent visual oracle. The source/output renders were inspected directly after the final changes.

| Sample | M0 structural findings | M1 structural findings | Visual outcome |
|---|---|---|---|
| Level 1 | 1 | 0 | Retains readable centered layout and original headline/CTA sizes; logo box proportions fixed |
| Level 2 | 3 | 0 | Image column beside enlarged headline/body; grouped badges and CTA remain intact; much better use of banner width |
| Level 3 | 5 | 0 | Headline/body now occupy useful width and rotated ribbon stays in bounds; secondary text remains too small for comfortable reading |

Level 3 sizes: headline 13.36px, body 7.35px, badges 5.46px, CTA 4.45px, ribbon 3.16px, legal copy 4.01px. These are unresolved quality limitations, not evidence of readable typography. The intentional missing asset still produces its expected placeholder; no replacement was created. Source decoration is now constrained in bounds under the conservative policy, so its original bleed is not preserved.

## Measured cost

Five warm repetitions per sample, same measurement boundaries as M0. Rounded medians:

| Sample | M0 engine | M1 engine | M0 repeat pipeline | M1 repeat pipeline |
|---|---|---|---|---|
| Level 1 | 0.0086 ms | 0.35 ms | 172.7 ms | 172.8 ms |
| Level 2 | 0.0134 ms | 3.99 ms | 150.1 ms | 154.7 ms |
| Level 3 | 0.0171 ms | 8.94 ms | 56.9 ms | 68.9 ms |

The new algorithm costs more than simple multiplication. These small local samples support only this observed tradeoff, not a statistical speed claim. Repeat pipeline means resize plus real PNG rendering/writing; import, validation, source rendering, and JSON writing are excluded. Evaluation imports the renderer before the engine to keep that startup measurement separate now that the engine uses font utilities. No memory, container, or scaled element-count benchmark has been run.

## Remaining limitations and next action

M1 exit criteria are met for the supplied cases, with visual compromises explicit. C7 offline-container validation remains unavailable without Docker; C8 generalization is not established by these samples and synthetic regressions.

The current layout chooses one fixed allocation per orientation, not several scored candidates. It can overallocate space to low-priority imagery, shrink labels too far, retain undesirable source overlaps on nearby targets, and separate ungrouped elements that were visually related. No semantic role labels are assumed. Group internal transforms preserve relationships but are not a proof of arbitrary rotated label containment. The text estimator follows current renderer behavior, including its inclusive style-run end; no renderer bug was silently repaired.

Next M2 task: introduce a small bounded set of image/text/group allocations and score hard-valid candidates for text readability and hierarchy, with explicit minimum-size quality diagnostics. Keep the M1 candidate as a baseline. Evaluate on new development design families before selecting a winner; do not claim unseen or sealed-holdout success yet. Additional visual judgment should focus on dense banners and ungrouped relationships.
