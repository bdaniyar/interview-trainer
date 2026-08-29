# WebSockets

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **WebSockets**, а не только запомнить термин;
- прочитать и изменить короткий пример для `connection lifecycle`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Как работает

Проследи request через router, Pydantic validation, dependency graph, service и response model.

**connection lifecycle.** `connection lifecycle` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**receive/send.** `receive/send` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**disconnect.** `disconnect` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**authentication.** Authentication устанавливает identity, authorization проверяет право этой identity выполнить конкретное действие над resource.

**reconnect.** `reconnect` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.

**horizontal scaling.** `horizontal scaling` занимает конкретный этап FastAPI request lifecycle между router, validation/dependencies, handler и response serialization.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `connection lifecycle` и `receive/send` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `connection lifecycle`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- connection lifecycle
- receive/send
- disconnect
- authentication

### Полезно

- reconnect
- horizontal scaling

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### WebSockets: отдельный пример

```python
def example_s14_websockets() -> tuple[str, ...]:
    # WebSockets: проверяем отдельный contract урока.
    return ('connection lifecycle', 'receive/send', 'disconnect', 'authentication',)

assert example_s14_websockets()
```

Проследи request через router, validation, dependency, service и response model.

## Common mistakes

### Ошибка 1

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `connection lifecycle` до запуска.

**B · Find the bug.** Найди нарушение `receive/send` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про WebSockets за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое WebSockets и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме WebSockets?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

WebSockets: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.

### Нормальный Junior answer

> WebSockets — тема, в которой я сначала фиксирую `connection lifecycle`, затем объясняю `receive/send` на коротком примере. Ключевой механизм: Проследи request через router, Pydantic validation, dependency graph, service и response model. Главная практическая ошибка — Открыть глобальный request resource или спрятать domain logic в framework hook.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме WebSockets?**

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Expected answer rubric

### Must mention

- connection lifecycle
- receive/send
- disconnect
- authentication

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Открыть глобальный request resource или спрятать domain logic в framework hook.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме WebSockets?

## Задача

Сделай короткую письменную практику по теме **WebSockets**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** WebSockets: Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Открыть глобальный request resource или спрятать domain logic в framework hook.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
