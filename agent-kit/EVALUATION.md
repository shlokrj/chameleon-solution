# Evaluation and efficiency gates

No official scoring implementation or numerical rubric weights were supplied. Keep local proxies labeled as such.

## Test layers

1. Contract: full schema, finite values, exact canvas, element counts/ID multisets, preserved fields and asset hashes, unchanged input including nested style runs, box and rotated extents, ordinary image proportions.
2. Semantics: group cohesion, label containment, intentional layering, text completeness/fit, image crop effects. Use renderer/font measurements; geometric overlap alone cannot distinguish correct layering.
3. Real rendering: directly import and call `render_design_to_png` from `renderer.converter.convert`; catch/report failure rather than accepting main.py's fallback as evidence. Inspect all three sample PNGs, worst cases, and every visually affected regression. Missing-asset placeholders must be identified separately.
4. Generalization: generated design families, held-out shape families, metamorphic checks, and adversarial cases.
5. Packaging: clean container build and offline full pipeline with verified output pairs. Host success does not establish container success.

## Case categories

- Supplied examples: 4 elements square-to-portrait, 11 square-to-wide, 17 portrait-to-728x90. Preserve their files.
- Valid-contract stress: schema-valid and semantically valid generated tasks, including zero dimensions where permitted. Distinguish feasible readability from irreducibly dense content.
- Robustness-only: duplicate IDs, nonfinite values, invalid dimensions/types, missing required fields, corrupt asset files. Document failure behavior; do not mix these into an official-distribution success rate.
- Renderer limitations: missing font/glyph support and unsupported rendering behavior. Reproduce independently before attributing to the solver.

## Metamorphic checks

Opaque ID renaming should preserve equivalent layout after matching identities. Changing input order with distinct z-indices should not change semantic quality. Repeated calls with the same seed/input should be deterministic. Changing one task must not contaminate another through cache state. Scaled inputs should preserve approximate relationships where absolute font minima and pixel rounding do not dominate. Identity resize should preserve a good source layout where feasible; it need not perpetuate source defects.

These are conditional properties, not unconditional pixel-equality assertions. Record tolerances and reasons before comparing candidates.

## Metrics

Report sample counts, per-family and worst-case results, hard-failure count, text overflow/clipping, unintended collision area, group violations, proportion error, and human/vision rubric judgments separately. State metric definitions and limitations. Vision evaluations should use source plus output, fixed prompts/model versions, anonymized ordering, and repeated judgment only for material ambiguity; they cannot override contract checks.

Measure engine time separately from rendering and total pipeline time. Report cold start, warm repeated runs, p50/p95/max with run counts, peak process/container memory, build/image size where relevant, and crash/fallback rates. For a tiny sample, report individual times rather than overstating percentile precision. Record hardware, OS, architecture/emulation, dependencies, seeds, and revision.

Compare on the same machine and fixtures. Use at least 5 timed repetitions for representative performance cases after a declared warmup; measure cold startup separately. Increase repetitions only if variance changes the conclusion. Sweep element count and aspect-ratio change. Include failed runs rather than silently dropping them.

## Acceptance policy

Hard constraints gate acceptance. Among valid candidates, reject material readability/brand regressions even if average speed improves. Keep the quality/runtime/memory tradeoff visible; use a Pareto comparison rather than inventing a single official score. Define project latency and memory targets after baseline measurement; the challenge gives no hard stage-one timeout and incomplete hardware limits.

Default iteration: run focused regressions per change, full development suite per milestone, and sealed holdout only after freezing a candidate. Do not repeatedly spend model tokens or render the entire suite for unrelated documentation edits.

## Release checklist

- [x] C1–C7 pass the documented local validation suites; C8 has bounded family/holdout evidence and no sample-specific branches. Known exceptions and quality limits are recorded; this does not certify hidden cases or universal correctness.
- [x] Supplied examples and development suite pass independent checks; relevant real PNGs inspected.
- [x] Holdout summary includes family counts, worst cases, and failures; exposed holdouts retired.
- [x] Runtime, memory, and fallback behavior measured; search/repair bounded.
- [x] No sample-specific branches, regenerated assets, runtime network calls, or concealed elements.
- [x] Clean `docker build --platform linux/amd64 -t my-chameleon-engine .` succeeds.
- [x] From repository root, `docker run --rm --network none -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" my-chameleon-engine` produces independently checked JSON/PNG pairs with the real renderer.
- [x] Required dependencies/weights are available at build time; dependency revisions recorded.
- [ ] Submission requirements in SOURCES resolved where applicable; README states verified instructions and limitations.

Checked items have current evidence in the [final local M4 review](runs/m4-final-review.md): 73 offline tests, three direct-render delivery pairs and current cold/warm/RSS measurements. Unchanged-engine catalogue, parity and independent review evidence remains in the M5 records. Local efficiency/packaging checks are complete; M4's full release exit stays blocked on the final unchecked submission-requirements item. Tiny secondary text is documented M5 quality debt, not an unreported hard-constraint pass. No competition submission has been made.
