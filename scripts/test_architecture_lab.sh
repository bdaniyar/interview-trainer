#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
compose=(docker compose -f projects/architecture_lab/compose.test.yml)
cleanup() { "${compose[@]}" down --remove-orphans; }
trap cleanup EXIT
"${compose[@]}" build orders
"${compose[@]}" up -d --wait db orders notifications monolith
"${compose[@]}" run --rm tests pytest -q -p no:cacheprovider tests "$@"
