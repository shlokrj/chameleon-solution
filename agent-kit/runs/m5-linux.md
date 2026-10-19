# M5 Linux integration verification

Date: 2026-10-18 America/Chicago. Reviewed teammate commits b2a484a, e1430e2, 98b6c6d and 5d5d09c after a clean fast-forward pull from d97405c. Integration owner: root. No engine changes in this verification step.

## Reviewed changes

Shared-scale wrapping replaces independent unit scaling; a hierarchy-aware floor helps smaller standalone copy; side-column candidates support banners; nearby-ratio layouts use extra room only when no new unit collision appears. Shape radii/stroke widths scale with their units, with the preservation policy explicitly amended. Contain-image packing and overlap scoring use cached alpha bounds, followed by rigid zone shrinking to keep full boxes on canvas. Missing images remain present as secondary placeholders. The candidate cap stays six. The contrast tiebreak was probed and rejected, not shipped. README now explains the method.

## Checks actually run

On the existing Colima Docker runtime, using linux/amd64 under Rosetta emulation on Apple Silicon:

```sh
./scripts/verify-container.sh
docker run --rm --platform linux/amd64 --network none --entrypoint sh \
  -v "$PWD/artifacts:/app/artifacts" chameleon-verify -c \
  'python -m evaluation.catalogue --output artifacts/m5-linux-catalogue && python -m evaluation.parity --output artifacts/m5-linux-parity && python -m evaluation.parity --output artifacts/m5-linux-repeat --reference artifacts/m5-linux-parity/report.json'
```

Both images rebuilt successfully (cached dependency layers); 61 tests passed offline. Production produced all three JSON/PNG pairs. Independent schema/contract checks and direct-render pixel comparison passed all three. This is an incremental rebuild, not a new no-cache dependency installation.

All 70 catalogue cases passed contract checks with no measured text overflow. Mean local loss: 0.029919; five cases have minimum text below 6px and twelve below 9px. All 42 parity cases, including the 15 saved adversarial regressions, passed structural and input-immutability checks. A second Linux run matched tasks, complete output designs, selected quality dictionaries and decoded render pixels exactly. These are exposed development/regression cases, not fresh holdouts or official scores.

[Summary and engine hashes](m5-linux-evidence/summary.json), [70 per-case results](m5-linux-evidence/catalogue.json), [delivery checks](m5-linux-evidence/delivery.json).

## Quality review and remaining work

Inspected all three production renders, dense-labels-compact, and the worst catalogue case (Level 3 at 300x250). Dense-labels-compact grouped labels improve from 6.325px in the saved M4 Linux run to 8.625px; legal copy improves from 6.654px to 9.956px. The headline falls from 18.061px to 16.897px. Its readability deficit improves from 0.164894 to 0.054598, with no measured overflow or new overlap. The small-format limitation is improved, not eliminated.

The worst catalogue case remains Level 3 at 300x250: minimum type 3.321px, local loss 0.386037. Level 3 at 160x600 has minimum type 3.823px under Linux, below the teammate's native result of about 5.3px. Do not assume the native quality measurements transfer exactly. Logo sizing and dense secondary groups remain next targets; collision-aware corner anchoring remains deferred. The overlap metric itself changed in M5, so aggregate M4/M5 loss comparisons are not controlled unchanged-metric comparisons.

The Fontconfig reset-dirs warning and intentional missing holiday badge persist; neither is concealed. No fresh judge/holdout or updated performance benchmark was run in this step. Existing M4 timings describe the older engine and must not be relabeled as M5 timings. Organizer requirements remain unresolved in SOURCES; this is not submission-readiness approval.

Local logs: artifacts/m5-linux-container.log and artifacts/m5-linux-broad.log. Local full reports/renders: artifacts/m5-linux-catalogue, artifacts/m5-linux-parity, artifacts/m5-linux-repeat and artifacts/container-check.rnugiO/output. No active ownership after this handoff.
