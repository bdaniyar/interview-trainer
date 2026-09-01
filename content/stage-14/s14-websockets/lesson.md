# WebSockets

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **WebSockets**, а не только запомнить термин;
- прочитать и изменить короткий пример для `connection lifecycle`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.

### Как работает

Проследи request через router, Pydantic validation, dependency graph, service и response model.

**connection lifecycle.** `connection lifecycle` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.

**receive/send.** `receive/send` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.

**disconnect.** `disconnect` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.

**аутентификацию.** Аутентификацию устанавливает identity, authorization проверяет право этой identity выполнить конкретное действие над resource.

**reconnect.** `reconnect` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.

**horizontal scaling.** `horizontal scaling` занимает конкретный этап FastAPI жизненный цикл запроса между router, validation/dependencies, handler и сериализация ответа.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `connection lifecycle` и `receive/send` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `connection lifecycle`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- connection lifecycle
- receive/send
- disconnect
- аутентификацию

### Полезно

- reconnect
- horizontal scaling

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### WebSockets: отдельный пример

```python
def example_s14_websockets() -> tuple[str, ...]:
    # WebSockets: проверяем отдельный contract урока.
    return ('connection lifecycle', 'receive/send', 'disconnect', 'authentication',)

assert example_s14_websockets()
```

Проследи request через router, validation, dependency, service и response model.

## Типичные ошибки

### Ошибка 1

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `connection lifecycle` до запуска.

**B · Найди ошибку.** Найди нарушение `receive/send` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про WebSockets за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое WebSockets и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме WebSockets?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

WebSockets: Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.

### Нормальный ответ уровня Junior

> WebSockets — тема, в которой я сначала фиксирую `connection lifecycle`, затем объясняю `receive/send` на коротком примере. Ключевой механизм: Проследи request через router, Pydantic validation, dependency graph, service и response model. Главная практическая ошибка — Открыть глобальный request resource или спрятать domain logic в framework hook.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме WebSockets?**

Открыть глобальный request resource или спрятать domain logic в framework hook.

## Критерии хорошего ответа

### Что обязательно упомянуть

- connection lifecycle
- receive/send
- disconnect
- аутентификацию

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Открыть глобальный request resource или спрятать domain logic в framework hook.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме WebSockets?

## Задача

Сделай короткую письменную практику по теме **WebSockets**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** WebSockets: Это часть FastAPI жизненный цикл запроса между routing, validation, dependencies, handler и сериализация ответа.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Открыть глобальный request resource или спрятать domain logic в framework hook.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
