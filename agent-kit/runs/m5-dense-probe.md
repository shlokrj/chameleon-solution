# Dense Level 3 allocation feasibility study

2026-10-22; frozen production revision `a411461`. This bounded builder study follows the grouped-label review. No agent tournament or production algorithm change. The sample targets are exposed development cases, not holdouts.

`evaluation.dense_probe` explores image shares 0.15/0.25/0.35/0.45/0.55 and group shares 0.20/0.35/0.50/0.65/0.80. Wide canvases test bottom and side groups (50 alternatives); tall canvases test bottom groups (25). It applies existing image/text refinements, full contract checks, final-output regression safeguards (at most 5% text shrink and 20% image short-edge shrink), and no increased unintended overlap. Candidates are ranked by overflow then local loss. This is 125 alternatives across three tasks, deliberately beyond the runtime six-candidate budget. The baseline remains the fallback. Source schema and unchanged nested input are checked.

| Target | Baseline → witness minimum font | Local loss | Allocation |
|---|---|---|---|
| 728×90 | 4.908 → 5.698px | 0.2230 → 0.1635 | image 0.15; side groups 0.35 |
| 300×250 | 3.333 → 3.333px | 0.2520 unchanged | baseline retained |
| 160×600 | 4.733 → 5.333px | 0.2235 → 0.1328 | image 0.15; bottom groups 0.35 |

The tall witness raises badge labels 4.733→6.507px, while legal copy remains 5.333px. The banner raises badge labels 4.908→5.698px but shrinks headline/subhead/legal copy about 1.6%, within the existing guard. All selected outputs have zero contract issues, measured overflow, support violations or new overlap. These are feasible improvements, not fully readable solutions. Failure to find a better compact rectangle is not proof of infeasibility.

All six baseline/witness renders were inspected in a paired contact sheet. The compact output is unchanged; the banner enlarges the label region and the tall layout reallocates space from imagery. Tiny copy and the intentional missing holiday-badge placeholder remain visible. A second full probe exactly reproduced all three selected JSON outputs. 73 existing tests pass offline Linux/amd64 with networking disabled. No latency improvement is claimed; production remains unchanged. Full per-candidate rejection reasons and metrics are retained in [report.json](m5-dense-probe-evidence/report.json).

## Reproduce

Use the supplied Level 3 task, replacing only `target_canvas` with each target above in a temporary task file. From repository root after building `chameleon-verify`:

```sh
docker run --rm --platform linux/amd64 --network none -v "$PWD:/app" --entrypoint python chameleon-verify -m evaluation.dense_probe --task artifacts/task.json --output artifacts/dense-study
```

The output includes source, baseline and best JSON/PNG pairs plus the complete report. Local study artifacts are in `artifacts/dense-probe/`. No supplied input or brand asset was edited.

## Next bounded step

Compare a 0.15 image-share alternative against an existing candidate slot across the full 70-case catalogue and nearby target ratios, with final-output text/image guards and direct render review. Keep six runtime candidates; do not transplant sample-specific targets or IDs. Only adopt a slot replacement if generalized gains justify losses and cost. Independently investigate the compact rectangle's legal-copy allocation; a wider search alone has not solved it. M4/M5 and organizer release questions remain open.
