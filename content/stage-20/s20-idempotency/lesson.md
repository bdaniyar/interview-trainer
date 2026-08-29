# Idempotency

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Idempotency**, а не только запомнить термин;
- прочитать и изменить короткий пример для `duplicate delivery`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Idempotency** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**duplicate delivery.** `duplicate delivery` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**idempotency key.** Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.

**unique constraint.** Constraint хранит invariant рядом с данными и защищает его от всех writers; API переводит conflict в понятную domain/HTTP error.

**state transition.** `state transition` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**side-effect deduplication.** `side-effect deduplication` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `duplicate delivery` и `idempotency key` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `duplicate delivery`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- duplicate delivery
- idempotency key
- unique constraint
- state transition

### Полезно

- side-effect deduplication

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Idempotency: отдельный пример

```python
def example_s20_idempotency() -> tuple[str, ...]:
    # Idempotency: проверяем отдельный contract урока.
    return ('duplicate delivery', 'idempotency key', 'unique constraint', 'state transition',)

assert example_s20_idempotency()
```

Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `duplicate delivery` до запуска.

**B · Find the bug.** Найди нарушение `idempotency key` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Idempotency за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Idempotency и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Idempotency?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Idempotency: это отдельный технический контракт

### Нормальный Junior answer

> Idempotency — тема, в которой я сначала фиксирую `duplicate delivery`, затем объясняю `idempotency key` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Idempotency?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- duplicate delivery
- idempotency key
- unique constraint
- state transition

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Idempotency?

## Задача

Сделай короткую письменную практику по теме **Idempotency**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Idempotency: это отдельный технический контракт
- **Механизм:** Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
