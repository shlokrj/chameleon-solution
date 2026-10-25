# Chameleon

Chameleon rearranges an existing design for a new canvas size. It returns the same text, images, and shapes with updated positions, dimensions, and font sizes, then renders a PNG using the supplied brand assets.

The engine is deterministic within the same runtime environment. It uses no model or external API and runs offline after installation.

## Run with Docker

From the repository root, with Docker running:

```sh
mkdir -p output
docker build --platform linux/amd64 -t chameleon-engine .
docker run --rm --platform linux/amd64 --network none \
  -v "$(pwd)/input:/app/input:ro" \
  -v "$(pwd)/output:/app/output" chameleon-engine
```

The build downloads dependencies; execution requires no network access. Each task in `input/` produces two files in `output/`:

- `<task>_output.json`: the resized design
- `<task>_output.png`: the rendered preview

Three sample tasks are included. To process another design, add a JSON file to `input/` with `source` and `target_canvas` fields. The source contains a `canvas` and an `elements` list; the target specifies `width` and `height`. See the [design schema](chameleon_design_schema_v0.9.json) and [sample tasks](input/).

## Run locally

Use Python 3.12. The Docker image uses Python 3.12.13 and pinned package versions.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m engine.main
```

Font measurements can differ between macOS and Linux. Use the Docker output for final checks.

## Approach

The entry point is `resize(source, target_canvas)` in [engine/resize.py](engine/resize.py).

1. **Identify layout units.** Explicit groups move together. Geometry and stacking order identify text that belongs on a backing panel or image. Backgrounds and decorations are handled separately.
2. **Preserve or reflow.** Similar canvas proportions retain the source arrangement where feasible. Larger changes use image, text, and grouped-content regions, with row or column packing.
3. **Compare up to six layouts.** Candidates vary the space assigned to each region. Structural checks reject invalid geometry and changed source properties. Regression checks limit text/image shrinkage relative to the initial candidate. Remaining layouts are ranked by text overflow, readability, hierarchy, overlap, and backing relationships.
4. **Use spare space.** Images and text can grow within their selected regions, subject to bounds, fit, spacing, and hierarchy checks. Transparent image padding is excluded when measuring visible content. Text fitting uses the renderer's actual fonts and wrapping behavior.

Text content, font families, asset references, styling, and element identities are preserved. Ordinary images keep their proportions; existing cover backgrounds retain their cropping behavior. Shape corner radii and stroke widths scale with their groups. The engine does not regenerate assets or rewrite copy.

The quality measures are local heuristics, not the official scoring system. Font-size targets guide fitting but are not guaranteed minimums.

## Code layout

| Path | Purpose |
|---|---|
| `engine/resize.py` | Candidate selection and final text refinements |
| `engine/layout.py` | Layout regions, packing, image sizing, and text placement |
| `engine/typography.py` | Font measurements and bounded text fitting |
| `engine/relationships.py` | Backing-panel relationships |
| `engine/quality.py` | Structural checks and layout metrics |
| `engine/main.py` | Input/output and rendering |
| `renderer/` | Conversion to the supplied rendering format |
| `brand_kit/` | Original assets and fonts |
| `tests/`, `evaluation/` | Regression tests and validation tools |

## Validation

Run the container checks:

```sh
./scripts/verify-container.sh
```

This builds production and verification images, runs the unit tests offline, processes the three samples, and independently checks the output JSON and rendered PNGs.

For local development:

```sh
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m evaluation.catalogue --output artifacts/catalogue
python -m evaluation.regressions --output artifacts/regressions
python -m evaluation.parity --output artifacts/parity
python -m evaluation.profile --output artifacts/profile
```

The validated engine passes 75 unit tests, all three sample delivery checks, and structural/text-fit checks across 70 catalogue layouts. Repeated evaluation of 42 cases produced identical designs and rendered pixels in Linux. These checks cover the included cases, not every possible design. See [tests/README.md](tests/README.md) for additional regression fixtures.

## Limitations

- Dense content in small canvases can still produce tiny text. The Level 3 sample has labels below 6px in the 728×90, 300×250, and 160×600 formats.
- Logos can remain small beside large product images. Source contrast is preserved, so low-contrast branding may remain difficult to read.
- Corner badges may be reflowed into a content region rather than kept at the same corner.
- Overlapping text boxes are handled conservatively, and rotated text is excluded from some final font-growth passes.
- The Level 3 sample intentionally references a missing holiday badge. It renders as a labelled placeholder; no replacement asset is supplied.

The original challenge rules are in [RULES.md](RULES.md). The supplied final challenge PDF takes precedence over older FAQ wording about the viewer: stage one requires the engine, Dockerfile, and README; the full Express add-on belongs to the finale.
