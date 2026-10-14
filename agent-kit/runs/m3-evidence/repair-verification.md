# Exposed-case image repair verification and round-2 adjudication

HEAD and origin/main verified at `3324d764acd92e2e32348b9dd35dee7156c5f23c`, with uncommitted repair files. Exact seven engine SHA256 values recorded in report.json; unchanged before/after evaluation. relationships.py hash is `4d3ab9d00f5542392301658949c3bac2022f02aa1274bcb6dd19176c6bb0ab7c`. No old manifest assumed. No Git, engine, or tracker mutations.

Reproduce `.venv/bin/python artifacts/m3-image-verification/run.py`. This is **exposed-case verification, not a fresh holdout**. Five existing valid-schema fixtures run, all inputs preserved, all returned outputs pass independent structural contract. Twelve real renders generated and inspected: five source/output pairs plus two feasibility witnesses. Witnesses independently pass contract and measured text extent. Exact JSON/PNG/report artifacts adjacent.

Accepted repair results:

- `image_supported_label`: complete EVENING EDITION now visibly readable on its dark supplied image; accepted repair of exposed contrast failure.
- `contrast-layer`: complete SOLSTICE remains on black panel; prior repair preserved.
- `zero-width-line`: width remains 0, height remains 200. Source and output still render blank; geometry repair preserved, renderer limitation unchanged.

Accepted remaining quality limitations:

- `rotated-copy`: still shrinks 28px font to 2.819175px, producing a near-invisible mark. Independent witness retains 28px and original 300x80 dimensions with only x/y placement changed on target. It passes rotated bounds and text fit, and direct PNG remains readable. Accept P1 avoidable readability regression; target is feasible, not irreducible density or renderer limitation.
- `dense-labels`: all twelve labels still become 11.517700px in one vertical column. Independent 3x4 witness retains 28px, no overlap, all boxes/font measurements fit, and renders legibly. Accept P2 avoidable readability/layout regression. No official minimum-font threshold claimed; the visible feasible witness establishes unnecessary loss.

Thus exposed image/panel/line repairs pass, but two independently adjudicated quality failure classes remain unresolved. Both are quality failures, not C1–C6 structural failures. Neither may be called fixed or hidden-set passing from this verification.

Same inherited model and separate context, procedural shared-filesystem isolation only. No new fixture generation, container validation, official scoring, full test suite, or resource benchmark. Parent integrator owns next bounded work/stop decision.
