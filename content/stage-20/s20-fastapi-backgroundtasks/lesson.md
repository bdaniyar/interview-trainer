# FastAPI BackgroundTasks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Learning objectives

После урока ты сможешь:

- объяснить `process-local` своими словами и связать с backend-сценарием;
- объяснить `non-durable` своими словами и связать с backend-сценарием;
- объяснить `small side effects` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Background work отделяет latency запроса от выполнения, но добавляет delivery, retry и idempotency concerns.

В теме **FastAPI BackgroundTasks** важно уверенно объяснять следующие части:

### process-local

Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

### non-durable

Для `non-durable` проследи delivery от commit до side effect, включая duplicate, retry и idempotency.

### small side effects

Для `small side effects` проследи delivery от commit до side effect, включая duplicate, retry и idempotency.

### crash loss

Для `crash loss` проследи delivery от commit до side effect, включая duplicate, retry и idempotency.

## Mental model

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
def handle(message, repository):
    if repository.was_processed(message.id):
        return
    repository.apply(message.payload)
    repository.mark_processed(message.id)
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Повторять side effect без idempotency или считать exactly-once свойством одного флага.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **FastAPI BackgroundTasks** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи событие от commit через broker/worker до повторной доставки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- process-local
- non-durable
- small side effects
- crash loss.
- Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Повторять side effect без idempotency или считать exactly-once свойством одного флага.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- process-local
- non-durable
- small side effects
- crash loss.

## Задача

Разбери backend-сценарий: **Проследи событие от commit через broker/worker до повторной доставки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **FastAPI BackgroundTasks**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
