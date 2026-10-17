# M3-R3/R4 independent repair verification

Base HEAD and origin/main verified at cb694d564b82acce0fe768472395c77a65fe5197. Reviewed uncommitted relationships.py/layout.py repair. Exact engine file SHA256 values recorded in report.json; all unchanged before/after six-case execution. Judge changed only this artifact directory. No Git/production/tracker mutation.

Reproduce `.venv/bin/python artifacts/m3-layer-judge/run.py`. Two original exposed fixtures copied without edits; four fresh deterministic variants target reversed input with distinct paint ordering, branching backing ancestry, full-canvas parent boundary, and explicit grouping with equal z-index. Same inherited model, separate context with shared filesystem/procedural isolation, not cross-model or sealed evidence. White-box review.

All six sources schema-valid; all six independent output contract checks pass; inputs unchanged; no exceptions or renderer warnings. Inspected all twelve direct real-renderer source/output PNGs plus the full-resolution large-inset output. No missing assets or whole-render fallbacks. No full unit suite, Docker or performance benchmark run by judge.

| Case | Expectation / result |
|---|---|
| large_inset_backing | PASS; entire AFTER HOURS now readable on black backing, including first A. Font 13.8px, uniformly fitted panel; smaller than a feasible stretched-panel alternative but no text invisibility. Accepted repair of original P1. |
| nested_support_panels | PASS; inner panel remains inside gray outer frame, white label contained and complete at 15.456px. Accepted repair of original P2. |
| reverse_input_distinct_paint | PASS; reversing source list with distinct z-index preserves exactly the same per-ID geometry and font sizes as nested original. |
| branching_ancestry | PASS; two labeled inner panels remain within shared outer panel, no ancestry loss or duplication. Complete labels at 13.8px. |
| full_canvas_parent_boundary | PASS; true full-canvas gray background fills target; inset black panel and complete label retain contrast. |
| equal_paint_explicit_group | PASS; explicit complete-card group and equal-z source paint order preserved, nested appearance retained. |

Six cases pass scoped structural and visible expectations; no new accepted failure. Small typography and unused space in uniform group scaling remain quality tradeoffs: large-inset and branching cases retain only 13.8px text despite available horizontal/vertical space. This is reported as a limitation, not a hard failure or proof that current typography is optimal. The repair does not establish arbitrary translucent, overlapping or image-pixel contrast inference.

These four fresh variants are nearby interaction cases, not a broad independent distribution sample. Once disclosed, they are exposed development evidence. No universal robustness, official score, container success, or release-readiness claim. Parent owns integration and milestone disposition.
