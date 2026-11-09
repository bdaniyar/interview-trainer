"""Deterministic editorial checks. These do not certify semantic correctness."""
from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

try:
    from .lesson_markdown import sections, disclosures, public_markdown, structural_lines, fenced_blocks
except ImportError:
    from lesson_markdown import sections, disclosures, public_markdown, structural_lines, fenced_blocks

GENERIC = (
    'восстановить mental model темы', 'найди нарушение `',
    'реализуй минимальную функцию или query', 'описывает отдельный контракт backend',
    'в backend эта тема важна в том месте', 'предскажи результат минимального примера для',
    'найди код, нарушающий `', 'измени один input в примере',
    'этот micro-scenario сформирован из outline', 'сначала фиксирую `',
)


# Verified occurrences of the old keyword router choosing another domain.
# Each entry is an exact stable ID plus a distinctive source fragment.
KNOWN_MISMATCHES = {
    'backend-interview.10.16.exists-vs-in': ('`list` — ordered mutable sequence', 'Python list substituted for SQL EXISTS/IN'),
    'backend-interview.12.6.post-vs-put': ('`SELECT` формирует result columns', 'SQL SELECT substituted for resource identifier choice'),
    'backend-interview.13.5.access-and-refresh-tokens': ('Session владеет identity map', 'ORM Session substituted for refresh session'),
    'backend-interview.13.10.sql-injection': ('`list` — ordered mutable sequence', 'Python list substituted for identifier allowlist'),
    'backend-interview.16.7.session-get': ('Identity отвечает на вопрос', 'Python identity substituted for ORM identity map lookup'),
    'backend-interview.18.4.fixture-scope': ('Session владеет identity map', 'ORM Session substituted for pytest session scope'),
    'backend-interview.19.2.data-structures': ('`list` — ordered mutable sequence', 'Python list implementation substituted for Redis list'),
    'backend-interview.22.9.reset-vs-revert': ('Index — отдельная структура доступа', 'Database index substituted for Git index'),
    'backend-interview.23.7.ports-and-network-diagnostics': ('`list` — ordered mutable sequence', 'Python list substituted for listening port'),
    'backend-interview.29.2.stateless-api-and-horizontal-scaling': ('Session владеет identity map', 'ORM Session substituted for sticky sessions'),
    'backend-interview.32.11.jwt-refresh-sessions': ('Session владеет identity map', 'ORM Session substituted for refresh session'),
    'backend-interview.32.22.redis-backed-password-reset': ('Session владеет identity map', 'ORM Session substituted for revoked auth sessions'),
}


def section(markdown: str, title: str) -> str:
    return next((s.body for s in sections(markdown) if s.title == title), '')


def prose(markdown: str) -> str:
    return re.sub(r'```.*?```', '', markdown, flags=re.S)


ANSWER_LABEL = re.compile(
    r"(?i)(?:ответ(?:\s+для\s+самопроверки)?|правильный\s+ответ|проверка\s+ответа|"
    r"критерии\s+ответа|слабый\s+ответ|ожидаем(?:ый|ые)\s+(?:вывод|результат|ответы)|"
    r"исправление|решение)\s*\*{0,2}\s*:"
)


def answer_leaks(metadata: dict, markdown: str, solution_source: str = "") -> list[dict]:
    """Check review-visible exercises, with explicit disclosures as boundaries.

    Theory/walkthroughs and coding input/output contracts are deliberately not
    classified as answers. This detects established authoring patterns; semantic
    hints without a marker still require editorial review.
    """
    issues = []
    for item in sections(markdown):
        if not re.search(r'практика|предсказание|^задача$|вопросы с собеседований', item.title, re.I):
            continue
        for answer in disclosures(item.body):
            if not answer.closed or not answer.summary or answer.initially_open:
                issues.append({'code': 'answer-disclosure', 'detail': f'{item.title}: answer must have a summary, closing tag and no open attribute'})
        if item.title == 'Задача' and metadata.get('has_task'):
            if solution_source:
                try:
                    definitions = {ast.dump(node) for node in ast.parse(solution_source).body
                                   if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
                    for language, source, _ in fenced_blocks(item.body):
                        if language not in {'python', 'py'}:
                            continue
                        for node in ast.parse(source).body:
                            if ast.dump(node) in definitions:
                                issues.append({'code': 'answer-task-solution', 'detail': f'{item.title}: implementation copied from solution/main.py'})
                except SyntaxError:
                    pass  # Syntax diagnostics are handled separately.
            continue  # Function name, I/O examples and edge cases stay public.
        for _, line, code, _ in structural_lines(item.body):
            if not code and '<details' in line.lower() and not re.match(r'^\s*<details(?:\s[^>]*)?>', line, re.I):
                issues.append({'code': 'answer-disclosure', 'detail': f'{item.title}: disclosure must start on its own line'})
        visible = public_markdown(item.body)
        for offset, line, code, _ in structural_lines(visible):
            label = ANSWER_LABEL.search(line)
            contract_output = item.title == 'Задача' and label and label[0].lower().startswith('ожидаем')
            heading_answer = re.match(r'^#{3,6}\s+(?:правильный ответ|ответ|решение|исправленный код|ожидаемый результат)\s*$', line.strip(), re.I)
            if not code and ((label and not contract_output) or heading_answer):
                line_number = markdown[:item.start].count('\n') + 2 + visible[:offset].count('\n')
                issues.append({'code': 'answer-inline', 'detail': f'{item.title}, line {line_number}: {line.strip()}'})
        # A supplied program is a question; a visible console/result block in a
        # prediction exercise gives away the result, even without "Ответ:".
        if re.search(r'предсказание', item.title, re.I):
            for match in re.finditer(r'^```(text|output|console)\s*\n(.*?)^```', visible, re.M | re.S):
                issues.append({'code': 'answer-prediction-output', 'detail': f'{item.title}: result block outside disclosure'})
        # Catch answers copied out of a disclosure while retaining the hidden
        # copy. Compare full prose lines, not matching words in the question.
        normalize = lambda text: re.sub(r'[^\w]+', ' ', text.lower()).strip()
        public_lines = [normalize(line) for _, line, code, _ in structural_lines(visible)
                        if not code and line.strip() and not line.lstrip().startswith('#')]
        for answer in disclosures(item.body):
            for _, line, code, _ in structural_lines(answer.body):
                normalized = normalize(line)
                if not code and len(normalized) >= 15 and normalized in public_lines:
                    issues.append({'code': 'answer-duplicate', 'detail': f'{item.title}: answer duplicated in open text: {line.strip()}'})
    return issues


def lesson_issues(metadata: dict, markdown: str, questions: list[dict], solution_source: str = "") -> list[dict]:
    issues = []
    def add(code, detail):
        issues.append({'code': code, 'detail': detail})
    issues.extend(answer_leaks(metadata, markdown, solution_source))
    lowered = markdown.lower()
    for marker in GENERIC:
        if marker in lowered:
            add('generic-copy', marker)
    if re.search(r'\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b|<insert[^>]*>|\{(?:topic|lesson_title|example)\}', prose(markdown), re.I):
        add('placeholder', 'Unresolved author placeholder in prose')
    fences = [line for line in markdown.splitlines() if re.match(r'^\s*```', line)]
    if len(fences) % 2:
        add('markdown-fence', 'Unclosed fenced block')
    headings = [item.title for item in sections(markdown)]
    for heading, count in Counter(headings).items():
        if count > 1:
            add('markdown-heading', f'Duplicate section {heading}')
    titles = [line for _, line, code, depth in structural_lines(markdown) if not code and not depth and re.match(r'^# [^#]', line)]
    if len(titles) != 1:
        add('markdown-title', 'Expected exactly one H1')
    for heading in headings:
        if not section(markdown, heading):
            add('markdown-empty', heading)
    practice = section(markdown, 'Практика')
    # A concrete prompt must refer to supplied data or a supplied piece of code,
    # not just an outline token or the word "practice".
    if not practice or ('```' not in practice and not re.search(r'\d|"[^"]+"|«[^»]+»|`[^`]+`', practice)):
        add('practice-unspecified', 'No supplied input, code or concrete scenario')
    if metadata.get('has_task'):
        task = section(markdown, 'Задача')
        if not re.search(r'`[^`]*(?:\(|[A-Za-z_]\w*)[^`]*`', task) or not re.search(r'пример|например', task, re.I):
            add('task-contract', 'Expected public name/signature and input/output example')
    # Narrow rules for previously observed cross-domain corruption. They are
    # keyed by stable lesson ID, not broad guesses about natural language.
    if metadata.get('id') == 'backend-interview.19.1.redis-mental-model':
        theory = section(markdown, 'Теория')
        if 'T | None' in theory or 'nullable' in theory:
            add('topic-mismatch', 'Python nullable explanation in Redis theory')
        if not all(word in theory for word in ('RDB', 'AOF')):
            add('topic-missing', 'Redis persistence requires RDB and AOF explanation')
    mismatch = KNOWN_MISMATCHES.get(metadata.get('id'))
    if mismatch and mismatch[0] in section(markdown, 'Теория'):
        add('topic-mismatch', mismatch[1])
    number = metadata.get('id', '').split('.')
    if len(number) > 2 and number[1:3] == ['8', '1']:
        if re.search(r'asyncio\.(?:gather|to_thread)\s*\(', section(markdown, 'Задача') + section(markdown, 'Примеры кода')):
            add('prerequisite-order', 'Advanced asyncio API in introductory execution model')
    for i, question in enumerate(questions):
        rubric = question.get('expected_answer', {})
        for key in ('must_mention', 'good_additions', 'common_wrong_answers', 'red_flags', 'follow_up_questions'):
            values = rubric.get(key, [])
            if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
                add('rubric-shape', f'{i}:{key} must be a list of nonempty strings')
        wrong = rubric.get('common_wrong_answers', []) + rubric.get('red_flags', [])
        correct = [question.get('short_answer', ''), question.get('junior_answer', ''), question.get('follow_up_answer', '')] + question.get('answer', [])
        coding = rubric.get('coding_mistakes', [])
        if any(item and any(item == value for value in correct + coding) for item in wrong):
            add('rubric-contradiction', f'{i}: expected answer or coding mistake marked as false assertion')
        if set(wrong) & set(rubric.get('must_mention', [])):
            add('rubric-contradiction', f'{i}: same concept required and forbidden')
        follow = question.get('follow_up_question')
        if follow and follow not in rubric.get('follow_up_questions', []):
            add('rubric-follow-up', f'{i}: follow-up fields disagree')
    return issues


def audit(content: Path) -> list[dict]:
    records = []
    bodies = defaultdict(list)
    practices = defaultdict(list)
    for path in sorted(content.glob('*/*/metadata.json')):
        meta = json.loads(path.read_text(encoding='utf-8'))
        if meta.get('module_order', -1) < 8 or meta.get('content_status') != 'complete':
            continue
        directory = path.parent
        markdown = (directory / 'lesson.md').read_text(encoding='utf-8')
        questions = json.loads((directory / 'interview.json').read_text(encoding='utf-8'))
        solution_path = directory / 'solution/main.py'
        solution_source = solution_path.read_text(encoding='utf-8') if solution_path.exists() else ''
        record = {'id': meta['id'], 'slug': meta['slug'], 'stage': meta['module_order'],
                  'reviewed': meta.get('content_source') == 'curated',
                  'issues': lesson_issues(meta, markdown, questions, solution_source)}
        records.append(record)
        # Titles, outline tokens and source footers cannot conceal exact repeats.
        body = re.sub(r'\s+', ' ', section(markdown, 'Теория')).strip()
        if body:
            bodies[body].append(record)
        prompts = section(markdown, 'Практика')
        prompts = re.sub(r'`[^`]+`', '`TOPIC`', prompts)
        prompts = re.sub(r'\s+', ' ', prompts).strip()
        if prompts:
            practices[prompts].append(record)
    for name, groups in [('duplicate-theory', bodies), ('duplicate-practice', practices)]:
        for group in groups.values():
            if len(group) > 1:
                for record in group:
                    record['issues'].append({'code': name, 'detail': ', '.join(r['slug'] for r in group if r is not record)})
    return records


def write_audit(content: Path, destination: Path) -> None:
    records = audit(content)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'audit.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    counts = Counter(r['stage'] for r in records)
    lines = ['# Аудит опубликованных материалов Stage 8+', '',
             'Автоматически проверены все перечисленные уроки. Это статический аудит известных дефектов, а не гарантия смысловой корректности. Содержательный аудит отмечен отдельно только у reviewed-комплектов.', '',
             '| Этап | Опубликовано | Проверено содержательно | С детерминированными замечаниями |',
             '| --- | ---: | ---: | ---: |']
    for stage, count in sorted(counts.items()):
        group = [r for r in records if r['stage'] == stage]
        lines.append(f"| {stage} | {count} | {sum(r['reviewed'] for r in group)} | {sum(bool(r['issues']) for r in group)} |")
    lines += ['', '## Приоритеты', '',
              '1. P0: архитектура сохранения bundles, порядок предпосылок Stage 8 и противоречивые interview rubric — исправлены; защита проверяется повторным запуском в копии репозитория.',
              '2. P0: 12 подтверждённых подмен тем точечно исправлены: SQL, refresh sessions, pytest scope, Redis lists, Git index и listening port. Правила topic-mismatch защищают от возврата известных ошибочных абзацев. Полный аудит этих уроков остаётся в очереди.',
              '3. P1: Stage 10–18 — следующий последовательный блок: SQL, PostgreSQL, HTTP, security, FastAPI, Pydantic, ORM, Alembic и testing. Требуется ручная переработка каждого legacy-урока, его задания и рубрики.',
              '4. P1: закончить Stage 19 после отдельно исправленного 19.1; затем Stage 20–32 по порядку. Planned-уроки не публиковались.',
              '', '## Покрытие по урокам', '',
              'В audit.json сохранены коды и детали каждого замечания. «Ожидает аудита» означает, что содержательная корректность не подтверждена, даже если статические проверки не нашли ошибки.', '']
    for r in records:
        status = 'содержательно переработан' if r['reviewed'] else 'ожидает содержательного аудита'
        codes = ', '.join(sorted({i['code'] for i in r['issues']})) or 'статических замечаний нет'
        lines.append(f"- `{r['id']}` ({r['slug']}): {status}; {codes}.")
    (destination / 'AUDIT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
