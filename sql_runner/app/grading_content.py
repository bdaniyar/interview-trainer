"""Immutable grader bundles, loaded only in the controller (not the sandbox)."""
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path

from .datasets import load_dataset

TASK_ID = "sql.guided.10.2.projection.v1"
GRADER_REVISION = "projection-v1"
TASK_DIGEST = "6ae7700181c75b63ba3c5060733fe2b90c1482f9723f3a04ccc866e79ef4fef6"
GRADING_ROOT = Path(__file__).resolve().parents[1] / "grading"


class UnknownTask(ValueError):
    pass


@dataclass(frozen=True)
class Case:
    id: str
    seed: str | None  # None means the immutable public baseline already loaded.


@dataclass(frozen=True)
class Task:
    id: str
    revision: int
    grader_revision: str
    dataset_checksum: str
    expected_columns: tuple[str, ...]
    comparison: str
    numeric_compatible: bool
    reference_sql: str
    cases: tuple[Case, ...]


def load_task(task_id=TASK_ID, task_revision=1, grader_revision=GRADER_REVISION):
    # No task ID, revision, filename or path is interpolated from a request.
    if (task_id, task_revision, grader_revision) != (TASK_ID, 1, GRADER_REVISION):
        raise UnknownTask("Unsupported grading configuration")
    root = GRADING_ROOT / "projection-v1"
    wire = (root / "task.json").read_bytes()
    if sha256(wire).hexdigest() != TASK_DIGEST:
        raise ValueError("Grader revision integrity check failed")
    config = json.loads(wire)
    if config["dataset_checksum"] != load_dataset().checksum:
        raise ValueError("Grader baseline revision mismatch")
    cases = []
    for case in config["cases"]:
        seed = None
        if not case["public"]:
            filename = case["seed_file"]
            if Path(filename).name != filename or not filename.endswith(".sql"):
                raise ValueError("Invalid trusted fixture filename")
            data = (root / filename).read_bytes()
            if sha256(data).hexdigest() != case["sha256"]:
                raise ValueError("Fixture revision integrity check failed")
            seed = data.decode("utf-8")
        cases.append(Case(case["id"], seed))
    return Task(config["task_id"], config["task_revision"], config["grader_revision"],
                config["dataset_checksum"], tuple(config["expected_columns"]), config["comparison"],
                config["numeric_compatible"], config["reference_sql"], tuple(cases))


def validate_graded_bank(bank):
    task = load_task()
    record = next((item for item in bank["sql"] if item["id"] == TASK_ID), None)
    if not record or any([
        record.get("kind") != "graded_select", record.get("revision") != task.revision,
        record.get("grader_revision") != task.grader_revision,
        record.get("dataset_id") != "shop-v1", record.get("dataset_checksum") != task.dataset_checksum,
        record.get("expected_columns") != list(task.expected_columns),
        record.get("comparison") != task.comparison, record.get("tests_total") != len(task.cases),
        record.get("solution_sql") is not None,
    ]):
        raise ValueError("Graded practice-bank contract differs from its server bundle")
