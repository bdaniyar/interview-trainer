# Python Backend Interview Trainer

Pythoria — локальная платформа подготовки к собеседованиям Intern / Trainee / Junior / Junior+ Python Backend. Программа покрывает Python Core, SQL/PostgreSQL, HTTP/security, FastAPI/Pydantic, SQLAlchemy/Alembic, testing, Redis, Docker/Git/Linux, architecture и честную защиту проектов StudyHub, Hotel Booking и Share Recipe. UX построен вокруг lesson reader, Monaco IDE, xterm.js, автоматической проверки, прогресса, XP и тематического interview mode.

## Что уже работает

- полная taxonomy из 406 стабильных lesson IDs в 33 stages;
- 359 опубликованных P0/P1-уроков; P2/P3 остаются честно помеченными `planned` и не открывают пустые страницы;
- 63 рабочие Python/FastAPI/Pydantic/SQLAlchemy/Alembic задачи со starter code, solutions и hidden pytest tests;
- 40 Python code-prediction snippets, 12 asyncio-задач, 48 полностью специфицированных PostgreSQL practice tasks, 59 debugging и 20 architecture scenarios;
- 20 interview sets, включая 25-вопросный Full Junior Interview, Crash Course и Resume Defense;
- Markdown с заголовками, списками, GFM-таблицами, цитатами/callouts, inline code и подсвеченными Python-блоками;
- Monaco Editor: Python highlighting, line numbers, tabs, auto-indent, несколько файлов, dark/light themes;
- file explorer: открыть, создать, переименовать и удалить пользовательский Python-файл;
- xterm.js с командами `python file.py`, `pytest`, `ls`, `pwd`, `clear`;
- отдельные Run и Check, stdout/stderr, exit code, timeout и список pytest-результатов;
- SQLite persistence для кода, прогресса, XP, попыток, последнего урока и interview answers;
- resizable sidebar, горизонтальный lesson/IDE split и editor/terminal panels;
- горячие клавиши `Cmd/Ctrl + Enter`, `Cmd/Ctrl + Shift + Enter`, `Cmd/Ctrl + S`;
- responsive sidebar и компактный mobile layout;
- оригинальные interview и code questions;
- Docker Compose с отдельными `frontend`, `backend`, `runner` и одноразовым sandbox-image service.

## Architecture

```text
Browser
  │
  ├── :3000  React / TypeScript / Vinext (Vite)
  │             ├── Monaco Editor
  │             ├── xterm.js
  │             └── React Markdown
  │
  └── :8000  FastAPI
                ├── content/ lesson loader
                ├── SQLAlchemy → SQLite volume
                └── :8001 Runner API
                           └── Docker Engine
                                └── temporary pythoria-sandbox container
                                     ├── Python 3.12
                                     └── hidden pytest tests
```

FastAPI никогда не исполняет пользовательский Python в собственном процессе. Backend передаёт разрешённую команду, пользовательские файлы и — только для Check — hidden tests отдельному runner service.

## Requirements

Рекомендуемый путь:

- Docker Desktop / Docker Engine с Compose v2;
- не менее 3 GB свободного места для первых image builds;
- свободные порты `3000`, `8000`, `8001`.

Для локальной разработки без Compose:

- Node.js 22.13+;
- Python 3.11+ (sandbox image использует Python 3.12);
- npm.

## Installation

Клонируй репозиторий и перейди в его корень. Дополнительная конфигурация для Docker-пути не требуется.

Для ручного dev-режима:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

cd frontend
npm ci
```

## Running

Полный безопасный локальный стек:

```bash
docker compose up --build
```

После запуска:

- UI: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)
- Runner health: [http://localhost:8001/health](http://localhost:8001/health)

Остановка без удаления SQLite volume:

```bash
docker compose down
```

Сбросить локальный прогресс намеренно можно удалением named volume:

```bash
docker compose down --volumes
```

Эта команда необратимо удаляет локальные XP, прогресс и сохранённый код.

### Development mode

Запусти три процесса в отдельных терминалах из корня проекта.

Runner без Docker sandbox — только для разработки и тестов:

```bash
RUNNER_MODE=local python -m uvicorn runner.app.main:app --reload --port 8001
```

Backend:

```bash
DATABASE_URL=sqlite:///./backend/data/dev.db \
CONTENT_ROOT="$PWD/content" \
RUNNER_URL=http://localhost:8001 \
python -m uvicorn backend.app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

## Project structure

```text
.
├── frontend/                 # React, Monaco, xterm, Markdown UI
│   ├── app/components/
│   └── Dockerfile
├── backend/
│   ├── app/
│   │   ├── content.py        # discovery/loading of lesson folders
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── main.py           # FastAPI endpoints
│   │   └── runner_client.py
│   └── tests/
├── runner/
│   ├── app/main.py           # execution limits and Docker lifecycle
│   ├── sandbox/Dockerfile    # Python + pytest image
│   └── tests/
├── content/
│   ├── curriculum.json       # полная taxonomy и planning status
│   ├── interview_sets.json   # тематические interview collections
│   ├── practice_banks.json   # SQL/debug/testing/architecture banks
│   ├── course.json           # сгенерированный published snapshot
│   └── <stage>/<lesson>/
├── scripts/smoke_test.py
├── tools/validate_content.py
├── tools/learning_materials.py       # reviewed Learn copy and Junior answer levels
├── tools/personalize_examples.py
├── tools/export_course_snapshot.py
├── docs/CONTENT_INVENTORY.md
├── docs/SQL_RUNNER_DESIGN.md
└── docker-compose.yml
```

## Content format

Каждый урок изолирован в отдельной директории:

```text
content/python-model/iterator-protocol/
├── lesson.md
├── metadata.json
├── interview.json            # optional
├── starter/
│   ├── main.py
│   └── service.py            # optional
├── tests/
│   └── test_main.py          # never returned to the browser
└── solution/
    └── main.py               # optional original solution
```

`metadata.json`:

```json
{
  "id": "backend-interview.4.2.iterator-protocol",
  "slug": "iterator-protocol",
  "title": "Iterator protocol",
  "module_slug": "stage-04",
  "module_title": "Stage 4 · Iteration, Generators, Exceptions and Context Managers",
  "order": 42,
  "priority": "P0",
  "interview_probability": "very_high",
  "market_frequency": "very_common",
  "market_evidence": "Python указан в 18/18 primary вакансий...",
  "prerequisites": ["backend-interview.4.1.iterable-vs-iterator"],
  "modes": ["learn", "interview", "practice"],
  "tracks": ["full", "interview_crash_course"],
  "content_status": "complete",
  "last_verified": "2026-08-27",
  "duration": 12,
  "xp": 25,
  "topics": ["Iterable", "Iterator", "StopIteration"],
  "description": "Iterable, iterator, __iter__, __next__ и StopIteration.",
  "has_task": true,
  "has_solution": true
}
```

Backend сканирует `metadata.json` при запросе, поэтому новый материал появляется без правок в React. `slug` — неизменяемый persistence key для progress/code; `id` — стабильный curriculum identifier. `curriculum.json` хранит taxonomy и planning status, lesson directories — опубликованный material, а `course.json` является только generated snapshot.

Lesson reader поддерживает два режима. **Learn** показывает теорию, примеры, характерные ошибки, практику и ответы с progressive disclosure. **Review** оставляет prediction/practice/task/interview blocks без подсказок; good answer и rubric раскрываются вручную.

Обязательный порядок `lesson.md`:

```text
Learning objectives
Theory
  Что это
  Как работает
  Пример
  Важный нюанс / limitation
  Где используется в backend (только при естественной связи)
Mental model
Что нужно знать на Junior
Code examples
Common mistakes
Practice
Code prediction / SQL practice (если применимо)
Interview questions
Good answers
Expected answer rubric
Задача
Cheat sheet
Sources
```

## Adding lessons

1. Сначала найди тему по `id`, `slug` и title в `content/curriculum.json`; duplicate запрещён.
2. Для planned record сохрани существующий ID/slug и переведи `content_status` в `complete` только после готовности материала.
3. Создай/обнови lesson directory, `lesson.md`, `metadata.json`, `interview.json` и `starter/main.py`.
4. Сохрани обязательные секции из Learn-flow выше. Theory должна сама объяснять concept; rubric не заменяет материал. `Code examples` обязан иллюстрировать именно этот subtopic: stage-wide дубликаты validator отклоняет.
5. Не переименовывай опубликованный slug: иначе потеряется связь с сохранённым progress/code.
6. Для high-frequency темы добавь reviewed dossier в `tools/learning_materials.py`: definition, mechanism, nuance, specific mistakes, Junior depth, practice и answer levels. Не добавляй stage-wide prompts вида «объясни X» вместо теории.
7. После массовой генерации запусти `python3 tools/personalize_examples.py`: tool использует curated core examples, публичный task starter и prediction/practice banks, чтобы соседние уроки не получали одинаковый пример и hidden solution не попадал в Markdown.
8. Запусти `python3 tools/validate_content.py` и `python3 tools/export_course_snapshot.py`.

Для будущего импорта материала формата `TOPIC:` / `MATERIAL:` сначала ищи урок по slug/title, затем разделяй текст на theory, examples, interview notes и task. Не создавай второй урок с той же темой.

## Adding tasks

1. Положи стартовые пользовательские файлы в `starter/`.
2. Опиши контракт в `lesson.md` под заголовком `## Задача`.
3. Добавь тесты в `tests/`.
4. При необходимости добавь оригинальное решение в `solution/`.
5. Установи `has_task: true` и `has_solution` в metadata.
6. Проверь как неправильное, так и правильное решение через UI или smoke-test.

File API принимает максимум 24 файла, 100 KB на файл и 500 KB на workspace. Абсолютные пути, `..` и неизвестные расширения отклоняются.

## Adding interview questions

`interview.json` хранит `question`, `level`, `priority`, `interview_probability`, `short_answer`, `junior_answer`, `follow_up_question`, `follow_up_answer`, краткий список `answer`, структурированный `expected_answer`, tags и sets. `expected_answer` содержит `must_mention`, `good_additions`, `common_wrong_answers`, `red_flags` и `follow_up_questions`. ID вопроса формируется стабильно как `<lesson-slug>:<index>`, поэтому не переставляй существующие вопросы без миграции progress.

Тематические collections определены в `content/interview_sets.json`. Full Junior Interview содержит ровно 25 curated questions; frontend позволяет переключать набор без внешнего LLM.

## Writing hidden tests

Тесты — обычный pytest:

```python
import pytest
from main import Countdown


def test_iteration_order():
    assert list(Countdown(3)) == [3, 2, 1]


def test_stop_iteration():
    iterator = Countdown(0)
    with pytest.raises(StopIteration):
        next(iterator)
```

Рекомендации:

- тестируй observable contract, а не внутреннюю реализацию;
- добавляй happy path, boundary и failure cases;
- не используй сеть и внешние сервисы;
- не полагайся на порядок запуска тестов;
- не импортируй зависимости, которых нет в sandbox image;
- сохраняй тесты только в `tests/`: endpoint урока их не раскрывает.

Sandbox Python 3.12 содержит pytest 8.4, FastAPI 0.116, Pydantic 2.11, SQLAlchemy 2.0.43, Alembic 1.19 и HTTPX 0.28. Версионно чувствительный material должен использовать именно Pydantic v2 и SQLAlchemy 2.x APIs.

## SQL practice

SQL runner в текущей архитектуре отсутствует. Поэтому сайт не заявляет интерактивное SQL execution: 48 PostgreSQL-compatible tasks содержат schema, seed, question, expected columns, ordered/unordered comparison, hidden solution или reasoning rubric. Они видны внутри SQL/PostgreSQL lessons и структурированы в `content/practice_banks.json`.

Безопасный disposable PostgreSQL design описан в `docs/SQL_RUNNER_DESIGN.md`. Не подменяй PostgreSQL SQLite-исполнением и не добавляй DB credentials в content.

## Priorities and planned content

- `P0` — обязательно для уверенного Junior interview;
- `P1` — часто встречается или заметно усиливает кандидата;
- `P2` — полезно для Junior+ или конкретного проекта;
- `P3` — bonus/advanced и не блокирует отклики.

P2/P3 metadata уже зарегистрирована, но `content_status: planned` исключает её из navigation. Чтобы опубликовать такой lesson, сначала добавь полный материал и только затем смени status; content validator не допускает пустые P0/P1 страницы.

## Python runner security

Каждый Run/Check создаёт отдельный временный Docker container. Применяются:

- `network_disabled=True`;
- 128 MB memory и такой же memory+swap limit;
- 0.5 CPU через `nano_cpus`;
- максимум 64 процесса;
- non-root UID/GID `65532`;
- dropped Linux capabilities;
- `no-new-privileges`;
- отдельный `tmpfs` для `/tmp`;
- 4-секундный timeout;
- stdout/stderr обрезаются после 32 KB;
- только allowlisted команды `python` и `pytest` без shell-интерпретации;
- container принудительно удаляется после попытки;
- hidden tests добавляются только runner-стороной.

Docker socket является сильной границей доверия. Runner service имеет к нему доступ, поэтому его API нельзя публиковать в недоверенную сеть. Для production runner следует размещать на отдельном worker host или заменять Docker socket на специализированный sandbox orchestrator.

## Database

SQLite хранится в named volume `pythoria_data`. Основные таблицы:

- `user_state` — XP, theme, last lesson;
- `lesson_progress` — status, theory/task completion;
- `code_files` — пользовательские файлы по lesson slug;
- `attempts` — Run/Check history и результаты;
- `interview_progress` — ответы и completion.

XP начисляется идемпотентно: +5 за первую отметку теории, +20 за первое успешное решение, +5 за первый ответ на interview question.

## Tests and verification

Unit/API tests:

```bash
python -m pytest backend/tests runner/tests -q
```

Content schema и все reference solutions:

```bash
python3 tools/validate_content.py --run-solutions
```

Frontend production build:

```bash
cd frontend
npm run build
```

End-to-end smoke-test для уже запущенного стека:

```bash
python scripts/smoke_test.py
```

Smoke-test проверяет frontend response, backend/runner health, 359 published lessons, 20 interview sets, сохранение файлов, stdout, SyntaxError, failed/passed hidden tests, terminal и persistent progress.
