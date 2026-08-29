# BackgroundTasks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **BackgroundTasks**, а не только запомнить термин;
- прочитать и изменить короткий пример для `runs after response in same application process`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

FastAPI `BackgroundTasks` schedules small in-process work after the response is sent.

### Как работает

The task runs in the same application process and has no durable delivery, distributed retry or crash recovery guarantee.


### Важный нюанс / limitation

Use it for small non-critical actions; use a queue/worker and idempotency for durable jobs.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- runs after response in same application process
- small non-critical work
- not durable
- lost on crash

### Полезно

- not a replacement for Celery/outbox

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### BackgroundTasks: отдельный пример

```python
def example_s14_backgroundtasks() -> tuple[str, ...]:
    # BackgroundTasks: проверяем отдельный contract урока.
    return ('runs after response in same application process', 'small non-critical work', 'not durable', 'lost on crash',)

assert example_s14_backgroundtasks()
```

Проследи request через router, validation, dependency, service и response model.

## Common mistakes

### Ошибка 1

Sending a critical payment/email only via BackgroundTasks can lose it on process restart.

## Practice

**A · Code/result prediction.** Change one input in the `runs after response in same application process` example and predict the result before running it.

**B · Find the bug.** Find code that violates `small non-critical work` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `runs after response in same application process` and add one edge-case test.

**E · Interview explanation.** Explain BackgroundTasks in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое BackgroundTasks и как это работает?

### Follow-up

Какая типичная ошибка связана с BackgroundTasks?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

FastAPI `BackgroundTasks` schedules small in-process work after the response is sent.

### Нормальный Junior answer

> FastAPI `BackgroundTasks` schedules small in-process work after the response is sent. The task runs in the same application process and has no durable delivery, distributed retry or crash recovery guarantee. Важное ограничение: Use it for small non-critical actions; use a queue/worker and idempotency for durable jobs.

### Углубление / follow-up

**Какая типичная ошибка связана с BackgroundTasks?**

Sending a critical payment/email only via BackgroundTasks can lose it on process restart.

## Expected answer rubric

### Must mention

- runs after response in same application process
- small non-critical work
- not durable
- lost on crash

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Sending a critical payment/email only via BackgroundTasks can lose it on process restart.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с BackgroundTasks?

## Задача

Сделай короткую письменную практику по теме **BackgroundTasks**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** FastAPI `BackgroundTasks` schedules small in-process work after the response is sent.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Sending a critical payment/email only via BackgroundTasks can lose it on process restart.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
