# StudyHub in 60 seconds

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- объяснить `student platform backend` своими словами и связать с backend-сценарием;
- объяснить `FastAPI/PostgreSQL/Redis` своими словами и связать с backend-сценарием;
- объяснить `communities/roles/discussions/materials/Q&A/moderation` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Resume Defense проверяет каждую заявленную технологию через конкретную роль в StudyHub, Hotel Booking или Share Recipe.

В теме **StudyHub in 60 seconds** важно уверенно объяснять следующие части:

### student platform backend

Для `student platform backend` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### FastAPI/PostgreSQL/Redis

Redis хранит данные в памяти и полезен для cache/TTL/atomic counters, но durability, eviction и outage policy нужно проектировать явно.

### communities/roles/discussions/materials/Q&A/moderation

Для `communities/roles/discussions/materials/Q&A/moderation` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### WebSocket for client connection

WebSocket держит долгоживущее соединение; масштабирование требует shared fan-out, а durable history хранится отдельно.

### Redis Pub/Sub for cross-instance live fan-out

Redis хранит данные в памяти и полезен для cache/TTL/atomic counters, но durability, eviction и outage policy нужно проектировать явно.

### PostgreSQL for history/read state

Для `PostgreSQL for history/read state` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### outbox worker

Для `outbox worker` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```text
Проблема → моё решение → почему так → failure mode → как проверил
Граница опыта → что изучил бы перед production rollout
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Приписывать себе production scale, AWS, Kubernetes, Kafka или RabbitMQ без фактического опыта.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **StudyHub in 60 seconds** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Защити один claim, назвав точный flow, failure mode и способ проверки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- student platform backend
- FastAPI/PostgreSQL/Redis
- communities/roles/discussions/materials/Q&A/moderation
- WebSocket for client connection
- Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Приписывать себе production scale, AWS, Kubernetes, Kafka или RabbitMQ без фактического опыта.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- student platform backend
- FastAPI/PostgreSQL/Redis
- communities/roles/discussions/materials/Q&A/moderation
- WebSocket for client connection
- Redis Pub/Sub for cross-instance live fan-out
- PostgreSQL for history/read state
- outbox worker
- MinIO

## Задача

Разбери backend-сценарий: **Защити один claim, назвав точный flow, failure mode и способ проверки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Architecture practice

### StudyHub pitch

**Сценарий:** Проект за 60 секунд.

**Rubric:** Problem, own role, stack, decision, verification.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **StudyHub in 60 seconds**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
