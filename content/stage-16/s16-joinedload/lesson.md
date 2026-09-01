# `joinedload`

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **`joinedload`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `join`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**join.** JOIN соединяет строки по условию и может изменить cardinality; перед SELECT полезно оценить связь one-to-one/one-to-many.

**row multiplication.** `row multiplication` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**scalar relationships.** `scalar relationships` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**result uniqueness when relevant.** `result uniqueness when relevant` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `join` и `row multiplication` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `join`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- join
- row multiplication
- scalar relationships
- result uniqueness when relevant

### Полезно

- связать `joinedload` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### `joinedload`: отдельный пример

```python
def orders_with_user(Order):
    raise NotImplementedError
```

Это публичный starter contract практики «joinedload scalar». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Типичные ошибки

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `join` до запуска.

**B · Найди ошибку.** Найди нарушение `row multiplication` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про `joinedload` за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое `joinedload` и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме `joinedload`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`joinedload`: Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.

### Нормальный ответ уровня Junior

> `joinedload` — тема, в которой я сначала фиксирую `join`, затем объясняю `row multiplication` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме `joinedload`?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Критерии хорошего ответа

### Что обязательно упомянуть

- join
- row multiplication
- scalar relationships
- result uniqueness when relevant

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме `joinedload`?

## Задача

### joinedload scalar

orders_with_user(Order): joinedload(Order.user), order id.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `joinedload`: Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
