# Python Interview Trainer

Pythoria — локальная интерактивная платформа для изучения продвинутого Python. UX построен вокруг плотного lesson reader, встроенного Monaco IDE, xterm.js-терминала, автоматической проверки задач, прогресса, XP и interview mode. Визуальная система самостоятельная; исходный код, логотипы и закрытые материалы UPSHELL не использовались.

## Что уже работает

- каталог из 67 уроков и 5 модулей;
- полноформатный первый урок «Устройство Python»;
- 5 обязательных оригинальных seed-уроков: `is` vs `==`, mutability, mutable defaults, iterator protocol, generators;
- дополнительная рабочая задача `MagicBox` в первом уроке;
- placeholders для остальных тем;
- Markdown с заголовками, списками, GFM-таблицами, цитатами/callouts, inline code и подсвеченными Python-блоками;
- Monaco Editor: Python highlighting, line numbers, tabs, auto-indent, несколько файлов, dark/light themes;
- file explorer: открыть, создать, переименовать и удалить пользовательский Python-файл;
- xterm.js с командами `python file.py`, `pytest`, `ls`, `pwd`, `clear`;
- отдельные Run и Check, stdout/stderr, exit code, timeout и список pytest-результатов;
- SQLite persistence для кода, прогресса, XP, попыток, последнего урока и interview answers;
- resizable course/sidebar, theory/workspace и editor/terminal panels;
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
│   ├── course.json
│   └── <module>/<lesson>/
├── scripts/smoke_test.py
├── tools/seed_content.py
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
  "slug": "iterator-protocol",
  "title": "Iterator protocol",
  "module_slug": "python-model",
  "module_title": "Модель Python и продвинутый ООП",
  "order": 5,
  "duration": 23,
  "xp": 25,
  "topics": ["Iterable", "Iterator", "StopIteration"],
  "description": "Iterable, iterator, __iter__, __next__ и StopIteration.",
  "has_task": true,
  "has_solution": true
}
```

Backend сканирует `metadata.json` при запросе, поэтому новый материал появляется без правок в React-коде. `content/course.json` — удобный сгенерированный snapshot каталога, а источником lesson details остаются директории уроков.

## Adding lessons

1. Найди подходящий модуль в `content/`.
2. Проверь slug существующих уроков, чтобы не создать duplicate.
3. Создай lesson directory, `lesson.md` и `metadata.json`.
4. Выбери уникальный глобальный `order`.
5. Добавь `starter/main.py`, даже если задача пока placeholder.
6. Перезапусти backend или просто обнови страницу: loader перечитывает файлы.
7. Обнови `content/course.json` вручную или осознанно запусти `python tools/seed_content.py`; без `--force` скрипт не перезаписывает существующие файлы.

Для будущего импорта материала формата `TOPIC:` / `MATERIAL:` сначала ищи урок по slug/title, затем разделяй текст на theory, examples, interview notes и task. Не создавай второй урок с той же темой.

## Adding tasks

1. Положи стартовые пользовательские файлы в `starter/`.
2. Опиши контракт в `lesson.md` под заголовком `## Задача`.
3. Добавь тесты в `tests/`.
4. При необходимости добавь оригинальное решение в `solution/`.
5. Установи `has_task: true` и `has_solution` в metadata.
6. Проверь как неправильное, так и правильное решение через UI или smoke-test.

File API принимает максимум 24 файла, 100 KB на файл и 500 KB на workspace. Абсолютные пути, `..` и неизвестные расширения отклоняются.

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

Frontend production build:

```bash
cd frontend
npm run build
```

End-to-end smoke-test для уже запущенного стека:

```bash
python scripts/smoke_test.py
```

Smoke-test проверяет frontend response, backend/runner health, 67-lesson catalog, сохранение файлов, stdout, SyntaxError, failed hidden tests, passed hidden tests, terminal и persistent progress.
