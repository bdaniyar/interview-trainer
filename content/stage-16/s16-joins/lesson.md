# Joins

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Joins**, а не только запомнить термин;
- прочитать и изменить короткий пример для `ORM joins`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**ORM joins.** JOIN соединяет строки по условию и может изменить cardinality; перед SELECT полезно оценить связь one-to-one/one-to-many.

**explicit conditions.** `explicit conditions` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**selecting entities/columns.** `SELECT` формирует result columns после FROM/JOIN/WHERE/GROUP/HAVING; порядок строк существует только при явном `ORDER BY`.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `ORM joins` и `explicit conditions` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `ORM joins`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- ORM joins
- explicit conditions
- selecting entities/columns

### Полезно

- связать Joins с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Joins: отдельный пример

```python
def orders_for_email(User, Order, email):
    raise NotImplementedError
```

Это публичный starter contract практики «ORM join». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `ORM joins` до запуска.

**B · Find the bug.** Найди нарушение `explicit conditions` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Joins за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Joins и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Joins?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Joins: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Нормальный Junior answer

> Joins — тема, в которой я сначала фиксирую `ORM joins`, затем объясняю `explicit conditions` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Joins?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Expected answer rubric

### Must mention

- ORM joins
- explicit conditions
- selecting entities/columns

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Joins?

## Задача

### ORM join

orders_for_email(User,Order,email): select Order join User, filter email, order id.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Joins: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
