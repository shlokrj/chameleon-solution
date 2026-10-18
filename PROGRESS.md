# Project progress and handoff

Read this first when joining or resuming work. This is the shared current-state summary; detailed evidence belongs in [experiment records](agent-kit/EXPERIMENTS.md). Verify the checkout and relevant artifacts before trusting an older entry.

## Current state

- **Phase:** M3 complete; M4 offline containers verified, final Linux quality/release review remains; M5 composition quality in progress (M5.1 accepted).
- **Implementation progress:** 4 of 5 milestones complete. Next: Linux quality follow-up and final release review. This count is not a percentage of effort or an estimate of time remaining.
- **Engine:** bounded candidate search, shared-scale flow packing, hierarchy-preserving type floor, plus inferred backing relationships. 60 tests pass natively (M5.1; Linux rerun pending); the M4 record shows 55 tests passing inside Linux amd64 with networking disabled; all three production output pairs validate; 42 Linux cases repeat exactly. Docker/Colima is running. Cross-platform font differences include a dense-label readability regression; see [container evidence](agent-kit/runs/m4-container.md).
- **Latest verified predecessor:** `d97405c` on `main`, pushed to `origin`. M5.1 composition changes are recorded in this containing commit; use `git log -1 -- PROGRESS.md` to resolve that revision without a self-referential hash.
- **Active implementation owners:** M5 (see Active work).
- **Next concrete action:** review dense-labels-compact under Linux (group labels 6.325px vs macOS 9.569px), retain Linux-based quality evidence, and resolve applicable organizer/release questions. Docker setup and offline verification are complete.

## Milestone board

The definitions and exit criteria live in [IMPLEMENTATION.md](agent-kit/IMPLEMENTATION.md). Mark a milestone complete only when those criteria have evidence. Use `not started`, `in progress`, `blocked`, or `complete`; record a blocked reason and next action.

| ID | Milestone | State | Evidence / remaining work |
|---|---|---|---|
| Prep | Specification, agent guidance, evaluation workflow | complete | `ea0b910`, `81de421`; links and both project skills validated |
| M0 | Establish evidence | complete | [Baseline evidence](agent-kit/runs/m0-baseline.md); real rendering verified; Docker unavailable |
| M1 | Deterministic reflow | complete | [Reflow evidence](agent-kit/runs/m1-reflow.md); sample checks pass; dense-banner readability remains limited |
| M2 | Bounded selection and repair | complete | [Selection evidence](agent-kit/runs/m2-selection.md); 15 paired cases, bounded/failure behavior verified |
| M3 | Adversarial hardening | complete | [Bounded-cycle closure](agent-kit/runs/m3-layer-repairs.md); accepted defects repaired, fresh interactions pass, quality limits recorded |
| M4 | Efficiency and delivery | in progress | [Offline container verification passed](agent-kit/runs/m4-container.md); Linux dense-layout quality and final release questions remain |
| M5 | Composition quality on catalogue formats | in progress | [M5.1 shared-scale packing/type floor](agent-kit/runs/m5-composition.md); next anchoring, alpha bounds, contrast tiebreak; Linux rerun pending |

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

M5 claimed: composition quality across catalogue formats (M5.1 accepted; M5.2 next).

| Task ID | Owner / session | Branch / worktree | Claimed paths | State | Last update (with timezone) | Next action / handoff |
|---|---|---|---|---|---|---|
| M5 | Aadhitya Balaji + Claude Code session | `main` | `engine/`, `evaluation/catalogue.py`, `tests/`, docs | in progress | 2026-10-18 America/Chicago | M5.1 done; next M5.2 corner/edge anchoring and alpha-aware image bounds |

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

| `docs: record post-restart docker verification` (containing commit) | Confirmed Docker/Colima recovery and complete container workflow after Mac restart | Both images built; 55 offline tests; 3 production JSON/PNG pairs independently validated | Docker work complete; Linux readability and final release review remain separate follow-ups |

## How to update this file

1. **At start:** read root AGENTS.md, inspect local work, pull the current branch from origin using its safe sync rule, then re-read this file and verify branch/revision and working-tree changes, then read the relevant spec/milestone/evidence. Claim the task with your actual owner/session identifier, paths, and timestamp. Do not guess another agent's state.
2. **During work:** update after a meaningful checkpoint, a scope/ownership change, or a blocker. Record what is complete and the exact next step, especially before interruption. Do not add every command or private reasoning.
3. **Before handoff or completion:** refresh the current state, milestone/step status, active claim, and work log. Include changed paths, revision or change label, evidence links, checks run and not run, failures, blockers, and a concrete resume action. Remove resolved blockers rather than leaving contradictory summaries.
4. **Before committing:** recheck/pull remote changes using the root sync rule, rerun affected checks, and re-read the latest tracker; merge concurrent entries without discarding anyone's work. Include the progress update in the same commit as the requested change. Do not check off a step merely because code exists.
5. **After pushing:** verify the push and report its outcome. If it fails, keep the local commit and report the failure; do not force-push or mark the remote synchronized. Git is authoritative for commit/push state, so no extra bookkeeping commit is required merely to insert the containing hash.

For longer work, add detailed run records under `agent-kit/runs/` using [EXPERIMENTS.md](agent-kit/EXPERIMENTS.md), then link them here. Keep the current-state sections short enough to read at every handoff. Archive older log entries only into a linked tracked document, preserving evidence and unresolved decisions.
