# Rollback

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Rollback**, а не только запомнить термин;
- прочитать и изменить короткий пример для `failed transaction state`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Rollback cancels the current database transaction and is required before reusing a Session after a flush/commit error.

### Как работает

SQLAlchemy marks the failed transaction state; catching IntegrityError without rollback leaves later operations failing.


### Важный нюанс / limitation

Translate known constraint conflicts after rollback and re-raise unexpected failures with their cause/context.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- failed transaction state
- rollback before reuse
- exception boundary

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Rollback: отдельный пример

```text
Сценарий: После IntegrityError новые queries падают.

Проверка:
Rollback failed transaction before reuse.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Continuing queries immediately after IntegrityError produces a pending-rollback error and obscures the original conflict.

## Practice

**A · Code/result prediction.** Change one input in the `failed transaction state` example and predict the result before running it.

**B · Find the bug.** Find code that violates `rollback before reuse` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `failed transaction state` and add one edge-case test.

**E · Interview explanation.** Explain Rollback in 45–60 seconds and include one limitation.

## Debugging practice

### Failed session

**Сценарий:** После IntegrityError новые queries падают.

**Rubric:** Rollback failed transaction before reuse.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Rollback и как это работает?

### Follow-up

Какая типичная ошибка связана с Rollback?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Rollback cancels the current database transaction and is required before reusing a Session after a flush/commit error.

### Нормальный Junior answer

> Rollback cancels the current database transaction and is required before reusing a Session after a flush/commit error. SQLAlchemy marks the failed transaction state; catching IntegrityError without rollback leaves later operations failing. Важное ограничение: Translate known constraint conflicts after rollback and re-raise unexpected failures with their cause/context.

### Углубление / follow-up

**Какая типичная ошибка связана с Rollback?**

Continuing queries immediately after IntegrityError produces a pending-rollback error and obscures the original conflict.

## Expected answer rubric

### Must mention

- failed transaction state
- rollback before reuse
- exception boundary

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Continuing queries immediately after IntegrityError produces a pending-rollback error and obscures the original conflict.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Rollback?

## Задача

### Rollback failed unit of work

persist делает add+commit; на любой Exception rollback и re-raise.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Rollback cancels the current database transaction and is required before reusing a Session after a flush/commit error.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Continuing queries immediately after IntegrityError produces a pending-rollback error and obscures the original conflict.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
