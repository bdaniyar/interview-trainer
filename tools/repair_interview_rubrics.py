"""One-time, idempotent structural repair of legacy Stage 8+ interview rubrics.

Does not invent wrong assertions. Candidate misconceptions must be authored
separately in a substantive review. Question count/order/IDs/sets stay intact.
"""
from __future__ import annotations

import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / 'content'


def repair(content: Path = CONTENT) -> int:
    changed = 0
    for path in content.glob('*/*/metadata.json'):
        meta = json.loads(path.read_text(encoding='utf-8'))
        if meta.get('module_order', -1) < 8 or meta.get('content_status') != 'complete' or meta.get('content_source') == 'curated':
            continue
        target = path.parent / 'interview.json'
        original = target.read_text(encoding='utf-8')
        questions = json.loads(original)
        for question in questions:
            rubric = question.get('expected_answer', {})
            if rubric.get('review_status') == 'pending-substantive-review':
                continue
            descriptions = list(dict.fromkeys(rubric.get('common_wrong_answers', []) + rubric.get('red_flags', [])))
            rubric['coding_mistakes'] = [value for value in descriptions if not value.startswith('Ответ без')]
            rubric['assessment_notes'] = [value for value in descriptions if value.startswith('Ответ без')]
            rubric['common_wrong_answers'] = []
            rubric['red_flags'] = []
            rubric['review_status'] = 'pending-substantive-review'
        rendered = json.dumps(questions, ensure_ascii=False, indent=2) + '\n'
        if rendered != original:
            target.write_text(rendered, encoding='utf-8')
            changed += 1
    return changed


if __name__ == '__main__':
    print(f'Repaired {repair()} legacy rubric files; substantive answer review remains pending')
