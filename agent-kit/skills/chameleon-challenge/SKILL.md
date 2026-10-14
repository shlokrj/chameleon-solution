---
name: chameleon-challenge
description: Generate and adjudicate reproducible edge cases for the Chameleon layout engine during an explicitly requested robustness or adversarial evaluation.
---

Read [spec](../../SPEC.md), [source caveats](../../SOURCES.md), [adversarial protocol](../../ADVERSARIAL.md), and [evaluation](../../EVALUATION.md). Stay in the assigned challenger or judge role; do not edit production code as challenger.

Generate a small batch spanning distinct plausible failure classes. Validate both the schema and semantic contract before calling a fixture an in-distribution counterexample. Keep malformed-input and renderer-limitation findings separate. Preserve literal text and original assets; never manufacture an asset to repair the intentional missing-badge case.

For each finding, provide a minimized input, seed/provenance, exact reproduction procedure, expected invariant, baseline/candidate artifacts, and observed failure. An unsupported model opinion is not a failing test. The judge must reproduce and inspect actual renders where geometry is insufficient.

Keep holdout fixtures unseen by the builder until its candidate is frozen; retire exposed cases into regression coverage. Follow bounded rounds and no-improvement stops. Record actual model identities and cost if available, and explicitly disclose same-model role separation. End with verified failure classes and unresolved limitations using [evidence records](../../EXPERIMENTS.md), not a claim of universal robustness.
