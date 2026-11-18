#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
compose=(docker compose -f projects/durable_queue/compose.test.yml)
cleanup() { "${compose[@]}" down --remove-orphans; }
trap cleanup EXIT
"${compose[@]}" build api
"${compose[@]}" up -d --wait db api
"${compose[@]}" run --rm tests
