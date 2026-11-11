#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose build sandbox sql-sandbox sql-runner
cleanup() { docker compose -f docker-compose.sql-workspace-test.yml down; }
trap cleanup EXIT
docker compose -f docker-compose.sql-workspace-test.yml up -d --build --wait
"${SQL_TEST_PYTHON:-python3}" scripts/smoke_sql_workspace.py
docker compose -f docker-compose.sql-workspace-test.yml stop sql-runner
"${SQL_TEST_PYTHON:-python3}" scripts/smoke_sql_workspace.py --sql-offline
