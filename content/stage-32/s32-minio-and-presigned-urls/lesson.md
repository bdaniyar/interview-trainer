# MinIO and presigned URLs

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- объяснить `S3-compatible object storage` своими словами и связать с backend-сценарием;
- объяснить `short-lived direct upload` своими словами и связать с backend-сценарием;
- объяснить `metadata/key in PostgreSQL` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Resume Defense проверяет каждую заявленную технологию через конкретную роль в StudyHub, Hotel Booking или Share Recipe.

В теме **MinIO and presigned URLs** важно уверенно объяснять следующие части:

### S3-compatible object storage

Для `S3-compatible object storage` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### short-lived direct upload

Для `short-lived direct upload` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### metadata/key in PostgreSQL

Для `metadata/key in PostgreSQL` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### authorization

Authorization выполняется server-side на каждом resource/action и не заменяется скрытой кнопкой, CORS или данными из непроверенного token.

### finalize validation

Для `finalize validation` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### no raw binary in relational row

Для `no raw binary in relational row` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### MinIO and presigned URLs: отдельный пример

```text
Сценарий: Слишком большой file.

Проверка:
Policy, size validation, delete/reject.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Приписывать себе production scale, AWS, Kubernetes, Kafka или RabbitMQ без фактического опыта.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **MinIO and presigned URLs** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Защити один claim, назвав точный flow, failure mode и способ проверки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- S3-compatible object storage
- short-lived direct upload
- metadata/key in PostgreSQL
- authorization
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

- S3-compatible object storage
- short-lived direct upload
- metadata/key in PostgreSQL
- authorization
- finalize validation
- no raw binary in relational row.

## Задача

Разбери backend-сценарий: **Защити один claim, назвав точный flow, failure mode и способ проверки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Architecture practice

### Presigned upload

**Сценарий:** Слишком большой file.

**Rubric:** Policy, size validation, delete/reject.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **MinIO and presigned URLs**;
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
