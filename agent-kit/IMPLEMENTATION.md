# Implementation plan

This is a proposed approach, not a challenge-mandated architecture. Change it when measurements support a better one.

## Milestone 0: establish evidence

Inspect repository status and environment. Run the starter on the three supplied cases; capture actual JSON, direct real-renderer PNGs, warnings, engine time, and full-pipeline time. Establish independent C1–C8 checks from SPEC. Preserve baseline outputs outside submission output directories. Do not install new runtime models before establishing this baseline.

Exit: reproducible baseline and an honest list of failures; real rendering confirmed or explicitly blocked.

## Milestone 1: deterministic reflow

Infer soft roles from source geometry, typography, group membership, spatial relationships, and stacking; IDs are identifiers, not semantic labels. Use source evidence to distinguish backgrounds, foreground imagery, text hierarchy, and deliberate overlap. Preserve uncertain relationships rather than inventing confident labels.

Treat explicit groups as layout units with internal constraints (e.g. label inside button). Consider a small number of general arrangements such as preserved topology, vertical stack, horizontal split, or grid. Choose arrangements from available space and element relationships, not exact resolution lookup tables. Preserve ordinary image aspect ratios; account for rotation when computing available bounds.

Fit text using brand-font glyph measurements and renderer wrapping behavior. Measure width and full block height; preserve content and style-run offsets. Keep typography hierarchy as a quality objective and avoid shrinking every item merely to make a box check pass.

Exit: all supplied cases produce contract-compliant outputs, with remaining visual compromises explicitly reported. Add generalized regressions for each discovered defect.

## Milestone 2: bounded candidate selection and repair

Use a small configurable candidate budget. Reject hard-invalid candidates before expensive rendering. Rank survivors using separate measures for text fit, unwanted overlap, group integrity, alignment, hierarchy, and source faithfulness. Do not let a weighted aesthetic score cancel a hard contract violation.

Render only a bounded shortlist when proxy geometry cannot distinguish candidates. Bound repair loops and detect repeated layout fingerprints/no improvement. Keep the best valid candidate encountered. If no candidate passes hard checks, report an explicit failure in the evaluation harness; never silently present invalid output as validated. Any production failure policy must remain compatible with the starter return contract and be tested separately.

Exit: improvements measured on unseen development families, with deterministic fallback and bounded work.

## Milestone 3: adversarial hardening

Follow ADVERSARIAL. Fix classes of failure, not specific fixtures. Use a fresh sealed holdout after development cases have influenced implementation. Keep contract failures, visual flaws, robustness-only invalid inputs, and renderer limitations distinct.

Exit: bounded rounds completed and the final report lists worst cases and remaining limitations, not just average quality.

## Milestone 4: efficiency and delivery

Profile first. Cache immutable font/asset metadata and repeated measurements using bounded keys that include text, font/style, size, and width as appropriate. Reuse work across candidates. Avoid full rendering or quadratic pair checks when a cheaper equivalent works; use spatial pruning only when scale justifies it. Benchmark cold and warm paths separately.

Try optional local model assistance only if a controlled comparison shows a useful quality gain within offline/resource constraints. Development-time model collaboration does not require inference in the shipped engine. Unconfirmed approved-model rules block claiming such a model is submission-ready.

Exit: complete EVALUATION release checklist and update the concise project README with verified run instructions and limitations.
