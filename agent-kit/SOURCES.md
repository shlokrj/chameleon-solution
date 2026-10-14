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
| Viewer timing | Local FAQ Q5 calls a viewer required for stage one; PDF pp. 8 and 14 put the full add-on in the finale and describe stage-one engine submission | Engine-first; verify viewer requirement before submission; do not declare submission complete while unresolved |
| Execution hardware | PDF p. 7 says team's machine; p. 11 and RULES name M5 Pro with missing details; Docker targets linux/amd64 | Test provided container interface; label local host/emulation measurements; confirm CPU/RAM/GPU and execution arrangement |
| Performance | resize.py says latency is not a scoring concern; RULES and PDF p. 11 prefer speed at equal quality with no hard stage-one timeout | Measure and optimize speed/reliability without sacrificing correctness or claiming an official time limit |
| Bleed | RULES says nothing off canvas; README permits judging sample decorative bleed as expected | Default output to in-bounds, including rotated extent; log decorative cases separately and seek clarification before allowing bleed |
| Renderer setup | Local FAQ contains older standalone-tool/vendor instructions; README, code, PDF pp. 13–14 show vendored integration | Use current `renderer/converter` integration; verify real rendering rather than following stale setup paths |
| Image tolerance | resize.py mentions approximately 5% ratio tolerance; RULES only says kept in proportion | Prefer exact proportion preservation; 5% is a starter hint, not a verified scorer threshold |

## Open organizer questions

Approved models and maximum weight/model size; final schema version; exact target-size catalogue; exact hardware and resource limits; treatment of rotated bleed and full-bleed crops; viewer requirement; submission location/deadline and precise scorer weights. These are unknown, not invented defaults. They do not prevent a deterministic offline baseline.

## Known local traps

- `engine/main.py` compares ID sets, so duplicate IDs can escape its self-check. It does not enforce image proportions, text visibility, rotated extents, or the complete schema.
- Self-check warnings do not fail the process; an exit code of zero is not acceptance evidence.
- Renderer import failure can silently produce labeled-box fallback previews. Validate direct real-renderer import and execution in evaluation.
- The converter iterates through style-run `end` inclusively, while schema v0.9 describes end-exclusive indices. M1 preserves the supplied runs and measures current renderer behavior; this discrepancy remains unresolved.
- `wrap_text` wraps at spaces and leaves overlong single words overflowing; measure actual wrapping instead of estimating character count. Check styled glyphs against final rendering too.
- The missing Level 3 holiday badge is intentional. Preserve its reference; do not create a replacement. Distinguish this one asset placeholder from a whole-render fallback.
- `requirements.txt` references a moving upstream renderer repository. Record the installed revision; assess pinning for reproducibility before final packaging.

When new organizer evidence arrives, record date, exact source, affected requirement, and decision here. Do not rewrite history to imply the question was always settled.
