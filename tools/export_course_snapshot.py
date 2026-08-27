"""Export a readable snapshot from the runtime content repository."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.app.content import content_repo


def main() -> None:
    modules = content_repo.modules()
    payload = {
        "title": "Python Backend Interview Trainer",
        "lessons_count": sum(len(module["lessons"]) for module in modules),
        "modules": modules,
        "note": "Generated snapshot; lesson folders and curriculum.json remain the authoring sources.",
    }
    (content_repo.root / "course.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Exported {payload['lessons_count']} published lessons")


if __name__ == "__main__":
    main()
