# Project structure

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Project structure**, а не только запомнить термин;
- прочитать и изменить короткий пример для `routers`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A practical FastAPI structure separates HTTP routers/schemas from use-case services and data-access details.

### Как работает

Routers adapt request/response, services hold business workflows/transaction decisions, repositories or query modules isolate persistence when they add value.


### Важный нюанс / limitation

Avoid pass-through layers with no behavior; boundaries should correspond to change/test seams.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- routers
- schemas
- services
- repositories/data access

### Полезно

- dependencies
- settings

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Project structure: отдельный пример

```python
def example_s14_project_structure() -> tuple[str, ...]:
    # Project structure: проверяем отдельный contract урока.
    return ('routers', 'schemas', 'services', 'repositories/data access',)

assert example_s14_project_structure()
```

Проследи request через router, validation, dependency, service и response model.

## Common mistakes

### Ошибка 1

Putting every concern into routes makes transaction testing and framework-independent business tests difficult.

## Practice

**A · Code/result prediction.** Change one input in the `routers` example and predict the result before running it.

**B · Find the bug.** Find code that violates `schemas` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `routers` and add one edge-case test.

**E · Interview explanation.** Explain Project structure in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Project structure и как это работает?

### Follow-up

Какая типичная ошибка связана с Project structure?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A practical FastAPI structure separates HTTP routers/schemas from use-case services and data-access details.

### Нормальный Junior answer

> A practical FastAPI structure separates HTTP routers/schemas from use-case services and data-access details. Routers adapt request/response, services hold business workflows/transaction decisions, repositories or query modules isolate persistence when they add value. Важное ограничение: Avoid pass-through layers with no behavior; boundaries should correspond to change/test seams.

### Углубление / follow-up

**Какая типичная ошибка связана с Project structure?**

Putting every concern into routes makes transaction testing and framework-independent business tests difficult.

## Expected answer rubric

### Must mention

- routers
- schemas
- services
- repositories/data access

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Putting every concern into routes makes transaction testing and framework-independent business tests difficult.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Project structure?

## Задача

Сделай короткую письменную практику по теме **Project structure**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A practical FastAPI structure separates HTTP routers/schemas from use-case services and data-access details.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Putting every concern into routes makes transaction testing and framework-independent business tests difficult.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
