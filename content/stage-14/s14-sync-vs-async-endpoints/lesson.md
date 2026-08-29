# Sync vs async endpoints

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Sync vs async endpoints**, а не только запомнить термин;
- прочитать и изменить короткий пример для `threadpool behavior for sync endpoint`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

FastAPI supports sync and async endpoints; async is useful when the dependency stack performs awaitable I/O.

### Как работает

Async endpoints run on the event loop, while sync endpoints are normally dispatched through a thread pool so blocking work does not directly block the loop.


### Важный нюанс / limitation

Declaring `async def` does not make sync drivers non-blocking; use an async driver/client or deliberately offload work.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- threadpool behavior for sync endpoint
- blocking inside async
- async only when dependency stack benefits

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Sync vs async endpoints: отдельный пример

```text
Сценарий: Async route вызывает sync dependency с долгим blocking client внутри event loop.

Проверка:
Использовать async client/driver или thread offload; измерить event-loop lag и concurrent latency.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Calling `requests` or a sync DB driver inside async endpoint blocks the loop despite the async function declaration.

## Practice

**A · Code/result prediction.** Change one input in the `threadpool behavior for sync endpoint` example and predict the result before running it.

**B · Find the bug.** Find code that violates `blocking inside async` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `threadpool behavior for sync endpoint` and add one edge-case test.

**E · Interview explanation.** Explain Sync vs async endpoints in 45–60 seconds and include one limitation.

## Debugging practice

### Blocking dependency

**Сценарий:** Async route вызывает sync dependency с долгим blocking client внутри event loop.

**Rubric:** Использовать async client/driver или thread offload; измерить event-loop lag и concurrent latency.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Sync vs async endpoints и как это работает?

### Follow-up

Какая типичная ошибка связана с Sync vs async endpoints?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

FastAPI supports sync and async endpoints; async is useful when the dependency stack performs awaitable I/O.

### Нормальный Junior answer

> FastAPI supports sync and async endpoints; async is useful when the dependency stack performs awaitable I/O. Async endpoints run on the event loop, while sync endpoints are normally dispatched through a thread pool so blocking work does not directly block the loop. Важное ограничение: Declaring `async def` does not make sync drivers non-blocking; use an async driver/client or deliberately offload work.

### Углубление / follow-up

**Какая типичная ошибка связана с Sync vs async endpoints?**

Calling `requests` or a sync DB driver inside async endpoint blocks the loop despite the async function declaration.

## Expected answer rubric

### Must mention

- threadpool behavior for sync endpoint
- blocking inside async
- async only when dependency stack benefits

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Calling `requests` or a sync DB driver inside async endpoint blocks the loop despite the async function declaration.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Sync vs async endpoints?

## Задача

Сделай короткую письменную практику по теме **Sync vs async endpoints**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** FastAPI supports sync and async endpoints; async is useful when the dependency stack performs awaitable I/O.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Calling `requests` or a sync DB driver inside async endpoint blocks the loop despite the async function declaration.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
