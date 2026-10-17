# M4: reuse cached typefaces during fitting

Date: 2026-10-17 America/Chicago. Baseline 338b50c. Change `perf: reuse cached typefaces during text fitting`.

## Change and correctness

Engine text measurement previously invoked the renderer helper that reconstructed a Skia typeface on every call, despite already having a 64-entry typeface cache. It now creates each local size-specific Font from that cached typeface and reuses the base glyph advances/height when the base style actually occurs. Fully overridden styled text does not inherit unused base metrics. Font objects and glyph arrays remain local; no new cache or runtime dependency. Renderer code, font assets, wrapping, layout search and scoring are unchanged.

47 tests pass. Added tests compare directly against unchanged renderer font operations across fractional sizes, wrap widths, Unicode/newlines/empty content, fully styled text and interleaved sizes. [Independent static review](m4-font-evidence/REVIEW.md) found no actionable regression; review is same-model separate-context, not cross-model validation. Optional mocked unequal style-height coverage remains a possible test improvement.

[Exact parity evidence](m4-font-evidence/parity.json): 42 cases have identical task data, output JSON and decoded RGBA pixel hashes before/after; all independent structural checks pass. Cases include three supplied examples, twelve development layouts, fifteen saved adversarial tasks, six scaling tasks and six typography variants. Brand/source files are unchanged. Intentional missing holiday-badge warnings persist in both supplied-case renders. Parity preserves known readability limits; it does not fix them.

## Sequential paired performance

[Raw timing and memory evidence](m4-font-evidence/profiles.json). Baseline was an isolated git archive of 338b50c using the same Python environment and assets. Baseline profile completed before candidate profile started; parity runs followed profiling. Nine cases, each with separate cold/warm processes and five measured warm repetitions following a first run. Both profiles verified stable code hashes; all 36 workers succeeded. Local macOS arm64 / Python 3.12.13; dependency versions and renderer source revision are recorded.

| Case | Baseline warm engine median (ms) | Candidate warm engine median (ms) | Ratio |
|---|---:|---:|---:|
| chameleon_sample_level1_warmup | 0.46 | 0.21 | 2.18× |
| chameleon_sample_level2_core | 1.07 | 0.53 | 2.03× |
| chameleon_sample_level3_advanced | 38.74 | 16.64 | 2.33× |
| scale-12-wide | 1.79 | 1.18 | 1.51× |
| scale-12-portrait | 10.47 | 1.94 | 5.40× |
| scale-48-wide | 245.52 | 39.94 | 6.15× |
| scale-48-portrait | 242.08 | 39.21 | 6.17× |
| scale-120-wide | 1209.42 | 174.65 | 6.92× |
| scale-120-portrait | 662.89 | 139.22 | 4.76× |

These are engine-only speedups, not end-to-end rendering speedups. Cold process wall includes imports, validation, rendering and report I/O; OS caches were not cleared. Whole-worker peak RSS was lower in each pair (roughly 0.3–25 MiB), but it includes interpreter, rendering and validation, so it is not a precise engine allocation saving. The existing cache remains capped at 64 typefaces, with immutable brand fonts assumed during the process. No cache of text, sizes or glyph arrays was added.

## Reproduction and handoff

Run evaluation.profile from baseline and candidate checkouts sequentially. To compare historical typography correctly, copy the current evaluation/parity.py into the isolated baseline checkout (the baseline already has evaluation/profile.py), then run:

```sh
# Baseline checkout, using the same virtual-environment interpreter:
python -m evaluation.parity --output /absolute/path/parity-before
# Candidate checkout:
python -m evaluation.parity --output artifacts/parity-after --reference /absolute/path/parity-before/report.json
python -m evaluation.profile --output artifacts/profile-after
python -m unittest discover -s tests -v
```

Local baseline archive and full JSON/PNG/profile artifacts are under artifacts/m4-font-baseline, m4-parity-before/after and m4-font-before/after. The compact tracked records preserve raw repetitions and hashes. The older evaluation.compare tool deliberately rejects historical typography differences; use isolated full-checkout parity/profile comparison for this change rather than bypassing that guard.

M4 remains in progress. Next measured opportunity: reuse bounds in pairwise overlap checks without changing scores; assess scaling costs on the existing 48/120-element tasks. Then complete reproducible dependency/offline packaging validation. Docker is still absent from PATH, so container build/runtime, image size and offline linux/amd64 behavior remain unverified. Dense-layout readability and small uniformly scaled group text remain documented quality limitations.
