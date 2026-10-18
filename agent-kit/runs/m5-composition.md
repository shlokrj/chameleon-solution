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

# M5.2 alpha-aware image bounds

Change `feat: pack contain images by visible pixels`. Parent: the M5.1 commit. Same owner and environment as above.

Hypothesis: contain-image boxes carry large transparent margins. Measured ink covers 40% of the logo file's width and 43% of the bottle's. Packing and collision checks on boxes therefore shrink imagery and waste banner space.

Changes:
- `engine/layout.py`:
  - `ink()` caches each asset's alpha bounding box.
  - `visual_bounds()` maps that box into the contain-fitted element.
  - `flow` packs by visual bounds.
  - `new_collision` compares visual bounds.
  - `keep_on_canvas` shrinks a packed zone about its visible center until every box is on canvas. The zone stays one rigid unit, so ink stays inside its slot and boxes stay inside the canvas.
- `engine/quality.py`: the overlap proxy uses visual bounds, so transparent margin over copy is not a collision.

Two rejected intermediate designs, recorded so they are not retried:
- Clamping each unit independently pushed neighbouring images together (ink overlap, catalog@twitter-header loss 0 → 0.445).
- Shifting the whole zone inward pushed bottle ink into the copy column (loss 0 → 0.257).

Results against the M5.1 report:
- Only 3 of 70 cases changed, all improvements:
  - catalog@leaderboard: min text 5.7 → 10.3px, loss 0.138 → 0.010; button labels readable in the side column.
  - Level 2 → 300x250: min text 4.2 → 5.0px, loss 0.263 → 0.195.
  - Level 3 skyscraper: min text 3.6 → 5.3px, loss 0.323 → 0.200.
- Against the original `d97405c` baseline: zero contract issues; mean loss 0.0532 → 0.0286; cases under 6px 11 → 5; under 9px 18 → 12.
- 61 tests pass. All 15 regression fixtures have zero contract issues. The supplied-sample evaluation exits 0. Changed renders were inspected side by side.

Limitation: at one shared scale the logo stays small beside a tall product (Level 2 leaderboard logo ink ≈ 31x19px). This needs role-aware minimum sizing.

Linux container rerun: unrun.

Decision: accept.
