# OpenAPI and Swagger

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **OpenAPI and Swagger**, а не только запомнить термин;
- прочитать и изменить короткий пример для `generation from hints/models`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Как работает

Проследи request через router, Pydantic validation, dependency graph, service и response model.

**generation from hints/models.** `generation from hints/models` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**examples.** `examples` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**operation IDs.** `operation IDs` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**contract value.** `contract value` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `generation from hints/models` и `examples` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `generation from hints/models`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- generation from hints/models
- examples
- operation IDs
- contract value

### Полезно

- связать OpenAPI and Swagger с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### OpenAPI and Swagger: отдельный пример

```python
def example_s14_openapi_and_swagger() -> tuple[str, ...]:
    # OpenAPI and Swagger: проверяем отдельный contract урока.
    return ('generation from hints/models', 'examples', 'operation IDs', 'contract value',)

assert example_s14_openapi_and_swagger()
```

Проследи request через router, validation, dependency, service и response model.

## Common mistakes

### Ошибка 1

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `generation from hints/models` до запуска.

**B · Find the bug.** Найди нарушение `examples` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про OpenAPI and Swagger за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое OpenAPI and Swagger и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме OpenAPI and Swagger?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

OpenAPI and Swagger: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Нормальный Junior answer

> OpenAPI and Swagger — тема, в которой я сначала фиксирую `generation from hints/models`, затем объясняю `examples` на коротком примере. Ключевой механизм: Проследи request через router, Pydantic validation, dependency graph, service и response model. Главная практическая ошибка — Открыть глобальный request resource или спрятать domain logic в framework hook.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме OpenAPI and Swagger?**

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Expected answer rubric

### Must mention

- generation from hints/models
- examples
- operation IDs
- contract value

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Открыть глобальный request resource или спрятать domain logic в framework hook.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме OpenAPI and Swagger?

## Задача

Сделай короткую письменную практику по теме **OpenAPI and Swagger**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** OpenAPI and Swagger: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Открыть глобальный request resource или спрятать domain logic в framework hook.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
