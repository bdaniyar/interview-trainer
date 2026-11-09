"""Disclosure-aware checks distinguish self-check answers from task contracts."""
import hashlib
import json
from pathlib import Path

import pytest

from tools.content_quality import answer_leaks, audit, section, lesson_issues
from tools.lesson_markdown import disclosures, public_markdown, sections

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize('label', ['Ответ:', 'Ответ для самопроверки:', 'Правильный ответ:', '**Критерии ответа:**', 'Решение:'])
def test_open_answer_labels_are_rejected_but_hidden_answers_are_allowed(label):
    public = f'# Example\n## Практика\nЧто получится? {label} семь секунд.\n'
    assert any(i['code'] == 'answer-inline' for i in answer_leaks({}, public))
    hidden = f'# Example\n## Практика\nЧто получится?\n\n<details><summary>Показать ответ</summary>\n\n{label} семь секунд.\n\n</details>\n'
    assert answer_leaks({}, hidden) == []


def test_context_and_code_are_not_treated_as_answer_labels():
    source = '''# Example
## Теория
Ответ: в этой секции разбираем механизм.
## Примеры кода
Правильный ответ: учебный разбор разрешён.
## Практика
Что напечатает код?
```python
print("Ответ: строка программы")
```
## Задача
Реализуй f(x). Пример: f(2) == 4. Ожидаемый вывод: 4.
'''
    assert answer_leaks({'has_task': True}, source) == []
    assert answer_leaks({'has_task': False}, source) == []


def test_open_prediction_result_and_duplicate_answer_are_reported():
    prediction = '# Example\n## Предсказание результата кода\nЧто напечатает print(42)?\n```text\n42\n```\n'
    assert any(i['code'] == 'answer-prediction-output' for i in answer_leaks({}, prediction))
    duplicate = '# Example\n## Практика\nПочему так?\n\nОба ожидания перекрываются.\n\n<details><summary>Показать ответ</summary>\n\nОба ожидания перекрываются.\n\n</details>\n'
    assert any(i['code'] == 'answer-duplicate' for i in answer_leaks({}, duplicate))


@pytest.mark.parametrize('markup', [
    '<details open><summary>Показать ответ</summary>\nОтвет: 42\n</details>',
    '<details><summary>Показать ответ</summary>\nОтвет: 42',
    '<details>\nОтвет: 42\n</details>',
    'Вопрос? <details><summary>Показать ответ</summary>\n42\n</details>',
])
def test_malformed_or_initially_open_disclosures_fail_the_gate(markup):
    issues = answer_leaks({}, '# Example\n## Практика\n' + markup)
    assert any(i['code'] == 'answer-disclosure' for i in issues)


def test_headings_and_tags_inside_code_and_answers_do_not_split_the_lesson():
    source = '''# Example
## Практика
Что напечатает код?
<details>
<summary>Показать ответ</summary>
```python
print("42")
## Code comment
```
## Heading inside answer
Ответ: 42.
</details>
## Задача
Контракт.
'''
    assert [s.title for s in sections(source)] == ['Практика', 'Задача']
    assert 'Ответ: 42' not in public_markdown(source)
    assert len(disclosures(source)) == 1
    assert '```python' in disclosures(source)[0].body
    assert answer_leaks({}, source) == []
    assert not [i for i in lesson_issues({}, source, []) if i["code"].startswith("markdown-")]
    literal = '```html\n<details><summary>Example</summary>\ntext\n</details>\n```'
    assert disclosures(literal) == []
    assert public_markdown(literal) == literal


def test_no_known_answer_leaks_in_any_published_stage_8_onward_lesson():
    records = audit(ROOT / 'content')
    assert len(records) == 295
    leaks = [(r['slug'], i) for r in records for i in r['issues'] if i['code'].startswith('answer-')]
    assert leaks == []


def test_programming_task_contracts_are_unchanged():
    baseline = json.loads((Path(__file__).parent / 'fixtures/answer-leak-task-contracts.json').read_text())
    for filename, original in baseline.items():
        task = section((ROOT / filename).read_text(), 'Задача')
        assert hashlib.sha256(task.encode()).hexdigest() == original, filename


def test_default_validator_rejects_leakage_even_in_legacy_debt(tmp_path, monkeypatch, capsys):
    import shutil
    from tools import validate_content
    destination = tmp_path / 'content'
    shutil.copytree(ROOT / 'content', destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    legacy = destination / 'reliability/mocks/lesson.md'
    legacy.write_text(legacy.read_text().replace('## Практика\n', '## Практика\n\nПравильный ответ: опубликован слишком рано.\n', 1))
    monkeypatch.setattr(validate_content, 'CONTENT', destination)
    with pytest.raises(SystemExit) as error:
        validate_content.validate(False)
    assert error.value.code == 1
    assert 'answer-inline' in capsys.readouterr().err


def test_ready_solution_next_to_prediction_question_is_not_open_content():
    source = '# Example\n## Предсказание результата кода\nЧто изменит исправление?\n### Исправленный код\n```python\nprint(42)\n```\n'
    assert any(i['code'] == 'answer-inline' for i in answer_leaks({}, source))


def test_coding_contract_cannot_include_the_reference_implementation():
    solution = 'def double(value):\n    return value * 2\n'
    source = '# Example\n## Задача\nРеализуй double(value). Пример: double(2) == 4.\n```python\n' + solution + '```\n'
    assert any(i['code'] == 'answer-task-solution' for i in answer_leaks({'has_task': True}, source, solution))
    stub = source.replace('return value * 2', 'raise NotImplementedError')
    assert answer_leaks({'has_task': True}, stub, solution) == []
