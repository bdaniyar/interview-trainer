# Celery workers

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Celery workers**, а не только запомнить термин;
- прочитать и изменить короткий пример для `durable task`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Celery workers** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**durable task.** `durable task` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**broker.** `broker` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**worker.** `worker` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**transient retry.** Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.

**backoff.** `backoff` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**idempotency.** Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `durable task` и `broker` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `durable task`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- durable task
- broker
- worker
- transient retry

### Полезно

- backoff
- idempotency

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Celery workers: отдельный пример

```text
Тема: Celery workers

Фокус:
- durable task
- broker
- worker
- transient retry

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `durable task` до запуска.

**B · Find the bug.** Найди нарушение `broker` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Celery workers за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Celery workers и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Celery workers?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Celery workers: это отдельный технический контракт

### Нормальный Junior answer

> Celery workers — тема, в которой я сначала фиксирую `durable task`, затем объясняю `broker` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Celery workers?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- durable task
- broker
- worker
- transient retry

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Celery workers?

## Задача

Сделай короткую письменную практику по теме **Celery workers**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Celery workers: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
