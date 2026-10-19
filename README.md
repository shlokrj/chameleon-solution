# CHAMELEON: automatic design resizing

Give this engine a finished design, such as a square Instagram post, and a new canvas size, such as a 728×90 web banner. It rearranges the same design to fit. It works the way a designer would: it moves things, resizes them, and reflows the text, rather than stretching the picture.

```
input:  a task JSON (the original design + the new canvas size)
              |
              v
        engine/resize.py      <-- the method described below
              |
              v
output: <task>_output.json    (the resized design, same format as the input)
        <task>_output.png     (a rendered preview of it)
```

## The ground rules it never breaks

Every result keeps:
- **every element**: nothing is added, removed or hidden;
- **the exact words and fonts**: text is never rewritten;
- **the original images**: pixels are never redrawn, cropped or distorted;
- **everything on the canvas**: nothing pokes off the edge.

What *can* change is where each element sits, how big it is, and the size of the text.

## How the resizing works, in plain terms

The engine works in six steps.

### 1. Work out what belongs together

A design is just a list of shapes, pictures and text boxes, with no labels saying "this is the logo" or "this is a button". So the engine first works out which pieces form a unit, so they never get split up:
- **Explicit groups.** Pieces the designer marked as a group, such as a button's shape and its label, move as one.
- **Text on a panel.** If a piece of text sits on a solid panel or a photo, the two are kept together. Otherwise white text could slide off its dark panel and vanish.
- **Background.** A picture or shape covering the whole canvas is treated as the background and stretched to fill the new canvas. Photos are trimmed at the edges rather than squashed.
- **Decorations.** Loose shapes behind everything, such as faint circles, keep roughly the same relative position.

### 2. Decide how big a change this is

The engine compares the shape of the old canvas with the new one.

- **Similar shape** (for example square → slightly taller portrait). The original layout is kept. Every unit stays in the same relative spot and grows to use any extra room. If growing would make two things bump into each other, it grows them less.
- **Very different shape** (for example square → long thin banner). Keeping the old arrangement would leave everything tiny, so the engine **rebuilds the layout** using steps 3–5.

### 3. Divide the new canvas into zones

Everything is sorted into three kinds of content: **pictures**, **buttons and badges**, and **text**.

| New canvas | Arrangement |
|---|---|
| Wide (banners, thumbnails) | Pictures in a column on the left, text in the middle, buttons along the bottom **or** in their own column on the right |
| Tall (stories, skyscrapers) | Pictures on top, text in the middle, buttons at the bottom |

A small margin is kept around the edges and between zones.

### 4. Fill each zone sensibly

**Pictures and buttons** are laid out like words in a paragraph: side by side, wrapping onto a new row when the zone runs out of width. The engine also tries columns and uses them when they let the items stay larger. All the items in a zone shrink or grow **by the same amount**, so a big "Shop now" button stays bigger than a small "NEW" badge. The engine picks the largest size at which everything still fits.

Two details make this look right:
- **Pictures are measured by what you can actually see.** A logo file is often mostly see-through padding; ours is about 60% empty. The engine sizes pictures by their visible part, so logos and products don't look needlessly tiny.
- **Rounded buttons stay rounded.** Corner rounding is resized along with the button.

An image whose file is missing still appears as a placeholder, but it goes in the buttons zone so it doesn't take the main picture spot.

**Text** is fitted using the real brand fonts, measuring the actual width of every letter. Each text box gets the largest size at which its words wrap neatly and fit without spilling over. Size order is preserved:
- The headline stays the largest piece of text.
- When space is very tight, smaller text such as fine print may stay at a readable **10px minimum** while the headline shrinks.
- That minimum never reaches the headline's size. Fine print stays at most 70% of the headline, so the headline always stands out.

### 5. Try a few layouts and keep the best

There is rarely one obvious answer, so the engine builds **up to six candidate layouts**. They differ in how much room goes to pictures versus buttons, and in whether buttons sit along the bottom or in a side column. Each candidate then goes through three checks, in order:

1. **Rule check.** Any candidate that breaks a ground rule is thrown out.
2. **Safety check.** A candidate is rejected if it makes things worse than the first layout. That means shrinking any text by more than 5%, shrinking a picture's shorter side by more than 20%, or creating new overlaps.
3. **Quality score.** The remaining candidates are scored, lower is better, on:
   - text that would spill out of its box (this counts most);
   - text below a readable size;
   - smaller text that grew larger than text that used to be bigger;
   - elements newly covering each other;
   - text that lost its backing panel.

The best-scoring candidate wins. If the very first layout is already perfect, the engine stops there.

### 6. Write the result

The winning layout is saved as JSON and rendered to a PNG preview.

### A worked example

Take the Level 3 sample: a tall 1080×1350 poster with a logo, a product photo, a long headline, a paragraph, legal text, three badges, a button and a tilted "SUNSET SALE" ribbon. Its target is a 728×90 leaderboard banner, eight times wider than it is tall.

1. The shape change is extreme, so the layout is rebuilt.
2. The logo and product take a narrow column on the left.
3. The text fills the middle. The headline is the largest text, at about 11.5px. The paragraph and legal line are held at 70% of it, about 8px. Under plain proportional shrinking, the legal line would have been about 3px.
4. The badges, ribbon, button and missing-image placeholder share a column on the right, all scaled together.
5. Of the six candidates, the side-column version scores best and is chosen.

This is the hardest kind of case. Seven secondary items crammed into a 90px-tall banner leave their labels small, about 4–6px; see Known limits.

## Where the code lives

| Step | File |
|---|---|
| Finding text-on-panel units | `engine/relationships.py` |
| Zones, row/column packing, keeping layouts, visible-pixel sizing | `engine/layout.py` |
| Fitting text with real font measurements | `engine/typography.py` |
| Rule checks, safety checks, quality score | `engine/quality.py` |
| Building candidates and picking the winner | `engine/resize.py` |
| Reading inputs, writing outputs, rendering | `engine/main.py` |

The whole method is deterministic: the same input always gives the same output. It uses no AI model and needs no internet connection. A typical design takes a few hundredths of a second, plus rendering time.

## Known limits

- Very dense designs squeezed into very small formats can still end up with small secondary labels: for example, the Level 3 sample in a 728×90, 300×250 or 160×600 ad.
- Because pictures in a zone share one scale, a logo beside a tall product photo can look small in thin banners.
- Text and fonts are never changed, by design. Shortening copy would be a separate, judged, creative step.

Progress and evidence for each change are tracked in [PROGRESS.md](PROGRESS.md) and [agent-kit/runs/](agent-kit/runs/).

## Running it

Requires Python 3.12 (the container uses 3.12.13). Package versions are pinned.

```bash
pip install -r requirements.txt
python -m engine.main
```

This processes every `*.json` task in `input/`, which ships with one sample per difficulty level. It writes `<task>_output.json` and `<task>_output.png` into `output/`.

### With Docker (how scoring runs it)

```bash
docker build --platform linux/amd64 -t my-chameleon-engine .
docker run --rm --network none \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  my-chameleon-engine
```

Everything is installed at build time, so the engine runs with networking disabled. `./scripts/verify-container.sh` builds the images, runs the tests and validates every output inside the container. Font rendering differs slightly between macOS and Linux, so use the container for final visual checks.

## Development checks

```bash
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m evaluation.catalogue --output artifacts/catalogue      # every sample × 10 real platform formats, with contact sheets
python -m evaluation.regressions --output artifacts/regressions  # saved tricky cases
python -m evaluation.baseline --output artifacts/current         # supplied samples
python -m evaluation.profile --output artifacts/profile          # speed and memory
python -m evaluation.parity --output artifacts/parity            # exact repeatability
```

These call the real renderer, write previews and a report, and exit with an error on any rule violation. The quality numbers are local estimates, not the official score, so look at the PNGs too. `evaluation.catalogue --reference <old report.json>` prints before/after changes per case.

`engine/main.py` also runs a quick self-check after each task (same IDs, required fields, nothing off-canvas). This is a safety net, not the official scorer. The Level 2 sample's corner-bleeding decorative circle is an expected warning case. The Level 3 sample's missing `holiday_watermark` image is intentional and renders as a labelled placeholder.

## See also

- `chameleon_design_schema_v0.9.json`: the field-by-field design format
- `RULES.md`: what is checked, graded, or disqualifying
- `FAQ.md`: organizer answers to common questions
