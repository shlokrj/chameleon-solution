# Project progress and handoff

Read this first when joining or resuming work. This is the shared current-state summary; detailed evidence belongs in [experiment records](agent-kit/EXPERIMENTS.md). Verify the checkout and relevant artifacts before trusting an older entry.

## Current state

- **Phase:** M3 panel/image backing and zero-width line repairs verified; rotation/grid findings remain open.
- **Implementation progress:** 3 of 5 milestones complete. Next: M3, adversarial hardening. This count is not a percentage of effort or an estimate of time remaining.
- **Engine:** bounded candidate search plus inferred backing relationships. 30 tests and 15 prior comparison cases pass structural checks. Judge verified panel/image contrast repairs and line geometry; rotated singleton text and dense grids still shrink unnecessarily. See [M3 handoff](agent-kit/runs/m3-hardening.md).
- **Latest verified predecessor:** `3324d76` on `main`, pushed to `origin`. The M3 repairs and evidence are recorded in this containing commit; use `git log -1 -- PROGRESS.md` to resolve that revision without a self-referential hash.
- **Active implementation owners:** none; challenger/judge passes ended and all claims released.
- **Next concrete action:** claim M3-R1 (rotation-aware text placement), then M3-R2 (bounded text-grid candidate). Reproduce the tracked fixtures/witnesses in [M3 handoff](agent-kit/runs/m3-hardening.md); final fresh-case judging is still outstanding.

## Milestone board

The definitions and exit criteria live in [IMPLEMENTATION.md](agent-kit/IMPLEMENTATION.md). Mark a milestone complete only when those criteria have evidence. Use `not started`, `in progress`, `blocked`, or `complete`; record a blocked reason and next action.

| ID | Milestone | State | Evidence / remaining work |
|---|---|---|---|
| Prep | Specification, agent guidance, evaluation workflow | complete | `ea0b910`, `81de421`; links and both project skills validated |
| M0 | Establish evidence | complete | [Baseline evidence](agent-kit/runs/m0-baseline.md); real rendering verified; Docker unavailable |
| M1 | Deterministic reflow | complete | [Reflow evidence](agent-kit/runs/m1-reflow.md); sample checks pass; dense-banner readability remains limited |
| M2 | Bounded selection and repair | complete | [Selection evidence](agent-kit/runs/m2-selection.md); 15 paired cases, bounded/failure behavior verified |
| M3 | Adversarial hardening | in progress | [Repairs verified](agent-kit/runs/m3-hardening.md); M3-R1/R2 quality defects remain open |
| M4 | Efficiency and delivery | not started | Profile, compare resource costs, verify offline packaging and release checklist |

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

No tasks are currently claimed. Replace the empty row when work starts; retain closed-task outcomes in the work log rather than leaving stale active claims.

| Task ID | Owner / session | Branch / worktree | Claimed paths | State | Last update (with timezone) | Next action / handoff |
|---|---|---|---|---|---|---|
| — | — | — | — | unassigned | — | Next: M3-R1, then M3-R2 |

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

## How to update this file

1. **At start:** read root AGENTS.md, inspect local work, pull the current branch from origin using its safe sync rule, then re-read this file and verify branch/revision and working-tree changes, then read the relevant spec/milestone/evidence. Claim the task with your actual owner/session identifier, paths, and timestamp. Do not guess another agent's state.
2. **During work:** update after a meaningful checkpoint, a scope/ownership change, or a blocker. Record what is complete and the exact next step, especially before interruption. Do not add every command or private reasoning.
3. **Before handoff or completion:** refresh the current state, milestone/step status, active claim, and work log. Include changed paths, revision or change label, evidence links, checks run and not run, failures, blockers, and a concrete resume action. Remove resolved blockers rather than leaving contradictory summaries.
4. **Before committing:** recheck/pull remote changes using the root sync rule, rerun affected checks, and re-read the latest tracker; merge concurrent entries without discarding anyone's work. Include the progress update in the same commit as the requested change. Do not check off a step merely because code exists.
5. **After pushing:** verify the push and report its outcome. If it fails, keep the local commit and report the failure; do not force-push or mark the remote synchronized. Git is authoritative for commit/push state, so no extra bookkeeping commit is required merely to insert the containing hash.

For longer work, add detailed run records under `agent-kit/runs/` using [EXPERIMENTS.md](agent-kit/EXPERIMENTS.md), then link them here. Keep the current-state sections short enough to read at every handoff. Archive older log entries only into a linked tracked document, preserving evidence and unresolved decisions.
