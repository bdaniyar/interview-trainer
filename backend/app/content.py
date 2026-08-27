from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import HTTPException


CONTENT_ROOT = Path(os.getenv("CONTENT_ROOT", Path(__file__).resolve().parents[2] / "content"))


class ContentRepository:
    def __init__(self, root: Path = CONTENT_ROOT):
        self.root = root

    def _records(self, *, published_only: bool = False) -> list[tuple[dict, Path]]:
        records: list[tuple[dict, Path]] = []
        for path in self.root.glob("*/*/metadata.json"):
            try:
                metadata = json.loads(path.read_text(encoding="utf-8"))
                if published_only and metadata.get("content_status", "complete") != "complete":
                    continue
                records.append((metadata, path.parent))
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Invalid lesson metadata: {path}") from exc
        return sorted(records, key=lambda item: item[0]["order"])

    def modules(self) -> list[dict]:
        modules: dict[str, dict] = {}
        for meta, _ in self._records(published_only=True):
            module = modules.setdefault(
                meta["module_slug"],
                {
                    "slug": meta["module_slug"],
                    "title": meta["module_title"],
                    "order": meta.get("module_order", len(modules) + 1),
                    "lessons": [],
                },
            )
            module["lessons"].append(meta)
        return sorted(modules.values(), key=lambda module: module["order"])

    def lesson_dir(self, slug: str) -> tuple[dict, Path]:
        for metadata, directory in self._records():
            if metadata["slug"] == slug:
                if metadata.get("content_status") == "planned" or not (directory / "lesson.md").exists():
                    raise HTTPException(status_code=404, detail="Урок запланирован, но материал ещё не опубликован")
                return metadata, directory
        raise HTTPException(status_code=404, detail="Урок не найден")

    def lesson(self, slug: str) -> dict:
        metadata, directory = self.lesson_dir(slug)
        markdown = (directory / "lesson.md").read_text(encoding="utf-8")
        interview_path = directory / "interview.json"
        interview = json.loads(interview_path.read_text(encoding="utf-8")) if interview_path.exists() else []
        return {**metadata, "markdown": markdown, "interview": interview}

    def starter_files(self, slug: str) -> dict[str, str]:
        _, directory = self.lesson_dir(slug)
        starter = directory / "starter"
        return {
            str(path.relative_to(starter)): path.read_text(encoding="utf-8")
            for path in starter.rglob("*")
            if path.is_file()
        }

    def hidden_tests(self, slug: str) -> dict[str, str]:
        _, directory = self.lesson_dir(slug)
        tests = directory / "tests"
        if not tests.exists():
            return {}
        return {
            str(Path("tests") / path.relative_to(tests)): path.read_text(encoding="utf-8")
            for path in tests.rglob("*.py")
        }

    def solution_files(self, slug: str) -> dict[str, str]:
        _, directory = self.lesson_dir(slug)
        solution = directory / "solution"
        if not solution.exists():
            raise HTTPException(status_code=404, detail="Решение пока не добавлено")
        return {
            str(path.relative_to(solution)): path.read_text(encoding="utf-8")
            for path in solution.rglob("*")
            if path.is_file()
        }

    def interview_sets(self) -> dict:
        path = self.root / "interview_sets.json"
        if not path.exists():
            return {"default_set": "", "sets": []}
        return json.loads(path.read_text(encoding="utf-8"))

    def interview_questions(self, set_slug: str | None = None) -> list[dict]:
        questions = []
        for metadata, directory in self._records(published_only=True):
            path = directory / "interview.json"
            if not path.exists():
                continue
            for index, question in enumerate(json.loads(path.read_text(encoding="utf-8"))):
                questions.append(
                    {
                        "id": f"{metadata['slug']}:{index}",
                        "lesson_slug": metadata["slug"],
                        "lesson_title": metadata["title"],
                        "stage_slug": metadata["module_slug"],
                        **question,
                    }
                )
        if set_slug:
            catalog = self.interview_sets()
            interview_set = next((item for item in catalog["sets"] if item["slug"] == set_slug), None)
            if interview_set is None:
                raise HTTPException(status_code=404, detail="Interview set не найден")
            explicit_ids = interview_set.get("question_ids")
            if explicit_ids:
                by_id = {question["id"]: question for question in questions}
                questions = [by_id[question_id] for question_id in explicit_ids if question_id in by_id]
            else:
                stages = set(interview_set.get("stage_slugs", []))
                priorities = set(interview_set.get("priorities", []))
                questions = [
                    question
                    for question in questions
                    if (not stages or question["stage_slug"] in stages)
                    and (not priorities or question.get("priority") in priorities)
                ]
                questions = questions[: interview_set.get("limit", len(questions))]
        return questions


content_repo = ContentRepository()
