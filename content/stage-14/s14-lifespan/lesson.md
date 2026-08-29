# Lifespan

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Lifespan**, а не только запомнить термин;
- прочитать и изменить короткий пример для `startup/shutdown`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

FastAPI lifespan manages resources that live for the application process, such as connection pools and shared HTTP clients.

### Как работает

An async context manager runs setup before yield and cleanup after yield during shutdown; tests should enter lifespan too.


### Важный нюанс / limitation

Application-level resources are shared, but request-specific Session/user state must not be stored in them.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- startup/shutdown
- shared client/pool initialization
- cleanup
- modern lifespan over scattered legacy hooks

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Lifespan: отдельный пример

```text
Сценарий: HTTP client создаётся на startup, но socket остаётся после shutdown.

Проверка:
Lifespan async context manager с cleanup в finally; test lifespan and close state.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Creating a new expensive client per request wastes pools, while never closing a shared client leaks resources at shutdown.

## Practice

**A · Code/result prediction.** Change one input in the `startup/shutdown` example and predict the result before running it.

**B · Find the bug.** Find code that violates `shared client/pool initialization` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `startup/shutdown` and add one edge-case test.

**E · Interview explanation.** Explain Lifespan in 45–60 seconds and include one limitation.

## Debugging practice

### Resource not closed

**Сценарий:** HTTP client создаётся на startup, но socket остаётся после shutdown.

**Rubric:** Lifespan async context manager с cleanup в finally; test lifespan and close state.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Lifespan и как это работает?

### Follow-up

Какая типичная ошибка связана с Lifespan?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

FastAPI lifespan manages resources that live for the application process, such as connection pools and shared HTTP clients.

### Нормальный Junior answer

> FastAPI lifespan manages resources that live for the application process, such as connection pools and shared HTTP clients. An async context manager runs setup before yield and cleanup after yield during shutdown; tests should enter lifespan too. Важное ограничение: Application-level resources are shared, but request-specific Session/user state must not be stored in them.

### Углубление / follow-up

**Какая типичная ошибка связана с Lifespan?**

Creating a new expensive client per request wastes pools, while never closing a shared client leaks resources at shutdown.

## Expected answer rubric

### Must mention

- startup/shutdown
- shared client/pool initialization
- cleanup
- modern lifespan over scattered legacy hooks

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Creating a new expensive client per request wastes pools, while never closing a shared client leaks resources at shutdown.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Lifespan?

## Задача

Сделай короткую письменную практику по теме **Lifespan**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** FastAPI lifespan manages resources that live for the application process, such as connection pools and shared HTTP clients.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Creating a new expensive client per request wastes pools, while never closing a shared client leaks resources at shutdown.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
