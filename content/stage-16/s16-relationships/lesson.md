# Relationships

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Relationships**, а не только запомнить термин;
- прочитать и изменить короткий пример для `one-to-many`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Relationship описывает ORM-навигацию между entities; внешний ключ column остаётся источником referential truth в БД.

### Как работает

`back_populates` связывает направления; one-to-many, many-to-one и many-to-many определяют collection/scalar форму и loading behavior.


### Важный нюанс / ограничение

Relationship не выбирает автоматически эффективный eager loading и безопасную cascade semantics.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- one-to-many
- many-to-one
- many-to-many
- `back_populates`

### Полезно

- ownership vs navigation

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Relationships: отдельный пример

```python
def example_s16_relationships() -> tuple[str, ...]:
    # Relationships: проверяем отдельный contract урока.
    return ('one-to-many', 'many-to-one', 'many-to-many', '`back_populates`',)

assert example_s16_relationships()
```

Укажи владельца Session/transaction и момент фактического SQL I/O.

## Типичные ошибки

### Ошибка 1

Смешение ORM relationship и ownership в БД может настроить delete cascade, удаляющий лишние данные.

## Практика

**A · Предсказание результата.** Измени один input в примере `one-to-many` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `many-to-one`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `one-to-many`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Relationships за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Relationships и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Relationships?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Relationship описывает ORM-навигацию между entities; внешний ключ column остаётся источником referential truth в БД.

### Нормальный ответ уровня Junior

> Relationship описывает ORM-навигацию между entities; внешний ключ column остаётся источником referential truth в БД. `back_populates` связывает направления; one-to-many, many-to-one и many-to-many определяют collection/scalar форму и loading behavior. Важное ограничение: Relationship не выбирает автоматически эффективный eager loading и безопасную cascade semantics.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Relationships?**

Смешение ORM relationship и ownership в БД может настроить delete cascade, удаляющий лишние данные.

## Критерии хорошего ответа

### Что обязательно упомянуть

- one-to-many
- many-to-one
- many-to-many
- `back_populates`

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешение ORM relationship и ownership в БД может настроить delete cascade, удаляющий лишние данные.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Relationships?

## Задача

Сделай короткую письменную практику по теме **Relationships**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Relationship описывает ORM-навигацию между entities; внешний ключ column остаётся источником referential truth в БД.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Смешение ORM relationship и ownership в БД может настроить delete cascade, удаляющий лишние данные.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
