# Fixed-budget candidate-slot comparison

2026-10-22, baseline `8156e7a` (production engine from `a411461`). Builder evaluation only; no fresh holdout or independent judge. **Reject all five direct slot replacements; production remains unchanged.**

The study tests replacing each non-baseline slot with image share 0.15/group share 0.35, using side groups for wide canvases and bottom groups for tall canvases. Each slot retains its existing text-grid setting. It exercises the actual selection/refinement pipeline by temporarily wrapping `build_layout` in an offline evaluator. The wrapper is serial, process-global test machinery and must not be used concurrently or in production. Runtime search remains capped at six; no extra runtime candidate was added.

Seven source families × 17 targets = 119 layouts per slot, 595 comparisons. Targets comprise the existing ten-format catalogue plus 299/300/301×300, 599/600/601×300 and 161×600. Each replacement was evaluated twice with exact JSON equality, unchanged source inputs, and independent contract checks. Final outputs are compared against the released engine, including per-element 5% text/20% image short-edge guards.

| Slot | Changed | Better local loss | Worse local loss | Cases violating final-output guard | Contract failures |
|---|---:|---:|---:|---:|---:|
| 1 | 23 | 5 | 0 | 1 | 0 |
| 2 | 23 | 5 | 2 | 2 | 0 |
| 3 | 16 | 5 | 2 | 3 | 0 |
| 4 | 8 | 5 | 1 | 1 | 0 |
| 5 | 7 | 5 | 2 | 2 | 0 |

Slot 1 is the strongest aggregate result but fails on Level 3 wide-banner: CTA 18.068→16.076px and ribbon 16.426→14.614px, roughly 11% smaller. Both layouts have zero local loss, illustrating saturation of the readability proxy. Existing runtime safeguards compare to candidate zero, not to the previous release's final selected output. Therefore a changed candidate set can pass runtime checks while regressing the released result.

Slot 1 improves Level 2 leaderboard, Level 3 leaderboard/skyscraper/161×600, and dense-label leaderboard. Ten before/after PNGs for the four catalogue improvements and the regression were inspected directly. Improved secondary groups are visible; the wide-banner composition materially changes and shrinks CTA/ribbon. The 161×600 boundary case was checked structurally and for exact repeatability, not separately visually adjudicated. No universal quality or official scorer claim.

All 73 tests pass offline Linux/amd64; the production engine and image are unchanged. Full local reports/renders live under `artifacts/slot-probe/`. Tracked [summary](m5-slot-probe-evidence/summary.json) and [changed cases](m5-slot-probe-evidence/changed-cases.json) preserve the rejection evidence. No runtime speed benefit is claimed.

## Reproduce

After building the verification image, from repository root:

```sh
docker run --rm --platform linux/amd64 --network none -v "$PWD:/app" --entrypoint python chameleon-verify -m evaluation.slot_probe --output artifacts/slot-probe
```

The command writes all 595 rows and the summary. It is an experiment, not an acceptance command: exit zero means the study finished, not that replacements are safe.

## Next step

Stop blind allocation-slot tuning. Investigate compact legal-copy geometry and whether its existing text region can fit larger type while preserving hierarchy and all other output elements. If returning to candidate changes, design a source-derived selection rule with final per-element evidence; do not exempt the wide-banner sample by ID or target size, relax the guards, or double the runtime budget simply to retain the old winner. M4/M5 quality and organizer release questions remain open.
