# Service layer

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Service layer**, а не только запомнить термин;
- прочитать и изменить короткий пример для `domain/use-case logic`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Как работает

Проследи request через router, Pydantic validation, dependency graph, service и response model.

**domain/use-case logic.** `domain/use-case logic` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**transaction boundary.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**framework-independent testing.** `framework-independent testing` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `domain/use-case logic` и `transaction boundary` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `domain/use-case logic`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- domain/use-case logic
- transaction boundary
- framework-independent testing

### Полезно

- связать Service layer с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Service layer: отдельный пример

```text
Сценарий: Route пишет current_user в module global.

Проверка:
Request-scoped dependency/context, immutable arguments; concurrent test обнаруживает утечку между запросами.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `domain/use-case logic` до запуска.

**B · Find the bug.** Найди нарушение `transaction boundary` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Service layer за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Global request state

**Сценарий:** Route пишет current_user в module global.

**Rubric:** Request-scoped dependency/context, immutable arguments; concurrent test обнаруживает утечку между запросами.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Service layer и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Service layer?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Service layer: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Нормальный Junior answer

> Service layer — тема, в которой я сначала фиксирую `domain/use-case logic`, затем объясняю `transaction boundary` на коротком примере. Ключевой механизм: Проследи request через router, Pydantic validation, dependency graph, service и response model. Главная практическая ошибка — Открыть глобальный request resource или спрятать domain logic в framework hook.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Service layer?**

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Expected answer rubric

### Must mention

- domain/use-case logic
- transaction boundary
- framework-independent testing

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Открыть глобальный request resource или спрятать domain logic в framework hook.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Service layer?

## Задача

Сделай короткую письменную практику по теме **Service layer**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Service layer: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Открыть глобальный request resource или спрятать domain logic в framework hook.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
