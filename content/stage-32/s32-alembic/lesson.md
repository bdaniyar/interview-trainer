# Alembic

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- объяснить `versioned schema` своими словами и связать с backend-сценарием;
- объяснить `autogenerate review` своими словами и связать с backend-сценарием;
- объяснить `expand/contract` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Resume Defense проверяет каждую заявленную технологию через конкретную роль в StudyHub, Hotel Booking или Share Recipe.

В теме **Alembic** важно уверенно объяснять следующие части:

### versioned schema

Для `versioned schema` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### autogenerate review

Для `autogenerate review` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### expand/contract

Для `expand/contract` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### data migration/rollback awareness

Rollback отменяет текущую transaction и возвращает Session в usable state; после flush error продолжать без rollback нельзя.

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

1. Объясни **Alembic** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Защити один claim, назвав точный flow, failure mode и способ проверки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- versioned schema
- autogenerate review
- expand/contract
- data migration/rollback awareness.
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

- versioned schema
- autogenerate review
- expand/contract
- data migration/rollback awareness.

## Задача

Разбери backend-сценарий: **Защити один claim, назвав точный flow, failure mode и способ проверки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Alembic**;
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
