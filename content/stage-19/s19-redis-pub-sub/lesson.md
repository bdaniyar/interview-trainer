# Redis Pub/Sub

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Redis Pub/Sub**, а не только запомнить термин;
- прочитать и изменить короткий пример для `publisher`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Redis Pub/Sub** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**publisher.** `publisher` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**subscriber.** `subscriber` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**channel.** `channel` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**live delivery.** `live delivery` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**no durable history.** `no durable history` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**offline subscriber misses message.** `offline subscriber misses message` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `publisher` и `subscriber` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `publisher`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- publisher
- subscriber
- channel
- live delivery

### Полезно

- no durable history
- offline subscriber misses message

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Redis Pub/Sub: отдельный пример

```text
Сценарий: Offline WebSocket client потерял события.

Проверка:
Pub/Sub только live fan-out; durable history/read state хранить в PostgreSQL или durable stream.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `publisher` до запуска.

**B · Find the bug.** Найди нарушение `subscriber` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Redis Pub/Sub за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### PubSub as history

**Сценарий:** Offline WebSocket client потерял события.

**Rubric:** Pub/Sub только live fan-out; durable history/read state хранить в PostgreSQL или durable stream.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Redis Pub/Sub и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Redis Pub/Sub?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Redis Pub/Sub: это отдельный технический контракт

### Нормальный Junior answer

> Redis Pub/Sub — тема, в которой я сначала фиксирую `publisher`, затем объясняю `subscriber` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Redis Pub/Sub?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- publisher
- subscriber
- channel
- live delivery

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Redis Pub/Sub?

## Задача

Сделай короткую письменную практику по теме **Redis Pub/Sub**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Redis Pub/Sub: это отдельный технический контракт
- **Механизм:** Для cache всегда определяй key, value, TTL, invalidation и fallback.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
