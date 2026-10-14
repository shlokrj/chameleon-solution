# M2: bounded candidate selection

Implemented a maximum of six deterministic candidates: the M1 layout plus five alternative image/group allocations. M1 remains the fallback. Output-contract checks precede scoring; duplicate layouts are not rescored. If no candidate is structurally valid, the engine raises a clear failure instead of returning knowingly invalid output. There is no open-ended repair loop or rendering inside search. `resize_with_diagnostics(..., max_candidates=1..6)` exposes development diagnostics without adding fields to the returned design.

Local quality measures report estimated text overflow, a 12px readability threshold, source font-hierarchy inversions, and increased foreground overlap relative to the source. These are explicitly proxies, not official weights, a contrast check, or proof of visual correctness. Selection rejects alternatives shrinking any existing text more than 5%, shrinking foreground image short edges more than 20%, or increasing the overlap proxy. These project guardrails were tightened during development after initial comparisons exposed excessive copy shrinkage. They do not guarantee every visual relationship is preserved.

## Validation

23 tests pass, including hard-invalid candidate rejection, explicit all-invalid failure, duplicate handling, configurable budget limits, and protection of group-label sizes. All 15 comparison tasks pass the independent schema/contract checks: the three supplied samples and 12 new development cases across editorial, product catalogue, event, and dense-label families at three targets each. Input immutability and repeat determinism were checked. These families informed development and are **not a sealed holdout**.

The paired reference loads the trusted M1 engine at `6d1dbe5` and verifies its typography file matches the current unchanged implementation. Five timed repetitions alternate baseline/candidate order per case. Every source, baseline, and selected candidate was rendered directly. The three changed output pairs were visually inspected; the other selected JSON outputs equal the reference. No production renderer or source sample changed.

| Development case | Local loss, M1 -> M2 | Observed result |
|---|---|---|
| catalog-compact | 0.112 -> 0.071 | Larger labels and less wasted image-column width; smallest type 6.325 -> 7.475px |
| dense-labels-story | 0.027 -> 0.000 | Much larger grouped labels; smallest type 9.488 -> 12.133px |
| dense-labels-compact | 0.165 -> 0.053 | Larger badges; compact body wraps less; minimum remains small at 6.485px |

The other 12 cases retain M1. In particular, Level 3 still has tiny secondary text: improving aggregate label scores was not enough to justify shrinking the main copy. Zero structural failures is not a claim of readable dense banners.

## Reproduction and cost

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m evaluation.compare --baseline 6d1dbe5 --output artifacts/m2-verified
```

See [full report](m2-selection-report.json) for parent revision, engine/evaluation hashes, per-case metrics, candidate eligibility decisions, render warnings, and all timings. Local generated JSON/PNG pairs are ignored under `artifacts/m2-verified/` and can be regenerated. Environment: the same native Apple M3 / 16 GiB / Python 3.12 environment documented in M0/M1.

Observed warm engine medians span 0.50–61.16ms for M2, versus 0.24–8.38ms for paired M1. Easy cases exit after one candidate; harder cases evaluate six. Search costs more, including cases where M1 is retained. These measurements exclude rendering/import and do not establish an execution budget for unknown hardware. No memory benchmark, sealed holdout, official scorer, or offline Docker run was performed.

M2 is complete as a bounded selection milestone, with the above limitations. Next: independent challenger/judge testing on a frozen revision. Keep exposed failures as regressions and generate fresh cases after fixes; separate-agent review does not automatically mean different-model review or filesystem-isolated holdout testing.
