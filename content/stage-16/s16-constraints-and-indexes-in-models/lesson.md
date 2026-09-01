# Constraints and indexes in models

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Constraints and indexes in models**, а не только запомнить термин;
- прочитать и изменить короткий пример для `DB migration still required`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**DB migration still required.** `DB migration still required` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**объявление модели не является миграцией рабочей схемы базы данных.** `model declaration is not production schema migration` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `DB migration still required` и `model declaration is not production schema migration` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `DB migration still required`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- DB migration still required
- объявление модели не является миграцией рабочей схемы базы данных

### Полезно

- связать Constraints and indexes in models с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Constraints and indexes in models: отдельный пример

```python
def example_s16_constraints_and_indexes_in_models() -> tuple[str, ...]:
    # Constraints and indexes in models: проверяем отдельный contract урока.
    return ('DB migration still required', 'model declaration is not production schema migration',)

assert example_s16_constraints_and_indexes_in_models()
```

Укажи владельца Session/transaction и момент фактического SQL I/O.

## Типичные ошибки

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `DB migration still required` до запуска.

**B · Найди ошибку.** Найди нарушение `model declaration is not production schema migration` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Constraints and indexes in models за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Constraints and indexes in models и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Constraints and indexes in models?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Constraints and indexes in models: Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.

### Нормальный ответ уровня Junior

> Constraints and indexes in models — тема, в которой я сначала фиксирую `DB migration still required`, затем объясняю `model declaration is not production schema migration` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Constraints and indexes in models?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Критерии хорошего ответа

### Что обязательно упомянуть

- DB migration still required
- объявление модели не является миграцией рабочей схемы базы данных

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Constraints and indexes in models?

## Задача

Сделай короткую письменную практику по теме **Constraints and indexes in models**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Constraints and indexes in models: Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
