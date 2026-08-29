# Celery model

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Celery model**, а не только запомнить термин;
- прочитать и изменить короткий пример для `task`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Celery model** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**task.** `task` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**broker.** `broker` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**worker.** `worker` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**result backend distinction.** `result backend distinction` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**serialization.** `serialization` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**retries.** `retries` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `task` и `broker` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `task`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- task
- broker
- worker
- result backend distinction

### Полезно

- serialization
- retries

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Celery model: отдельный пример

```python
def example_s20_celery_model() -> tuple[str, ...]:
    # Celery model: проверяем отдельный contract урока.
    return ('task', 'broker', 'worker', 'result backend distinction',)

assert example_s20_celery_model()
```

Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `task` до запуска.

**B · Find the bug.** Найди нарушение `broker` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Celery model за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Celery model и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Celery model?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Celery model: это отдельный технический контракт

### Нормальный Junior answer

> Celery model — тема, в которой я сначала фиксирую `task`, затем объясняю `broker` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Celery model?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- task
- broker
- worker
- result backend distinction

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Celery model?

## Задача

Сделай короткую письменную практику по теме **Celery model**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Celery model: это отдельный технический контракт
- **Механизм:** Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
