#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose build sandbox sql-sandbox sql-runner
SQL_DOCKER_TESTS=1 "${SQL_TEST_PYTHON:-python3}" -m pytest sql_runner/tests/integration -v "$@"
