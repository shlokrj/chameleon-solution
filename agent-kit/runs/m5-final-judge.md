# Final bounded M5 acceptance review

2026-10-23, frozen `9dc59b3`. **Accepted within the bounded review scope; no new reproduced defect.** Three fresh deterministic valid-contract cases passed; this supports closing M5 with its existing explicit quality limitations, not universal visual correctness or an official score.

The integration owner froze production before the reviewer created these cases. Details were withheld until evaluation and actual render inspection finished. Reviewer and integration owner use inherited models whose exact identity is not exposed: this is role separation, not a verified cross-model comparison. The shared filesystem was not technically sealed. No production edits, Git mutations, or follow-up repair rounds were performed by the reviewer. Cases are now exposed and retired.

## Evidence

Linux/amd64 `chameleon-verify`, network disabled. Container and checkout `engine/resize.py` SHA256 both `262efe24dbd66ce64112ea7d2891ec385a044343f46cd5b510db465818b90951`.

All three source designs pass schema validation; all outputs pass the independent contract checker, including preserved content/style/grouping and geometry. All have zero overflow IDs, support violations, new-overlap proxy and hierarchy inversions. Each task was called twice: outputs and diagnostics match exactly, and inputs remain unchanged. No external assets are used, so asset-pixel checks are not exercised by these fixtures.

| Fresh case | Final-tail ablation comparison | Visual verdict |
|---|---|---|
| Styled multiline tail, 800-square to 300×250 | Tail 10→10.5px; height26→101.8px; peers unchanged; local loss0.014468→0.010417 | Complete copy, bold run/spacing preserved, hierarchy retained, no clipping or collisions |
| Rotated tail, 800-square to468×100 | No changes; rotated tail10px | Rotation retained, complete wrapped copy, safely within target; sparse/asymmetric composition is a quality limit |
| Italic tail and grouped button, 800-square to320×180 | Tail10→10.4px; height26→46.802px; peers unchanged; local loss0.011389→0.008889 | Headline prominence and button containment retained; italic/newline text complete |

Inspected nine real renders in source/baseline/output order: three source PNGs, three current outputs, and three outputs with only `refine_tail_text` disabled. Review was not anonymized. The rendered gray button is also gray in the source render; it is not a resize-induced color regression. Text remains modest in size (minimum10,10.4 or10.5px), and this does not establish a universal12px floor.

Static inspection of final refinement confirms bounded fitting, source-font/12px caps, rotated-tail skip, stronger-source-hierarchy cap, and rollback on non-improvement, increased loss/hierarchy inversion/overflow. No clear additional defect was reproduced. This inspection does not prove all interactions safe.

## Reproduction and limits

Preserved [fixtures and executable check](../../tests/fixtures/m5-final/README.md). Running its command recreates JSON, report and PNGs in ignored `artifacts/m5-final-judge/`. The ablation isolates the tail refinement; it is not a comparison with a historical full engine. The integration owner runs the broad suite, catalogue, delivery and efficiency checks separately; this reviewer did not duplicate them or measure performance.

Existing small-logo and dense secondary-label limits remain outside these three cases. Zero new failures is bounded evidence only; hidden-case generalization, official scoring and actual submission are unverified. No further round is required for this scoped final review.
