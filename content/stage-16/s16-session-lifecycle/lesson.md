# Session lifecycle

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Session lifecycle**, а не только запомнить термин;
- прочитать и изменить короткий пример для `create`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Session lifecycle: создать, использовать в одном unit of work, выполнить commit или rollback и закрыть.

### Как работает

FastAPI yield-dependency может владеть одной Session на request; service решает исход transaction, а cleanup всегда закрывает Session.


### Важный нюанс / ограничение

Одну AsyncSession нельзя одновременно использовать в нескольких tasks: она содержит mutable transaction и identity state.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- create
- use
- commit/rollback
- close

### Полезно

- request-scoped session
- never share one session globally

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Session lifecycle: отдельный пример

```python
def example_s16_session_lifecycle() -> tuple[str, ...]:
    # Session lifecycle: проверяем отдельный contract урока.
    return ('create', 'use', 'commit/rollback', 'close',)

assert example_s16_session_lifecycle()
```

Укажи владельца Session/transaction и момент фактического SQL I/O.

## Типичные ошибки

### Ошибка 1

Module-global Session переносит tracked objects и transaction failures между requests.

## Практика

**A · Предсказание результата.** Измени один input в примере `create` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `use`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `create`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Session lifecycle за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Session lifecycle и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Session lifecycle?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Session lifecycle: создать, использовать в одном unit of work, выполнить commit или rollback и закрыть.

### Нормальный ответ уровня Junior

> Session lifecycle: создать, использовать в одном unit of work, выполнить commit или rollback и закрыть. FastAPI yield-dependency может владеть одной Session на request; service решает исход transaction, а cleanup всегда закрывает Session. Важное ограничение: Одну AsyncSession нельзя одновременно использовать в нескольких tasks: она содержит mutable transaction и identity state.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Session lifecycle?**

Module-global Session переносит tracked objects и transaction failures между requests.

## Критерии хорошего ответа

### Что обязательно упомянуть

- create
- use
- commit/rollback
- close

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Module-global Session переносит tracked objects и transaction failures между requests.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Session lifecycle?

## Задача

Сделай короткую письменную практику по теме **Session lifecycle**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Session lifecycle: создать, использовать в одном unit of work, выполнить commit или rollback и закрыть.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Module-global Session переносит tracked objects и transaction failures между requests.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
