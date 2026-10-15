# Exposed six-case repair verification

Reproduced the same six fixtures from prior judge run, verified JSON inputs exactly equal prior saved fixtures, and preserved original evidence. Engine hashes captured in report.json and unchanged before/after evaluation; layout.py SHA256 recorded there. Reproduce: `.venv/bin/python artifacts/m3-text-judge-repair/run.py`.

All six source schemas valid; all six independent output contracts pass, inputs unchanged, no exceptions. Inspected all twelve direct real-renderer source/output PNGs in contact.png.

Fractional-grid repair accepted: previously 11.5177px column now returns complete 42px 3x4 grid. Original rotated-copy and dense-labels remain readable at 42px; diagonal and upside-down variants remain complete and readable. Hierarchy-grid remains a readable column with preserved font hierarchy; no new visible regression accepted.

This is exposed-case verification, not a fresh holdout, and does not prove general robustness. Same inherited model, separate context, procedural shared-filesystem isolation only. Did not independently rerun the parent's 36-test suite, Docker, or full regression/benchmark suite. No Git/production/tracker modifications. All previously accepted failures in these six cases are now repaired.
