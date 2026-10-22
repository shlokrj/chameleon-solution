# M5 fresh challenger cases

Six deterministic hand-authored cases, created against frozen `34edde9` on 2026-10-22; no RNG. The challenger had isolated context and the same inherited model configuration as the builder/judge (exact model identifier unavailable). This is independent role review, not verified cross-model evaluation.

Cases cover a rotated alpha logo, grouped pill labels, mixed image/text units, styled text and newlines, a stroked frame, and two buttons with an alpha logo. Supplied assets and fonts are unchanged. Sources and outputs were rendered and inspected. All six source schemas and output contracts pass. The frame's gray fill/absent stroke is already present in the source renderer and is not an engine defect.

The pill case established a feasible same-box 9px witness for baseline 6.264px labels. The accepted repair reaches 9.321px. See [independent adjudication](../../../agent-kit/runs/m5-fresh-review-judge.md). These cases are now exposed development regressions.

After building the verification image, reproduce from repository root:

```sh
docker run --rm --platform linux/amd64 --network none -v "$PWD:/app" --entrypoint python chameleon-verify -m evaluation.regressions --fixtures tests/fixtures/m5-review --output artifacts/m5-review
```
