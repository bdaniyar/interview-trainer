#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose build sql-sandbox
docker build -t pythoria-transaction-sandbox:phase9c -f transaction_lab/Dockerfile .
SQL_DOCKER_TESTS=1 "${SQL_TEST_PYTHON:-python3}" -m pytest transaction_lab/tests/integration -v "$@"
