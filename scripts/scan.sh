#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
trivy fs --scanners vuln,secret --format json --output artifacts/trivy.json .
echo 'Saved artifacts/trivy.json (review findings; do not claim zero risk).'
