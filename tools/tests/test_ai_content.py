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
