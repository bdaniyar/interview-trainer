# In-request vs background work

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Background work/outbox/Celery нужны для защиты фактических project claims; broker depth ниже core.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **In-request vs background work**, а не только запомнить термин;
- прочитать и изменить короткий пример для `latency`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Тема **In-request vs background work** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы сценарий ошибки.

**latency.** `latency` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**reliability.** `reliability` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**user-visible result.** `user-visible result` является этапом delivery от DB commit до side effect, где возможны duplicate, retry и idempotency requirements.

**retry.** Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.

**transaction boundary.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `latency` и `reliability` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `latency`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- latency
- reliability
- user-visible result
- retry

### Полезно

- transaction boundary

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### In-request vs background work: отдельный пример

```python
def example_s20_in_request_vs_background_work() -> tuple[str, ...]:
    # In-request vs background work: проверяем отдельный contract урока.
    return ('latency', 'reliability', 'user-visible result', 'retry',)

assert example_s20_in_request_vs_background_work()
```

Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.

## Типичные ошибки

### Ошибка 1

Игнорировать ограничение механизма и проверять только основной сценарий.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `latency` до запуска.

**B · Найди ошибку.** Найди нарушение `reliability` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про In-request vs background work за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое In-request vs background work и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме In-request vs background work?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

In-request vs background work: это отдельный технический контракт

### Нормальный ответ уровня Junior

> In-request vs background work — тема, в которой я сначала фиксирую `latency`, затем объясняю `reliability` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме In-request vs background work?**

Нужно назвать конкретный сценарий ошибки и способ его проверить.

## Критерии хорошего ответа

### Что обязательно упомянуть

- latency
- reliability
- user-visible result
- retry

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Игнорировать ограничение механизма и проверять только основной сценарий.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме In-request vs background work?

## Задача

Сделай короткую письменную практику по теме **In-request vs background work**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** In-request vs background work: это отдельный технический контракт
- **Механизм:** Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.
- **Ограничение:** Игнорировать ограничение механизма и проверять только основной сценарий.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Celery tasks](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Kafka concepts](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

Последняя проверка версий: **2026-08-27**.
