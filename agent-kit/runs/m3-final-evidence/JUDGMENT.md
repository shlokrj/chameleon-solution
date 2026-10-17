# Final bounded fresh review at b7515b9

HEAD and origin/main independently verified at b7515b9148f4b8b0591e48232b50f1dcd4a282fb. Initial tracked modification was the integrator-owned PROGRESS.md; judge did not modify it. All engine file hashes recorded in report.json and unchanged before/after execution. Brand-kit hashes recorded and unchanged. Judge owns only this artifact directory; no Git/production/tracker mutation.

One batch of six new deterministic, valid-contract cases, following chameleon-challenge and ADVERSARIAL. White-box: inspected relationships.py after freeze before constructing inputs. Same inherited model in a separate context, shared filesystem with procedural isolation only, neither cross-model nor sealed holdout. Cases now disclosed are exposed development evidence. No repair round undertaken.

Reproduce from repository root: `.venv/bin/python artifacts/m3-final-review/run.py`. Script verifies revision, writes six literal fixtures, calls direct real renderer, checks input immutability and independent output contract, records candidate diagnostics and engine/asset hashes. It also reproduces two manually specified feasible witnesses. All six source schema validations and all six output structural checks pass, inputs unchanged, no exceptions, renderer warnings empty. Inspected all twelve source/output PNGs plus both witnesses. No full test suite, Docker, official scoring, runtime or memory benchmark run by judge.

| Fresh case | Expected invariant | Judgment |
|---|---|---|
| opposed_rotation_pair | Two opposing rotated labels remain complete, in bounds and readable without new collision. | Pass: both preserved clearly. |
| grid_with_group_footer | Mixed grid and explicit label/background group retain readable content and intended relationships. | Pass: readable 3x2 grid and contained footer label. |
| large_inset_backing | White text retains contrast support from a large inset black panel. | Accepted P1 visible completeness defect: part of initial A disappears on white canvas. |
| full_bleed_and_badge | Full-canvas background and contrasting explicit badge preserve complete text and contrast. | Pass: title and badge remain readable; sparse portrait layout is a design tradeoff. |
| multiline_rotated | Explicit newline, rotation and full text survive with readable wrapping. | Pass: complete rotated three-line output, no clipping found. |
| nested_support_panels | Intentionally nested outer frame, inner panel and label remain nested where feasible. | Accepted P2 layering/relationship limitation: outer and inner become disjoint. Text remains readable. |

## Worst case: large inset backing

Minimal two-element source 600x600: black rectangle (20,20,560,560), white AFTER HOURS text (80,180,440,90), 28px; distinct z order. Target 900x300. Source is visibly complete. Output panel (30,10,280,280), text (12,120.5998,876,58.8004), 42px. Initial glyph begins at x=12 outside panel, and its left part disappears on white canvas. Direct full-resolution PNG confirms partial missing A. This violates readable complete text on the actual composited background and preservation of intentional layering (SPEC quality objectives 1/4), despite all JSON/box constraints passing. It is not clipping caused by insufficient target space.

Source backing occupies 87.11% of canvas; support_pairs excludes rectangles at or above 80%, while full-canvas special handling does not apply to an inset panel. This explains the observed case without claiming every large panel must always follow one layout policy. Witness stretches this shape to (20,10,860,280) and retains 28px text at (70,100,700,90). It preserves all immutable fields, passes contract, and renders the entire phrase. Shape stretching is allowed. No source alteration was used to make output pass.

## Nested layering limitation

Three-element source nests black inner panel entirely within gray outer rectangle, with readable white label. Output outer bounds y=125..300; inner bounds y=316.35..433.65, so they no longer overlap at all. This breaks the clear intentional nested-frame composition (quality objectives 3/4), though text is complete and hierarchy judgment is less objective than missing glyphs. Accepted as P2 relationship quality failure, not hard contract failure. A uniform half-scale source placement fits 300x750, preserves nesting and 14px label, passes contract, and renders legibly; no density impossibility.

## Limits and final result

Four cases pass visible expectations; two reproducible quality defects remain. Zero hard structural findings does not establish visual correctness. No claim of M3 universal robustness, official score or submission readiness. Previously documented source-renderer line/stroke limitations, dense-banner readability and container validation were not re-evaluated by this batch. Root owns milestone disposition and any later explicitly scoped repair cycle; this authorized batch is complete.
