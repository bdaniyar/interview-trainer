# Revision, upgrade and downgrade

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Alembic защищает заявленный migration опыт и безопасные schema changes.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Revision, upgrade and downgrade**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Revision, upgrade and downgrade`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.

### Как работает

Раздели upgrade, совместимость старого/нового кода, backfill и rollback; autogenerate обязательно review.

**Revision, upgrade and downgrade.** `Revision, upgrade and downgrade` является частью versioned schema transition; безопасный вариант учитывает upgrade, deploy compatibility, backfill и rollback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Revision, upgrade and downgrade` и `Revision, upgrade and downgrade` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Revision, upgrade and downgrade`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Revision, upgrade and downgrade

### Полезно

- связать Revision, upgrade and downgrade с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Revision, upgrade and downgrade: отдельный пример

```bash
alembic revision -m "s17_revision_upgrade_and_downgrade"
# review upgrade/downgrade for: Revision, upgrade and downgrade
alembic upgrade head
```

Review migration как versioned schema transition; autogenerate — только кандидат.

## Common mistakes

### Ошибка 1

Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Revision, upgrade and downgrade` до запуска.

**B · Find the bug.** Найди нарушение `Revision, upgrade and downgrade` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Revision, upgrade and downgrade за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Revision, upgrade and downgrade и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Revision, upgrade and downgrade?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Revision, upgrade and downgrade: Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.

### Нормальный Junior answer

> Revision, upgrade and downgrade — тема, в которой я сначала фиксирую `Revision, upgrade and downgrade`, затем объясняю `Revision, upgrade and downgrade` на коротком примере. Ключевой механизм: Раздели upgrade, совместимость старого/нового кода, backfill и rollback; autogenerate обязательно review. Главная практическая ошибка — Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Revision, upgrade and downgrade?**

Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

## Expected answer rubric

### Must mention

- Revision, upgrade and downgrade

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Revision, upgrade and downgrade?

## Задача

Сделай короткую письменную практику по теме **Revision, upgrade and downgrade**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Revision, upgrade and downgrade: Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.
- **Механизм:** Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.
- **Ограничение:** Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

Последняя проверка версий: **2026-08-27**.
