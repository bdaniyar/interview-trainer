import asyncio
import json
from pathlib import Path

from contracts import PROMPT_DEMO, PROMPT_V1
from evaluate import DATA, evaluate
from metrics import score
from prompt import EXAMPLES


def test_frozen_dataset_and_reproducible_report():
    cases=[json.loads(line) for line in DATA.read_text().splitlines()]
    assert len({case["id"] for case in cases}) == len(cases) == 20
    assert sum(case["partition"] == "dev" for case in cases) == 12
    assert not {case["text"] for case in cases} & {text for text,_ in EXAMPLES}
    report=asyncio.run(evaluate())
    expected=json.loads((Path(__file__).parents[1] / "data/evaluation-report.json").read_text())
    assert report == expected == asyncio.run(evaluate())


def test_regression_is_detected_separately_from_schema():
    report=asyncio.run(evaluate())["versions"]
    baseline, changed=report[PROMPT_V1],report[PROMPT_DEMO]
    for partition, expected_counts in {"dev": (8,5), "holdout": (8,4)}.items():
        before,after=baseline[partition]["metrics"],changed[partition]["metrics"]
        assert before["schema_validity"] == after["schema_validity"]
        assert before["unknown_correctness"]["total"] == after["unknown_correctness"]["total"] == 8
        assert (before["unknown_correctness"]["passed"],after["unknown_correctness"]["passed"]) == expected_counts
    assert baseline["dev"]["errors"]["trip-11"] == ["city"]
    assert baseline["holdout"]["errors"]["trip-19"] == ["status", "check_out"]


def test_undefined_metrics_have_null_rate():
    empty=score([], {})
    assert empty["errors"] == {} and all(
        value == {"passed":0,"total":0,"rate":None} for value in empty["metrics"].values()
    )
