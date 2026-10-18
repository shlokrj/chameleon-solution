#!/usr/bin/env bash
# Build both images and verify production outputs with networking disabled.
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"
command -v docker >/dev/null || { echo 'Docker is required for container validation.' >&2; exit 1; }
mkdir -p artifacts
run_dir="$(mktemp -d "$repo_root/artifacts/container-check.XXXXXX")"
mkdir -p "$run_dir/output"
docker build --platform linux/amd64 --target production -t chameleon-engine .
docker build --platform linux/amd64 --target verification -t chameleon-verify .
docker run --rm --network none --entrypoint python chameleon-verify -m unittest discover -s tests -v
docker run --rm --network none -v "$repo_root/input:/app/input:ro" -v "$run_dir/output:/app/output" chameleon-engine
docker run --rm --network none --entrypoint python -v "$repo_root/input:/app/input:ro" -v "$run_dir/output:/app/output" chameleon-verify -m evaluation.delivery --report /app/output/validation-report.json
printf 'Validated output pairs and report: %s/output\n' "$run_dir"
