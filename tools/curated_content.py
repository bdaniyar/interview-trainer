"""Published lesson directories are the source of truth, never generator output.

A reviewed bundle includes Markdown, rubric, metadata and the entire task. IDs,
slugs and interview array positions are persistence keys. Curation is recorded
separately from publication: a complete legacy lesson is not a reviewed lesson.
"""
from __future__ import annotations

import json
from pathlib import Path


def stage_number(record: dict) -> int:
    if 'number' in record:
        return int(str(record['number']).split('.')[0])
    return int(record.get('module_order', -1))


def preserve_bundle(directory: Path, *, rewrite_legacy: bool = False) -> bool:
    path = directory / 'metadata.json'
    if not path.exists():
        return False
    metadata = json.loads(path.read_text(encoding='utf-8'))
    if metadata.get('content_source') == 'curated' or stage_number(metadata) >= 8:
        return True
    return not rewrite_legacy


def reviewed_bundle(content: Path, lesson: dict) -> Path:
    # Resolve by stable ID, including legacy implementation slugs.
    for path in content.glob('*/*/metadata.json'):
        meta = json.loads(path.read_text(encoding='utf-8'))
        if meta.get('id') == lesson['id'] and meta.get('content_source') == 'curated':
            return path.parent
    raise ValueError(f"{lesson['id']}: reviewed content required; automatic theory generation is disabled")
