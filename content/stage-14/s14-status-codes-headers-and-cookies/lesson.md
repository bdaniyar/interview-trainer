# Status codes, headers and cookies

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Status codes, headers and cookies**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Status codes, headers and cookies`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Как работает

Проследи request через router, Pydantic validation, dependency graph, service и response model.

**Status codes, headers and cookies.** Status code сообщает результат HTTP operation: 2xx success, 4xx client/request state, 5xx server failure; error body добавляет стабильный machine-readable code.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Status codes, headers and cookies` и `Status codes, headers and cookies` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Status codes, headers and cookies`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Status codes, headers and cookies

### Полезно

- связать Status codes, headers and cookies с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Status codes, headers and cookies: отдельный пример

```text
Сценарий: API отдаёт 403 пользователю без валидной authentication.

Проверка:
401 — нет/невалидна authentication (с challenge), 403 — identity известна, permission недостаточно.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Status codes, headers and cookies` до запуска.

**B · Find the bug.** Найди нарушение `Status codes, headers and cookies` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Status codes, headers and cookies за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Wrong 401/403

**Сценарий:** API отдаёт 403 пользователю без валидной authentication.

**Rubric:** 401 — нет/невалидна authentication (с challenge), 403 — identity известна, permission недостаточно.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Status codes, headers and cookies и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Status codes, headers and cookies?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Status codes, headers and cookies: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Нормальный Junior answer

> Status codes, headers and cookies — тема, в которой я сначала фиксирую `Status codes, headers and cookies`, затем объясняю `Status codes, headers and cookies` на коротком примере. Ключевой механизм: Проследи request через router, Pydantic validation, dependency graph, service и response model. Главная практическая ошибка — Открыть глобальный request resource или спрятать domain logic в framework hook.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Status codes, headers and cookies?**

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Expected answer rubric

### Must mention

- Status codes, headers and cookies

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Открыть глобальный request resource или спрятать domain logic в framework hook.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Status codes, headers and cookies?

## Задача

Сделай короткую письменную практику по теме **Status codes, headers and cookies**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Status codes, headers and cookies: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Открыть глобальный request resource или спрятать domain logic в framework hook.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
