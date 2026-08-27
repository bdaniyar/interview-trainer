"""Import the curriculum taxonomy from the product brief into stable JSON.

This is an authoring helper, not a runtime dependency. It deliberately parses
only the Stage/lesson section so prose outside the taxonomy never becomes
course content by accident.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "content" / "curriculum.json"
TRANSLIT = str.maketrans(
    {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value.lower()).translate(TRANSLIT)
    value = value.replace("__", " ").replace("+", " plus ").replace("/", " ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:72]


def clean_outline(block: str) -> list[str]:
    items: list[str] = []
    in_code = False
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.startswith("- "):
            continue
        item = line[2:].strip().rstrip(";")
        if item and item not in items:
            items.append(item)
    return items


def priority_fields(block: str) -> tuple[str, str, str]:
    match = re.search(r"`(?P<label>P[0-3][^`]*)`", block)
    label = match.group("label") if match else "P2 | medium"
    priority_match = re.search(r"P[0-3]", label)
    priority = priority_match.group(0) if priority_match else "P2"
    probability = "medium"
    normalized_label = label.lower().replace("_", " ").replace("/", " ")
    for value in ("very_high", "high", "medium", "low"):
        if value.replace("_", " ") in normalized_label:
            probability = value
            break
    return priority, probability, label


def market_frequency(priority: str, stage_number: int) -> str:
    if stage_number in {1, 2, 3, 4, 10, 11, 12, 14, 15, 16, 18, 22, 32} and priority == "P0":
        return "very_common"
    return {"P0": "common", "P1": "common", "P2": "occasional", "P3": "rare_for_junior"}[priority]


def parse_taxonomy(text: str) -> dict:
    start = text.index("# 9. Полная taxonomy курса")
    end = text.index("## 10. Обязательная структура каждого lesson")
    section = text[start:end]
    stage_matches = list(re.finditer(r"^## Stage (?P<number>\d+) — (?P<title>.+)$", section, re.MULTILINE))
    stages: list[dict] = []
    total = 0
    for stage_index, stage_match in enumerate(stage_matches):
        stage_end = stage_matches[stage_index + 1].start() if stage_index + 1 < len(stage_matches) else len(section)
        stage_block = section[stage_match.end():stage_end]
        lesson_matches = list(re.finditer(r"^### (?P<number>\d+\.\d+) (?P<title>.+)$", stage_block, re.MULTILINE))
        lessons: list[dict] = []
        stage_number = int(stage_match.group("number"))
        for lesson_index, lesson_match in enumerate(lesson_matches):
            lesson_end = lesson_matches[lesson_index + 1].start() if lesson_index + 1 < len(lesson_matches) else len(stage_block)
            lesson_block = stage_block[lesson_match.end():lesson_end]
            priority, probability, original_priority = priority_fields(lesson_block)
            number = lesson_match.group("number")
            title = lesson_match.group("title").replace("\\_", "_").strip()
            slug = f"s{stage_number:02d}-{slugify(title)}"
            lessons.append(
                {
                    "id": f"backend-interview.{number}.{slugify(title)}",
                    "slug": slug,
                    "number": number,
                    "title": title,
                    "priority": priority,
                    "priority_note": original_priority,
                    "interview_probability": probability,
                    "market_frequency": market_frequency(priority, stage_number),
                    "market_evidence": "Приоритет основан на market sample n=18 и фундаментальной ценности для Junior Python Backend.",
                    "priority_basis": ["market", "technical_interview", "backend_work"],
                    "prerequisites": [],
                    "modes": ["learn", "interview"] + (["practice"] if priority in {"P0", "P1"} else []),
                    "tracks": ["full"] + (["interview_crash_course"] if priority in {"P0", "P1"} else []),
                    "content_status": "complete" if priority in {"P0", "P1"} else "planned",
                    "estimated_minutes": 12 if priority == "P0" else 10,
                    "difficulty": "junior" if priority in {"P0", "P1"} else "junior_plus",
                    "outline": clean_outline(lesson_block),
                    "last_verified": "2026-08-27",
                }
            )
            total += 1
        stages.append(
            {
                "slug": f"stage-{stage_number:02d}",
                "number": stage_number,
                "title": stage_match.group("title").strip(),
                "lessons": lessons,
            }
        )
    return {
        "schema_version": 1,
        "title": "Python Backend Interview Trainer",
        "audience": "Intern / Trainee / Junior / Junior+ Python Backend Developer",
        "market_sample": {"date": "2026-08-25", "region": "Kazakhstan + available remote", "n": 18},
        "lesson_count": total,
        "stages": stages,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", type=Path, help="Path to the curriculum brief")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = parse_taxonomy(args.brief.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {payload['lesson_count']} lessons into {args.output}")


if __name__ == "__main__":
    main()
