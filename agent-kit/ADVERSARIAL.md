# Model-versus-model robustness protocol

Purpose: use disagreement to discover reproducible failures, not to reward confident prose. Run this protocol when the user explicitly launches adversarial implementation/evaluation. It does not start merely because this file exists.

## Roles

| Role | Access and responsibility |
|---|---|
| Builder | Own production changes and development fixtures; fix verified failure classes |
| Challenger | Propose valid hard cases, minimal reproducers, and hypotheses; no production edits |
| Judge/integrator | Independently validate fixtures, reproduce failures, compare renders and metrics, accept/reject fixes |

Prefer different available model families for builder and challenger, with actual model/version recorded. If only one model is available, use isolated sessions/contexts and disclose that this is role separation, not cross-model validation. Swap roles in a later round to reduce anchoring. One integration owner prevents conflicting edits. Model output is a proposal, never proof.

## Default development budget (local policy, not competition rules)

At most 3 rounds per cycle, 6 proposed cases per challenger per round, and 2 repair attempts per accepted failure. Begin with one builder, one challenger, and one judge only if those resources are available. Record actual time/token cost when exposed by tools; do not invent it. Reduce parallel work if coordination costs exceed progress. Continue beyond this budget only under a new explicit work scope.

## Round procedure

1. Freeze baseline/candidate revisions, fixture generator version, seeds, environment, and evaluation settings. Partition by design family, not only random rows; related perturbations stay together.
2. Challenger gets the contract, renderer behavior, and failure taxonomy. For a black-box round, show outputs without implementation details; for a white-box round, permit source inspection and label the mode.
3. Each case includes input JSON, provenance/seed, source-schema status, semantic validity status, expected invariant or visual defect, and exact reproduction procedure. Compare source and target renders. Avoid cases dependent on fabricated assets; reuse supplied assets or intentionally missing references only in that designated robustness category.
4. Judge reproduces, checks that the expectation follows the spec, minimizes the case, and deduplicates by root cause. Invalid input is not proof of failure on the official distribution. Subjective disagreement needs visible evidence and rubric reasoning.
5. Builder receives accepted development cases, implements one general fix, and reruns prior regressions. Builder must not alter the failing fixture or judge thresholds to pass.
6. Judge compares baseline/candidate on the same fixtures, checks hard constraints first, then visually assesses outputs with anonymized A/B order where practical. Preserve results per case and category. No fix is accepted solely on a vision-model score.
7. Save accepted cases as regressions. Finish with a fresh holdout generated/held by the judge, unseen by the builder until its implementation is frozen. Once a holdout failure is revealed for fixing, retire it into development and create a new holdout.

## Useful attack families

- Extreme portrait-to-banner and banner-to-story reflows; nearby ratios; identical target/source dimensions.
- Long unbreakable words, explicit newlines, empty text, mixed-weight style runs, Unicode/unsupported glyphs, near-fit thresholds, large letter spacing.
- Button groups, stacked labels, semi-transparent overlays, intentional overlap versus unrelated collisions, equal z-index order.
- Rotation near canvas edges; thin lines and zero-area elements; missing optional fields versus explicit defaults/nulls.
- Foreground image proportion, cover background crop, extreme asset dimensions, intentional missing asset.
- Many text boxes/images, many tiny groups, one dominant group, dense irreducible content, increasing element counts.
- Renamed opaque IDs and reordered input with distinct z-indices; ensure algorithm does not rely on sample names or incidental ordering. Equal-z order is meaningful and must not be casually shuffled.

## Stop conditions

Stop after the round budget, two consecutive rounds with no new independently reproduced failure class, or a repeated no-improvement repair. Preserve the best verified candidate and unresolved cases. Stop an individual branch if it breaks hard constraints or relies on unavailable infrastructure. Zero discovered failures is not proof of general correctness.

## Challenger prompt

> Read agent-kit/SPEC.md, SOURCES.md, EVALUATION.md, and the challenge skill. Act as challenger, within ADVERSARIAL.md's budget. Find reproducible weaknesses in the assigned engine revision. Keep fixtures separate from production code, distinguish valid-contract cases from robustness-only malformed inputs, and deliver minimized JSON plus expected invariant and evidence. Do not fix the engine or claim failures without reproducing them.

## Judge prompt

> Independently adjudicate these cases against agent-kit/SPEC.md and EVALUATION.md. Verify expectations before running candidate comparisons. Reject invalid or unsupported failure claims. Record artifacts and per-case results; inspect real renders. Keep fresh holdout cases away from the builder until the revision is frozen. Report remaining defects and resource tradeoffs without claiming official scores.
