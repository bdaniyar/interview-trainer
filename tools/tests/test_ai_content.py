import json
from pathlib import Path
import shutil

from tools.ai_content import validate_ai

CONTENT = Path(__file__).resolve().parents[2] / "content"


def copy_manifest(tmp_path):
    file = tmp_path / "ai_curriculum.json"
    shutil.copyfile(CONTENT / file.name, file)
    manifest = json.loads(file.read_text())
    bundles = [
        (json.loads(path.read_text()), tmp_path / path.parent.relative_to(CONTENT))
        for path in CONTENT.glob("ai-stage-*/*/metadata.json")
    ]
    for _, directory in bundles:
        shutil.copytree(CONTENT / directory.relative_to(tmp_path), directory)
    return file, manifest, bundles


def test_manifest_dependencies_and_published_records(tmp_path):
    file, manifest, bundles = copy_manifest(tmp_path)
    assert validate_ai(tmp_path, bundles, []) == []
    lesson = next(item for item in manifest["stages"][0]["lessons"] if item["number"] == "AI1.2")
    lesson["prerequisites"] = [lesson["id"]]
    file.write_text(json.dumps(manifest))
    errors = validate_ai(tmp_path, bundles, [])
    assert any("cycle" in error for error in errors)
    assert any("not published earlier" in error for error in errors)


def test_planned_bundle_and_backend_collision(tmp_path):
    file, manifest, bundles = copy_manifest(tmp_path)
    first = next(item for item in manifest["stages"][0]["lessons"] if item["number"] == "AI1.2")
    first["status"] = "planned"
    file.write_text(json.dumps(manifest))
    errors = validate_ai(tmp_path, bundles, [first])
    assert "AI published manifest and bundles differ" in errors
    assert "AI slug collision" in errors


def test_r0_manifest_and_bundle_identity(tmp_path):
    path, current, bundles = copy_manifest(tmp_path)
    baseline = json.loads((Path(__file__).parent / "fixtures/ai-r0-manifest.json").read_text())
    r0 = {item["id"]: item for stage in baseline["stages"] for item in stage["lessons"]}
    current_records = {item["id"]: item for stage in current["stages"] for item in stage["lessons"]}
    assert {key: current_records[key] for key in r0} == r0
    path.write_text(json.dumps(baseline))
    assert validate_ai(tmp_path, [(meta, d) for meta, d in bundles if meta["id"] in r0], []) == []


def test_r1_completion_requires_all_stages(tmp_path):
    path, manifest, bundles = copy_manifest(tmp_path)
    manifest.update(release="R1", release_status="complete")
    manifest["stages"][3]["lessons"].clear()
    path.write_text(json.dumps(manifest))
    assert any("29 lessons" in error for error in validate_ai(tmp_path, bundles, []))


def test_r1_manifest_remains_valid_and_identical(tmp_path):
    path, current, bundles = copy_manifest(tmp_path)
    baseline = json.loads((Path(__file__).parent / "fixtures/ai-r1-manifest.json").read_text())
    assert current["stages"][:4] == baseline["stages"][:4]
    path.write_text(json.dumps(baseline))
    assert validate_ai(tmp_path, [(meta, d) for meta, d in bundles if meta["module_order"] < 105], []) == []


def test_r2_completion_requires_seven_graded_ai5_labs(tmp_path):
    path, manifest, bundles = copy_manifest(tmp_path)
    manifest.update(release="R2", release_status="complete")
    manifest["stages"][4]["lessons"].pop()
    manifest["stages"][4]["lessons"][0]["practice"] = "guided"
    path.write_text(json.dumps(manifest))
    errors = validate_ai(tmp_path, bundles, [])
    assert any("36 lessons" in error for error in errors)
    assert "AI5 lessons require graded labs" in errors

def test_r2_snapshot_remains_valid_and_identical(tmp_path):
    path, current, bundles = copy_manifest(tmp_path)
    baseline = json.loads((Path(__file__).parent / "fixtures/ai-r2-manifest.json").read_text())
    assert current["stages"][:5] == baseline["stages"][:5]
    path.write_text(json.dumps(baseline))
    assert validate_ai(tmp_path, [(m, d) for m, d in bundles if m["module_order"] < 106], []) == []


def test_r3_completion_requires_ten_offline_components(tmp_path):
    path, manifest, bundles = copy_manifest(tmp_path)
    manifest["release_status"] = "complete"
    manifest["stages"][5]["lessons"].pop()
    manifest["stages"][5]["lessons"][0]["practice"] = "guided"
    path.write_text(json.dumps(manifest))
    errors = validate_ai(tmp_path, bundles, [])
    assert any("46 lessons" in error for error in errors)
    assert "AI6 requires offline graded components" in errors
