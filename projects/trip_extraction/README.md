# P2 · Structured Trip Extraction

Локальный FastAPI-сервис переводит синтетические запросы о поездках в проверенный TripRequest. Стандартный адаптер выдаёт scripted fixtures. Он покрывает примеры RU/EN и возвращает неизвестные поля при незнакомом запросе. Для работы нужны Python 3.12 и зависимости из lock-файла.

```sh
cd projects/trip_extraction
uv venv --python 3.12
uv pip sync --python .venv/bin/python --require-hashes requirements.txt
.venv/bin/python -m pytest -q tests
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8765
```

Установка использует индекс пакетов или заранее заполненный кэш. Добавь `--offline` к `uv pip sync` при работе из кэша. Тесты запускаются локально с запретом сетевых подключений.

```sh
curl -sS http://127.0.0.1:8765/extract-trip \
  -H 'Content-Type: application/json' \
  -d '{"text":"Хочу поехать в Алматы с 10 по 15 декабря, нас трое."}'
curl -sS http://127.0.0.1:8765/extract-trip \
  -H 'Content-Type: application/json' \
  -d '{"text":"В Алматы с 2027-12-10 по 2027-12-15, нас трое."}'
```

Первый ответ имеет статус `needs_clarification`, город Алматы, 3 гостей и обе даты null. Второй возвращает `completed` с двумя полными ISO-датами. Локальная политика принимает дату из ответа, если её полная строка YYYY-MM-DD встречается в пользовательском запросе. Число в номере брони и дата из недоверенной заметки не подтверждают дату. При расплывчатых или не-ISO формулировках нужны уточнения. Порядок дат и положительный strict int проверяет домен.

## Путь запроса

1. FastAPI проверяет `ExtractRequest`, генерирует request ID и получает provider через dependency.
2. `prompt.py` собирает версию, инструкции, два демонстрационных примера и независимые поля текста и заметки.
3. `Provider.extract` возвращает типизированный исход с wire payload. Адаптер можно подменить через `create_app(provider=...)`.
4. `pipeline.py` читает целый JSON или typed Envelope, проверяет TripRequest, ограничивает время ожидания и формирует результат с model, prompt и schema version.
5. FastAPI возвращает typed DTO. Стандартный запуск не пишет сырые запросы, ключи или provider exceptions в логи.
6. `evaluate.py` прогоняет те же версии по замороженным dev и holdout. `metrics.py` сохраняет знаменатели и ошибки по ID.

| Исход | HTTP | Trip |
| --- | --- | --- |
| completed / needs_clarification | 200 | Проверенный DTO, включая null у неизвестных значений |
| refusal / incomplete | 200 | null и конкретная категория |
| invalid_schema / invalid_domain | 502 | null, безопасная категория |
| unavailable / timeout | 503 / 504 | null |
| invalid_request | 422 | null, провайдер не вызывается |

По умолчанию одна попытка. Сервер может явно разрешить один repair для incomplete, invalid wire или подтверждённого временного отказа до выполнения. При этом сохраняются один запрос, correlation ID и общий deadline. Refusal и неизвестный timeout завершают операцию.

## Воспроизводимая оценка

```sh
.venv/bin/python evaluate.py --output /tmp/p2-evaluation.json
cmp data/evaluation-report.json /tmp/p2-evaluation.json
```

Данные содержат 12 dev и 8 holdout. Baseline — `trip.prompt.v1`. Учебный `trip.prompt.v2-regression` в отдельном eval добавляет ложные defaults для city и guests. Схема, входы и эталоны сохранены. API работает с baseline.

| Метрика | Dev v1 → v2 | Holdout v1 → v2 |
| --- | --- | --- |
| Schema validity | 10/10 → 10/10 | 6/7 → 6/7 |
| Domain validity | 8/10 → 8/10 | 5/6 → 5/6 |
| Field accuracy, известные факты | 23/24 → 23/24 | 11/12 → 11/12 |
| Unknown correctness | 8/8 → 5/8 | 8/8 → 4/8 |
| Exact match | 7/8 → 4/8 | 4/5 → 1/5 |
| Refusal handling | 1/1 → 1/1 | 1/1 → 1/1 |
| Outcome accuracy | 12/12 → 10/12 | 7/8 → 6/8 |

Ошибки `trip-11` и `trip-19` намеренно заложены и видны уже в baseline. Например, чужой город проходит форму, а придуманная дата становится null и переводит ответ в needs_clarification. Candidate отклонён за потерю unknown correctness в dev. Holdout показан для воспроизводимости и не использовался для подгона. Доля при пустом знаменателе — null. Упражнение подтверждает поведение scripted системы. Факты реального провайдера потребуют независимой оценки.

[ADR провайдерской границы](ADR.md) · [Источники и версии](SOURCES.md) · [Отдельная проверка реального SDK](LIVE_PROVIDER.md)
