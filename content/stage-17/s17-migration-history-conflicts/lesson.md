# Migration history conflicts

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Alembic защищает заявленный migration опыт и безопасные schema changes.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Migration history conflicts**, а не только запомнить термин;
- прочитать и изменить короткий пример для `multiple heads`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.

### Как работает

Раздели upgrade, совместимость старого/нового кода, backfill и rollback; autogenerate обязательно review.

**multiple heads.** `multiple heads` является частью versioned schema transition; безопасный вариант учитывает upgrade, deploy compatibility, backfill и rollback.

**merge revision.** `merge revision` является частью versioned schema transition; безопасный вариант учитывает upgrade, deploy compatibility, backfill и rollback.

**team workflow.** `team workflow` является частью versioned schema transition; безопасный вариант учитывает upgrade, deploy compatibility, backfill и rollback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `multiple heads` и `merge revision` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `multiple heads`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- multiple heads
- merge revision
- team workflow

### Полезно

- связать Migration history conflicts с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Migration history conflicts: отдельный пример

```bash
alembic revision -m "s17_migration_history_conflicts"
# review upgrade/downgrade for: multiple heads, merge revision, team workflow
alembic upgrade head
```

Review migration как versioned schema transition; autogenerate — только кандидат.

## Common mistakes

### Ошибка 1

Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `multiple heads` до запуска.

**B · Find the bug.** Найди нарушение `merge revision` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Migration history conflicts за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Migration history conflicts и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Migration history conflicts?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Migration history conflicts: Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.

### Нормальный Junior answer

> Migration history conflicts — тема, в которой я сначала фиксирую `multiple heads`, затем объясняю `merge revision` на коротком примере. Ключевой механизм: Раздели upgrade, совместимость старого/нового кода, backfill и rollback; autogenerate обязательно review. Главная практическая ошибка — Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Migration history conflicts?**

Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

## Expected answer rubric

### Must mention

- multiple heads
- merge revision
- team workflow

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Migration history conflicts?

## Задача

Сделай короткую письменную практику по теме **Migration history conflicts**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Migration history conflicts: Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.
- **Механизм:** Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.
- **Ограничение:** Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

Последняя проверка версий: **2026-08-27**.
