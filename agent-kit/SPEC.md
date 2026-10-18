# Stage-one specification

## Objective

Rearrange an existing design for a target canvas so it remains readable, on brand, and intentionally composed. Geometric stretching alone is not a solution. Robustness across unseen designs and shapes matters more than perfection on the three supplied examples. User priority: achieve this efficiently, including development cost and execution cost.

## Interface

Task input is `{ "source": { "canvas": ..., "elements": [...] }, "target_canvas": { "width": ..., "height": ... } }`. The public function receives the two values separately and returns a design `{ "canvas": ..., "elements": [...] }`, not the task wrapper. Output canvas dimensions must exactly match the target.

Validate against [schema v0.9](../chameleon_design_schema_v0.9.json), a provisional Draft 2020-12 schema. Canvas dimensions are positive integers; element widths/heights can be zero; text font size is at least 1. The schema does not encode every semantic constraint. Inputs do not supply headline/logo semantic labels. `group_id` does convey designer-intended units.

## Requirements and checks

| ID | Requirement | Evidence required |
|---|---|---|
| C1 | Every source element occurs exactly once, with its original ID and type; no additions/removals | Compare counts and ID multisets, not sets alone |
| C2 | Return schema-valid design and exact target canvas with finite numeric values | Draft 2020-12 validation plus finite-number and target checks |
| C3 | No output off canvas | Box checks plus rotated-corner/render checks; resolve bleed conflict in SOURCES |
| C4 | Preserve text content and font family for stage one | Exact field comparison, including Unicode and newlines |
| C5 | Preserve asset identity and original pixel content | Asset references and file hashes unchanged; no generated/replacement assets |
| C6 | Preserve image proportions, with existing full-bleed/cover cropping exceptions | Geometric and rendered checks; do not change fit merely to evade distortion checks |
| C7 | Work offline in the supplied container interface | Clean linux/amd64 build and network-disabled run producing JSON and PNG per task |
| C8 | Generalize beyond known samples | Unseen design-family and target-family evaluation; no sample-specific branches |

Engineering preservation policy: also retain colors, font weight/style, style runs, grouping, opacity, stacking order, and unrelated metadata by default. Change position, dimensions, and text font size first. Any broader property change needs source support, a documented rationale, and visual regression evidence. The schema permits fields that are not blanket permission to change brand styling. Accepted exception (M5, [evidence](runs/m5-composition.md)): `corner_radius` and `stroke_width` scale by the same factor as their unit, so the rendered shape (e.g. a pill button) is preserved rather than changed.

A zero-area source element is schema-valid and needs deliberate handling; do not divide by its aspect ratio. A 1px font is schema-valid but is not proof of readable typography. Some extreme combinations cannot preserve every readability preference. Keep hard constraints, report the quality shortfall, and do not pretend the case is fully solved.

## Quality objectives

1. Readable complete text: correct wrapping, no clipping, sensible contrast on the actual composited background.
2. Preserved hierarchy and brand: logo/product proportions, headline prominence, faithful colors/fonts.
3. Intentional relationships: grouped label/button containment, consistent alignment and spacing, appropriate reading order.
4. Intentional layering survives; unwanted foreground collisions do not. Backgrounds and enclosing shapes are not ordinary collision failures.
5. Reliable and efficient behavior over increasing element counts, extreme aspect-ratio changes, and missing assets.

These are evaluation categories, not published numerical weights. The official scorer is unavailable. Local quality metrics and vision-model ratings are proxies.

## Deliverables

Engine, Dockerfile/dependencies, short run/approach README, reproducible validation evidence. Both returned JSON and its real rendered PNG matter. Viewer/add-on timing, approved models, model size limits, and hardware details remain unresolved in [SOURCES.md](SOURCES.md). Do not start a viewer as part of engine implementation without checking scope.
