from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import HTTPException


CONTENT_ROOT = Path(os.getenv("CONTENT_ROOT", Path(__file__).resolve().parents[2] / "content"))


class ContentRepository:
    def __init__(self, root: Path = CONTENT_ROOT):
        self.root = root

    def _records(self) -> list[tuple[dict, Path]]:
        records: list[tuple[dict, Path]] = []
        for path in self.root.glob("*/*/metadata.json"):
            try:
                records.append((json.loads(path.read_text(encoding="utf-8")), path.parent))
            except (OSError, json.JSONDecodeError) as exc:
                raise RuntimeError(f"Invalid lesson metadata: {path}") from exc
        return sorted(records, key=lambda item: item[0]["order"])

    def modules(self) -> list[dict]:
        modules: dict[str, dict] = {}
        for meta, _ in self._records():
            module = modules.setdefault(
                meta["module_slug"],
                {
                    "slug": meta["module_slug"],
                    "title": meta["module_title"],
                    "order": len(modules) + 1,
                    "lessons": [],
                },
            )
            module["lessons"].append(meta)
        return list(modules.values())

    def lesson_dir(self, slug: str) -> tuple[dict, Path]:
        for metadata, directory in self._records():
            if metadata["slug"] == slug:
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

    def interview_questions(self) -> list[dict]:
        questions = []
        for metadata, directory in self._records():
            path = directory / "interview.json"
            if not path.exists():
                continue
            for index, question in enumerate(json.loads(path.read_text(encoding="utf-8"))):
                questions.append(
                    {
                        "id": f"{metadata['slug']}:{index}",
                        "lesson_slug": metadata["slug"],
                        "lesson_title": metadata["title"],
                        **question,
                    }
                )
        return questions


content_repo = ContentRepository()
