# AI Engineering R2 · проверка выпуска

Проверено 2026-11-24. Стек начинается от `9ca61dcb1f6269c23f26e5d49a79a605c8bdb9fd`, merge PR #30. AI1–AI5 закрыты по манифесту (4, 10, 8, 7 и 7 уроков). Опубликовано 36 из 72 уроков, всего 27 graded labs в AI. AI6–AI10 остаются в плане. Снапшот Backend содержит 370 опубликованных уроков.

## Новые лаборатории

Все строки имеют статус published. Указанные числа — количество собираемых pytest cases после параметризации. Колонка «Негативный контроль» описывает изменённый эталон, который Check должен отклонить вместе со starter. В каждом случае успешный Check начисляет XP один раз.

| Урок | Стабильный lesson ID | Стабильный task ID | Скрытых проверок | Негативный контроль |
| --- | --- | --- | ---: | --- |
| AI5.1 | `ai-engineering.05.01.tool-call-protocol` | `ai-engineering.05.01.tool-call-protocol.practice` | 18 | Сопоставить результаты по provider item ID. |
| AI5.2 | `ai-engineering.05.02.validated-tool-registry` | `ai-engineering.05.02.validated-tool-registry.practice` | 15 | Вернуть фиксированную проекцию без вызова внедрённого tool. |
| AI5.3 | `ai-engineering.05.03.tool-authorization` | `ai-engineering.05.03.tool-authorization.practice` | 13 | Убрать сверку собственника. |
| AI5.4 | `ai-engineering.05.04.bounded-tool-loop` | `ai-engineering.05.04.bounded-tool-loop.practice` | 17 | Убрать условие остановки по числу шагов. |
| AI5.5 | `ai-engineering.05.05.conversation-state` | `ai-engineering.05.05.conversation-state.practice` | 16 | При обрезке истории игнорировать резерв на ответ. |
| AI5.6 | `ai-engineering.05.06.tool-trust-boundaries` | `ai-engineering.05.06.tool-trust-boundaries.practice` | 21 | При запрещённом call выполнить предлагаемую запись в фикстуру. |
| AI5.7 | `ai-engineering.05.07.booking-assistant-project` | `ai-engineering.05.07.booking-assistant-project.practice` | 22 | Вернуть публичную бронь 42 без repository I/O. |

Редакционная самопроверка по разделу 15 плана прошла 2026-11-24. Проверены связь объяснения с первичными источниками, ход от интуиции к механизму, воспроизводимость, открытый контракт и закрытые разборы. Примеры объясняют отдельные механизмы, а скрытые сценарии меняют входы, владельцев, результаты и порядок работы. Markdown содержит краткий конспект, вопросы для самопроверки и источники. Самооценка по десяти критериям в порядке плана, от источников до ограничений: AI5.1 — 19/20 (краткий обзор wire formats), AI5.2 — 19/20 (упрощённый домен в примере), AI5.3 — 19/20 (синтетическая модель политики), AI5.4 — 19/20 (компактный пример deadline), AI5.5 — 19/20 (сводки разобраны концептуально), AI5.6 — 19/20 (аудит развёрнут в P3), AI5.7 — 19/20 (HTTP и история разбираются на уровне проекта). Открытый GitHub review остаётся этапом независимой проверки. Скрытые тесты синтетические и служат оценке учебного решения.

## Протокол и источники

Официальные разделы OpenAI Function calling и Conversation state подтверждают перенос исходных output items, `function_call_output.call_id` и обработку нескольких calls. Python asyncio подтверждает семантику timeout и cancellation. FastAPI и Pydantic описывают DI и строгую валидацию. OWASP LLM01 и API1:2023 обосновывают явную авторизацию перед чтением. AI5.1 объясняет сопоставление с Claude Messages и Gemini Interactions на уровне документации. У каждого урока указаны раздел, область применимости и дата проверки. [Манифест источников P3](../projects/booking_assistant/SOURCES.md).

`tools/ai_sdk_verify/tools_roundtrip.py` проходит реальный SDK с MockTransport. Проверены декларации, два разных ID, два результата, сохранённый reasoning item, continuation, malformed payload, timeout и 503. Оба прогона, OpenAI 3.57.0 из lock и отдельная проверка на 3.58.0, дали 22/22 (10 новых). SDK lock сохранился. Проверка проходила вне student Runner. Совместимость с живой моделью не тестировалась. [Инструкция SDK](../tools/ai_sdk_verify/README.md).

## P3

FastAPI использует synthetic principal из dependency. История проверяет tenant и subject, берёт claim на один turn и сохраняет только завершённый обмен. Контекст включает policy, текущий ввод, полный хронологический суффикс и резерв. P3 сопоставляет независимо возвращённые observations по исходным ID. Trace содержит request ID, шаг, безопасный tool alias, outcome, расход бюджета и измеренную задержку. Подробности и ограничения описаны в [P3 README](../projects/booking_assistant/README.md) и [ADR](../projects/booking_assistant/ADR.md).

Сервис сначала читает индекс политики и только затем payload. У `list_my_bookings` и `get_booking` есть проверяемый эффект чтения, а `propose_cancel` выдаёт pending предложение без записи. При инъекции scripted provider запрашивает запрещённый tool после чтения записи с частной заметкой. Наблюдение скрывает заметку, а registry возвращает `unknown_tool`. Негативные контроли отключают проверку владельца и имитируют запись из предложения. Оценка регистрирует оба дефекта как отдельные ошибки.

| Измерение | Результат |
| --- | ---: |
| Сценарии с ожидаемым наблюдаемым поведением | 27/27 |
| Успешные завершения среди ожидаемых `completed` | 16/16 |
| Корректные терминальные состояния, включая отмену | 27/27 |
| Нарушения авторизации | 0 |
| Неавторизованные чтения защищённого payload | 0 из 11 чтений |
| Изменения бронирований | 0 из 27 сценариев |
| Ошибочные счётчики вызовов | 0 из 27 сценариев, всего 17 вызовов |
| Ошибки корреляции call ID | 0 из 27 сценариев, в том числе при обратном порядке |
| Нарушения бюджета | 0 из 27 сценариев |
| Нарушения изоляции истории | 0 из 27 сценариев |

Воспроизводится побайтово. SHA-256 `500875d3eb4aef3c791a86c64a8396c88957807cf558c9dfd6650b44d0e70eed`. Оценка измеряет deterministic application contracts на зафиксированном сценарии провайдера. HTTP-тест проверяет независимое хранилище, 409 на параллельный turn в том же диалоге и освобождение claim после отмены. Отдельный сценарий проверяет параллельные turns в двух диалогах. Дедлайн во время tool очищает ожидающий I/O до выхода. [Сценарии](../projects/booking_assistant/data/workflows.jsonl), [отчёт](../projects/booking_assistant/data/evaluation.json), [локальный HTTP trace](../projects/booking_assistant/data/redacted-trace.json).

## Результаты проверок

| Команда | Результат |
| --- | --- |
| `python3 -m pytest` из корня | 320 passed. Backend, content, Runner, SQL policy, Transaction и Index policy. |
| `python3 tools/validate_content.py --run-solutions` | 406 опубликованных уроков, 95 исполняемых задач. Примеры и эталоны прошли. Аудит отдельно отмечает 222 прежних урока Stage 8+, ожидающих редакционной проверки. |
| `npm test`, `npm run lint`, `npx tsc --noEmit`, `npm run build` в `frontend` | 85 тестов; ESLint, TypeScript и сборка прошли. Vite сообщил о размере чанков и классификации маршрута. |
| `python -m pytest -o addopts='' -q tests` в P1 / P2 / P3 | 26 / 33 / 33 passed в отдельных окружениях. P3 установлен офлайн из lock с проверкой хешей. |
| `python -m pytest tools/ai_sdk_verify` | 22 passed в каждой из двух указанных SDK сред. |
| `python evaluate.py --output /tmp/booking-assistant-evaluation.json` и `cmp` в P3 | Побайтовое совпадение. |
| `python -m uvicorn main:app --host 127.0.0.1 --port 18765` и `python smoke_http.py --port 18765` в P3 | Создание диалога, чтение, отказ другому tenant, предложение и повторное чтение прошли через loopback. Опциональный скрипт проверен на отказ без opt-in. |
| `python3 scripts/smoke_ai_runtime.py --lesson AI5.1 … --lesson AI5.7` | 7 Run и 7 успешных Check, 122 hidden cases. Все 7 starter и 7 негативных контролей отклонены, файлы сохранились, повторный Check дал 0 XP. Из песочницы нет маршрута наружу, базы или Docker socket. |
| `node scripts/smoke_sql_browser.mjs --ai-only` | 36 уроков открыты через поиск с проверкой закрытых ответов в Learn/Review. Экспорт AI5.7, глубокая ссылка, Monaco, Run, сохранение и reload прошли. AI3.1 и AI5.7 отклонили starter и приняли эталон с 11/11 и 22/22. Проверены оба трека, отдельные показатели прогресса, ширина 390 px, desktop и смена темы. |
| `node scripts/smoke_sql_browser.mjs` | 23 SQL Run/Check, пять Worker labs, три Architecture-урока, JSONB, Web Transaction Lab и Index Lab. Проверены блокировка и commit release, план индекса, desktop/mobile, черновики после reload и сохранение XP. |
| `SQL_DOCKER_TESTS=1 python -m pytest -o addopts='' -q sql_runner/tests/integration/test_postgres.py` | 19 passed на disposable PostgreSQL. Проверены corpus SQL, привилегии, изоляция, таймауты и очистка. |

## Совместимость

`test_expansion_preserves_synthetic_progress_and_files` проверяет 15→29 и 29→36 на отдельной SQLite с сохранёнными AI и Backend файлами, прогрессом, вопросом собеседования, XP, темой и последним открытым Backend-уроком. Повторная отметка собеседования начисляет 0 XP. Новые задачи и теория остаются незавершёнными. Backend summary сравнивается целиком. Chrome проверяет сохранение SQL draft после reload и Python-файлов при переключении.

Сравнение дерева с `origin/main` подтверждает сохранение 29 прежних AI-уроков, Backend-снапшота, регистраций и grader bundles SQL, backend/frontend runtime, Python Runner, P1, P2 и Compose. Для browser и Run/Check использованы read-only content bind, tmpfs SQLite и Docker project `pythoria-r2-preview`. Основная SQLite и именованные volumes не подключались к preview. Основная сборка Pythoria не заменялась. P3 использует только локальные fixtures и память процесса.

## Порядок интеграции

| Поставка | PR | Исходная база | Лаборатории |
| --- | --- | --- | --- |
| 12A | [#31](https://github.com/bdaniyar/interview-trainer/pull/31) | `main` | AI5.1, AI5.2 |
| 12B | [#32](https://github.com/bdaniyar/interview-trainer/pull/32) | `feat/ai-tool-protocol-phase12a` | AI5.3, AI5.4 |
| 12C | [#33](https://github.com/bdaniyar/interview-trainer/pull/33) | `feat/ai-tool-authorization-phase12b` | AI5.5, AI5.6 |
| 12D | [#34](https://github.com/bdaniyar/interview-trainer/pull/34) | `feat/ai-conversation-boundaries-phase12c` | AI5.7 и P3 |

Ручной порядок merge commits **#31 → #32 → #33 → #34**. После каждого merge перевести base следующего PR на `main` и сверить список файлов. Этот порядок сохраняет коммиты и границы ревью. Автоматических merge и force-push в R2 не было.
