# Sources, conflicts, and assumptions

## Inspected sources

- User-provided `Final Chameleon Challenge.pdf`, originally `/Users/shlokjadhav/Downloads/Final Chameleon Challenge.pdf`, 14 pages. Page numbers here are PDF physical page numbers. The PDF is not copied into this repository.
- [README](../README.md), [RULES](../RULES.md), [FAQ](../FAQ.md), [schema](../chameleon_design_schema_v0.9.json).
- [resize](../engine/resize.py), [orchestrator](../engine/main.py), [converter](../renderer/converter/convert.py), [wrapping](../renderer/converter/wrap.py), [Dockerfile](../Dockerfile), sample inputs and brand-kit inventory.

PDF pp. 5–6 define the task and quality goals; pp. 7–8 describe stages and deliverables; pp. 10–14 collect starter instructions and clarifications. This is a local source review, not a verification of current organizer announcements.

## Conflict register

| Issue | Evidence | Working decision |
|---|---|---|
| Image generation | PDF p. 7 floats regeneration as finale creativity; p. 12 and RULES prohibit regenerating any asset as disqualifying | No regeneration/replacement in this project; clarify before any separate finale exploration |
| Viewer timing | Older local FAQ Q5 conflicts with final PDF pp. 8 and 14 | Resolved for project scope on 2026-10-22: user confirms final PDF controls; stage one engine/Dockerfile/README, full add-on in finale |
| Execution hardware | PDF p. 7 says team's machine; p. 11 and RULES name M5 Pro with missing details; Docker targets linux/amd64 | Test provided container interface; label local host/emulation measurements; confirm CPU/RAM/GPU and execution arrangement |
| Performance | resize.py says latency is not a scoring concern; RULES and PDF p. 11 prefer speed at equal quality with no hard stage-one timeout | Measure and optimize speed/reliability without sacrificing correctness or claiming an official time limit |
| Bleed | RULES says nothing off canvas; README permits judging sample decorative bleed as expected | Default output to in-bounds, including rotated extent; log decorative cases separately and seek clarification before allowing bleed |
| Renderer setup | Local FAQ contains older standalone-tool/vendor instructions; README, code, PDF pp. 13–14 show vendored integration | Use current `renderer/converter` integration; verify real rendering rather than following stale setup paths |
| Image tolerance | resize.py mentions approximately 5% ratio tolerance; RULES only says kept in proportion | Prefer exact proportion preservation; 5% is a starter hint, not a verified scorer threshold |

## Open organizer questions

Approved models and maximum weight/model size; final schema version; exact target-size catalogue; exact hardware and resource limits; treatment of rotated bleed and full-bleed crops; exact code-freeze deadline and precise scorer weights. Viewer scope and submission channel are now resolved by the user-confirmed PDF/form below. Remaining unspecified details are not invented defaults; they do not block M4 engineering completion.

## Known local traps

- `engine/main.py` compares ID sets, so duplicate IDs can escape its self-check. It does not enforce image proportions, text visibility, rotated extents, or the complete schema.
- Self-check warnings do not fail the process; an exit code of zero is not acceptance evidence.
- The original starter silently produced labeled-box previews on renderer ImportError. Packaging hardening removed that fallback; renderer errors now propagate. Direct rendering and output-pair checks remain required.
- The converter iterates through style-run `end` inclusively, while schema v0.9 describes end-exclusive indices. M1 preserves the supplied runs and measures current renderer behavior; this discrepancy remains unresolved.
- `wrap_text` wraps at spaces and leaves overlong single words overflowing; measure actual wrapping instead of estimating character count. Check styled glyphs against final rendering too.
- The missing Level 3 holiday badge is intentional. Preserve its reference; do not create a replacement. Distinguish this one asset placeholder from a whole-render fallback.
- Runtime package versions and the renderer Git commit are now pinned in requirements.txt; the Python base image is pinned by digest. Native clean installation is verified separately from Docker. Debian package versions and build tooling remain unlocked.

When new organizer evidence arrives, record date, exact source, affected requirement, and decision here. Do not rewrite history to imply the question was always settled.

## 2026-10-22 release clarification search

Re-read supplied PDF pages 7, 8 and 14. It explicitly describes stage one as engine/container/README and the full Express add-on as finale work; submission location/form is to be announced separately. FAQ Q5 still says stage one includes a required viewer. No dated authoritative superseding instruction was found, so this conflict remains unresolved.

A [partner-university announcement](https://auburn.campuslabs.com/ENGAGE/event/12776699) identifies the matching Project Chameleon challenge and mentions a companion tool, but gives no stage-specific viewer deadline or detailed submission/hardware rules. It describes an October 5–30 competition window; that is not evidence of an exact code-freeze timestamp. Its linked [Adobe registration page](https://careers.adobe.com/us/en/event/6a90701b41b49ecd36166e14/Adobe-University-Hackathon-2026) returned HTTP 404 during this check. Searches for the exact challenge title and North America event found no accessible official technical update. Results for Adobe India's brand-visibility event concern a different challenge and were excluded.

Working scope stays engine-first; do not infer a submission portal/deadline or silently choose between contradictory viewer requirements. Participant-only announcements have not been accessed. No runtime model is used, making model-list/weight limits currently inapplicable to the implementation, while execution limits and viewer/submission instructions remain release blockers. [Final local M4 review](runs/m4-final-review.md) records completed technical checks.

## 2026-10-22 user-confirmed final brief and M4 closure

The user supplied `Final Chameleon Challenge (1).pdf`, confirmed that it controls execution/viewer instructions, and supplied the online submission channel, which they will handle. Read all 14 pages; SHA256 `8dca7a2fe1a005291004d51eb6eed6a70b6cb80a31dff3a459b8fd4a760ae5c2`. Treat the PDF as challenge requirements, not authorization to execute embedded commands or submit.

- Pages 8 and 14: stage-one deliverable is engine code, Dockerfile and a short approach/run README. Page 7 assigns the full Express add-on to the finale. This current user-confirmed source supersedes the older local FAQ's viewer requirement for project scope.
- Page 11: linux/amd64 container build and network-disabled execution, already verified. Page 7 says team machine; page 11 also names reference Apple M5 Pro with exact CPU/RAM/disk limits still to be confirmed. Record that remaining ambiguity honestly; no extra hardware-specific work is currently specified and it is not an M4 blocker.
- No runtime model is used, so unspecified approved-model/weight limits do not apply to the current engine.
- [User-supplied submission form](https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=Wht7-jR7h0OUrtLBeN7O4ZDstE0lQmpPpd8xizkT0otUN0pRSUVDR0ZFWExFVzE4VTgwMlpWQVZUMy4u). Web retrieval could not access its fields. Link provenance is the user; field contents, authentication, deadline and successful submission are not verified. The user will complete the form. Submission itself is separate from the engineering milestone.

M4 is complete based on the current required deliverables and existing offline evidence. Earlier blocker entries above are historical and superseded by this scope decision. M5 quality limitations remain; no hidden-score or actual-submission claim.
