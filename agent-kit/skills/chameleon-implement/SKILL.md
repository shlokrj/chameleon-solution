---
name: chameleon-implement
description: Implement or improve this repository's Chameleon retargeting engine with contract checks, real-render validation, and measured efficiency.
---

Read [working agreement](../../AGENTS.md), [spec](../../SPEC.md), and [source caveats](../../SOURCES.md). Use [implementation milestones](../../IMPLEMENTATION.md) to choose the smallest useful next change; load [evaluation](../../EVALUATION.md) for its acceptance checks.

Preserve the `resize` interface and every source element. Infer relationships from source evidence rather than sample IDs. Fit text with the actual fonts/wrapper, preserve groups and intended layering, and enforce ordinary image proportions and rotated bounds. Keep internal metadata out of the output.

First establish a real-rendered baseline. `main.py`'s successful exit and self-check are insufficient: fallback boxes, duplicate IDs, or clipped text can escape them. Keep test fixtures separate from supplied input files.

Use bounded deterministic candidate search before adding model dependencies. Profile engine and rendering separately before optimizing. Finish each milestone with reproduced evidence in the [record format](../../EXPERIMENTS.md), including failures and unrun checks. Load [adversarial protocol](../../ADVERSARIAL.md) only when adversarial work is in scope. Follow the repository standing commit-and-push instruction after validating completed requested changes; competition submission needs separate user instruction.
