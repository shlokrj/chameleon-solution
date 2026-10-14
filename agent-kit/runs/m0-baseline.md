# M0: starter baseline

## State and reproduction

Engine revision: `b2b1e22612492588ffe934c42a0936f31adbef4e`. Evaluation tooling is in this record's containing commit. The production engine, renderer, sample inputs, and brand files were not changed. Owner: primary agent in the project chat; this was not an independent model tournament.

Environment: Apple M3, 16 GiB RAM; native macOS 26.6.2 arm64, Python 3.12.13 in local `.venv`. See [machine-readable results](m0-baseline-report.json) for renderer revision/package versions and all timings; [installed dependencies](m0-environment.txt) captures the exact local installation. Docker executable was unavailable, so no container build, emulation, or network-disabled container run was attempted.

From the repository root:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m evaluation.baseline
```

The final command intentionally exits **1** because the unchanged baseline violates checks. This is a completed evaluation with reported failures, not a renderer-import failure. Dependencies are currently unpinned in the starter; use the recorded environment and renderer commit when reproducing this exact run rather than assuming a future fresh install is equivalent.

Generated source/output PNGs, JSON, and the full report are under local ignored `artifacts/baseline/`. Collaborators can regenerate them with the command above; these local files are not assumed available in another checkout. The compact report and environment are tracked here. No whole-image placeholder fallback is used: evaluation calls the real renderer directly and fails if it cannot import or run.

## Checks and observations

Eight checker regression tests pass, covering valid identity output, duplicate IDs, nonfinite coordinates, rotated overflow, image distortion/asset replacement, cover exceptions, schema/target failures, and content/nested style changes. All three sample source designs validate against the supplied schema.

The baseline returns schema-valid output, preserves element IDs/types and protected fields, does not mutate inputs, preserves brand file hashes, and produces identical output over five repeated calls per case. These successes do not cancel the failures below.

| Sample | Independent findings | Visual comparison of source and real output |
|---|---|---|
| Level 1 | C6: logo box ratio changed | Readable, with similar centered composition and more vertical spacing; `contain` keeps visible logo pixels proportional despite changed box |
| Level 2 | C3: decorative circle extends off canvas; C6: logo and product box ratios changed | Portrait stack compressed into a wide banner; tiny text/product and large unused horizontal space; badges/buttons excessively wide |
| Level 3 | C3: rotated ribbon shape and label exceed canvas; C6: logo, product, missing-badge box ratios changed | Severe readability loss at 728×90; tiny product/copy and clipped ribbon; cannot be considered successful merely because JSON validates |

Level 2 decorative bleed is inherited from an intentional source design choice; the current conservative rule still flags it. This is the documented organizer ambiguity, not evidence that all overlap is wrong. `contain` can preserve visible pixels despite changed box ratios; C6 findings here are explicitly source-box contract checks, not claims of visually stretched foreground pixels.

The Level 3 holiday badge is intentionally missing and produces the expected per-asset warning/placeholder. Its source render already overlaps part of the lower region; do not attribute every inherited source issue to resizing. No replacement asset was created.

## Initial timing evidence

Five warm repetitions per case, following the first output render and source render. Medians below are observations, not quality-adjusted performance wins or a hardware guarantee.

| Sample | Engine median | Engine + JSON-free repeat rendering median |
|---|---|---|
| Level 1 | 0.0086 ms | 172.7 ms |
| Level 2 | 0.0134 ms | 150.1 ms |
| Level 3 | 0.0171 ms | 56.9 ms |

Warm pipeline measurements include resize and writing the real PNG; they exclude source rendering, validation, JSON serialization, and renderer import. The first `pipeline_seconds` measurement in the JSON includes resize, output JSON writing, and output rendering, but still excludes import and checks. No percentile claims are made from five observations.

The first fresh-environment renderer import took 23.93 s; a later process import took 1.17 s. These are two separate startup observations, not a controlled cold-cache benchmark. Memory, container size, and full process cold-start distributions have not been measured. No official scorer, unseen family suite, automated text-clipping oracle, or sealed holdout has been run.

## Decision and next bounded task

M0 is complete: a reproducible baseline exists, real rendering works, independent checks expose failures, and visual limitations are recorded. C7 (offline packaging) remains unverified due to missing Docker; C8 (generalization) requires later unseen-family work. Neither is implied by the checker.

Next M1 task: preserve ordinary image proportions and source groups while generating a simple deterministic horizontal/vertical reflow from geometry, then fit text using actual font metrics. Start with sample-independent unit cases, compare all three source/output renders, and preserve the baseline for regression comparison. Do not launch adversarial agents or add a runtime model as part of this baseline task.
