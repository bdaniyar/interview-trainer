"""Immutable grader bundles, loaded only in the controller (not the sandbox)."""
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re
from types import MappingProxyType

from .datasets import load_dataset

GRADING_ROOT = Path(__file__).resolve().parents[1] / "grading"


class UnknownTask(ValueError):
    pass


@dataclass(frozen=True)
class Registration:
    task_id: str
    task_revision: int
    grader_revision: str
    bundle: str
    sha256: str


def build_registry(entries):
    registry = {}
    for entry in entries:
        if entry.task_id in registry:
            raise ValueError("Duplicate SQL task registration")
        if (type(entry.task_revision) is not int or entry.task_revision < 1 or not re.fullmatch(r"[a-z][a-z0-9-]*", entry.bundle)
                or not re.fullmatch(r"[a-f0-9]{64}", entry.sha256)):
            raise ValueError("Invalid grader registration")
        registry[entry.task_id] = entry
    return MappingProxyType(registry)


REGISTRY = build_registry((
    Registration("sql.guided.10.2.projection.v1", 1, "projection-v1", "projection-v1",
        "6ae7700181c75b63ba3c5060733fe2b90c1482f9723f3a04ccc866e79ef4fef6"),
    Registration("sql.basic.01", 1, "active-users-v1", "active-users-v1",
        "2025fe522b74fd9b2644a03f657dbfffe059e26ba319d6771228e5faa3bcd2b4"),
    Registration("sql.basic.03", 1, "null-country-v1", "null-country-v1",
        "566c85cefbc748bb0d85583dd482cbfddbcbff9d6396d2ee104eb4790e73aeda"),
    Registration("sql.basic.04", 1, "latest-orders-v1", "latest-orders-v1",
        "f0dfddb0e8b4c25429561b4e78370436656b07b52bf1806fa39190cd733213ba"),
    Registration("sql.basic.05", 1, "distinct-countries-v1", "distinct-countries-v1",
        "c86a3312b1886cfbd69fd937504ceb41410c5f73108073d346c3ad3897c35989"),
    Registration("sql.aggregation.09", 1, "count-orders-v1", "count-orders-v1",
        "f2d259c30d38072ed0c169e7761f99254f39851cd231ad249da4cb6841bc39c7"),
    Registration("sql.aggregation.10", 1, "orders-by-status-v1", "orders-by-status-v1",
        "3b51098df8ef8df18f504f650ad77b5ea149229a2f31f4e86aa0bd4b4e8004c5"),
    Registration("sql.aggregation.13", 1, "users-with-two-orders-v1", "users-with-two-orders-v1",
        "d5a27f000cf187672630f6e430aa18a632fa46f9e4c32e2f3b1d6ae4791d2f44"),
))


@dataclass(frozen=True)
class Case:
    id: str
    seed: str | None  # None means the immutable public baseline already loaded.


@dataclass(frozen=True)
class Task:
    id: str
    revision: int
    grader_revision: str
    dataset_id: str
    dataset_checksum: str
    expected_columns: tuple[str, ...]
    comparison: str
    numeric_compatible: bool
    reference_sql: str
    cases: tuple[Case, ...]


def load_task(task_id, task_revision, grader_revision):
    # No task ID, revision, filename or path is interpolated from a request.
    entry = REGISTRY.get(task_id)
    if entry is None or type(task_revision) is not int or (task_revision, grader_revision) != (entry.task_revision, entry.grader_revision):
        raise UnknownTask("Unsupported grading configuration")
    root = GRADING_ROOT / entry.bundle
    wire = (root / "task.json").read_bytes()
    if sha256(wire).hexdigest() != entry.sha256:
        raise ValueError("Grader revision integrity check failed")
    config = json.loads(wire)
    if (config["task_id"], config["task_revision"], config["grader_revision"]) != (
            entry.task_id, entry.task_revision, entry.grader_revision):
        raise ValueError("Grader identity mismatch")
    if config["dataset_checksum"] != load_dataset(config["dataset_id"]).checksum:
        raise ValueError("Grader baseline revision mismatch")
    if (config["comparison"] not in {"ordered", "unordered"} or type(config["numeric_compatible"]) is not bool
            or not config["expected_columns"] or not all(isinstance(c, str) and c for c in config["expected_columns"])
            or not isinstance(config["reference_sql"], str) or not config["reference_sql"].strip()
            or not 1 <= len(config["cases"]) <= 16):
        raise ValueError("Invalid grader contract")
    cases = []
    for case in config["cases"]:
        if type(case["public"]) is not bool or not isinstance(case["id"], str) or not case["id"]:
            raise ValueError("Invalid fixture revision")
        seed = None
        if not case["public"]:
            filename = case["seed_file"]
            if (Path(filename).name != filename or not filename.endswith(".sql")
                    or not (root / filename).resolve().is_relative_to(root.resolve())):
                raise ValueError("Invalid trusted fixture filename")
            data = (root / filename).read_bytes()
            if len(data) > 65536 or sha256(data).hexdigest() != case["sha256"]:
                raise ValueError("Fixture revision integrity check failed")
            seed = data.decode("utf-8")
        cases.append(Case(case["id"], seed))
    if len({case.id for case in cases}) != len(cases):
        raise ValueError("Duplicate fixture revision")
    return Task(config["task_id"], config["task_revision"], config["grader_revision"],
                config["dataset_id"], config["dataset_checksum"], tuple(config["expected_columns"]), config["comparison"],
                config["numeric_compatible"], config["reference_sql"], tuple(cases))


def validate_graded_bank(bank):
    records = {item["id"]: item for item in bank["sql"]}
    if len(records) != len(bank["sql"]):
        raise ValueError("Duplicate practice-bank task ID")
    for entry in REGISTRY.values():
        task = load_task(entry.task_id, entry.task_revision, entry.grader_revision)
        record = records.get(task.id)
        if record is None or (record.get("expected_columns"), record.get("comparison")) != (
                list(task.expected_columns), task.comparison):
            raise ValueError("Graded practice-bank contract differs from its server bundle")
        for key, value in dict(revision=task.revision, grader_revision=task.grader_revision,
                dataset_id=task.dataset_id, dataset_checksum=task.dataset_checksum, tests_total=len(task.cases)).items():
            if key in record and record[key] != value:
                raise ValueError("Practice-bank revision differs from server bundle")
        if record.get("solution_sql") is not None and record["solution_sql"] != task.reference_sql:
            raise ValueError("Legacy reference contract changed")


def validate_registered_tasks():
    # Startup/explicit tests validate references too; the content loader above
    # stays stdlib-only so content validation does not require pglast/Docker.
    from .policy import validate
    for entry in REGISTRY.values():
        validate(load_task(entry.task_id, entry.task_revision, entry.grader_revision).reference_sql)
