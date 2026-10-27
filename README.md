# Chameleon

Made by **Shlok Jadhav** and **Aadithya Balaji** for the **Adobe University Hackathon: North America 2026**.

Chameleon rearranges text, images, and shapes to fit a new canvas size. It preserves the source content and brand assets, and produces a resized JSON design and a rendered PNG. No model, API key, or internet connection is needed at runtime.

## Run

With Docker running, execute these commands from the repository root:

```sh
mkdir -p output
docker build --platform linux/amd64 -t chameleon-engine .
docker run --rm --platform linux/amd64 --network none \
  -v "$(pwd)/input:/app/input:ro" \
  -v "$(pwd)/output:/app/output" chameleon-engine
```

Dependencies are downloaded during the build. The engine processes every JSON task in `input/` and writes `<task>_output.json` and `<task>_output.png` to `output/`.

Three [sample tasks](input/) are included. Each task has a `source` design and a `target_canvas` with `width` and `height`. The full format is defined in the [design schema](chameleon_design_schema_v0.9.json).

For local development, use Python 3.12:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m engine.main
```

Use Docker for final validation: font measurements can differ between macOS and Linux.

## How it works

The engine implements `resize(source, target_canvas)` in [engine/resize.py](engine/resize.py).

It keeps explicit groups and inferred text/backing relationships together. Similar canvas proportions retain the original arrangement where feasible; larger changes reflow content into image, text, and grouped-content regions.

Up to six layouts are compared using structural checks, text fit, hierarchy, overlap, and readability estimates. Text is measured with the renderer's fonts. Image sizing accounts for transparent padding. Final adjustments use spare space without changing the selected arrangement or accepting worse fit and hierarchy scores.

Text content, font families, element IDs, and asset references are preserved. Ordinary images keep their proportions; existing cover backgrounds retain their cropping behavior. The engine does not rewrite copy or regenerate image assets. Selection is deterministic within the same runtime environment and does not branch on sample IDs or exact target sizes.

## Tests

```sh
./scripts/verify-container.sh
```

This builds both images, runs 75 unit tests offline, processes the three supplied tasks, and validates output structure and rendered pixels. Additional evaluation covers 70 catalogue layouts and exact repeatability across 42 cases. These are local checks, not official scores. See [tests/README.md](tests/README.md) for regression commands.

## Limitations

Dense layouts can still have small text: some Level 3 labels are below 6px in small banner, rectangle, and tall formats. Logos may remain small or low-contrast, and corner badges may move into a content region. The intentionally missing Level 3 holiday badge renders as a labelled placeholder.

This is the stage-one engine submission. The final challenge brief places the full Adobe Express add-on in the finale.
