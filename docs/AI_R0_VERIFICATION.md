# Проверки Phase 10 R0

Исходная точка стека — `main` `ae33a09`, в котором уже находятся Phase 8D и 9A–9C. Пять PR образуют одну цепочку. Первый направлен в `main`. После ручного merge каждого PR поменяй базу следующего на `main` и проверь, что предыдущий head входит в историю. Используй коммиты слияния. Это сохраняет границу каждого ревью.

| PR | Содержание | Общая проверка на его ветке |
| --- | --- | --- |
| [#19](https://github.com/bdaniyar/interview-trainer/pull/19) | AI-трек, независимый прогресс и AI1.2 | 313 pytest, 85 Vitest, lint, TypeScript, build, примеры и эталоны, Chrome AI и полный Backend walkthrough |
| [#20](https://github.com/bdaniyar/interview-trainer/pull/20) | AI1.1 и AI1.3 | 313 pytest, 85 Vitest, lint, TypeScript, build, примеры и эталоны, Run трёх уроков через Docker |
| [#21](https://github.com/bdaniyar/interview-trainer/pull/21) | AI2.1, AI2.5, AI2.8, AI2.10 | 313 pytest, 85 Vitest, lint, TypeScript, build, примеры и эталоны, Run семи уроков через Docker |
| [#22](https://github.com/bdaniyar/interview-trainer/pull/22) | AI3.1–AI3.4 | 314 pytest, 85 Vitest, lint, TypeScript, build, 34 Check cases через Docker, 5 SDK mock tests |
| [#23](https://github.com/bdaniyar/interview-trainer/pull/23) | AI3.5–AI3.8 и P1 | 314 pytest, 85 Vitest, lint, TypeScript, build, полные примеры и эталоны, 26 P1 tests, 6 SDK mock tests |

На финальном дереве 370 опубликованных Backend и 15 AI-уроков. Запуск `tools/export_course_snapshot.py` восстановил исходный `content/course.json` побайтно. Старые lesson bundles, SQL-регистрации и grading bundles, PostgreSQL/Transaction/Index сервисы, настройки Python Runner и схема SQLite совпали с `main`. Валидатор проверяет 15 карточек, восемь graded IDs, отсутствие циклов, публикацию обязательных prerequisites и источники. 222 старых материала в curation debt отражены отдельно, AI-пакеты в этот список не добавлялись.

## Просмотр и запуск

```sh
python3 -m pytest
python3 tools/validate_content.py --run-solutions
(cd frontend && npm test && npm run lint && npx tsc --noEmit && npm run build)
docker compose -p pythoria-ai-r0-preview -f docker-compose.sql-workspace-test.yml up -d --build --wait
node scripts/smoke_sql_browser.mjs --ai-only
```

Preview использует 13000 и 18080, SQLite в tmpfs и изолированные сервисы. Для `python3 scripts/smoke_ai_runtime.py` создай свежую preview БД или отдельный тестовый экземпляр backend, чтобы браузерный Check и HTTP-матрица стартовали с собственным набором файлов. Сценарий проверяет исходный starter, намеренно неверный вариант и эталон. Повторный Check подтверждает одно начисление XP. Проверка sandbox ищет маршруты IPv4 и IPv6 к документальным адресам без отправки данных и проверяет отсутствие Docker socket и основной БД.

Проверки браузера включили поиск по треку, desktop/mobile, тёмную и светлую тему, Learn/Review с закрытыми ответами, Monaco, неуспешный и успешный Check, раздельный прогресс, редактирование файла, сохранение и перезагрузку. При нескольких AI-уроках первый сквозной тест обнаружил неверный ключ восстановления последнего урока. Повтор после унификации ключа прошёл. Отдельные таймауты sandbox при нагрузке проверены повтором с прежними лимитами. Для AI3.8 hidden tests захватывают реальные ASGI-наблюдения один раз и меняют по одному свойству. Публичный harness использует отдельный синтетический сервис и не содержит эталонов предыдущих лабораторий.

Backend-повтор в Chrome прошёл 23 SQL-урока, пять Python worker labs, три урока архитектуры, Transaction Lab, JSONB и Index Lab. Последовательный PostgreSQL-прогон прошёл 19 интеграционных проверок, включая изоляцию, сбой контроллера, cleanup и security policy. Параллельный запуск нагружал Docker и приводил к таймаутам. Дополнительные полные raw suites Transaction и Index остановлены после 12 и 3 успешных проверок; их браузерные smoke прошли полностью. Preserved fixtures включали Python-файлы, SQL drafts и SQL XP. Отдельно SQLite-копия с 115 строками прогресса, 112 файлами и 122 попытками сохраняла существующие строки, тему, Backend anchor и completion после записи нового AI-урока; +5 XP возникли только в копии. SHA-256 read-only выгрузки исходной SQLite совпал до и после работ.

[P1](../projects/chat_api/README.md) прошёл реальный loopback HTTP для JSON `POST /chat` и SSE `POST /chat/stream`. В тестовом процессе запретили сокеты. [SDK verification](../tools/ai_sdk_verify/README.md) закрепляет Python 3.12, OpenAI 3.57.0 и HTTPX2 2.16.2. Тесты проверяют payload и типы Responses, несколько output items, usage, incomplete, 401/429, timeout, unicode delta, terminal и закрытие потока. Это transport-проверка с вымышленными ценами и моделями; живых обращений к провайдеру не было.
