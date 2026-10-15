# Independent M3 text repair review

Base HEAD/origin main: c8de17fc7e7ea8e7e5b43168733aadd38baf38a6. Inspected uncommitted layout.py/resize.py changes. Exact engine hashes captured in report.json and verified unchanged before/after six-case run. Shared checkout, same inherited model, separate context and procedural isolation only; not cross-model or sealed validation. No Git, production or tracker changes by judge.

Reproduce: `.venv/bin/python artifacts/m3-text-judge/run.py`. Original rotated-copy/dense-labels inputs untouched. Four fresh deterministic variants created after inspecting repair. All six sources schema valid, all six output contracts pass, all inputs unchanged. Direct renderer source/output calls succeeded; inspected all 12 real PNGs plus fractional-grid witness PNG. No Docker, official scorer, full suite or timing benchmark.

| Case | Result |
|---|---|
| rotated-copy exposed | Repair accepted: 42px visible complete SOLSTICE versus prior 2.819px. |
| dense-labels exposed | Repair accepted: all twelve labels 42px in readable 3x4 grid versus prior 11.518px column. |
| diagonal-copy fresh | Pass: -35-degree FRESH IDEAS readable at 42px with legal extents. |
| upside-down-copy fresh | Pass: 180-degree READ BOTH WAYS remains complete, wraps to two lines at 40.0215px. |
| fractional-grid fresh | Accepted remaining P2 quality defect: imperceptible 0/0.25/0.5px within-row y offsets cause all twelve labels to revert to 11.5177px single column. |
| hierarchy-grid fresh | Complete readable output, hierarchy preserved (30.2855/18.9284px). Source grid becomes column, but no accepted readability failure because all content remains legible. |

## Fractional-grid finding

Only change from original dense-labels source is each element y += (index % 3)*0.25. Source rows remain plainly aligned to the eye, nonoverlapping, and valid. Expected: nearly identical alignment should not cause disproportionate loss of readability when a readable grid is feasible. Actual source/output PNGs show the return to a narrow vertical text column with most target width unused. Current source_grid uses 1e-6 y equality, rejecting these rows. This is an exposed limitation of grid recognition, not a hard constraint failure or a regression relative to pre-repair engine.

The existing 28px dense-labels-witness layout was independently checked against the fractional source and passes contract unchanged; copied as fractional-grid-witness.json/png and rendered. It demonstrates feasibility without altered literal text, font family, style or metadata. Original repaired exact-alignment case also renders successfully at 42px. No official minimum font rule is claimed.

Original two failure reproducers are repaired. New variants: three pass, one accepted quality limitation. Once disclosed, all four variants are development evidence, not a reusable fresh holdout. Parent owns bounded repair/stop decision.
