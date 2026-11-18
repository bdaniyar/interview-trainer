#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
runner=${SQL_TEST_PYTHON:-python3}
PYTHONPATH=. "$runner" scripts/verify_stage11.py
compose=(docker compose -p pythoria-stage11-examples -f projects/durable_queue/compose.test.yml)
scratch=$(mktemp)
cleanup() {
  local code=$?
  "${compose[@]}" down
  rm -f "$scratch"
  return "$code"
}
trap cleanup EXIT
"$runner" - "$scratch" <<'PY'
from pathlib import Path
import re
import sys
source = Path("content/stage-11/s11-connection-pooling/lesson.md").read_text()
blocks = re.findall(r"```python\n(.*?)```", source, re.S)
assert len(blocks) == 1
Path(sys.argv[1]).write_text(blocks[0])
PY
"${compose[@]}" build api
"${compose[@]}" up -d --wait db
"${compose[@]}" run --rm -T --no-deps api python -c "$(cat scripts/verify_stage11_pooling.py)" < "$scratch"
