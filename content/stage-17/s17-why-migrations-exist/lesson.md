# Why migrations exist

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Alembic защищает заявленный migration опыт и безопасные schema changes.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Why migrations exist**, а не только запомнить термин;
- прочитать и изменить короткий пример для `model code does not update an existing DB`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A migration is a versioned, reviewable transition of an existing database schema/data; changing ORM model code alone does not update deployed databases.

### Как работает

Alembic revisions define upgrade/downgrade steps and form an ordered history applied consistently across environments.


### Важный нюанс / limitation

Schema changes must stay compatible with old/new application versions during rolling deploys.

## Mental model

Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- model code does not update an existing DB
- versioned schema history

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Why migrations exist: отдельный пример

```bash
alembic revision -m "s17_why_migrations_exist"
# review upgrade/downgrade for: model code does not update an existing DB, versioned schema history
alembic upgrade head
```

Review migration как versioned schema transition; autogenerate — только кандидат.

## Common mistakes

### Ошибка 1

Running `create_all` on startup cannot safely express rename, backfill or staged constraint changes.

## Practice

**A · Code/result prediction.** Change one input in the `model code does not update an existing DB` example and predict the result before running it.

**B · Find the bug.** Find code that violates `versioned schema history` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `model code does not update an existing DB` and add one edge-case test.

**E · Interview explanation.** Explain Why migrations exist in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Why migrations exist и как это работает?

### Follow-up

Какая типичная ошибка связана с Why migrations exist?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A migration is a versioned, reviewable transition of an existing database schema/data; changing ORM model code alone does not update deployed databases.

### Нормальный Junior answer

> A migration is a versioned, reviewable transition of an existing database schema/data; changing ORM model code alone does not update deployed databases. Alembic revisions define upgrade/downgrade steps and form an ordered history applied consistently across environments. Важное ограничение: Schema changes must stay compatible with old/new application versions during rolling deploys.

### Углубление / follow-up

**Какая типичная ошибка связана с Why migrations exist?**

Running `create_all` on startup cannot safely express rename, backfill or staged constraint changes.

## Expected answer rubric

### Must mention

- model code does not update an existing DB
- versioned schema history

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Running `create_all` on startup cannot safely express rename, backfill or staged constraint changes.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Why migrations exist?

## Задача

Сделай короткую письменную практику по теме **Why migrations exist**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A migration is a versioned, reviewable transition of an existing database schema/data; changing ORM model code alone does not update deployed databases.
- **Механизм:** Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.
- **Ограничение:** Running `create_all` on startup cannot safely express rename, backfill or staged constraint changes.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

Последняя проверка версий: **2026-08-27**.
