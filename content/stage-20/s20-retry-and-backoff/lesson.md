# Retry and backoff

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Retry and backoff**, а не только запомнить термин;
- прочитать и изменить короткий пример для `transient vs permanent failure`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Retry and backoff** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**transient vs permanent failure.** `transient vs permanent failure` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**exponential backoff.** `exponential backoff` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**jitter.** `jitter` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**retry limit.** Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `transient vs permanent failure` и `exponential backoff` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `transient vs permanent failure`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- transient vs permanent failure
- exponential backoff
- jitter
- retry limit

### Полезно

- связать Retry and backoff с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Retry and backoff: отдельный пример

```python
def example_s20_retry_and_backoff() -> tuple[str, ...]:
    # Retry and backoff: проверяем отдельный contract урока.
    return ('transient vs permanent failure', 'exponential backoff', 'jitter', 'retry limit',)

assert example_s20_retry_and_backoff()
```

Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `transient vs permanent failure` до запуска.

**B · Find the bug.** Найди нарушение `exponential backoff` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Retry and backoff за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Retry and backoff и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Retry and backoff?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Retry and backoff: это отдельный технический контракт

### Нормальный Junior answer

> Retry and backoff — тема, в которой я сначала фиксирую `transient vs permanent failure`, затем объясняю `exponential backoff` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Retry and backoff?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- transient vs permanent failure
- exponential backoff
- jitter
- retry limit

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Retry and backoff?

## Задача

Сделай короткую письменную практику по теме **Retry and backoff**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Retry and backoff: это отдельный технический контракт
- **Механизм:** Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
