# Model collaboration and improvement notes

These are development policies, not claims that any model or algorithm has been evaluated. Use this document with [ADVERSARIAL.md](ADVERSARIAL.md) and [EVALUATION.md](EVALUATION.md). Keep architecture proposals provisional until experiments support them.

## Decide what is being compared

Separate three questions:

| Question | Controlled comparison | Useful outcome |
|---|---|---|
| Which builder produces better changes? | Same starting revision, task, available tools, evidence, and budget; isolated branches/workspaces | Verified improvement and regression count, quality, implementation cost |
| Which challenger finds useful weaknesses? | Same frozen engine, contract, available artifacts, and budget | Independently reproduced unique failure classes per time/cost |
| Does a model help the shipped engine? | Same engine with and without that component on the same development cases | Quality gain versus latency, memory, packaging, and failure cost |

A stronger challenger does not prove its builder is stronger. A development-model win does not justify adding that model to runtime. Do not mix these into a single leaderboard.

Record actual model identifier, configuration if exposed, prompt, tool access, context supplied, time budget, and actual resource usage. If access or budgets differ, label the comparison exploratory rather than fair. Do not choose a model from brand reputation alone or invent unavailable configuration details.

For builder comparisons, start each candidate from the same revision and keep branches separate until evaluation finishes. Compare the complete candidate diff and complexity as well as output quality. Integrate only the selected, independently checked changes; do not automatically combine all proposals.

## Make challenging productive

Use most of each small case batch for plausible failures that matter to users. Reserve the remaining cases for a boundary condition and an interaction between known weaknesses. For the default six-case batch, a useful starting mix is three realistic layouts, two boundary cases, and one interaction case. This mix is adjustable, not a requirement to fabricate six findings.

Prefer under-tested families to many variants of one easy-to-break example. Track coverage across aspect-ratio change, text density, element count, grouping, rotation, layering, and asset behavior. Cross a few high-risk dimensions rather than enumerating their full Cartesian product.

A challenger finding earns attention only when it has a valid expectation and a reproducible failure. Deduplicate by cause, not merely by different input hashes. Record rejected findings too, so another challenger does not repeatedly spend effort on the same invalid expectation.

A minimized reproducer should retain the behavior that caused the failure. Removing a background or group member can change whether an overlap is intentional; validate the reduced case again. Preserve the original case alongside its reduction.

## Prioritize fixes

| Priority | Meaning | Response |
|---|---|---|
| P0 | Broken contract, changed content/assets, runtime crash, or nonfunctional offline packaging on valid input | Repair before accepting the candidate |
| P1 | Unreadable/cut-off text, distorted key imagery, broken group, or severe unintended occlusion | Fix the general cause before aesthetic tuning |
| P2 | Weaker alignment, spacing, hierarchy, crop quality, or excessive measured resource cost | Compare benefit against effort and regression risk |
| Separate queue | Malformed-input robustness or independently reproduced renderer limitation | Track honestly; do not inflate valid-input failure rates |

Each accepted issue records: case ID, family/root cause, violated requirement, severity, reproduction, affected revision, evidence, and status. Use proposed -> reproduced -> fixed -> independently verified, or rejected/deferred with a reason. A builder's assertion that a fix works is not the final state transition.

Prioritize severity first, then breadth across cases, confidence, and repair cost. Case frequency in a synthetic suite is not an estimate of the hidden distribution. Avoid false numerical precision in a made-up impact score.

## Prevent agreement from replacing evidence

Judge hard requirements with executable independent checks. For subjective layout comparison, give the judge the source and anonymized A/B outputs without model names, implementation rationale, or expected winner. Allow ties and inconclusive results. Reverse presentation order for material disagreements; use a second independent review only if the decision warrants its cost.

Do not send the builder's persuasive explanation to the judge before its first assessment. A majority vote of models does not override schema failures or a visible clipped headline. Record uncertain visual findings as uncertain instead of forcing a winner.

Logical role separation is not filesystem isolation. In a shared workspace, an instruction not to read a holdout provides only procedural separation. For a stronger holdout, use a judge-controlled location unavailable to the builder or generate fresh cases after its revision is frozen. Record the actual isolation used. Never call a shared, previously inspected suite sealed.

## Improve with small experiments

Change one substantial mechanism at a time: grouping, candidate generation, text fitting, ranking, or repair. Write the expected benefit and acceptance condition before running the comparison. Keep the old candidate available as the baseline.

Use ablation when a new component adds meaningful cost: disable it and compare on the same cases. Keep it only if the measured benefit justifies its runtime, maintenance, and failure modes. If several mechanisms changed together, report that attribution is uncertain rather than claiming one caused the gain.

Do not optimize against repeatedly viewed holdout scores. Reveal the final holdout after freezing the candidate, report once, then retire exposed cases if they drive another fix. Stop at the adversarial budget; save the next hypothesis instead of extending a debate indefinitely.

## Spend computation where it changes a decision

Run schema/contract checks before rendering, rendering before optional vision judgment, and expensive model reasoning only for unresolved decisions. Cache repeatable analysis by revision plus input/settings hashes so stale evidence cannot pass as a fresh result. Keep caches bounded and invalidate them when fonts, assets, renderer, or relevant settings change.

Measure total work as well as wall time: parallel agents may finish sooner while consuming more tokens or compute. Track accepted unique findings and verified improvements per cycle, along with actual cost where available. If two cycles find no new verified failure class, end the cycle under the existing stopping rule.

After baseline profiling, set explicit development budgets for candidate count, repair iterations, rendered shortlist size, and optional inference. These are configurable project limits, not invented competition limits. Cheap geometry may prune candidates but must not become the sole quality judge.

## What to hand back

Use [EXPERIMENTS.md](EXPERIMENTS.md). State the selected revision, evidence supporting it, unresolved worst case, compared resource costs, and next useful experiment. A narrow measured improvement is a valid result. Do not claim "best model," "fully robust," or "submission ready" from one cycle or one small synthetic suite.

## Lessons from the M3 text repair cycle

Use feasibility witnesses to distinguish unavoidable density from unnecessary shrinkage. Test small coordinate perturbations as well as exact grids: a 0.25px alignment change exposed a large readability discontinuity despite passing structural checks. Reserve rotation-aware extents before font fitting rather than shrinking an already-fitted box again. Keep layout alternatives within the existing candidate budget and compare worst-case readability as well as runtime. The [text repair record](runs/m3-text-repairs.md) separates fresh discovery from exposed-case verification; repaired cases must not be reused as a final holdout.

## Fresh-review and scaling lessons

The [final M3 batch](runs/m3-final-review.md) exposed two limits in previously successful backing inference: a fixed area cutoff misses large inset panels, and selecting only the nearest backing loses outer nesting. Challenge heuristic boundaries and relationship chains, not just isolated elements. Six structural passes accompanied two visual defects; retain rendered witnesses as evidence.

The [M4 profile](runs/m4-profile.md) shows why candidate count is not a runtime budget: 120-element cases cost much more than the supplied examples. Separate engine time, rendering, process startup, and whole-worker peak memory. Keep poor-readability cases in performance reports and optimize measured hotspots only after higher-priority contrast defects.

## Closing the bounded M3 cycle

[Backing ancestry repairs](runs/m3-layer-repairs.md) replaced an arbitrary area cutoff with actual full-canvas geometry and followed text-backed nesting through paint order. Check chains, branches, and input reordering when adding inferred relationships; single-pair tests miss merge-order bugs. The judge accepted both defects and four fresh interaction cases. Close the bounded milestone with explicit remaining tradeoffs instead of equating small-case success with universal quality: uniform grouped scaling preserves contrast but can waste space and reduce typography. Next compare measured efficiency changes against unchanged-output evidence and bounded memory.

## Measured M4 font reuse

The [font optimization](runs/m4-font-reuse.md) removed repeated typeface construction using an existing bounded cache; it did not require caching arbitrary text or sizes. Compare full JSON and decoded render pixels against an isolated baseline, especially when changing typography dependencies that older comparison tools intentionally require to remain identical. Distinguish engine speedups from total rendering time and whole-worker memory from engine allocations. Fully styled text must not accidentally inherit unused base-font metrics.

## Measured overlap reuse

[Overlap geometry reuse](runs/m4-overlap-reuse.md) keeps per-candidate bounds local and preserves formula and summation order. Verify exact numerical scores as well as selected layouts/pixels; shared-helper unit references alone cannot catch a shared formula change. Linear geometry storage does not make pairwise scoring linear. After two measured optimization steps, prioritize reproducible packaging and the remaining release checks instead of extending optimization without evidence.

## Packaging evidence boundaries

The [packaging pass](runs/m4-packaging.md) aligns Python with installed dependency requirements, pins runtime versions/source/image digest, and removes a success-looking whole-render fallback. Keep native clean install, cross-platform wheel resolution, and actual network-disabled container execution as separate evidence. A resolved wheel does not prove shared-library compatibility; a static Dockerfile review does not prove a build. Fail output-pair validation on missing or incorrect pixels and retain the intentional single missing-asset placeholder as its own case.

## Validate in the target container

[Offline container testing](runs/m4-container.md) passed but strict macOS/Linux parity did not: font metrics and pixels differ, and one dense group-label case shrinks materially under Linux. Preserve failed cross-platform comparisons as evidence; repeat within the fixed container to distinguish determinism from portability. Use Linux renders for final quality decisions rather than treating host-native speed/parity results as target-platform guarantees.
