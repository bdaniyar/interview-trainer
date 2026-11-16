from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path

from backend.app.sql_content import REGISTRY as BACKEND
from sql_runner.app.grading_content import REGISTRY as RUNNER, load_task

ROOT=Path(__file__).resolve().parents[2]
BASELINE=json.loads((Path(__file__).with_name('fixtures')/'sql-phase7-contracts.json').read_text())


def test_every_previous_registration_field_and_bank_record_is_immutable():
    for current,key in [(BACKEND,'backend'),(RUNNER,'runner')]:
        # JSON round trip normalizes tuple/list representation only.
        assert json.loads(json.dumps([asdict(v) for v in list(current.values())[:12]]))==BASELINE[key]
    records={r['id']:r for r in json.loads((ROOT/'content/practice_banks.json').read_text())['sql']}
    for task_id,digest in BASELINE['bank'].items():
        assert sha256(json.dumps(records[task_id],sort_keys=True,ensure_ascii=False).encode()).hexdigest()==digest


def test_historical_bank_lesson_numbers_have_explicit_current_capabilities(client):
    records={r['id']:r for r in json.loads((ROOT/'content/practice_banks.json').read_text())['sql']}
    for task_id,historical,slug in [('sql.subquery.32','10.17','s10-recursive-cte'),('sql.window.38','10.21','s10-lag-and-lead')]:
        assert records[task_id]['lesson_number']==historical
        result=client.get('/api/sql/lessons/'+slug)
        assert result.status_code==200 and result.json()['task_id']==task_id
        assert client.get('/api/lessons/'+slug).json()['workspace_kind']=='sql'
    for task_id in list(RUNNER)[:12]:
        entry=RUNNER[task_id]
        assert not load_task(task_id,entry.task_revision,entry.grader_revision).ordered_key_columns
