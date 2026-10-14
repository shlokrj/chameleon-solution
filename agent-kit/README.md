# Chameleon agent kit

A working brief for building a robust, efficient design-retargeting engine. This kit was prepared from the supplied challenge PDF and inspected starter repository on 2026-10-13. It is guidance, not an implemented solution or evidence of benchmark performance.

## Start here

1. Read [AGENTS.md](AGENTS.md) and [SPEC.md](SPEC.md).
2. Check [SOURCES.md](SOURCES.md) for source conflicts and unresolved organizer details.
3. Implement in milestones from [IMPLEMENTATION.md](IMPLEMENTATION.md).
4. Validate with [EVALUATION.md](EVALUATION.md); use [ADVERSARIAL.md](ADVERSARIAL.md) for model-versus-model rounds.
5. Record evidence using [EXPERIMENTS.md](EXPERIMENTS.md).

Load only the documents relevant to the current milestone. The schema and original rules remain in the repository; this kit deliberately does not duplicate them field by field.

## Reusable skills

- [chameleon-implement](skills/chameleon-implement/SKILL.md): implementation and regression workflow.
- [chameleon-challenge](skills/chameleon-challenge/SKILL.md): reproducible adversarial cases and independent adjudication.

These are project-local skill source files. They are not automatically installed or registered in an agent's skill catalogue. Explicitly instruct an agent to read the relevant file; keep the kit together so relative references resolve.

## Launch prompt

> Work on the Chameleon engine in this repository. Read AGENTS.md and agent-kit/README.md, then follow the linked spec and implementation skill. Establish a measured baseline before changing the algorithm. Implement and validate one milestone at a time. Optimize robustness and quality first, then reduce measured runtime and resource cost. Preserve source assets, text, fonts, element identity, and grouping. Report evidence and unresolved limitations. Do not commit or submit.

To explicitly enable adversarial collaboration, append:

> Run bounded builder/challenger/judge rounds following agent-kit/ADVERSARIAL.md. Use distinct model families if available; otherwise disclose the models actually used. You may delegate those roles. Begin with the default round budget and stop at its defined stopping conditions. Keep one integration owner and do not let agents edit the same files concurrently.

Do not claim different roles are different models unless their actual model identities are known. No particular model or model subscription is required by this kit.
