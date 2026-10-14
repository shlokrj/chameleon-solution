# Frozen M3 repair: independent judge

Candidate is HEAD `3324d764acd92e2e32348b9dd35dee7156c5f23c` plus engine hashes from artifacts/m3-freeze.json, copied into report.json. Canonical manifest SHA256 (`json.dumps(manifest, sort_keys=True)`) is `0e9a096302a8a425a05d9a1c33d6dc12016dea7a86199cec4a7a08357ec48187`; raw file SHA256 is `ac6aeef49e3ecca2194aca96cd37ffe5dfa8aa18f67bedc1adbeef5d7d48c137`. All seven engine hashes independently matched before and after execution. Initial raw-file digest assertion stopped before running anything; corrected verification to the supplied canonical digest, then completed evaluation.

Reproduce: `.venv/bin/python artifacts/m3-judge-final/run.py`. Deterministic literal fixtures authored here after freeze, not provided to builder until results. White-box role: read candidate layout.py before authoring fixtures. Separate same-model context, shared filesystem, procedural isolation only. No claim of sealed or cross-model evaluation.

Ran two exposed regressions and six fresh valid-contract cases. All eight source schemas valid, unique IDs, allowed metadata, source immutable, target exact, zero independent C1–C6/preservation findings. Existing asset references only. Direct renderer imported and called for all 16 source/output PNGs; all inspected in contact sheet. Warnings are recorded in report.json. Single-call engine timings are diagnostic only. No Docker, official scorer, full regression suite, or performance benchmark run by judge.

| Case | Expected invariant and result |
|---|---|
| contrast-layer (exposed) | Original white text fully readable on preserved black support. PASS: complete SOLSTICE remains on black panel; accepted repair of the demonstrated shape-supported case. |
| zero-width-line (exposed) | Identity resize should preserve its nonzero 200px longitudinal extent. PASS in JSON: height remains 200, width 0. Source/output still blank due renderer; no claim of visible renderer repair. |
| two_label_panel (fresh) | Two independent labels retain readable shared background. PASS visually, complete labels on black panel. |
| image_supported_label (fresh) | White label originally contained over dark supplied gradient remains readable on supported background. FAIL: output moves text away from image and entire label disappears against white canvas. |
| side_by_side_cards (fresh) | Two ungrouped supported labels preserve respective card relationships during portrait reflow. PASS: both labels still contained and readable. |
| explicit_translucent_group (fresh) | Explicit group with opacity preserved and complete label on support. PASS, though small typography is a quality limitation. |
| styled_multiline (fresh) | Explicit newline, style run, max-lines and complete literal text preserved and visibly fit. PASS; complete three-line output. |
| empty_caption (fresh) | Empty source text remains valid without crash, addition, removal, or invented visible copy. PASS. |

## Accepted unresolved failure

`image_supported_label.json` is minimal: supplied solstice_bg_gradient.png in a 440x160 cover image, white EVENING EDITION label fully inside, distinct z-indices, no grouping. Source 600x600 to target 900x300. The literal source and output are adjacent, together with real source/output PNGs. Source has readable white text on dark image; output image occupies a left region while white text shifts to the right onto white canvas and becomes invisible. This is the same high-level loss of contrast-support class on a different valid substrate (image rather than shape). The shape-specific repair is accepted, but does not establish general contrast/layering preservation. SPEC quality objectives 1 and 4 violated; not a hard geometry/identity-schema failure. Priority P1 because all message text vanishes despite feasible sparse layout.

Fixture remains unchanged and should now retire to exposed regression evidence if repaired. Further final-pass claims require a new freeze and genuinely fresh cases, within remaining protocol budget. Zero structural errors do not establish visual correctness; final six-case holdout contains one failure.
