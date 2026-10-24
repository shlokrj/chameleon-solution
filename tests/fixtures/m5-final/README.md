# Final bounded M5 holdout

Three deterministic hand-authored cases, no RNG, authored by the independent review role after engine freeze at `9dc59b3` on 2026-10-23. These combine styled multiline final copy, rotated final copy, and final-copy hierarchy next to a grouped button. All use supplied font families; no assets were manufactured. Details were withheld from the integration owner until evaluation and visual review finished. Shared filesystem isolation is procedural, not a sealed sandbox. Cases are now exposed and retired into regression coverage.

From repository root, with the verification image built for this revision:

```sh
docker run --rm --platform linux/amd64 --network none --entrypoint python -e PYTHONPATH=/app -v "$PWD/tests/fixtures/m5-final:/app/tests/fixtures/m5-final:ro" -v "$PWD/artifacts:/app/artifacts" chameleon-verify /app/tests/fixtures/m5-final/verify.py
```

This writes source, output and an ablated comparison with only final-tail refinement disabled; validates source schema and output contract; records quality, unchanged input and exact repeated output/diagnostics. The report deliberately does not turn local readability proxies into official scores. Inspect the generated PNGs separately. See [judge report](../../../agent-kit/runs/m5-final-judge.md).
