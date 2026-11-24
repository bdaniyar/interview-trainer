"""AI-specific checks used by validate_content alongside the existing curation gate."""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from graphlib import CycleError, TopologicalSorter
from pathlib import Path
from urllib.parse import urlsplit


def validate_ai(content: Path, bundles: list[tuple[dict, Path]], taxonomy: list[dict]) -> list[str]:
    path = content / "ai_curriculum.json"
    if not path.exists():
        return ["AI bundles require ai_curriculum.json"] if bundles else []
    manifest = json.loads(path.read_text(encoding="utf-8"))
    stages = manifest["stages"]
    records = [(stage, item) for stage in stages for item in stage["lessons"]]
    by_id = {item["id"]: item for _, item in records}
    errors: list[str] = []
    if (
        manifest["track"] != "ai-engineering" or len(stages) != 10
    ):
        errors.append("AI roadmap requires 10 stages and 72 planned or published lessons")
    if manifest["lesson_count"] != 72 or sum(s["lesson_count"] for s in stages) != 72:
        errors.append("AI roadmap total must be 72")
    release = manifest["release"]
    status = manifest.get("release_status")
    stage_counts = [len(stage["lessons"]) for stage in stages]
    if manifest["release_lesson_count"] != len(records):
        errors.append("AI release lesson count differs from the manifest")
    if status not in {"in_progress", "complete"}:
        errors.append("AI release status must be in_progress or complete")
    if status == "complete" and any(item["status"] != "published" for _, item in records):
        errors.append("Complete AI release must publish every scheduled lesson")
    if release == "R0":
        if len(records) != 15 or sum(item["practice"] == "graded" for _, item in records) != 8:
            errors.append("AI R0 requires 15 lessons including eight graded assignments")
    elif release == "R1":
        r1_sizes = [4, 10, 8, 7] + [0] * 6
        if any(count > limit for count, limit in zip(stage_counts, r1_sizes)):
            errors.append("AI R1 scope ends at AI4")
        if status == "complete" and stage_counts != r1_sizes:
            errors.append("Complete AI R1 requires all 29 lessons across AI1–AI4")
    elif release == "R2":
        ai5 = stages[4]["lessons"] if len(stages) > 4 else []
        if stage_counts[:4] != [4, 10, 8, 7] or len(ai5) > 7 or any(stage_counts[5:]):
            errors.append("AI R2 preserves AI1–AI4 and ends at AI5")
        if any(item["status"] != "published" for stage in stages[:4] for item in stage["lessons"]):
            errors.append("AI R2 must preserve all published R1 lessons")
        if any(item["practice"] != "graded" for item in ai5):
            errors.append("AI5 lessons require graded labs")
        if status == "complete" and len(ai5) != 7:
            errors.append("Complete AI R2 requires 36 lessons including all seven AI5 labs")
    else:
        errors.append(f"Unknown AI release {release}")
    for field in ("id", "slug", "number"):
        values = [item[field] for _, item in records]
        backend = {item[field] for item in taxonomy}
        if len(values) != len(set(values)) or set(values) & backend:
            errors.append(f"AI {field} collision")
    if len({stage["slug"] for stage in stages}) != len(stages):
        errors.append("duplicate AI stage slug")
    for stage in stages:
        if len(stage["lessons"]) > stage["lesson_count"]:
            errors.append(f"{stage['slug']}: more release records than roadmap lessons")
    graph = TopologicalSorter({item["id"]: item["prerequisites"] for _, item in records})
    try:
        tuple(graph.static_order())
    except CycleError:
        errors.append("AI prerequisites contain a cycle")

    published = set()
    for stage, item in records:
        lesson_id, slug = item["id"], item["slug"]
        match = re.fullmatch(r"ai-engineering\.(\d{2})\.(\d{2})\.[a-z0-9-]+", lesson_id)
        if not match or stage["slug"] != f"ai-stage-{match[1]}" or not re.fullmatch(rf"ai{match[1]}-[a-z0-9-]+", slug) or item["number"] != f"AI{int(match[1])}.{int(match[2])}":
            errors.append(f"{lesson_id}: invalid stage/id/slug/number")
        if item["status"] not in {"planned", "published"} or item["practice"] not in {"diagnostic", "concept", "guided", "graded"}:
            errors.append(f"{lesson_id}: invalid status or practice")
        for prerequisite in item["prerequisites"]:
            if prerequisite not in by_id:
                errors.append(f"{lesson_id}: unknown prerequisite {prerequisite}")
            elif item["status"] == "published" and prerequisite not in published:
                errors.append(f"{lesson_id}: prerequisite not published earlier: {prerequisite}")
        if item["status"] == "published":
            published.add(lesson_id)
    if Counter(meta["id"] for meta, _ in bundles) != Counter(published):
        errors.append("AI published manifest and bundles differ")
    roadmap = {item["id"]: (stage, item) for stage, item in records}
    for metadata, directory in bundles:
        lesson_id = metadata["id"]
        if lesson_id not in roadmap:
            continue
        stage, item = roadmap[lesson_id]
        if (
            any(metadata.get(key) != item[key] for key in ("id", "slug", "title", "prerequisites", "number", "practice"))
            or metadata.get("module_slug") != stage["slug"]
            or directory.relative_to(content).parts != (stage["slug"], item["slug"])
            or metadata.get("tracks") != ["ai-engineering"]
            or metadata.get("module_order") != 100 + int(stage["slug"][-2:])
            or metadata.get("has_task") != (item["practice"] == "graded")
            or metadata.get("task_id") != (f"{lesson_id}.practice" if metadata.get("has_task") else None)
            or metadata.get("content_source") != "curated" or metadata.get("editorial_status") != "published"
            or not metadata.get("has_solution") or metadata.get("content_status") != "complete"
        ):
            errors.append(f"{lesson_id}: bundle metadata differs from AI publication contract")
        if not all((directory / name).is_file() for name in ("starter/main.py", "solution/main.py", "tests/test_main.py")):
            errors.append(f"{lesson_id}: practice bundle is incomplete")
        sources = metadata.get("sources", [])
        if not sources:
            errors.append(f"{lesson_id}: primary sources are required")
        for source in sources:
            try:
                if not all(source[key] for key in ("source_id", "section", "applicability", "claim_kind")):
                    raise ValueError("empty source metadata")
                parsed = urlsplit(source["url"])
                if parsed.scheme != "https" or not parsed.hostname:
                    raise ValueError("invalid primary source URL")
                date.fromisoformat(source["verified_on"])
            except (KeyError, ValueError) as exc:
                errors.append(f"{lesson_id}: {exc}")
    return errors
