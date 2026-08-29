# Add, flush, commit and refresh

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Add, flush, commit and refresh**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``add``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`add` attaches a new entity, `flush` emits pending SQL inside the transaction, `commit` finalizes it and `refresh` reloads current DB values.

### Как работает

Autoflush may run before a query; generated primary keys often become available after flush without commit.


### Важный нюанс / limitation

After commit objects may be expired depending on configuration; refresh is not a substitute for correct transaction ownership.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `add`
- `flush` sends SQL inside transaction
- `commit` finalizes
- `refresh` reloads

### Полезно

- generated ID may appear after flush

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Add, flush, commit and refresh: отдельный пример

```text
Сценарий: repository.save неожиданно commit-ит половину use case.

Проверка:
Transaction boundary принадлежит service/use case; repository делает add/flush, caller решает commit/rollback.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Committing only to obtain an id breaks atomic use cases; flush is sufficient inside the still-open transaction.

## Practice

**A · Code/result prediction.** Change one input in the ``add`` example and predict the result before running it.

**B · Find the bug.** Find code that violates ``flush` sends SQL inside transaction` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates ``add`` and add one edge-case test.

**E · Interview explanation.** Explain Add, flush, commit and refresh in 45–60 seconds and include one limitation.

## Debugging practice

### Commit in repository

**Сценарий:** repository.save неожиданно commit-ит половину use case.

**Rubric:** Transaction boundary принадлежит service/use case; repository делает add/flush, caller решает commit/rollback.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Add, flush, commit and refresh и как это работает?

### Follow-up

Какая типичная ошибка связана с Add, flush, commit and refresh?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`add` attaches a new entity, `flush` emits pending SQL inside the transaction, `commit` finalizes it and `refresh` reloads current DB values.

### Нормальный Junior answer

> `add` attaches a new entity, `flush` emits pending SQL inside the transaction, `commit` finalizes it and `refresh` reloads current DB values. Autoflush may run before a query; generated primary keys often become available after flush without commit. Важное ограничение: After commit objects may be expired depending on configuration; refresh is not a substitute for correct transaction ownership.

### Углубление / follow-up

**Какая типичная ошибка связана с Add, flush, commit and refresh?**

Committing only to obtain an id breaks atomic use cases; flush is sufficient inside the still-open transaction.

## Expected answer rubric

### Must mention

- `add`
- `flush` sends SQL inside transaction
- `commit` finalizes
- `refresh` reloads

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Committing only to obtain an id breaks atomic use cases; flush is sufficient inside the still-open transaction.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Add, flush, commit and refresh?

## Задача

### Flush generated id

add_and_flush делает add+flush и возвращает entity; commit запрещён.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `add` attaches a new entity, `flush` emits pending SQL inside the transaction, `commit` finalizes it and `refresh` reloads current DB values.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Committing only to obtain an id breaks atomic use cases; flush is sufficient inside the still-open transaction.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
