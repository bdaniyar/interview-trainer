"""Regression checks for content safety, editorial diagnostics and persistence."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from content_quality import lesson_issues
from curated_content import reviewed_bundle
from learning_materials import compact_dossier, fallback_dossier, dossier_for
from populate_curriculum import explain_point


def digest_tree(directory):
    return {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def test_generators_preserve_all_published_bundles_twice(tmp_path):
    """Real entry points must preserve Markdown, rubric, metadata and code together."""
    shutil.copytree(ROOT / 'content', tmp_path / 'content', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    shutil.copytree(ROOT / 'tools', tmp_path / 'tools', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    before = digest_tree(tmp_path / 'content')
    for _ in range(2):
        for script in ('populate_curriculum.py', 'add_coding_tasks.py', 'add_backend_tasks.py', 'personalize_examples.py', 'repair_interview_rubrics.py', 'add_practice_banks.py', 'seed_content.py', 'enrich_curriculum.py', 'build_interview_sets.py'):
            result = subprocess.run([sys.executable, str(tmp_path / 'tools' / script)], cwd=tmp_path,
                                    capture_output=True, text=True, timeout=30)
            assert result.returncode == 0, result.stdout + result.stderr
        assert digest_tree(tmp_path / 'content') == before


def test_topic_selection_cannot_match_optional_to_redis():
    with pytest.raises(ValueError, match='no reviewed explanation'):
        explain_point('optional persistence modes', ('', '', '', ''), 19)
    with pytest.raises(ValueError):
        explain_point('some unrelated identity map usage', ('', '', '', ''), 16)


def test_no_generic_generation_for_new_stage_8_lessons():
    lesson = {'id': 'new.lesson', 'number': '8.99', 'title': 'Unknown', 'outline': ['optional']}
    with pytest.raises(ValueError):
        compact_dossier(lesson, ('what', 'how', 'limit', None, 'error'))
    with pytest.raises(ValueError):
        fallback_dossier(lesson, 8, lambda _: 'wrong')
    with pytest.raises(ValueError):
        dossier_for(lesson, 8, lambda _: 'wrong')
    with pytest.raises(ValueError, match='reviewed content required'):
        reviewed_bundle(ROOT / 'content', lesson)


def test_validator_detects_known_defects_and_rubric_contradiction():
    meta = {'id': 'backend-interview.19.1.redis-mental-model', 'has_task': True}
    markdown = '''# Redis
## Теория
optional persistence: T | None nullable
## Практика
Найди нарушение `fast`.
## Задача
TODO
## Задача
```python
'''
    questions = [{'short_answer': 'Redis stores data in memory', 'answer': [],
                  'expected_answer': {'must_mention': ['RDB'], 'common_wrong_answers': ['RDB'],
                                      'red_flags': ['Redis stores data in memory']}}]
    codes = {i['code'] for i in lesson_issues(meta, markdown, questions)}
    assert {'generic-copy', 'placeholder', 'topic-mismatch', 'topic-missing',
            'markdown-fence', 'markdown-heading', 'task-contract', 'rubric-contradiction'} <= codes


def test_preserved_keys_and_early_stages():
    baseline = json.loads((Path(__file__).parent / 'fixtures/persistence-baseline.json').read_text())
    for filename, original in baseline['metadata'].items():
        current = json.loads((ROOT / filename).read_text())
        assert [current.get(k) for k in baseline['metadata_keys']] == original, filename
    for filename, original in baseline['early_stage_sha256'].items():
        assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == original, filename
    for filename, original in baseline['interview_positions'].items():
        current = json.loads((ROOT / filename).read_text())
        assert [[q.get(k) for k in baseline['interview_keys']] for q in current] == original, filename


def test_saved_stage_8_submissions_remain_accepted(tmp_path):
    curriculum = json.loads((ROOT / 'content/curriculum.json').read_text())
    lessons = {l['number']: l for s in curriculum['stages'] for l in s['lessons']}
    for number in ('8.1', '8.3'):
        bundle = reviewed_bundle(ROOT / 'content', lessons[number])
        workspace = tmp_path / number
        workspace.mkdir()
        (workspace / 'main.py').write_bytes((Path(__file__).parent / f'fixtures/saved-{number}.py').read_bytes())
        shutil.copytree(bundle / 'tests', workspace / 'tests', ignore=shutil.ignore_patterns('__pycache__'))
        result = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', 'tests'], cwd=workspace,
                                env={**os.environ, 'PYTHONPATH': str(workspace), 'PYTEST_DISABLE_PLUGIN_AUTOLOAD': '1'},
                                capture_output=True, text=True, timeout=20)
        assert result.returncode == 0, result.stdout + result.stderr


def test_curated_python_examples_execute_as_explained(tmp_path):
    import re
    outputs = {
        '8.1': '5\n3\n',
        '8.2': 'created\ninside\nПривет, Алия\n',
        '8.3': 'start a\nend a\nstart b\nend b\nAB\n',
        '8.4': 'before\ncallback\nafter\n',
        '8.5': 'scheduled\nquote started\n120\n',
        '8.6': "done fast\ndone slow\n['SLOW', 'FAST']\n",
        '8.7': "deadline\n['closed']\n",
        '8.8': "cancelled\n['released']\n",
        '8.9': "['begin', 'end', 'tick']\n['begin', 'tick', 'end']\n",
        '8.10': "['open', 'connection', 'close', 'handled']\n",
        '8.11': "page-1\n['closed']\n",
        '8.12': "['A', 'B'] 1\n",
        '9.1': '300\n', '9.2': '[4, 9, 16]\n', '9.3': '[450, 120]\n',
    }
    curriculum = json.loads((ROOT / 'content/curriculum.json').read_text())
    lessons = {l['number']: l for s in curriculum['stages'] for l in s['lessons']}
    for number, expected in outputs.items():
        bundle = reviewed_bundle(ROOT / 'content', lessons[number])
        markdown = (bundle / 'lesson.md').read_text()
        example = re.findall(r'```python\n(.*?)```', markdown, re.S)[0]
        script = tmp_path / ('example_' + number.replace('.', '_') + '.py')
        script.write_text(example)
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, (number, result.stderr)
        assert result.stdout == expected, (number, result.stdout)


def test_validator_guards_all_repaired_topic_mismatches():
    from content_quality import KNOWN_MISMATCHES, audit
    for lesson_id, (incorrect_fragment, _) in KNOWN_MISMATCHES.items():
        markdown = f'# Lesson\n## Теория\n{incorrect_fragment}\n## Практика\nПроверь пример `x=1`.\n'
        codes = {i['code'] for i in lesson_issues({'id': lesson_id}, markdown, [])}
        assert 'topic-mismatch' in codes, lesson_id
    actual = audit(ROOT / 'content')
    assert not [(r['id'], i) for r in actual for i in r['issues'] if i['code'] == 'topic-mismatch']


def test_duplicate_theory_and_practice_are_reported(tmp_path):
    from content_quality import audit
    for i in (1, 2):
        bundle = tmp_path / 'stage-10' / f'lesson-{i}'
        bundle.mkdir(parents=True)
        (bundle / 'metadata.json').write_text(json.dumps({'id': f'lesson.{i}', 'slug': f'lesson-{i}', 'module_order': 10, 'content_status': 'complete'}))
        (bundle / 'lesson.md').write_text(f'# Lesson {i}\n## Теория\nОдинаковая теория.\n## Практика\nПроверь `value=1`.\n')
        (bundle / 'interview.json').write_text('[]')
    records = audit(tmp_path)
    assert len(records) == 2
    for record in records:
        assert {'duplicate-theory', 'duplicate-practice'} <= {i['code'] for i in record['issues']}
