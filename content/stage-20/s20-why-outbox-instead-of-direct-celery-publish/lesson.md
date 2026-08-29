# Why outbox instead of direct Celery publish

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Why outbox instead of direct Celery publish**, а не только запомнить термин;
- прочитать и изменить короткий пример для `publish after commit can be lost`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Why outbox instead of direct Celery publish** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**publish after commit can be lost.** `publish after commit can be lost` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**publish before commit can observe rolled-back state.** `publish before commit can observe rolled-back state` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**outbox closes atomicity gap.** `outbox closes atomicity gap` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**Celery may still be delivery/execution layer.** `Celery may still be delivery/execution layer` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `publish after commit can be lost` и `publish before commit can observe rolled-back state` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `publish after commit can be lost`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- publish after commit can be lost
- publish before commit can observe rolled-back state
- outbox closes atomicity gap
- Celery may still be delivery/execution layer

### Полезно

- связать Why outbox instead of direct Celery publish с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Why outbox instead of direct Celery publish: отдельный пример

```python
def example_s20_why_outbox_instead_of_direct_celery_publish() -> tuple[str, ...]:
    # Why outbox instead of direct Celery publish: проверяем отдельный contract урока.
    return ('publish after commit can be lost', 'publish before commit can observe rolled-back state', 'outbox closes atomicity gap', 'Celery may still be delivery/execution layer',)

assert example_s20_why_outbox_instead_of_direct_celery_publish()
```

Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `publish after commit can be lost` до запуска.

**B · Find the bug.** Найди нарушение `publish before commit can observe rolled-back state` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Why outbox instead of direct Celery publish за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Why outbox instead of direct Celery publish и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Why outbox instead of direct Celery publish?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Why outbox instead of direct Celery publish: это отдельный технический контракт

### Нормальный Junior answer

> Why outbox instead of direct Celery publish — тема, в которой я сначала фиксирую `publish after commit can be lost`, затем объясняю `publish before commit can observe rolled-back state` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Why outbox instead of direct Celery publish?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- publish after commit can be lost
- publish before commit can observe rolled-back state
- outbox closes atomicity gap
- Celery may still be delivery/execution layer

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Why outbox instead of direct Celery publish?

## Задача

Сделай короткую письменную практику по теме **Why outbox instead of direct Celery publish**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Why outbox instead of direct Celery publish: это отдельный технический контракт
- **Механизм:** Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
