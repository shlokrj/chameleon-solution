# Stage-one submission handoff

Engineering milestones M0–M5 are complete. The production engine is the version frozen at `9dc59b3`; subsequent commits add final review fixtures and documentation. This handoff does not assert an official score or successful submission.

## What to submit

Use the [project repository](https://github.com/shlokrj/chameleon-solution) or a source ZIP of its current committed revision, according to the form's actual requirements. The source contains the engine, Dockerfile, pinned Python dependencies, schema, renderer integration, supplied assets/fonts and the approach/run README. Evaluation tools and evidence are included for reproducibility; Docker production does not include the evaluation/test tools.

The user will complete the [provided submission form](https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=Wht7-jR7h0OUrtLBeN7O4ZDstE0lQmpPpd8xizkT0otUN0pRSUVDR0ZFWExFVzE4VTgwMlpWQVZUMy4u). Its fields, deadline, upload type and access requirements have not been inspected successfully here. Supply team details yourself and ensure judges can access the repository or uploaded source. No submission has been made by the agent.

The user-confirmed final PDF requires engine/Dockerfile/README for stage one. The full Adobe Express add-on is finale work. Exact hardware limits remain unspecified; see [source decisions](agent-kit/SOURCES.md).

## Run and verify

From the extracted repository root with Docker running:

```sh
mkdir -p output
docker build --platform linux/amd64 -t chameleon-engine .
docker run --rm --platform linux/amd64 --network none \
  -v "$(pwd)/input:/app/input:ro" \
  -v "$(pwd)/output:/app/output" chameleon-engine
```

Each task in `input/` produces `<task>_output.json` and `<task>_output.png` in `output/`. All runtime dependencies are installed during build; runtime requires no network, model weights, credentials or external API. The build itself needs dependency downloads when layers are not cached.

Run `./scripts/verify-container.sh` for the complete container unit/delivery checks. Saved final review fixtures can be rerun using [their instructions](tests/fixtures/m5-final/README.md).

## Evidence and honest limitations

- 75 offline tests and all three supplied JSON/PNG delivery checks pass.
- 70 catalogue layouts pass contracts and measured text fit; 42 parity cases repeat exactly.
- Final independent review passes three fresh cases, now preserved as exposed regressions.
- Very dense Level 3 layouts still contain small text; small/low-contrast logos and collision-aware corner anchoring remain limitations. No perfect readability or hidden-set success is claimed.
- The supplied missing holiday badge is intentional and remains a visible placeholder; do not replace its asset.

See [approach and run instructions](README.md), [M4 verification](agent-kit/runs/m4-final-review.md), [M5 closure](agent-kit/runs/m5-final.md), and [project progress](PROGRESS.md).
