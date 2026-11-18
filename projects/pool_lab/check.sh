#!/usr/bin/env bash
set -euo pipefail
project=$(cd "$(dirname "$0")" && pwd)
submission=${1:-"$project/starter.py"}
scratch=$(mktemp -d)
namespace="pythoria-pool-$(basename "$scratch" | tr '[:upper:]' '[:lower:]' | tr -dc 'a-z0-9')"
compose=(docker compose -p "$namespace" -f "$scratch/compose.yml")
cleanup() {
  local code=$?
  "${compose[@]}" down --volumes
  rm -rf "$scratch"
  return "$code"
}
trap cleanup EXIT
cp "$project"/{compose.yml,schema.sql,Dockerfile,requirements.txt,test_pool.py} "$scratch/"
cp "$submission" "$scratch/submission.py"
"${compose[@]}" up --build --abort-on-container-exit --exit-code-from exercise
