# Проверка AI Engineering R1

Срез R1 от 2026-11-22 добавляет 14 опубликованных уроков и P2 поверх `c8421fc43207099cb84d42897b543ab8304a8a57`. Все 15 идентификаторов R0 сохранены. Валидатор проверяет исторический манифест R0, промежуточные состояния R1 и полный состав R1.

| Этап | Опубликовано | С практикой Check | С самостоятельной сверкой |
| --- | ---: | ---: | ---: |
| AI1 | 4/4 | 0 | 4 |
| AI2 | 10/10 | 6 | 4 |
| AI3 | 8/8 | 8 | 0 |
| AI4 | 7/7 | 6 | 1 |
| AI5–AI10 | 0/43 | — | — |
| Итого | **29/72** | **20** | **9** |

## Новые уроки

Все строки имеют статус `published`. Для каждой лаборатории с Check идентификатор упражнения образуется добавлением `.practice` к указанному ID. У AI1.4 и AI4.7 Run дополняет самостоятельную сверку по рубрике.

| Поставка | Урок и стабильный ID | Сценарии | Что проверяется |
| --- | --- | ---: | --- |
| 11A | AI1.4 `ai-engineering.01.04.ai-task-and-baseline` | 17 авторских | Правила для фактов и подтверждений, неоднозначность, обязательная проверка владельца |
| 11A | AI2.2 `ai-engineering.02.02.vectors-and-matrices` | 10 скрытых | Пустой вектор, отрицательные числа, нули, float, прямоугольность и конечность |
| 11A | AI2.3 `ai-engineering.02.03.loss-and-gradient-step` | 8 скрытых | MSE, согласованное обновление, обе производные, последовательность шагов |
| 11B | AI2.4 `ai-engineering.02.04.neural-network-forward` | 8 скрытых | Формы слоёв, ReLU, исходные веса, численная чувствительность |
| 11B | AI2.6 `ai-engineering.02.06.transformer-attention` | 8 скрытых | Масштаб, ось softmax, нормировка, большие логиты и causal mask |
| 11C | AI2.7 `ai-engineering.02.07.pretraining-and-alignment` | 9 скрытых | Сдвиг целей, маска, вероятность, NLL и классификация изменений |
| 11C | AI2.9 `ai-engineering.02.09.embedding-intuition` | 7 скрытых | Cosine, нормировка, совместимость моделей и ранжирование |
| 11D | AI4.1 `ai-engineering.04.01.prompt-contract` | 9 скрытых | Структура и версия, Unicode, границы ввода, недоверенный контекст |
| 11D | AI4.2 `ai-engineering.04.02.schema-and-domain-model` | 13 скрытых | Обязательная nullable форма, strict guests, лишние ключи, календарь и порядок дат |
| 11E | AI4.3 `ai-engineering.04.03.structured-output-parser` | 12 скрытых | Typed and nested output, пропуск parsed, ревизия схемы, refusal, incomplete |
| 11E | AI4.4 `ai-engineering.04.04.structured-output-failures` | 9 скрытых | Тип и приоритет ошибки, бюджет попыток, безопасный retry |
| 11F | AI4.5 `ai-engineering.04.05.extraction-evaluation` | 7 скрытых | Знаменатели, строгие типы, ошибки по кейсам, undefined и раздельные выборки |
| 11F | AI4.6 `ai-engineering.04.06.extraction-api` | 14 скрытых | Типизированный HTTP, статусы, приватность, ошибки и конкурентные запросы |
| 11F | AI4.7 `ai-engineering.04.07.extraction-project-review` | 3 авторских | Сравнение baseline и candidate, замороженный holdout, аргументация по рубрике |

Суммарно 12 новых лабораторий и 114 скрытых сценариев. Формулы потерь и производных проверены в исполняемых примерах и в эталонах. Для AI2.3 шаг от `w=b=0` на `[(0,1),(1,3)]` при `α=0.1` снижает MSE с 5 до 2.825. При `α=2` пример даёт MSE 85. Обе частные производные сравниваются с центральными разностями при `ε=1e−5`. В AI2.4 та же техника проверяет влияние отдельных весов вдали от излома ReLU. В AI2.6 для трёх токенов форма логитов `(3,3)`, форма результата `(3,d_v)`. У второй строки примера после маски остаются логиты `[0,2]`. Взвешенный результат с V `[3,6]` равен 5.642 с округлением. Тесты проверяют нулевую массу будущих токенов и нормировку по строкам на других входах.

Источники и их применимость записаны в метаданных и конспектах каждого урока. Авторская редакционная сверка выполнена по разделу 15 плана 2026-11-22. Включены официальные материалы Python, Google Machine Learning Crash Course, оригинальная статья о Transformer, документация Pydantic, FastAPI, OpenAI и OWASP. Уроки и примеры проверены автором. Самостоятельное объяснение решения и защита проекта оцениваются по рубрике.

## P2 и Structured Outputs

Локальный `POST /extract-trip` проходит typed provider, проверку wire-schema, домен и политику явных ISO-дат. API различает success, needs clarification, refusal, incomplete, invalid schema, invalid domain, timeout и unavailable. При включённом repair допускается одна дополнительная попытка в пределах общего deadline. Отказ и timeout завершают обработку. Поскольку в примере про поездку в Алматы нет года, обе даты остаются null. Формально валидный ответ с чужим городом обнаруживает оценка, поскольку форма DTO сама по себе город не подтверждает.

Датасет включает 20 синтетических запросов RU/EN. Версии, результаты по отдельным кейсам и хеши лежат в `projects/trip_extraction/data/evaluation-report.json`. SHA-256 данных `dc128857a417fa01b69ea49f5b8eed81ef08dd8d319869ddbd33faaeccb610c4`. Кандидат `trip.prompt.v2-regression` уступил baseline по unknown и exact match. Решение об отклонении принято на dev, holdout сохранён.

| Метрика | Dev, 12 запросов, v1 → v2 | Holdout, 8 запросов, v1 → v2 |
| --- | --- | --- |
| Валидность схемы среди ответов с проверяемым wire payload | 10/10 → 10/10 | 6/7 → 6/7 |
| Валидность домена среди результатов с проверяемым доменом | 8/10 → 8/10 | 5/6 → 5/6 |
| Точность известных полей | 23/24 → 23/24 | 11/12 → 11/12 |
| Сохранение unknown | 8/8 → 5/8 | 8/8 → 4/8 |
| Совпадение всех полей | 7/8 → 4/8 | 4/5 → 1/5 |
| Обработка отказа | 1/1 → 1/1 | 1/1 → 1/1 |
| Классификация итогового статуса | 12/12 → 10/12 | 7/8 → 6/8 |

Метрика без наблюдений сохраняется как `null`. Baseline включает намеренные дефекты, которые видны в отчёте. Scripted provider возвращает неизвестные поля для незнакомого текста. Оценка характеризует локальный контракт и контролируемое изменение. Отдельные инструкции по установке, схеме вызовов, локальной политике дат и версиям доступны в [P2 README](../projects/trip_extraction/README.md), [ADR](../projects/trip_extraction/ADR.md) и [списке источников](../projects/trip_extraction/SOURCES.md).

SDK-проверки выполнены под Python 3.12.13 с OpenAI 3.57.0, HTTPX2 2.16.2 и Pydantic 2.14.4. Шесть сценариев R1 плюс шесть сценариев R0 прошли с MockTransport и блокировкой исходящих подключений. `responses.parse` возвращает typed `output_parsed` для полного объекта. Для incomplete с оборванным JSON автопарсер может выбросить `ValidationError` до получения объекта ответа. Пример содержит эту проверку и вариант разбора, при котором статус читается первым. См. [SDK lock и команды](../tools/ai_sdk_verify/README.md), [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [PyPI OpenAI 3.57.0](https://pypi.org/project/openai/3.57.0/).

## Команды и результаты

| Команда | Результат |
| --- | --- |
| `.venv/bin/python -m pytest` | 317 passed. Сюда входят штатные backend, content, runner и policy suites. |
| `.venv/bin/python tools/validate_content.py --run-solutions` | 406 записей таксономии, 399 опубликованных уроков двух треков, 88 задач. Проверены примеры и эталоны. Валидатор отдельно сообщает о 222 старых уроках Stage 8+, ожидающих редакционной сверки. |
| `cd frontend && npm test && npm run lint && npx tsc --noEmit && npm run build` | 85 тестов. ESLint, TypeScript и сборка прошли. Сборщик предупредил о размере чанков и статической классификации маршрута. |
| `python -m pytest -o addopts='' -q tests` в `projects/chat_api`, lock P1 | 26 passed. |
| `python -m pytest -q tests` в `projects/trip_extraction`, чистая среда из `uv pip sync --offline --require-hashes` | 33 passed. |
| `python evaluate.py --output /tmp/p2-evaluation.json` и `cmp data/evaluation-report.json /tmp/p2-evaluation.json` в P2 | Отчёт совпал побайтово. |
| `python -m pytest tools/ai_sdk_verify` в среде из SDK lock | 12 passed. |
| `.venv/bin/python scripts/smoke_ai_runtime.py --lesson AI…` по строкам каждой поставки | 14 Run, 12 успешных Check, стартовые решения и дополнительные правдоподобные ошибочные решения отклонены. Файлы сохранились. Проверены границы sandbox. |
| `node scripts/smoke_sql_browser.mjs --ai-only` | Все 29 AI-уроков открылись через поиск. Проверены Learn и Review, Markdown, навигация, файлы, XP и desktop/mobile. AI3.1 и AI4.6 отклонили старт и приняли эталон с 11/11 и 14/14. |
| `node scripts/smoke_sql_browser.mjs` | 23 SQL Run и Check через Monaco, пять Worker-упражнений, три Architecture-урока, JSONB, Web Transaction и Index Lab. |
| `SQL_DOCKER_TESTS=1 .venv/bin/python -m pytest -o addopts='' -q sql_runner/tests/integration/test_postgres.py` | 19 passed. Выбранный набор покрывает реальный PostgreSQL, corpus решений, привилегии, изоляцию, таймауты, очистку и Python Runner. |

Негативный контроль AI2.2 заменил вычисление `matvec` константой `[8, 7, -2]`. Публичный пример напечатал ожидаемый вывод. Скрытые сценарии на других данных отклонили решение, 8 failed и 2 passed.

В P2 дополнительно сделаны восемь loopback-запросов к Uvicorn, семь из них конкурентно. Подтверждены успешный ответ, отсутствие выдуманного года, 502 при противоречивых датах и malformed payload, refusal, incomplete, 422 и уникальные request ID. Тесты дополнительно проверяют типы, recovery, отсутствие приватного текста и ключа в ответах и логах и запрет сетевых подключений.

В браузерных регрессиях Web Transaction Lab проверены два независимых редактора, наблюдаемая блокировка PostgreSQL, освобождение при commit, serializable, ошибочный и успешный Check, черновики и прогресс после reload. Index Lab проверен на чтение строк и реального плана, на оба исхода Check и сохранение состояния после reload и reset. Прогресс SQL учитывается отдельно от XP. Основной прогон подтверждает сохранение Python-файлов при переходе между SQL и Python.

Для AI проверено сворачивание ответов в обоих режимах на всех этапах, скачивание `ai04-extraction-project-review.md` с конспектом и источниками, переключение Backend и AI, изолированный процент, Monaco, прямые ссылки, 390 px и сохранение темы и файлов после reload. На повторном запуске smoke выявил зависимость от заранее выбранной темы. Сценарий теперь определяет ожидаемую тему по состоянию интерфейса до переключения. Итоговый браузерный прогон прошёл на чистой preview-базе.

## Совместимость и данные

Тест `test_r1_expansion_preserves_synthetic_r0_progress_and_files` заполняет тестовую SQLite записями Backend, R0 и ответа на собеседовании, переключает каталог на 29 AI-уроков и сравнивает сохранённые файлы, прогресс и XP. Повторная отметка прежнего ответа даёт 0 XP. Новые уроки остаются незавершёнными. Экспорт через `.venv/bin/python tools/export_course_snapshot.py` сохранил 370 уроков Backend, `content/course.json` совпадает побайтово с `origin/main`. Сравнение деревьев подтверждает сохранение регистрации SQL, grader bundles, P1, AI3, Docker-конфигурации, Python Runner и кода серверной и клиентской части приложения. Временные Docker и browser-прогоны используют проект `pythoria-r1-preview`, namespace песочниц, синтетическую SQLite на tmpfs и временный профиль Chrome. Основная SQLite, volume и контейнеры остались под запущенным Pythoria.

Wire data, текст и заметка разделены. Полномочия проверяет приложение. Песочница блокирует сеть и доступ к базе. Скрытые сценарии синтетические, Python Runner выполняет код ученика и тесты в общем изолированном контейнере. R1 проверен офлайн на синтетических данных. Независимая педагогическая проверка и оценка качества внешней модели остаются за пределами этих проверок.

## Порядок интеграции

| Поставка | PR | Ветка назначения | Коммит реализации | Graded |
| --- | --- | --- | --- | ---: |
| 11A | [#24](https://github.com/bdaniyar/interview-trainer/pull/24) | `main` | `6dd95cbd5cbfe8639b556ef9e129485e9051ff7c` | 2 |
| 11B | [#25](https://github.com/bdaniyar/interview-trainer/pull/25) | `feat/ai-numerical-foundations-phase11a` | `f273c1dda0af9024d3de18c3ed01a97f38cabd45` | 2 |
| 11C | [#26](https://github.com/bdaniyar/interview-trainer/pull/26) | `feat/ai-neural-attention-phase11b` | `d2a990db2282c15e40c89cd3d7e472e220813173` | 2 |
| 11D | [#27](https://github.com/bdaniyar/interview-trainer/pull/27) | `feat/ai-training-embeddings-phase11c` | `5cc7942f6b8ef58e08d9b6c9f76171cce7aa938d` | 2 |
| 11E | [#28](https://github.com/bdaniyar/interview-trainer/pull/28) | `feat/ai-prompt-schema-phase11d` | `c9aff30ae713820202f6b6a82993069ac8e38b05` | 2 |
| 11F | [#29](https://github.com/bdaniyar/interview-trainer/pull/29) | `feat/ai-structured-failures-phase11e` | `2a05e7e79fc5f410f425c119ea6b1132665f80b6` | 2 |

Ожидаемый порядок ревью и merge commits `#24 → #25 → #26 → #27 → #28 → #29`. После слияния каждой зависимости переведи следующую ветку на `main` в настройках base PR и проверь перечень файлов перед ревью. Этот порядок сохраняет историю коммитов и границы изменений каждой поставки.
