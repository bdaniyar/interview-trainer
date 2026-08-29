# Why outbox instead of direct Celery publish

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Learning objectives

После урока ты сможешь:

- объяснить `publish after commit can be lost` своими словами и связать с backend-сценарием;
- объяснить `publish before commit can observe rolled-back state` своими словами и связать с backend-сценарием;
- объяснить `outbox closes atomicity gap` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Background work отделяет latency запроса от выполнения, но добавляет delivery, retry и idempotency concerns.

В теме **Why outbox instead of direct Celery publish** важно уверенно объяснять следующие части:

### publish after commit can be lost

Для `publish after commit can be lost` проследи delivery от commit до side effect, включая duplicate, retry и idempotency.

### publish before commit can observe rolled-back state

Для `publish before commit can observe rolled-back state` проследи delivery от commit до side effect, включая duplicate, retry и idempotency.

### outbox closes atomicity gap

Для `outbox closes atomicity gap` проследи delivery от commit до side effect, включая duplicate, retry и idempotency.

### Celery may still be delivery/execution layer

Для `Celery may still be delivery/execution layer` проследи delivery от commit до side effect, включая duplicate, retry и idempotency.

## Mental model

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Why outbox instead of direct Celery publish: отдельный пример

```python
def example_s20_why_outbox_instead_of_direct_celery_publish() -> tuple[str, ...]:
    # Why outbox instead of direct Celery publish: проверяем отдельный contract урока.
    return ('publish after commit can be lost', 'publish before commit can observe rolled-back state', 'outbox closes atomicity gap', 'Celery may still be delivery/execution layer',)

assert example_s20_why_outbox_instead_of_direct_celery_publish()
```

Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.

## Common mistakes

**Ошибка:** Повторять side effect без idempotency или считать exactly-once свойством одного флага.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Why outbox instead of direct Celery publish** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи событие от commit через broker/worker до повторной доставки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- publish after commit can be lost
- publish before commit can observe rolled-back state
- outbox closes atomicity gap
- Celery may still be delivery/execution layer.
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

- publish after commit can be lost
- publish before commit can observe rolled-back state
- outbox closes atomicity gap
- Celery may still be delivery/execution layer.

## Задача

Разбери backend-сценарий: **Проследи событие от commit через broker/worker до повторной доставки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Why outbox instead of direct Celery publish**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
