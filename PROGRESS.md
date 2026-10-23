# Project progress and handoff

Read this first when joining or resuming work. This is the shared current-state summary; detailed evidence belongs in [experiment records](agent-kit/EXPERIMENTS.md). Verify the checkout and relevant artifacts before trusting an older entry.

## Current state

- **Phase:** M3 complete; M4 complete under the user-confirmed final PDF; submission handled by the user; M5 grouped-label repair and bounded fresh review verified; M5.3 contrast tiebreak remains rejected.
- **Implementation progress:** 5 of 6 implementation milestones complete (M0–M5; M5 remains in progress). This count is not an effort estimate.
- **Engine:** bounded candidate search, shared-scale row/column packing, hierarchy-preserving type floor, alpha-aware image packing, post-selection image expansion, plus inferred backing relationships. 75 offline Linux tests pass; all three production pairs validate; 70 catalogue cases have no contract/overflow findings; 42 Linux cases repeat exactly. See [final-box text evidence](agent-kit/runs/m5-tail-copy.md).
- **Latest verified predecessor:** `6a5433e` on `main`, pulled from origin. This containing commit adds guarded final-box text growth and verification; use Git history to resolve its revision.
- **Active implementation owners:** none; M5 final-box text claim released.
- **Next concrete action:** address remaining small grouped labels/logos with a feasible general improvement, or perform a bounded final M5 review with explicit quality limits. Compact Level 3 legal copy now reaches 6.111px without changing peers; seven catalogue layouts improve, but three still have sub-6px text. M4 remains complete; user handles submission.

## Milestone board

The definitions and exit criteria live in [IMPLEMENTATION.md](agent-kit/IMPLEMENTATION.md). Mark a milestone complete only when those criteria have evidence. Use `not started`, `in progress`, `blocked`, or `complete`; record a blocked reason and next action.

| ID | Milestone | State | Evidence / remaining work |
|---|---|---|---|
| Prep | Specification, agent guidance, evaluation workflow | complete | `ea0b910`, `81de421`; links and both project skills validated |
| M0 | Establish evidence | complete | [Baseline evidence](agent-kit/runs/m0-baseline.md); real rendering verified; Docker unavailable |
| M1 | Deterministic reflow | complete | [Reflow evidence](agent-kit/runs/m1-reflow.md); sample checks pass; dense-banner readability remains limited |
| M2 | Bounded selection and repair | complete | [Selection evidence](agent-kit/runs/m2-selection.md); 15 paired cases, bounded/failure behavior verified |
| M3 | Adversarial hardening | complete | [Bounded-cycle closure](agent-kit/runs/m3-layer-repairs.md); accepted defects repaired, fresh interactions pass, quality limits recorded |
| M4 | Efficiency and delivery | complete | [Technical verification and closure](agent-kit/runs/m4-final-review.md); current final PDF controls stage-one scope, submission channel supplied by user; M5 quality debt remains |
| M5 | Composition quality on catalogue formats | in progress | [M5.1 shared-scale packing/type floor, M5.2 alpha-aware bounds](agent-kit/runs/m5-composition.md); M5.3 contrast tiebreak rejected (0/85 selections changed); [Linux validation passed](agent-kit/runs/m5-linux.md); remaining: logo minimum, dense secondary groups, anchoring |

## Completed steps within M0

Evidence for all five steps: [M0 run record](agent-kit/runs/m0-baseline.md).

Check boxes mean verified completion, not intent. Link an experiment record or commit when checking one. Split further if needed; keep stable IDs so collaborators can refer to the same work.

- [x] **M0.1** Inspect current checkout, dependencies, Python/renderer availability, and container capability; record environment and any blockers.
- [x] **M0.2** Establish independent checks for the contract in [SPEC.md](agent-kit/SPEC.md), distinguishing directly testable invariants from generalization evidence.
- [x] **M0.3** Run all three unchanged sample inputs and capture output JSON, direct real-renderer PNGs, warnings, and engine/pipeline timings.
- [x] **M0.4** Inspect the renders, document baseline failures and measurement limits, and link a reproducible experiment record.
- [x] **M0.5** Review M0 exit criteria, update the milestone board, and define the next bounded M1 task.

## Completed steps within M1

Evidence: [M1 run record](agent-kit/runs/m1-reflow.md).

- [x] **M1.1** Implement geometry-based orientation changes, image proportions, and explicit group transforms.
- [x] **M1.2** Fit text with brand-font measurements and bounded searches without changing source content.
- [x] **M1.3** Verify regression cases and all supplied outputs; inspect final real renders and record timings/remaining limitations.
- [x] **M2.1** Compare bounded layout candidates on new development families with explicit readability diagnostics.

M2 evidence: [paired selection run](agent-kit/runs/m2-selection.md).

## Active work and ownership

No active claims. Root completed and verified the guarded final-box text repair. M4 remains complete; M5 quality work is still in progress.

| Task ID | Owner / session | Branch / worktree | Claimed paths | State | Last update (with timezone) | Next action / handoff |
|---|---|---|---|---|---|---|
| — | — | — | — | unassigned | 2026-10-23 America/Chicago | Text repair claim released. Next: remaining M5 quality limits/final review |

Claims are coordination records, not locks. Before editing, re-read this table and check current Git status. Do not overwrite another owner's changes. Assign one integrator for overlapping paths or the shared tracker. In separate clones/branches, reconcile claims through the collaborators' coordination channel; a local Markdown edit cannot reserve remote work. Treat old claims as needing verification, not automatic permission to take over.

## Decisions and unresolved questions

- Preserve supplied text, fonts, element identity, grouping, and original asset pixels. No sample-specific layout branches.
- Development-time agent collaboration does not require a model in the runtime engine.
- User standing instruction: validate, commit, and push each completed requested change; lowercase Conventional Commit subjects, user's identity only, no co-authors.
- [SOURCES.md](agent-kit/SOURCES.md) is the authority for source conflicts and unknown organizer details, including viewer timing, model limits, hardware, and bleed. These questions do not block a deterministic baseline, but relevant unresolved submission requirements block a submission-ready claim.
- The user authorized continuing implementation; M2 has now been completed; next-stage independent agent review is authorized. Do not interpret the next-step list as a new instruction to begin implementation or launch agents without an applicable task request.

## Work log

Keep entries concise and factual. Use a stable change label when the containing commit hash is not yet available; Git history provides that hash. Never claim a push succeeded before checking its result.

| Change / revision | Work completed | Validation actually run | Remaining / handoff |
|---|---|---|---|
| `ea0b910` | Added spec, source register, implementation/evaluation plans, adversarial workflow, prompts, and two skills | Markdown links and both skill validators passed | Engine unchanged; no benchmark evidence |
| `81de421` | Added model comparison/improvement notes and standing commit-and-push policy | Markdown links, both skill validators, whitespace checks passed | No model comparisons or engine experiments run |
| `b2b1e22` | Added this tracker and mandatory agent read/update rules | Relative Markdown links, tracker consistency, and diff whitespace checked before commit | M0 remains unstarted; next owner should claim M0.1 |
| `ae6e289` | Added `evaluation/`, `tests/`, development dependencies, and M0 evidence; production code unchanged | 8 unit tests passed; 3 source schemas valid; 6 real source/output PNGs reviewed; 5 repeated timings per case; baseline correctly exits 1 with 9 findings | M0 complete; no active owner; next M1.1; Docker unavailable |
| `6d1dbe5` | Added reflow and font fitting; improved evaluation output and README; recorded M1 evidence | 16 tests passed; all 3 supplied outputs have zero structural findings; final renders reviewed; 5 timing repetitions per case | M1 complete; next M2.1; dense-banner readability and Docker remain open |
| `3324d76` | Added contract gates, quality diagnostics, development comparison, and sync-before-work rules | 23 tests; 15 paired cases structurally valid; three changed pairs visually reviewed; five timing repetitions | M2 complete; freeze and start M3; Docker unavailable |
| `fix: preserve implicit text backing during reflow` (containing commit) | Preserved panel/image-backed text and one-dimensional geometry; tracked adversarial fixtures and independent findings | 30 tests; 15 development/sample comparisons; judge verified repairs | M3 remains open: rotated text and dense grids; no active agents |
| `fix: preserve readable rotated text and source grids` (containing commit) | Repaired M3-R1/R2 and subpixel alignment; refined model notes | 36 tests; 15 comparisons; 5 saved regressions; independent six-case repair verification | Final fresh review, then M4 profiling/offline packaging |
| `test: record fresh review and isolated performance baseline` (containing commit) | Saved six fresh tasks/two feasible witnesses; added isolated profiling and model notes | 38 tests; 11 rendered structural regressions; judge 4/6 visual passes; 18 profile workers with raw timings/RSS | R3/R4 remain open; Docker unavailable; prioritize contrast before optimization |

| `fix: preserve large and nested backing relationships` (containing commit) | Repaired R3/R4; closed bounded M3 cycle; preserved four fresh cases and refined notes | 44 tests; 15 rendered adversarial tasks; 15 unchanged development outputs; judge 6/6 scoped passes | M4 optimization next; small-group type, dense banners and Docker remain limitations |

| `perf: reuse cached typefaces during text fitting` (containing commit) | Reused bounded typefaces/base metrics; added isolated parity harness and notes | 47 tests; 42 identical JSON/pixel results; 36 sequential profile workers; independent static review | M4 overlap costs and offline packaging remain; no readability change |

| `perf: reuse bounds during overlap scoring` (containing commit) | Reused per-call rotated bounds; added exact quality parity and tests | 50 tests; 42 identical selected scores/JSON/pixels; 36 sequential profile workers; static review | Dependency reproducibility and offline Docker validation next; quality limitations unchanged |

| `build: pin tested dependencies and require real rendering` (containing commit) | Pinned runtime/dev versions and Python image; removed whole-render fallback; added delivery validator/container script | Clean native install + pip check; 55 tests; 42 parity cases; 3 entrypoint pairs; Linux wheel dry-run; static review | Docker build/offline run blocked; image/container resource and release checks unrun |

| `build: verify offline amd64 containers on colima` (containing commit) | Installed Docker/Colima, verified real amd64 builds/offline outputs, recorded resources and platform caveat | 55 container tests; 3 production pairs; 42 deterministic Linux repeats; five resource runs | Docker blocker resolved; dense Linux labels and organizer/release questions remain |

| `feat: pack units at shared scale with readable type floor` (containing commit) | Shared-scale flow packing, shape-length scaling, hierarchy-preserving 10px type floor, missing-asset demotion, banner side column, near-ratio room; catalogue sweep harness | 60 tests; 70 catalogue cases zero contract issues, mean loss 0.053→0.033, <6px cases 11→6; 15 regressions zero issues; renders inspected vs isolated baseline worktree | Linux container rerun unrun; dense 300x250/160x600 still small; next M5.2 |

| `feat: pack contain images by visible pixels` (containing commit) | Alpha-bbox visual bounds for packing/collision/overlap proxy; rigid zone shrink keeps boxes on canvas and ink in slot | 61 tests; 70 catalogue cases zero issues, 3 changed (all improved), mean loss vs d97405c 0.053→0.029; 15 regressions zero issues; renders inspected | Linux rerun unrun; logo small beside tall product; next M5.3 |

| `docs: record rejected contrast tiebreak and release m5 claim` (containing commit) | Probed rendered-contrast tiebreak; recorded rejection, deferrals, lessons | 85-case probe: 0 selection changes; no production code changed | Linux container rerun; logo minimum; anchoring |

| `docs: explain the resize method in plain language` (containing commit) | Rewrote README around a six-step plain-language explanation, worked Level 3 example, code map, limits; removed starter-template wording | Worked example checked against engine output; README links resolved; no code changed | None new |

| `docs: record post-restart docker verification` (containing commit) | Confirmed Docker/Colima recovery and complete container workflow after Mac restart | Both images built; 55 offline tests; 3 production JSON/PNG pairs independently validated | Docker work complete; Linux readability and final release review remain separate follow-ups |

| `test: verify teammate composition changes in linux` (containing commit) | Reviewed four teammate commits; rebuilt and verified M5 offline; refreshed Linux quality evidence and milestone count | 61 tests; 3 delivery pairs; 70 catalogue cases; 42 exact repeated parity cases; five renders inspected | No engine changes; tiny text/logo sizing, fresh review and final release questions remain |

| `feat: compare row and column packing for larger groups` (containing commit) | Added bounded alternate packing direction, retained common scale and row tie-break; README/model notes updated | 62 offline tests; 3 validated production pairs; 70 catalogue cases with 3 improvements; 42 repeated parity cases; renders inspected; five timed sweeps per revision | Five sub-6px cases remain; logo sizing/anchoring and release questions remain; ~4.8% warm engine cost accepted |

| `feat: enlarge standalone images within spare zone space` (containing commit) | Added bounded post-selection image growth; preserved gaps/canvas bounds and candidate selection; updated README/model notes | 66 offline tests; 3 production pairs; 70 cases with unchanged metrics/non-image fields and no shrunk images; 42 exact repeat cases; 15 changed renders inspected; five timing sweeps per revision | Crowded Level 2 logo and five sub-6px cases remain; ~1.4% warm engine cost; no fresh holdout |

| `feat: allocate more group space on compact canvases` (containing commit) | Replaced near-square side-column candidates with deeper bottom sections; retained regression guards and six-candidate cap | 67 offline tests; 3 production pairs; 70 catalogue cases; 49 boundary cases without measured regressions; 42 unchanged and repeated regression cases; changed renders inspected | Five sub-6px catalogue cases remain; no fresh holdout; dense fine print and crowded logos still open |

| `fix: preserve readable text floors when downscaling` (containing commit) | Added guarded post-selection text refit; preserved layout selection, source-size cap and hierarchy; refined model notes | 71 offline tests; 3 validated pairs; 70 catalogue + 49 boundary cases with seven improvements each and no measured regressions; 42 repeated cases; changed renders inspected | Four sub-6px cases remain; next fresh M5 review; no official scoring or submission claim |

| `fix: fit grouped labels within their existing boxes` (containing commit) | Completed six-case challenger round, accepted one repair, verified three fresh judge-held cases; saved fixtures and model notes | 73 offline tests; 3 delivery pairs; 70 catalogue cases (16 improvements, none worse); 42 exact repeat cases; 15 M3 + 9 M5 cases; paired renders inspected; warm sweep median 0.549→0.703s | Review closed; three sub-6px catalogue cases remain; M4/M5 quality and organizer release questions open |

| `test: add bounded dense layout feasibility probe` (containing commit) | Added offline allocation probe; saved two feasible improvements and compact negative result; updated model notes | 125 alternatives × two exact-repeat runs; six paired renders inspected; 75 offline Linux tests pass; source immutability and candidate contracts checked | Engine unchanged; compare candidate-slot replacement broadly before integration; three dense cases still below 6px |

| `test: reject regressive allocation slot replacements` (containing commit) | Compared all five non-baseline slots with low-image-share allocation; saved rejection evidence and model lesson | 595 comparisons repeated exactly, unchanged inputs, zero contract failures, 73 offline tests; ten paired PNGs inspected | All variants rejected due per-element regressions; engine unchanged; next compact legal-copy geometry |

| `docs: finalize local m4 verification and release blockers` (containing commit) | Refreshed offline delivery, nine-case cold/warm/RSS profiles and five production runs; researched organizer requirements; updated release checklist | 73 tests; 3 validated/inspected output pairs; 18 profile workers all pass; five offline production runs 1.657–1.904s; source/PDF/public announcement review | Local M4 technical work complete; full M4 blocked only on applicable organizer release instructions; no submission claim |

| `docs: close m4 against confirmed final challenge brief` (containing commit) | Read supplied Final Chameleon Challenge (1).pdf; adopted user-confirmed PDF over stale FAQ; recorded submission channel and closed M4 | PDF pages 7–8, 11 and 14 checked; prior unchanged-engine technical evidence retained; form fields inaccessible through web tool | M5 remains open; user submits form; hardware specifics still unspecified, not an engineering blocker |

| `fix: grow final copy into unused text region space` (containing commit) | Added guarded final-box font/height growth with unchanged peers; updated model notes | 75 offline tests, 3 delivery pairs, 70 catalogue cases with seven improvements and no worse loss, 42 exact repeat cases, 9 saved M5 cases; all changed catalogue/review renders inspected; five warm sweeps per revision | M4 complete; M5 remains open, three catalogue cases still have sub-6px copy |

## How to update this file

1. **At start:** read root AGENTS.md, inspect local work, pull the current branch from origin using its safe sync rule, then re-read this file and verify branch/revision and working-tree changes, then read the relevant spec/milestone/evidence. Claim the task with your actual owner/session identifier, paths, and timestamp. Do not guess another agent's state.
2. **During work:** update after a meaningful checkpoint, a scope/ownership change, or a blocker. Record what is complete and the exact next step, especially before interruption. Do not add every command or private reasoning.
3. **Before handoff or completion:** refresh the current state, milestone/step status, active claim, and work log. Include changed paths, revision or change label, evidence links, checks run and not run, failures, blockers, and a concrete resume action. Remove resolved blockers rather than leaving contradictory summaries.
4. **Before committing:** recheck/pull remote changes using the root sync rule, rerun affected checks, and re-read the latest tracker; merge concurrent entries without discarding anyone's work. Include the progress update in the same commit as the requested change. Do not check off a step merely because code exists.
5. **After pushing:** verify the push and report its outcome. If it fails, keep the local commit and report the failure; do not force-push or mark the remote synchronized. Git is authoritative for commit/push state, so no extra bookkeeping commit is required merely to insert the containing hash.

For longer work, add detailed run records under `agent-kit/runs/` using [EXPERIMENTS.md](agent-kit/EXPERIMENTS.md), then link them here. Keep the current-state sections short enough to read at every handoff. Archive older log entries only into a linked tracked document, preserving evidence and unresolved decisions.
