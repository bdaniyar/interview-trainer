"""Build deterministic thematic interview collections from stable lesson slugs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

FULL_NUMBERS = [
    "1.2", "1.3", "3.4", "3.7", "5.6",
    "10.8", "10.10", "11.4", "11.9",
    "12.4", "12.7", "13.7",
    "14.8", "15.4", "16.4", "16.13",
    "8.4", "8.9",
    "18.3", "22.9",
    "19.5", "29.7",
    "32.1", "32.8",
    "28.3",
]

CRASH_NUMBERS = [
    "1.1", "1.2", "1.3", "1.7", "3.4", "3.7", "3.9", "3.10", "3.11",
    "4.1", "4.3", "4.7", "5.2", "5.6", "5.10",
    "10.8", "10.9", "10.10", "10.11", "10.16", "10.21",
    "11.2", "11.4", "11.9", "11.10", "12.3", "12.4", "12.7",
    "13.1", "13.5", "13.7", "14.8", "14.15", "15.4", "16.4", "16.8",
    "16.13", "18.3", "19.4", "20.5", "21.13", "22.9", "23.3", "32.1",
]

THEMATIC = [
    ("python-core", "Python Core Interview", "Object model, collections, functions and iteration.", ["stage-01","stage-02","stage-03","stage-04"]),
    ("python-advanced", "Python Advanced Interview", "Typing, CPython internals and concurrency boundaries.", ["stage-05","stage-06","stage-07"]),
    ("oop-data-model", "OOP and Data Model Interview", "Objects, protocols, composition and data model.", ["stage-05"]),
    ("async-python", "Async Python Interview", "Event loop, tasks, cancellation, threads and processes.", ["stage-08","stage-09"]),
    ("sql", "SQL Interview", "Queries, joins, aggregation, subqueries and windows.", ["stage-10"]),
    ("postgresql", "PostgreSQL Interview", "Constraints, indexes, transactions and concurrency.", ["stage-11"]),
    ("http-rest", "HTTP and REST Interview", "HTTP semantics, networking and API contracts.", ["stage-12"]),
    ("fastapi", "FastAPI Interview", "ASGI request lifecycle, Depends, validation and testing.", ["stage-14"]),
    ("pydantic", "Pydantic Interview", "Pydantic v2 validation and serialization.", ["stage-15"]),
    ("sqlalchemy-alembic", "SQLAlchemy and Alembic Interview", "Session, transactions, loading and migrations.", ["stage-16","stage-17"]),
    ("auth-security", "Authentication and Security Interview", "AuthN/AuthZ, tokens, OAuth and web security.", ["stage-13"]),
    ("redis-background", "Redis and Background Jobs Interview", "Cache, Pub/Sub, outbox, retries and workers.", ["stage-19","stage-20"]),
    ("docker", "Docker Interview", "Images, containers, Compose and debugging.", ["stage-21"]),
    ("git-linux", "Git and Linux Interview", "Working tree, history, shell and process diagnostics.", ["stage-22","stage-23"]),
    ("testing", "Testing Interview", "pytest, fixtures, mocks and isolation.", ["stage-18"]),
    ("backend-fundamentals", "Backend Fundamentals Interview", "Architecture, patterns and junior system design.", ["stage-27","stage-29"]),
    ("django-drf", "Django/DRF Interview", "Working Django and DRF fundamentals.", ["stage-26"]),
    ("resume-defense", "Resume Defense Interview", "StudyHub, Hotel Booking and Share Recipe claims.", ["stage-32"]),
]


def main() -> None:
    curriculum = json.loads((CONTENT / "curriculum.json").read_text(encoding="utf-8"))
    lessons = {lesson["number"]: lesson for stage in curriculum["stages"] for lesson in stage["lessons"]}

    def ids(numbers: list[str]) -> list[str]:
        return [f"{lessons[number]['implementation_slug']}:0" for number in numbers]

    sets = [
        {
            "slug": "full-junior-backend",
            "title": "Full Junior Python Backend Interview",
            "description": "25 вопросов по Python, SQL, HTTP, framework, debugging и защите проектов.",
            "question_ids": ids(FULL_NUMBERS),
            "estimated_minutes": 70,
        },
        {
            "slug": "interview-crash-course",
            "title": "Interview Crash Course",
            "description": "Быстрый повтор наиболее вероятных P0/P1 вопросов по всему backend path.",
            "question_ids": ids(CRASH_NUMBERS),
            "estimated_minutes": 95,
        },
    ]
    sets.extend(
        {
            "slug": slug,
            "title": title,
            "description": description,
            "stage_slugs": stage_slugs,
            "limit": 30,
            "estimated_minutes": 45,
        }
        for slug, title, description, stage_slugs in THEMATIC
    )
    payload = {"schema_version": 1, "default_set": "full-junior-backend", "sets": sets}
    (CONTENT / "interview_sets.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Built {len(sets)} interview sets; Full Interview contains {len(FULL_NUMBERS)} questions")


if __name__ == "__main__":
    main()
