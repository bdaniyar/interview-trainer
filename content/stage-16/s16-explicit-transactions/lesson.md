# Explicit transactions

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Explicit transactions**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``begin``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Explicit transaction boundary объединяет все database changes одного use case в одно решение commit или rollback.

### Как работает

`with session.begin()` делает commit при normal exit и rollback при exception; repositories не должны незаметно фиксировать отдельные части.


### Важный нюанс / ограничение

External network calls по возможности выносят за transaction, чтобы не удерживать locks и connection.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- `begin`
- atomic service operation
- избегать скрытой фиксации транзакции внутри вызовов репозитория

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Explicit transactions: отдельный пример

```python
def transfer(session, source, target, amount):
    raise NotImplementedError
```

Это публичный starter contract практики «Explicit transfer transaction». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Типичные ошибки

### Ошибка 1

Несколько скрытых commits в repository оставляют частичные данные после ошибки позднего шага.

## Практика

**A · Предсказание результата.** Измени один input в примере ``begin`` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `atomic service operation`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие ``begin``, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Explicit transactions за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Explicit transactions и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Explicit transactions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Explicit transaction boundary объединяет все database changes одного use case в одно решение commit или rollback.

### Нормальный ответ уровня Junior

> Explicit transaction boundary объединяет все database changes одного use case в одно решение commit или rollback. `with session.begin()` делает commit при normal exit и rollback при exception; repositories не должны незаметно фиксировать отдельные части. Важное ограничение: External network calls по возможности выносят за transaction, чтобы не удерживать locks и connection.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Explicit transactions?**

Несколько скрытых commits в repository оставляют частичные данные после ошибки позднего шага.

## Критерии хорошего ответа

### Что обязательно упомянуть

- `begin`
- atomic service operation
- избегать скрытой фиксации транзакции внутри вызовов репозитория

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Несколько скрытых commits в repository оставляют частичные данные после ошибки позднего шага.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Explicit transactions?

## Задача

### Explicit transfer transaction

transfer проверяет positive amount/balance и меняет два Account внутри session.begin.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Explicit transaction boundary объединяет все database changes одного use case в одно решение commit или rollback.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Несколько скрытых commits в repository оставляют частичные данные после ошибки позднего шага.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
