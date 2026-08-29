"""Validate curriculum metadata, published lessons and executable solutions."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
REQUIRED_METADATA = {
    "id",
    "slug",
    "title",
    "module_slug",
    "module_title",
    "order",
    "priority",
    "interview_probability",
    "market_frequency",
    "market_evidence",
    "prerequisites",
    "modes",
    "tracks",
    "content_status",
    "last_verified",
}
REQUIRED_HEADINGS = {
    "## Learning objectives",
    "## Theory",
    "## Mental model",
    "## Code examples",
    "## Common mistakes",
    "## Interview questions",
    "## Expected answer rubric",
    "## Задача",
    "## Cheat sheet",
    "## Sources",
}
PLACEHOLDERS = {"Материал урока пока не добавлен", "Задача будет добавлена позже", "Учебный блок:"}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate(run_solutions: bool) -> None:
    errors: list[str] = []
    curriculum = json.loads((CONTENT / "curriculum.json").read_text(encoding="utf-8"))
    taxonomy = [lesson for stage in curriculum["stages"] for lesson in stage["lessons"]]
    if curriculum["lesson_count"] != len(taxonomy):
        fail(errors, "curriculum lesson_count does not match stages")
    for field in ("id", "slug", "number"):
        counts = Counter(str(item[field]) for item in taxonomy)
        for value, count in counts.items():
            if count > 1:
                fail(errors, f"duplicate taxonomy {field}: {value}")
    if not any(item["content_status"] == "planned" for item in taxonomy):
        fail(errors, "taxonomy must keep honest planned P2/P3 records")
    for item in taxonomy:
        if item["priority"] in {"P0", "P1"} and item["content_status"] != "complete":
            fail(errors, f"P0/P1 taxonomy record is not complete: {item['number']}")
        if not item.get("implementation_slug"):
            fail(errors, f"taxonomy record has no implementation_slug: {item['number']}")

    practice_path = CONTENT / "practice_banks.json"
    if not practice_path.exists():
        fail(errors, "practice_banks.json is missing")
    else:
        banks = json.loads(practice_path.read_text(encoding="utf-8"))
        minimums = {
            "python_prediction": 40,
            "sql": 48,
            "testing": 12,
            "operations": 15,
            "debugging": 59,
            "architecture": 20,
        }
        for name, minimum in minimums.items():
            if len(banks.get(name, [])) < minimum:
                fail(errors, f"practice bank {name}: expected {minimum}, got {len(banks.get(name, []))}")
        sql_categories = Counter(item["category"] for item in banks.get("sql", []))
        expected_sql = {
            "basic": 8,
            "aggregation": 8,
            "join": 10,
            "subquery": 6,
            "window": 6,
            "postgresql_reasoning": 10,
        }
        for category, minimum in expected_sql.items():
            if sql_categories[category] < minimum:
                fail(errors, f"SQL category {category}: expected {minimum}, got {sql_categories[category]}")

    sets_path = CONTENT / "interview_sets.json"
    if not sets_path.exists():
        fail(errors, "interview_sets.json is missing")
    else:
        interview_sets = json.loads(sets_path.read_text(encoding="utf-8"))["sets"]
        if len(interview_sets) < 20:
            fail(errors, f"expected 20 interview sets, got {len(interview_sets)}")
        full = next((item for item in interview_sets if item["slug"] == "full-junior-backend"), None)
        if not full or len(full.get("question_ids", [])) != 25:
            fail(errors, "Full Junior Interview must contain 25 curated questions")

    metadata_paths = sorted(CONTENT.glob("*/*/metadata.json"))
    published = 0
    tasks: list[Path] = []
    seen_slugs: set[str] = set()
    seen_ids: set[str] = set()
    seen_example_sources: dict[str, str] = {}
    for metadata_path in metadata_paths:
        directory = metadata_path.parent
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(errors, f"invalid JSON {metadata_path}: {exc}")
            continue
        missing = REQUIRED_METADATA - metadata.keys() if metadata.get("generated_by") else set()
        if missing:
            fail(errors, f"{metadata_path}: missing {sorted(missing)}")
        slug = metadata.get("slug")
        if slug in seen_slugs:
            fail(errors, f"duplicate published/legacy slug: {slug}")
        seen_slugs.add(slug)
        lesson_id = metadata.get("id")
        if lesson_id and metadata.get("content_status") == "complete":
            if lesson_id in seen_ids:
                fail(errors, f"duplicate published id: {lesson_id}")
            seen_ids.add(lesson_id)
        if metadata.get("content_status", "complete") != "complete":
            continue
        published += 1
        lesson_path = directory / "lesson.md"
        if not lesson_path.exists():
            fail(errors, f"published lesson has no Markdown: {directory}")
            continue
        markdown = lesson_path.read_text(encoding="utf-8")
        for marker in PLACEHOLDERS:
            if marker in markdown:
                fail(errors, f"placeholder in published lesson {slug}: {marker}")
        if metadata.get("generated_by"):
            for heading in REQUIRED_HEADINGS:
                if heading not in markdown:
                    fail(errors, f"{slug}: missing heading {heading}")
        example_section = re.search(
            r"^## Code examples\n+(.*?)(?=^## |\Z)",
            markdown,
            re.MULTILINE | re.DOTALL,
        )
        if not example_section:
            fail(errors, f"{slug}: Code examples section is empty")
        else:
            blocks = re.findall(r"```([^\n]*)\n(.*?)```", example_section.group(1), re.DOTALL)
            if not blocks:
                fail(errors, f"{slug}: Code examples has no fenced example")
            else:
                normalized_blocks = []
                for language, source in blocks:
                    if language.strip().lower() in {"python", "py"}:
                        try:
                            compile(source, f"<{slug}:Code examples>", "exec")
                        except SyntaxError as exc:
                            fail(errors, f"{slug}: invalid Python Code example: {exc.msg} at line {exc.lineno}")
                    normalized_source = re.sub(r"\s+", " ", source).strip()
                    normalized_blocks.append(f"{language.strip()}\n{normalized_source}")
                signature = "\n---\n".join(normalized_blocks)
                duplicate = seen_example_sources.get(signature)
                if duplicate:
                    fail(errors, f"duplicate Code examples in {duplicate} and {slug}")
                else:
                    seen_example_sources[signature] = slug
        interview_path = directory / "interview.json"
        if not interview_path.exists():
            fail(errors, f"published lesson has no interview rubric: {slug}")
        else:
            try:
                questions = json.loads(interview_path.read_text(encoding="utf-8"))
                if not questions or any(not item.get("question") or not item.get("answer") for item in questions):
                    fail(errors, f"invalid interview questions: {slug}")
            except json.JSONDecodeError as exc:
                fail(errors, f"invalid interview JSON {slug}: {exc}")
        if metadata.get("has_task"):
            tasks.append(directory)
            for expected in (directory / "starter" / "main.py", directory / "solution" / "main.py", directory / "tests" / "test_main.py"):
                if not expected.exists():
                    fail(errors, f"task {slug} missing {expected.relative_to(directory)}")

    if published < 350:
        fail(errors, f"expected at least 350 complete P0/P1 lessons, got {published}")
    if len(tasks) < 60:
        fail(errors, f"expected at least 60 executable tasks, got {len(tasks)}")

    if run_solutions and not errors:
        for directory in tasks:
            with tempfile.TemporaryDirectory(prefix="pythoria-content-") as temporary:
                workspace = Path(temporary)
                for source in (directory / "solution").rglob("*"):
                    if source.is_file():
                        destination = workspace / source.relative_to(directory / "solution")
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(source, destination)
                shutil.copytree(directory / "tests", workspace / "tests")
                env = {
                    **os.environ,
                    "PYTHONPATH": str(workspace),
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
                }
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests"],
                    cwd=workspace,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=20,
                    check=False,
                )
                if result.returncode:
                    fail(errors, f"solution failed for {directory.name}:\n{result.stdout}{result.stderr}")

    if errors:
        print("Content validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Content validation passed: {len(taxonomy)} taxonomy records, {published} published lessons, {len(tasks)} executable tasks")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-solutions", action="store_true")
    args = parser.parse_args()
    validate(args.run_solutions)


if __name__ == "__main__":
    main()
