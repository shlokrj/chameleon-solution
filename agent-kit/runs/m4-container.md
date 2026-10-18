# Docker runtime setup and offline verification

Date: 2026-10-18 America/Chicago. Parent fe4e76f. Change `build: verify offline amd64 containers on colima`.

## Runtime setup

Docker was absent; Podman was installed but had no machine. Installed Homebrew docker 29.9.1, docker-buildx 0.38.0, colima 0.10.3 (Lima 2.2.1 dependency). Added Homebrew's CLI plugin directory to the existing Docker config without replacing other settings. Started Colima's Docker runtime with 4 CPUs, 4 GiB memory, 20 GiB data disk, VZ virtualization and Rosetta amd64 emulation. Docker server reports 29.5.2. Existing Podman configuration was untouched. No login-start service was enabled. Colima remains running for use; restart later with `colima start`, stop with `colima stop`.

Docker context is now colima. Repository verification commands explicitly request linux/amd64 for runs as well as builds, avoiding the previous host-architecture warning. Both production and verification images were built from the pinned Python digest and dependency set; first build installed all dependencies and system libraries, subsequent script verification reused layers.

## Executed checks

- scripts/verify-container.sh completed successfully twice (second run verifies explicit platform flags). Production and verification images are linux/amd64.
- All 55 unit tests pass inside the verification container with --network none.
- Production entrypoint runs with --network none and read-only source mounts, generating all three supplied JSON/PNG pairs in a fresh output directory.
- Independent validation inside the verification image passes schema/contract and direct-render pixel checks for all three pairs. [Delivery report](m4-container-evidence/delivery.json). All three output PNGs inspected by the integrator; dense sample remains small and its missing holiday badge is intentional.
- All 42 broader parity tasks pass structural checks under Linux. A second run in the same Linux image reproduces exact layouts, selected scores and pixels for all 42. [Repeat and cross-platform evidence](m4-container-evidence/parity.json).
- Container resources: five fresh production-entrypoint processes each handled all three inputs. End-to-end wall times 1.66–2.34 s, peak child RSS 282357760 bytes (269.3 MiB), cgroup memory.peak 222621696 bytes (212.3 MiB). These accounting methods differ and are not interchangeable. Timings include Python startup/imports/engine/render/output; OS caches were not cleared. This is emulated amd64 on Apple Silicon, not native benchmark hardware. [Raw measurements](m4-container-evidence/resources.json), [measurement script](m4-container-evidence/measure.py).
- docker image ls reports production 1.23 GB and verification 1.24 GB. Image inspect exposes a smaller Size field with this containerd-backed engine; both raw views/IDs are preserved rather than conflated. [Environment](m4-container-evidence/environment.json).

Temporary measurement container was removed after confirming NetworkMode=none and exit code 0. Images and Colima remain available. Build cache was retained for subsequent work; no unrelated containers/volumes/images were deleted.

## Cross-platform quality caveat

Strict macOS-to-Linux comparison failed, rather than being silently weakened: 30/42 layouts, 41/42 pixel hashes and 7/42 score dictionaries differ. Renderer font advances/heights differ between these environments (e.g. rotated SOLSTICE width 187.488 vs 186px). No structural or text-overflow set changes appeared. Exact determinism is verified within Linux, not across operating systems.

One material follow-up is dense-labels-compact: five group-label font sizes fall from 9.569px on macOS to 6.325px on Linux; local loss rises from 0.0527 to 0.1649, despite all hard constraints passing. Linux output was inspected and remains very small. Use container-based quality baselines for subsequent tuning rather than assuming native macOS typography predicts the judged output. No runtime fix for this separate quality issue was attempted here.

Fontconfig emits an unknown reset-dirs element warning from the Debian configuration; all renderer calls and checks succeed. It is retained in evidence, not suppressed or misclassified as a full-render fallback. The expected single missing-asset badge warning also persists. Base/system dependency reproducibility limitations from the packaging record still apply.

## Status and resume

Docker availability/build/offline-execution blocker is resolved. M4 remains in progress for final quality/release review: review Linux dense-label readability and unresolved organizer requirements in SOURCES (including viewer/submission details). This report does not claim competition submission readiness. Release checklist container items can now be checked with actual evidence.

Run again from the repository root:

```sh
colima start
./scripts/verify-container.sh
```

Final local artifacts: artifacts/m4-container-final.log and artifacts/container-check.HtLlhL/output. Earlier clean-build log is artifacts/m4-container-run.log. Broader Linux reports/PNGs are artifacts/m4-container-parity and artifacts/m4-container-repeat.
