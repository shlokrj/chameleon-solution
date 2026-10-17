# M3 backing ancestry repairs and bounded-cycle closure

Date: 2026-10-17 America/Chicago. Parent revision cb694d5; change `fix: preserve large and nested backing relationships`.

## Changes

Large inset backing panels are now identified by containment and paint order, without the former 80%-of-canvas cutoff. True unrotated full-canvas backgrounds remain independently resized. Starting at supported text, inference follows enclosing backing ancestors in strictly earlier paint order. This preserves nested frames and shared ancestors without cycles. Unrelated shape-only compositions and explicit groups remain outside inferred relationships. Connected units merge without changing element order, IDs, grouping fields, assets or styles.

The existing quality diagnostic also checks the newly inferred parent/child relationships. Geometry and six-candidate budget remain bounded as before; ancestor lookup is cached per call. This is geometric inference, not image-pixel contrast analysis or arbitrary translucent-layer reasoning.

## Validation

- 44 unit tests pass, including large inset boundaries, shared ancestors, nesting, reordered input with distinct paint order, equal-z cycles, explicit-group exclusions, immutable input, and quality diagnostics for broken nesting.
- All 15 saved adversarial tasks pass independent structural checks and direct real rendering. Both original repair renders inspected by root and judge.
- All 15 supplied/development comparison cases pass independent contract checks. Selected JSON outputs match the previous text-repair comparison exactly. Five warm timing repetitions per case: medians 0.27–39.11 ms on local macOS arm64 / Python 3.12.13. [Comparison record](m3-layer-evidence/comparison.json) uses historical M1 6d1dbe5 as its timed reference; no speedup claim against the immediate predecessor.
- Judge independently accepted M3-R3/R4, then four new frozen-engine interaction cases: reversed distinct-z order, branching ancestry, full-canvas parent boundary, and explicit group/equal-z ordering. All six source/output pairs visually pass; no new accepted defect. [Judge report](m3-layer-evidence/JUDGMENT.md), [hashes and results](m3-layer-evidence/report.json).
- Judge cases are tracked under tests/fixtures/m3 with hyphenated names; historical artifacts/ paths in the report refer to local ignored PNGs/scripts. Reproduce their structural checks and renders with evaluation.regressions.

## Milestone disposition and limitations

Close M3's bounded adversarial-hardening cycle: accepted R1–R4 defects and fractional-grid alignment were repaired and independently verified; the final four fresh interaction cases found no new accepted failure. This closes a bounded engineering milestone, not a claim of universal robustness, a sealed benchmark, or a submission-ready engine. All disclosed cases are now development evidence. Judge used the same inherited model in a separate context with shared filesystem/procedural isolation; the latest cases are nearby interactions rather than a broad distribution sample.

Worst remaining quality tradeoffs: uniform group scaling leaves large-inset and branching labels at 13.8px with spare canvas space; nested label is 15.456px. Stretchable-panel layout could improve these. Dense extreme banners and high-element-count scaling cases can still yield much smaller text. Geometric support inference does not guarantee contrast for arbitrary image pixels, translucent panels, or partially overlapping objects. Source-renderer thin-line/stroke limitations remain documented separately.

M4 remains in progress. Next: use the recorded profile to reduce repeated font measurement/typeface work and overlap geometry work, preserving outputs and bounded memory, then rerun paired performance/quality checks. Docker remains unavailable from prior checks; offline linux/amd64 packaging and release checklist are not complete.

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m evaluation.regressions --output artifacts/regressions
.venv/bin/python -m evaluation.compare --baseline 6d1dbe5 --output artifacts/comparison
```
