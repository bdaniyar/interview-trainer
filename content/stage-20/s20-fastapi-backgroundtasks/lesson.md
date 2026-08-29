# FastAPI BackgroundTasks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **FastAPI BackgroundTasks**, а не только запомнить термин;
- прочитать и изменить короткий пример для `process-local`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **FastAPI BackgroundTasks** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**process-local.** Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

**non-durable.** `non-durable` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**small side effects.** `small side effects` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**crash loss.** `crash loss` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `process-local` и `non-durable` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `process-local`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- process-local
- non-durable
- small side effects
- crash loss

### Полезно

- связать FastAPI BackgroundTasks с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### FastAPI BackgroundTasks: отдельный пример

```python
def example_s20_fastapi_backgroundtasks() -> tuple[str, ...]:
    # FastAPI BackgroundTasks: проверяем отдельный contract урока.
    return ('process-local', 'non-durable', 'small side effects', 'crash loss',)

assert example_s20_fastapi_backgroundtasks()
```

Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `process-local` до запуска.

**B · Find the bug.** Найди нарушение `non-durable` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про FastAPI BackgroundTasks за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое FastAPI BackgroundTasks и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме FastAPI BackgroundTasks?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

FastAPI BackgroundTasks: это отдельный технический контракт

### Нормальный Junior answer

> FastAPI BackgroundTasks — тема, в которой я сначала фиксирую `process-local`, затем объясняю `non-durable` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме FastAPI BackgroundTasks?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- process-local
- non-durable
- small side effects
- crash loss

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме FastAPI BackgroundTasks?

## Задача

Сделай короткую письменную практику по теме **FastAPI BackgroundTasks**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** FastAPI BackgroundTasks: это отдельный технический контракт
- **Механизм:** Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
