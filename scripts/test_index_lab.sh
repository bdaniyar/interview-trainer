#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose build index-sandbox
SQL_DOCKER_TESTS=1 "${SQL_TEST_PYTHON:-python3}" -m pytest -o addopts='' -v index_lab/test_postgres.py "$@"
