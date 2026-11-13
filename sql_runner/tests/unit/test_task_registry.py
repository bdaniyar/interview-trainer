from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import shutil

import pytest

from sql_runner.app import grading_content as content
from sql_runner.app.datasets import load_dataset
from sql_runner.app.policy import PolicyError


@pytest.fixture
def bundles(tmp_path, monkeypatch):
    shutil.copytree(content.GRADING_ROOT, tmp_path / "grading")
    monkeypatch.setattr(content, "GRADING_ROOT", tmp_path / "grading")
    return content.GRADING_ROOT


def load(entry):
    return content.load_task(entry.task_id, entry.task_revision, entry.grader_revision)


def repin(entry, config, monkeypatch):
    wire = json.dumps(config).encode()
    (content.GRADING_ROOT / entry.bundle / "task.json").write_bytes(wire)
    entries = [replace(item, sha256=sha256(wire).hexdigest()) if item.task_id == entry.task_id else item
               for item in content.REGISTRY.values()]
    monkeypatch.setattr(content, "REGISTRY", content.build_registry(entries))
    return content.REGISTRY[entry.task_id]


def test_all_registered_tasks_and_references_validate_without_changing_projection():
    content.validate_registered_tasks()
    assert set(content.REGISTRY) == {"sql.guided.10.2.projection.v1", "sql.basic.01", "sql.basic.03"}
    for entry in content.REGISTRY.values():
        task = load(entry)
        assert task.id == entry.task_id and task.revision == 1
        assert task.dataset_id == "shop-v1" and task.dataset_checksum == load_dataset().checksum
        assert task.comparison == "unordered" and task.numeric_compatible
        assert len(task.cases) == (4 if entry.grader_revision == "projection-v1" else 5)
    projection = content.REGISTRY["sql.guided.10.2.projection.v1"]
    assert projection.sha256 == "6ae7700181c75b63ba3c5060733fe2b90c1482f9723f3a04ccc866e79ef4fef6"


def test_duplicate_task_ids_and_invalid_bundle_names_are_rejected():
    entry = next(iter(content.REGISTRY.values()))
    with pytest.raises(ValueError, match="Duplicate"):
        content.build_registry([entry, replace(entry, task_revision=2)])
    with pytest.raises(ValueError, match="Invalid"):
        content.build_registry([replace(entry, bundle="../outside")])


@pytest.mark.parametrize("task_id,revision,grader", [
    ("../../etc/passwd", 1, "projection-v1"),
    ("sql.basic.01", 2, "active-users-v1"), ("sql.basic.01", True, "active-users-v1"),
    ("sql.basic.01", 1, "null-country-v1"), ("sql.basic.03", 1, "active-users-v1"),
])
def test_cross_task_and_wrong_revisions_fail_closed(task_id, revision, grader):
    with pytest.raises(content.UnknownTask):
        content.load_task(task_id, revision, grader)


@pytest.mark.parametrize("damage", ["manifest", "seed", "missing"])
def test_bundle_integrity_and_missing_fixture_fail_closed(bundles, damage):
    entry = content.REGISTRY["sql.basic.01"]
    path = bundles / entry.bundle / ("task.json" if damage == "manifest" else "mixed-v1.sql")
    if damage == "missing":
        path.unlink()
    else:
        path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises((ValueError, FileNotFoundError)):
        load(entry)


def test_task_a_cannot_load_task_b_even_with_a_trusted_wrong_registration(monkeypatch):
    a, b = content.REGISTRY["sql.basic.01"], content.REGISTRY["sql.basic.03"]
    wrong = replace(a, bundle=b.bundle, sha256=b.sha256)
    monkeypatch.setattr(content, "REGISTRY", content.build_registry([wrong]))
    with pytest.raises(ValueError, match="identity"):
        load(wrong)


@pytest.mark.parametrize("damage", ["path", "duplicate", "comparison", "reference"])
def test_invalid_trusted_configuration_is_rejected_at_validation(bundles, monkeypatch, damage):
    entry = content.REGISTRY["sql.basic.01"]
    config = json.loads((bundles / entry.bundle / "task.json").read_bytes())
    if damage == "path":
        config["cases"][1]["seed_file"] = "../projection-v1/extra-users-v1.sql"
    elif damage == "duplicate":
        config["cases"][1]["id"] = config["cases"][0]["id"]
    elif damage == "comparison":
        config["comparison"] = "set"
    else:
        config["reference_sql"] = "DELETE FROM users"
    repin(entry, config, monkeypatch)
    with pytest.raises((ValueError, PolicyError)):
        content.validate_registered_tasks()


def test_bank_contracts_are_validated_for_all_tasks():
    bank = json.loads((Path(__file__).resolve().parents[3] / "content/practice_banks.json").read_text())
    content.validate_graded_bank(bank)
    bank["sql"].append(bank["sql"][0].copy())
    with pytest.raises(ValueError, match="Duplicate"):
        content.validate_graded_bank(bank)
