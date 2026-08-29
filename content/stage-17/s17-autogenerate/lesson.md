# Autogenerate

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Alembic защищает заявленный migration опыт и безопасные schema changes.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Autogenerate**, а не только запомнить термин;
- прочитать и изменить короткий пример для `generated diff is a draft`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.

### Как работает

Раздели upgrade, совместимость старого/нового кода, backfill и rollback; autogenerate обязательно review.

**generated diff is a draft.** `generated diff is a draft` является частью versioned schema transition; безопасный вариант учитывает upgrade, deploy compatibility, backfill и rollback.

**manual review.** `manual review` является частью versioned schema transition; безопасный вариант учитывает upgrade, deploy compatibility, backfill и rollback.

**rename may look like drop/add.** `rename may look like drop/add` является частью versioned schema transition; безопасный вариант учитывает upgrade, deploy compatibility, backfill и rollback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `generated diff is a draft` и `manual review` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `generated diff is a draft`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- generated diff is a draft
- manual review
- rename may look like drop/add

### Полезно

- связать Autogenerate с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Autogenerate: отдельный пример

```python
def unsafe_operations(operations):
    raise NotImplementedError
```

Это публичный starter contract практики «Review autogenerate». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `generated diff is a draft` до запуска.

**B · Find the bug.** Найди нарушение `manual review` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Autogenerate за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Autogenerate и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Autogenerate?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Autogenerate: Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.

### Нормальный Junior answer

> Autogenerate — тема, в которой я сначала фиксирую `generated diff is a draft`, затем объясняю `manual review` на коротком примере. Ключевой механизм: Раздели upgrade, совместимость старого/нового кода, backfill и rollback; autogenerate обязательно review. Главная практическая ошибка — Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Autogenerate?**

Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.

## Expected answer rubric

### Must mention

- generated diff is a draft
- manual review
- rename may look like drop/add

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Autogenerate?

## Задача

### Review autogenerate

unsafe_operations возвращает DROP/DELETE/SET NOT NULL/nullable=false operations без изменения порядка.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Autogenerate: Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.
- **Механизм:** Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.
- **Ограничение:** Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

Последняя проверка версий: **2026-08-27**.
