# Declarative models

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Declarative models**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``Mapped``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Декларативные ORM-модели сопоставляют Python classes и attributes с таблицами и columns через `Mapped` и `mapped_column` в SQLAlchemy 2.x.

### Как работает

Class metadata формирует описание schema для ORM statements и migration tooling; instances представляют rows в состоянии Session.


### Важный нюанс / ограничение

Изменение model code не мигрирует существующую production database: schema transition выполняет Alembic revision.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- `Mapped`
- `mapped_column`
- types
- primary keys

### Полезно

- constraints

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Declarative models: отдельный пример

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Создай User.
```

Это публичный starter contract практики «Declarative User model». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Типичные ошибки

### Ошибка 1

`create_all` как стратегия миграций рабочего окружения не даёт versioned и reviewable истории schema.

## Практика

**A · Предсказание результата.** Измени один input в примере ``Mapped`` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий ``mapped_column``, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие ``Mapped``, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Declarative models за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Declarative models и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Declarative models?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Декларативные ORM-модели сопоставляют Python classes и attributes с таблицами и columns через `Mapped` и `mapped_column` в SQLAlchemy 2.x.

### Нормальный ответ уровня Junior

> Декларативные ORM-модели сопоставляют Python classes и attributes с таблицами и columns через `Mapped` и `mapped_column` в SQLAlchemy 2.x. Class metadata формирует описание schema для ORM statements и migration tooling; instances представляют rows в состоянии Session. Важное ограничение: Изменение model code не мигрирует существующую production database: schema transition выполняет Alembic revision.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Declarative models?**

`create_all` как стратегия миграций рабочего окружения не даёт versioned и reviewable истории schema.

## Критерии хорошего ответа

### Что обязательно упомянуть

- `Mapped`
- `mapped_column`
- types
- primary keys

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- `create_all` как стратегия миграций рабочего окружения не даёт versioned и reviewable истории schema.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Declarative models?

## Задача

### Declarative User model

SQLAlchemy 2.x User(id,email,active): email unique+index, active default True; Mapped/mapped_column.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Декларативные ORM-модели сопоставляют Python classes и attributes с таблицами и columns через `Mapped` и `mapped_column` в SQLAlchemy 2.x.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** `create_all` как стратегия миграций рабочего окружения не даёт versioned и reviewable истории schema.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
