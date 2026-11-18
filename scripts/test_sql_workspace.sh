#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose build sandbox sql-sandbox sql-runner tx-sandbox tx-runner
cleanup() {
  local smoke_exit_code=$?
  if (( smoke_exit_code != 0 )); then
    docker compose -f docker-compose.sql-workspace-test.yml logs --no-color --tail=80 || true
  fi
  docker compose -f docker-compose.sql-workspace-test.yml down
  return "$smoke_exit_code"
}
trap cleanup EXIT
docker compose -f docker-compose.sql-workspace-test.yml up -d --build --wait
"${SQL_TEST_PYTHON:-python3}" scripts/smoke_sql_workspace.py
docker compose -f docker-compose.sql-workspace-test.yml stop sql-runner
"${SQL_TEST_PYTHON:-python3}" scripts/smoke_sql_workspace.py --sql-offline

"${SQL_TEST_PYTHON:-python3}" scripts/smoke_worker_lessons.py
