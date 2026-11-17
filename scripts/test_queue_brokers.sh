#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
compose=(docker compose -f projects/durable_queue/compose.brokers.yml)
cleanup() { "${compose[@]}" down --remove-orphans; }
trap cleanup EXIT
docker compose -f projects/durable_queue/compose.test.yml build api
"${compose[@]}" up -d --wait --wait-timeout 120 redis rabbit kafka celery
"${compose[@]}" run --rm client
python3 projects/durable_queue/check_kafka.py
