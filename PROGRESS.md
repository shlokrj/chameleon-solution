# Project progress and handoff

Read this first when joining or resuming work. This is the shared current-state summary; detailed evidence belongs in [experiment records](agent-kit/EXPERIMENTS.md). Verify the checkout and relevant artifacts before trusting an older entry.

## Current state

- **Phase:** planning and agent guidance complete; engine implementation has not started.
- **Implementation progress:** 0 of 5 milestones complete. Next: M0, establish evidence. This count is not a percentage of effort or an estimate of time remaining.
- **Engine:** supplied stretch baseline remains unchanged. No engine tests, real-render validation, Docker runs, or performance benchmarks have been executed during the documentation work.
- **Latest verified predecessor:** `81de421` on `main`, pushed to `origin`. This progress-tracking change is recorded in its containing commit; use `git log -1 -- PROGRESS.md` to resolve that revision without a self-referential hash.
- **Active implementation owners:** none assigned. Do not infer that an agent is running from a historical entry.
- **Next concrete action:** claim M0.1 below, inspect the environment, and establish the independent baseline described in [IMPLEMENTATION.md](agent-kit/IMPLEMENTATION.md).

## Milestone board

The definitions and exit criteria live in [IMPLEMENTATION.md](agent-kit/IMPLEMENTATION.md). Mark a milestone complete only when those criteria have evidence. Use `not started`, `in progress`, `blocked`, or `complete`; record a blocked reason and next action.

| ID | Milestone | State | Evidence / remaining work |
|---|---|---|---|
| Prep | Specification, agent guidance, evaluation workflow | complete | `ea0b910`, `81de421`; links and both project skills validated |
| M0 | Establish evidence | not started | Environment, real renders, independent contract checks, baseline measurements |
| M1 | Deterministic reflow | not started | Depends on M0; implement and verify generalized layout behavior |
| M2 | Bounded selection and repair | not started | Depends on M1; compare candidates and verify bounded fallback |
| M3 | Adversarial hardening | not started | Requires explicit launch and a frozen candidate; independent failure reproduction and fresh holdout |
| M4 | Efficiency and delivery | not started | Profile, compare resource costs, verify offline packaging and release checklist |

## Next steps within M0

Check boxes mean verified completion, not intent. Link an experiment record or commit when checking one. Split further if needed; keep stable IDs so collaborators can refer to the same work.

- [ ] **M0.1** Inspect current checkout, dependencies, Python/renderer availability, and container capability; record environment and any blockers.
- [ ] **M0.2** Establish independent checks for the contract in [SPEC.md](agent-kit/SPEC.md), distinguishing directly testable invariants from generalization evidence.
- [ ] **M0.3** Run all three unchanged sample inputs and capture output JSON, direct real-renderer PNGs, warnings, and engine/pipeline timings.
- [ ] **M0.4** Inspect the renders, document baseline failures and measurement limits, and link a reproducible experiment record.
- [ ] **M0.5** Review M0 exit criteria, update the milestone board, and define the next bounded M1 task.

## Active work and ownership

No tasks are currently claimed. Replace the empty row when work starts; retain closed-task outcomes in the work log rather than leaving stale active claims.

| Task ID | Owner / session | Branch / worktree | Claimed paths | State | Last update (with timezone) | Next action / handoff |
|---|---|---|---|---|---|---|
| — | — | — | — | unassigned | — | Claim a bounded task before editing |

Claims are coordination records, not locks. Before editing, re-read this table and check current Git status. Do not overwrite another owner's changes. Assign one integrator for overlapping paths or the shared tracker. In separate clones/branches, reconcile claims through the collaborators' coordination channel; a local Markdown edit cannot reserve remote work. Treat old claims as needing verification, not automatic permission to take over.

## Decisions and unresolved questions

- Preserve supplied text, fonts, element identity, grouping, and original asset pixels. No sample-specific layout branches.
- Development-time agent collaboration does not require a model in the runtime engine.
- User standing instruction: validate, commit, and push each completed requested change; lowercase Conventional Commit subjects, user's identity only, no co-authors.
- [SOURCES.md](agent-kit/SOURCES.md) is the authority for source conflicts and unknown organizer details, including viewer timing, model limits, hardware, and bleed. These questions do not block a deterministic baseline, but relevant unresolved submission requirements block a submission-ready claim.
- The user requested planning and progress documentation so far. Do not interpret the next-step list as a new instruction to begin implementation or launch agents without an applicable task request.

## Work log

Keep entries concise and factual. Use a stable change label when the containing commit hash is not yet available; Git history provides that hash. Never claim a push succeeded before checking its result.

| Change / revision | Work completed | Validation actually run | Remaining / handoff |
|---|---|---|---|
| `ea0b910` | Added spec, source register, implementation/evaluation plans, adversarial workflow, prompts, and two skills | Markdown links and both skill validators passed | Engine unchanged; no benchmark evidence |
| `81de421` | Added model comparison/improvement notes and standing commit-and-push policy | Markdown links, both skill validators, whitespace checks passed | No model comparisons or engine experiments run |
| `docs: add shared progress tracking and agent handoff rules` (containing commit) | Added this tracker and mandatory agent read/update rules | Relative Markdown links, tracker consistency, and diff whitespace checked before commit | M0 remains unstarted; next owner should claim M0.1 |

## How to update this file

1. **At start:** read root AGENTS.md and this file, verify branch/revision and working-tree changes, then read the relevant spec/milestone/evidence. Claim the task with your actual owner/session identifier, paths, and timestamp. Do not guess another agent's state.
2. **During work:** update after a meaningful checkpoint, a scope/ownership change, or a blocker. Record what is complete and the exact next step, especially before interruption. Do not add every command or private reasoning.
3. **Before handoff or completion:** refresh the current state, milestone/step status, active claim, and work log. Include changed paths, revision or change label, evidence links, checks run and not run, failures, blockers, and a concrete resume action. Remove resolved blockers rather than leaving contradictory summaries.
4. **Before committing:** re-read the latest tracker; merge concurrent entries without discarding anyone's work. Include the progress update in the same commit as the requested change. Do not check off a step merely because code exists.
5. **After pushing:** verify the push and report its outcome. If it fails, keep the local commit and report the failure; do not force-push or mark the remote synchronized. Git is authoritative for commit/push state, so no extra bookkeeping commit is required merely to insert the containing hash.

For longer work, add detailed run records under `agent-kit/runs/` using [EXPERIMENTS.md](agent-kit/EXPERIMENTS.md), then link them here. Keep the current-state sections short enough to read at every handoff. Archive older log entries only into a linked tracked document, preserving evidence and unresolved decisions.
