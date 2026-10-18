# M5.1 composition: shared-scale packing, type floor, banner column, near-ratio room

Date: 2026-10-18 America/Chicago. Parent `d97405c`. Change `feat: pack units at shared scale with readable type floor`.
Owner: Aadhitya Balaji with a Claude Code session (Claude Opus 5.5); single builder, no independent judge for this step.
Environment: macOS arm64 native, Python 3.12.13 venv from requirements-dev.txt. Linux container run not repeated for this step (unrun).

## Hypothesis

A code review plus a hand trace of Level 3 → 728x90 found four general causes of weak extreme reflows:
- `stack` scaled each unit independently, so a large CTA rendered smaller than small badges (inverted hierarchy).
- `stack` used a fixed direction, so images were stacked vertically in a narrow column on banners.
- One shared text scale drove fine print to 2–4px.
- The missing-asset placeholder took a hero image slot.

Also, near-ratio targets (portrait, story) left extra room as empty bands.

## Changes

- `engine/layout.py`:
  - `flow` replaces `stack`. It wraps units into centered rows at a single shared scale, found by bisection and capped at `max(sx, sy)`.
  - Shapes scale `corner_radius`/`stroke_width` with their unit.
  - `text_stack` sizes copy as `max(k·orig, min(10px, 0.7·k·largest))`, capped at `orig·upper`. Order and headline dominance are preserved.
  - Images whose asset file is missing (renderer `asset_path`) join the secondary group zone.
  - New `group_side` banner archetype: groups get a full-height right column.
  - The near-ratio path tries the geometric-mean scale, then a midpoint, then `min(sx, sy)`, keeping the first scale that adds no new unit collision.
- `engine/resize.py`: two of the five wide share-sweep candidates become side-column candidates. The candidate budget is unchanged (6).
- `engine/quality.py`, `evaluation/contract.py`: `corner_radius` and `stroke_width` are mutable (see the SPEC preservation note).
- `evaluation/catalogue.py`: sweeps 3 samples and 4 development families across 10 catalogue formats. It writes renders, contact sheets and a report, with `--reference` deltas.
- `tests/test_composition.py`: 5 new tests.

## Commands actually run

```sh
.venv/bin/python -m unittest discover -s tests            # 60 tests OK
.venv/bin/python -m evaluation.catalogue --output artifacts/m5-final --reference artifacts/m5-baseline/report.json
.venv/bin/python -m evaluation.regressions --output artifacts/m5-regressions   # 15/15 zero contract issues
.venv/bin/python -m evaluation.baseline --output artifacts/m5-current          # supplied samples pass
```

The baseline renders came from an isolated `git worktree` of `d97405c`.

## Results (70 catalogue cases, local proxies only)

| Measure | Baseline `d97405c` | This change |
|---|---|---|
| Contract issues | 0 | 0 |
| Mean local loss | 0.0532 | 0.0332 |
| Cases with min text < 6px | 11 | 6 |
| Cases with min text < 9px | 18 | 13 |
| Level 3 → 1200x628 min / max text | 5.4 / 44.1px | 11.5 / 44.1px |
| event → 728x90 min / max text | 3.4 / 21.4px | 9.4 / 28.7px |
| Engine median, Level 3 sample | 0.019s | 0.019s |

Visual review (inspected PNGs):
- CTAs now dominate badges.
- Logo and product wrap instead of being squeezed into one column.
- The Level 2 leaderboard gains a large right-column CTA.
- Portrait targets use their extra height.
- Changed adversarial fixtures stayed equivalent. Single-unit fixtures (contrast-layer, image-supported-label) now keep margins rather than touching the edges, because of the upscale cap.

Regressions (accepted tradeoffs, recorded rather than hidden):
- Nine cases have a smaller minimum font. Mostly badges give a few px so the CTA keeps its source dominance; Level 2 fb-link badge goes 23.6 → 20px.
- Level 3 skyscraper secondary units: 4.4 → 3.6px. Six width-limited units share one scale, so they stay unreadable either way.
- Level 3 leaderboard loss: 0.329 → 0.359. Headline 13.4 → 11.5px while body/legal rise to 10px.
- Worst case remains Level 3 → 300x250 (loss 0.386, down from 0.803).

## Unrun checks and limitations

- No Linux container run or Linux parity for this revision. Rerun `./scripts/verify-container.sh` before release.
- No independent judge or fresh holdout. The catalogue families are exposed development cases.
- Dense content in very small formats (300x250, 160x600, 728x90) still produces sub-9px secondary labels.

## Next bounded step

- Corner/edge anchoring for badges and stickers.
- Alpha-aware visual bounds for contain images.
- Render-in-the-loop contrast as a tiebreaker.

Decision: accept.
