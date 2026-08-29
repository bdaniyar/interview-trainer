# Outbox pattern

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Outbox pattern**, а не только запомнить термин;
- прочитать и изменить короткий пример для `business row + outbox row in one DB transaction`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Outbox pattern** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**business row + outbox row in one DB transaction.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**worker.** `worker` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**at-least-once.** `at-least-once` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**retry.** Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.

**idempotent consumer.** Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.

**dual-write problem.** `dual-write problem` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `business row + outbox row in one DB transaction` и `worker` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `business row + outbox row in one DB transaction`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- business row + outbox row in one DB transaction
- worker
- at-least-once
- retry

### Полезно

- idempotent consumer
- dual-write problem

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Outbox pattern: отдельный пример

```python
def example_s20_outbox_pattern() -> tuple[str, ...]:
    # Outbox pattern: проверяем отдельный contract урока.
    return ('business row + outbox row in one DB transaction', 'worker', 'at-least-once', 'retry',)

assert example_s20_outbox_pattern()
```

Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `business row + outbox row in one DB transaction` до запуска.

**B · Find the bug.** Найди нарушение `worker` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Outbox pattern за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Outbox pattern и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Outbox pattern?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Outbox pattern: это отдельный технический контракт

### Нормальный Junior answer

> Outbox pattern — тема, в которой я сначала фиксирую `business row + outbox row in one DB transaction`, затем объясняю `worker` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Outbox pattern?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- business row + outbox row in one DB transaction
- worker
- at-least-once
- retry

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Outbox pattern?

## Задача

Сделай короткую письменную практику по теме **Outbox pattern**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Outbox pattern: это отдельный технический контракт
- **Механизм:** Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
