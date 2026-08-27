"""Synchronize dependency and market evidence metadata without changing slugs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

FIRST_PREREQUISITE = {
    0: None, 1: "0.2", 2: "1.3", 3: "1.1", 4: "3.2", 5: "1.1",
    6: "3.6", 7: "1.1", 8: "3.1", 9: "8.1", 10: None, 11: "10.1",
    12: None, 13: "12.1", 14: "12.1", 15: "6.1", 16: "10.1",
    17: "16.2", 18: None, 19: "11.9", 20: "12.3", 21: None, 22: None,
    23: None, 24: "22.2", 25: "12.1", 26: "10.1", 27: "5.6",
    28: "2.5", 29: "12.1", 30: "21.1", 31: "0.2", 32: "0.3",
}

EVIDENCE = {
    0: "Interview foundation; приоритет подтверждён целью Junior screening.",
    1: "Python указан в 18/18 primary вакансий; object model — базовый screening foundation.",
    2: "Python указан в 18/18; collections — ежедневная data transformation работа backend.",
    3: "Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.",
    4: "Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.",
    5: "Python указан в 18/18; OOP/data model важны для чтения framework и domain code.",
    6: "Python указан в 18/18; typing повышает надёжность API contracts.",
    7: "Python указан в 18/18; CPython details приоритетны только там, где объясняют реальные bugs.",
    8: "Async явно встречался в 5/18 и является P0/P1 для FastAPI async-проектов кандидата.",
    9: "Concurrency fundamentals поддерживают выбор threads/processes/async без мифов о GIL.",
    10: "SQL/relational DB явно встречались в 15/18 — один из главных P0-разделов.",
    11: "PostgreSQL явно встречался в 13/18; indexes/transactions/concurrency критичны для backend.",
    12: "HTTP/REST/API явно встречались в 13/18 — P0 внешний контракт backend.",
    13: "Auth/security защищают заявленные JWT/OAuth2/PKCE и API permissions.",
    14: "FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.",
    15: "Pydantic v2 — validation boundary основной FastAPI trajectory.",
    16: "ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.",
    17: "Alembic защищает заявленный migration опыт и безопасные schema changes.",
    18: "Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.",
    19: "Redis явно встречался в 6/18 и входит в фактические проекты кандидата.",
    20: "Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.",
    21: "Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.",
    22: "Git явно встречался в 7/18 и, вероятно, недоучтён как assumed foundation.",
    23: "Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.",
    24: "CI/CD явно встречался в 11/18; junior должен понимать quality gates и читать logs.",
    25: "Observability явно встречалась в 7/18; особенно важна для защиты Prometheus/Grafana/Sentry claims.",
    26: "Django/DRF встречался в 7/18 и расширяет Казахстанскую junior-воронку.",
    27: "Architecture basics нужны для объяснения design choices без senior-level overengineering.",
    28: "Базовые structures/complexity проверяют на coding screen; competitive programming не приоритет.",
    29: "Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.",
    30: "Cloud встречался в 6/18, Kubernetes — 1/18; инфраструктура остаётся P2/P3 после core.",
    31: "Screening communication влияет на прохождение remote и local interviews.",
    32: "Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.",
}


def probability(note: str) -> str:
    normalized = note.lower().replace("_", " ").replace("/", " ")
    for value in ("very_high", "high", "medium", "low"):
        if value.replace("_", " ") in normalized:
            return value
    return "medium"


def main() -> None:
    curriculum_path = CONTENT / "curriculum.json"
    curriculum = json.loads(curriculum_path.read_text(encoding="utf-8"))
    by_number = {lesson["number"]: lesson for stage in curriculum["stages"] for lesson in stage["lessons"]}
    metadata_by_id = {}
    for path in CONTENT.glob("*/*/metadata.json"):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        if metadata.get("id"):
            metadata_by_id[metadata["id"]] = (path, metadata)

    for stage in curriculum["stages"]:
        previous_id = None
        for index, lesson in enumerate(stage["lessons"]):
            lesson["interview_probability"] = probability(lesson["priority_note"])
            lesson["market_evidence"] = EVIDENCE[stage["number"]]
            if index == 0:
                prerequisite_number = FIRST_PREREQUISITE[stage["number"]]
                lesson["prerequisites"] = [by_number[prerequisite_number]["id"]] if prerequisite_number else []
            else:
                lesson["prerequisites"] = [previous_id] if previous_id else []
            previous_id = lesson["id"]
            record = metadata_by_id.get(lesson["id"])
            if record:
                path, metadata = record
                metadata["interview_probability"] = lesson["interview_probability"]
                metadata["market_evidence"] = lesson["market_evidence"]
                metadata["prerequisites"] = lesson["prerequisites"]
                path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    curriculum_path.write_text(json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Synchronized probability, market evidence and prerequisites")


if __name__ == "__main__":
    main()
