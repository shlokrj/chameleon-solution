# CHAMELEON — starter repo

This is the scaffolding for your engine. It handles input loading, output
writing, rendering, and Docker packaging — with layout logic in **`engine/resize.py`** and font fitting in
**`engine/typography.py`**.

```
input:  a task JSON (source design + target canvas)
              |
              v
        engine/resize.py   <-- YOU IMPLEMENT THIS
              |
              v
output: <task>_output.json  (schema-valid resized design)
        <task>_output.png   (rendered preview)
```

Both the JSON and the PNG are what get evaluated — see `RULES.md`.

## Repo layout

```
engine/
  resize.py        <- implement your approach here
  main.py           <- orchestrator (input -> resize() -> output). Don't need to edit this.
renderer/           <- the real renderer (transformer-convertor + cr-renderer), already vendored
brand_kit/
  assets/           <- image files referenced by asset_id in the sample designs
  fonts/            <- font files matching the schema's font_family values
input/               <- drop task JSON files here for local testing (3 samples included)
output/              <- results land here
chameleon_design_schema_v0.9.json   <- full field-by-field spec for the design format
Dockerfile
RULES.md
```

## Quick start (no Docker needed for iterating on `resize()`)

Requires Python 3.12 (the container pins 3.12.13). Runtime package versions and
the renderer Git revision are pinned to the tested environment.

```bash
pip install -r requirements.txt
python -m engine.main
```

This processes every `*.json` file in `input/` (the 3 sample designs are
already there — one per difficulty level) and writes an `_output.json` and
`_output.png` for each into `output/`.

The engine uses at most six deterministic layout candidates with structural gates
and readability regression guards. It keeps the existing layout as a fallback
and avoids further search when local quality checks are already satisfied. Reflow preserves nearby layouts, places
imagery beside copy for wide targets, and stacks content for tall targets.
Explicit groups move together, ordinary images retain their box proportions,
and text uses brand-font measurements with bounded size fitting. No runtime
model or network access is required by the layout algorithm.

This is an initial heuristic, not a finished solution: dense extreme banners
can still have very small text, and broader generalization remains limited. Offline Linux amd64 container
execution is verified. See [PROGRESS.md](PROGRESS.md) for the current milestone.

## Development checks

```bash
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m evaluation.baseline --output artifacts/current
python -m evaluation.regressions --output artifacts/regressions
python -m evaluation.profile --output artifacts/profile
python -m evaluation.parity --output artifacts/parity
```

The evaluation command calls the real renderer directly, writes source/output
previews and a report, and exits nonzero on structural findings. Text-fit
measurements are estimates shared with the engine, not an independent visual
oracle. Inspect the PNGs too. Generated artifacts stay local; milestone reports
are tracked in `agent-kit/runs/`.

The profiler runs separate processes for startup and warmed measurements on
three supplied cases and six element-count/shape cases. It records engine and
render times separately, whole-process peak memory, structural failures, and
readability diagnostics. These are local measurements, not container results. The parity command captures
complete layouts, quality scores, and rendered-pixel hashes; pass `--reference /path/to/report.json`
to compare against a report produced in an isolated baseline checkout.

## What the self-check does (and doesn't do)

`main.py` runs a quick structural check after every task — same element
`id`s as the source, required fields present, nothing off-canvas. **This
is not the official scorer.** It exists to catch obvious mistakes before
you waste a submission on them. See `RULES.md` for what's actually
checked and graded.

A self-check warning does not fail the run — your JSON and PNG are still
written either way. Read the warning; decide whether it's a real problem
or, like the Level 2 sample's intentionally corner-bleeding decorative
circle, an expected one.

## The renderer

`main.py` calls `renderer/converter/convert.py`'s `render_design_to_png()`
(a vendored copy of `transformer-convertor`, wrapping `cr-renderer`) to
produce each task's PNG — already wired in, no setup needed. It reads
fonts/assets from `brand_kit/` and requires the real renderer. Missing renderer
imports or backend errors fail the process; no whole-design placeholder is
generated. The supplied Level 3 missing badge still uses its intentional
per-asset placeholder.

## Docker (how you'll actually be run)

```bash
docker build --platform linux/amd64 -t my-chameleon-engine .
docker run --rm --network none \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  my-chameleon-engine
```

`--network none` matches how stage-one scoring runs: everything your
engine needs must be installed at **build** time (add it to
`requirements.txt`), not fetched at run time. If you're using a locally
hosted model, bake its weights into the image during the build step.

To build production and verification images, run tests, execute the production
entrypoint, and independently validate its JSON/PNG pairs with runtime networking
disabled:

```bash
./scripts/verify-container.sh
```

This saves each run in a fresh `artifacts/container-check.*` directory. The
verification image adds tests and evaluation dependencies; the production image
does not include them. The base image is pinned by digest; Debian packages and
build tooling are not fully locked. Offline Linux amd64 validation passed under Colima/Rosetta on Apple Silicon;
see [container evidence](agent-kit/runs/m4-container.md). Native macOS and Linux
font rendering can differ; use the container for final visual checks.

On this Mac, Docker is configured through Colima. Run `colima start` after a
restart, or `colima stop` to release its VM resources.

## See also

- `chameleon_design_schema_v0.9.json` — full input/output field spec
- `RULES.md` — what's checked, what's graded, and what disqualifies a submission
- FAQ — for anything not covered above
