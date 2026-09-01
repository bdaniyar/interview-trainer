# Rollback

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Rollback**, а не только запомнить термин;
- прочитать и изменить короткий пример для `failed transaction state`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Rollback отменяет текущую database transaction и обязателен перед повторным использованием Session после flush или commit error.

### Как работает

SQLAlchemy помечает transaction как failed; перехват `IntegrityError` без rollback оставляет дальнейшие операции нерабочими.


### Важный нюанс / ограничение

После rollback известный constraint conflict переводят в domain error, а неожиданный сбой поднимают с исходной причиной.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- failed transaction state
- rollback before reuse
- exception boundary

### Полезно

- один короткий пример кода с результатом

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Rollback: отдельный пример

```text
Сценарий: После IntegrityError новые queries падают.

Проверка:
Rollback failed transaction before reuse.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Query сразу после IntegrityError без rollback вызывает pending-rollback error и скрывает исходный conflict.

## Практика

**A · Предсказание результата.** Измени один input в примере `failed transaction state` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `rollback before reuse`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `failed transaction state`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Rollback за 45–60 секунд и назови одно ограничение.

## Практика: Отладка

### Failed session

**Сценарий:** После IntegrityError новые queries падают.

**Критерии ответа:** Rollback failed transaction before reuse.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Rollback и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Rollback?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Rollback отменяет текущую database transaction и обязателен перед повторным использованием Session после flush или commit error.

### Нормальный ответ уровня Junior

> Rollback отменяет текущую database transaction и обязателен перед повторным использованием Session после flush или commit error. SQLAlchemy помечает transaction как failed; перехват `IntegrityError` без rollback оставляет дальнейшие операции нерабочими. Важное ограничение: После rollback известный constraint conflict переводят в domain error, а неожиданный сбой поднимают с исходной причиной.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Rollback?**

Query сразу после IntegrityError без rollback вызывает pending-rollback error и скрывает исходный conflict.

## Критерии хорошего ответа

### Что обязательно упомянуть

- failed transaction state
- rollback before reuse
- exception boundary

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Query сразу после IntegrityError без rollback вызывает pending-rollback error и скрывает исходный conflict.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Rollback?

## Задача

### Rollback failed unit of work

persist делает add+commit; на любой Exception rollback и re-raise.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Rollback отменяет текущую database transaction и обязателен перед повторным использованием Session после flush или commit error.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Query сразу после IntegrityError без rollback вызывает pending-rollback error и скрывает исходный conflict.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
