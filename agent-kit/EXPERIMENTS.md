# Evidence records

No implementation experiments have been run for this kit. Create one Markdown record per meaningful milestone or adversarial round under `agent-kit/runs/` when work begins; do not prepopulate fictional results.

## Record template

```markdown
# <experiment ID and question>

Date:
Owner/role and actual model/version:
Baseline revision:
Candidate revision and dirty diff identifier:
Changed paths:
Hypothesis:
Fixture family IDs, split, provenance, generator version, seeds:
Environment, dependency/renderer versions, architecture/emulation:
Search/repair budget and evaluation settings:
Commands actually run:
Artifact paths (input, output JSON, real PNG, metrics/logs):

| Case/family | Hard checks | Visual findings | Engine/pipeline time | Memory | Verdict |
|---|---|---|---|---|---|

Worst case and minimized reproducer:
Baseline comparison and regressions:
Development cost (actual time/tokens if available):
Unrun checks and limitations:
Decision: accept / reject / inconclusive
Reason and next bounded step:
Holdout exposure/retirement status:
```

Keep detailed run evidence separate from the short public project README. Never record credentials, private model reasoning, or invented metrics. A summarized rationale and observable evidence are sufficient.
