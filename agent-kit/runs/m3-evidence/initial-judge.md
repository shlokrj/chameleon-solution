# Independent judge pass at 3324d76

Frozen revision and origin/main both verified as `3324d764acd92e2e32348b9dd35dee7156c5f23c`. Six independently authored valid-contract cases; no supplied/development fixtures or challenger artifacts inspected. Same inherited model, separate context, shared filesystem with procedural isolation only; not sealed or cross-model validation. No memory used. No production or Git mutations.

Reproduce from repository root: `.venv/bin/python artifacts/m3-judge/run.py`. Input/output JSON, direct real-renderer source/output PNGs, diagnostics, and single-call engine timings are adjacent. Timing is diagnostic only, not a benchmark. Font initially used during fixture drafting was unavailable Montserrat; fixtures were corrected to the provided Solstice Sans before final evaluation to remove fallback confounding. Source schema validation passes for all six; unique IDs, finite dimensions, allowed zero-height rule, provided image asset, intact source input. All six return zero independent structural-contract findings and no renderer-returned warnings. Direct render import/call succeeded; no whole-image fallback.

Inspected all 12 source/output renders in contact.png.

| Case | Judgment |
|---|---|
| rotated_badge | Pass: rotated label remains visibly inside badge, all extents in bounds. |
| zero_rule | Structural pass. Source and output rule invisible because renderer does not visibly draw zero-height line; preexisting renderer limitation, not accepted engine regression. Text complete and readable. |
| spaced_title | Structural/visible fit pass with quality limitation: 28px title becomes 13.737px despite large unused vertical space. A 28px manual layout wrapping across two lines is feasible (spaced_title_feasible.json/png). This establishes a readability/layout tradeoff, not hard violation: source one-line rhythm differs from alternative, no official minimum font exists. |
| border_extent | Structural pass. Renderer ignores the declared red stroke even in source; cannot attribute absence or missing stroke extent to engine. No visible output bleed. |
| product_and_copy | Pass: asset identity/proportion and literal newline preserved; text complete. Product is small in a sparse tall composition, subjective weakness without accepted invariant violation. |
| unbroken_contact | Pass: full token visible and fits, still legible. |

**Accepted new engine failure classes: zero.** Two renderer limitations (stroke and zero-height line invisibility) and two quality observations, none presented as proof of a hard defect. Six hand-authored cases are not distribution evidence or proof of general robustness. The manual spacing alternative is diagnostic and is not counted as a seventh independent case. No Docker, container, official scorer, or performance sweep run. Source/output do not mutate assets; production asset files were never written by this runner.

Cases are now exposed to builder and should be considered development/regression evidence if used for fixes. Judge remains available for independent challenger adjudication and a fresh bounded pass after the next explicit candidate freeze.
