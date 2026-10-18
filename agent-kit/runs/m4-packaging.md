# M4 packaging hardening: native verified, container blocked

Date: 2026-10-17 America/Chicago. Parent f43272e; change `build: pin tested dependencies and require real rendering`.

## Changes

Pinned the 40-package installed runtime dependency closure, including cr-renderer Git commit a17e1fb9a732959dd6c21ae168d5ee09d74bd64f, plus four development validation packages. Python target changes from 3.11 to tested 3.12.13 because pinned NumPy 2.5.4 requires Python >=3.12. The official registry returned a Python 3.12.13-slim index including linux/amd64; Dockerfile pins that verified digest. [Registry manifest evidence](m4-package-evidence/base-image.json).

The Docker build context whitelist excludes local environments, artifacts, Git history and generated output. Production copies only engine/renderer/assets/schema and runtime requirements. Optional verification stage adds test/evaluation dependencies and inputs; final default stage remains production. scripts/verify-container.sh builds both, runs tests and production with --network none, then independently validates JSON/PNG pairs in the verification image. It uses fresh output directories, read-only source mounts, and explicit entrypoint overrides for test/validation commands.

Removed the starter's whole-design placeholder fallback. Renderer import/backend failures now propagate and fail the entrypoint; the intentional missing holiday-badge asset placeholder remains. evaluation.delivery checks every input has independently contract-valid JSON and a real PNG matching a direct re-render; missing, corrupt or mismatched pairs fail. The normal successful output contract is unchanged.

## Verified evidence

- Created fresh native Python 3.12 virtual environment under artifacts/m4-clean-env and installed pinned development requirements successfully. pip check reports no broken requirements. This uses normal build-time network access and pip cache; it is not an offline install.
- 55 unit tests pass there, including missing-renderer/backend failure propagation and delivery rejection of incorrect pixels, duplicate-element JSON, and missing PNG.
- Real production entrypoint generated all three supplied pairs. [Independent delivery check](m4-package-evidence/delivery.json) passes; the expected Level 3 missing-asset warning is retained.
- [42-case comparison](m4-package-evidence/parity.json) matches prior selected quality scores, output JSON and decoded pixels exactly in the clean environment. No layout/readability improvement is claimed.
- [Linux wheel resolution](m4-package-evidence/linux-resolution.json): pip dry-run successfully resolved pinned binary packages for CPython 3.12/linux amd64. This excludes the VCS renderer package (installed natively from its fixed commit) and does not prove Linux import/shared-library/runtime success.
- [Independent static review](m4-package-evidence/REVIEW.md) found no confirmed packaging blocker. Same inherited model in separate context with shared filesystem, not cross-model validation. Review is not container execution evidence.
- Container script syntax passes bash -n. Actual script invocation reports Docker is required before building anything because Docker is absent from PATH. Docker builds, network-disabled execution, image size and container memory remain UNRUN.

## Reproducibility limits and resume

Package versions, renderer source revision and Python image digest are fixed. Debian apt package versions, Python build-system dependencies and PyPI artifact hashes are not enforced in requirements, so this is not a hermetic/bit-reproducible build. Linux-resolution evidence records selected archive hashes for inspection. The native runtime closure may need explicit platform-specific adjustments only if actual container validation reveals them; do not claim cross-platform success from metadata resolution.

M4 is blocked on a Docker-capable environment. Do not mark it complete from native results. Resume with:

```sh
./scripts/verify-container.sh
```

Then inspect the saved validation report/output PNGs, record image size and container resource results, and complete the release checklist. Source caveats (viewer requirement, approved model rules, judging hardware, bleed) remain unresolved where relevant to submission. No competition submission is authorized or performed.
