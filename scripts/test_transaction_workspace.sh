#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
scratch=$(mktemp -d)
compose=(docker compose -p pythoria-sql-workspace-test -f docker-compose.sql-workspace-test.yml -f "$scratch/storage.yml")
cleanup() {
  local code=$?
  if (( code != 0 )); then
    "${compose[@]}" logs --no-color --tail=50 backend tx-runner || true
  fi
  "${compose[@]}" down --volumes
  rm -rf "$scratch"
  return "$code"
}
trap cleanup EXIT
cat > "$scratch/storage.yml" <<'YAML'
services:
  backend:
    tmpfs: !reset []
    volumes:
      - transaction_test_data:/data
volumes:
  transaction_test_data:
YAML
docker compose build sandbox sql-sandbox sql-runner tx-sandbox tx-runner
"${compose[@]}" up -d --build --wait
python3 scripts/smoke_transaction_workspace.py --save-replays "$scratch/replays.json"
"${compose[@]}" restart backend
"${compose[@]}" up -d --wait
python3 scripts/smoke_transaction_workspace.py --verify-replays "$scratch/replays.json"
