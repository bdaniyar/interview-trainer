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
    Registration("sql.join.17", 1, "join-order-users-v1", "join-order-users-v1",
        "8316ccd5c366a5e1c14162e9840103a88360be5248f5a44407df2623f646d6cf"),
    Registration("sql.join.18", 1, "users-without-orders-v1", "users-without-orders-v1",
        "731d8847752ad3de61e3820403c6043a63183d3b6c64a48848a74aa2fd35203c"),
    Registration("sql.join.25", 1, "right-join-products-v1", "right-join-products-v1",
        "5230bd59e0b64827fa92aa6c283f97f808431d061f242c7d72cb279fcaaddb29"),
    Registration("sql.join.20", 1, "users-managers-v1", "users-managers-v1",
        "40fae9ee42c21d79a0eec3b148294dddf69e2fa02e13fc18490e2bebdaf2ab3e"),
    Registration('sql.subquery.27', 1, 'above-average-v1', 'above-average-v1',
        'ac02027baa30aff909dd56a05bd32e3697bc7551bd82f5e6f43e3ad0e732cbb3'),
    Registration('sql.subquery.31', 1, 'latest-per-user-v1', 'latest-per-user-v1',
        '1c999e14ae69477ffd5a91e41ec6f17655635b4849ff6400ea828c0f9d25eb31'),
    Registration('sql.subquery.28', 1, 'paid-buyers-v1', 'paid-buyers-v1',
        'cf3ca9b468f4e3d1fc41a0e25746ec3a42085cd6b751368ab580146c5f84d48d'),
    Registration('sql.subquery.30', 1, 'paid-revenue-v1', 'paid-revenue-v1',
        '9c746bffcd24bb1a00a095a8d12a5acb7d4627f5e797aa02e29a21bd0febaf74'),
    Registration('sql.subquery.32', 1, 'manager-chain-v1', 'manager-chain-v1',
        '2b24058adc5f74ee74d5939efcdb7da97dd9f6bfd4a32644e55c322d7afa6872'),
    Registration('sql.basic.06', 1, 'status-label-v1', 'status-label-v1',
        '4f921aca36a46ed0010de54bc7f147d23c1b1815210159aa15757a72182d9bfe'),
    Registration('sql.set.50', 1, 'active-countries-except-paid-v1', 'active-countries-except-paid-v1',
        '8f7c27505ac0f619845bd71b432256dd6002545043e943ad32d0262a5b30a912'),
    Registration('sql.window.37', 1, 'previous-total-v1', 'previous-total-v1',
        'c5881d79a1163909636c4d054376964fd8a5e6577638837949fc2d20a9d77505'),
    Registration('sql.window.33', 1, 'order-row-number-v1', 'order-row-number-v1',
        'a09e9d50d62e1f496e49efbe66d6a86fa7261cd35ae25b9e64148cb0c3235413'),
    Registration('sql.window.36', 1, 'running-revenue-v1', 'running-revenue-v1',
        '649ca508cb2847bfe1bcb02c8ab4ed76e308540c0382db416506fc49787ad8ff'),
    Registration('sql.window.38', 1, 'next-order-time-v1', 'next-order-time-v1',
        'aa23f03eedf94e102a9a445ca906c53c8e5079265a360397c28185578364fd59'),
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
    # Optional ordered groups: rows tied on these output columns form a bag.
    # Legacy bundles omit this and retain their exact sequence/bag behavior.
    ordered_key_columns: tuple[str, ...] = ()


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
    keys = config.get("ordered_key_columns", [])
    if (not isinstance(keys, list) or not all(isinstance(key, str) for key in keys)
            or len(set(keys)) != len(keys) or not set(keys).issubset(config["expected_columns"])
            or (keys and config["comparison"] != "ordered")):
        raise ValueError("Invalid ordered group contract")
    return Task(config["task_id"], config["task_revision"], config["grader_revision"],
                config["dataset_id"], config["dataset_checksum"], tuple(config["expected_columns"]), config["comparison"],
                config["numeric_compatible"], config["reference_sql"], tuple(cases), tuple(keys))


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
