# Redis mental model

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Redis mental model**, а не только запомнить термин;
- прочитать и изменить короткий пример для `in-memory data structure server`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Redis mental model** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**in-memory data structure server.** `in-memory data structure server` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**fast.** `fast` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**optional persistence modes.** `T | None` разрешает значение `None`, но не делает аргумент или поле необязательным без default; missing и explicit null — разные состояния.

**not a relational source of truth by default.** `not a relational source of truth by default` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `in-memory data structure server` и `fast` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `in-memory data structure server`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- in-memory data structure server
- fast
- optional persistence modes
- not a relational source of truth by default

### Полезно

- связать Redis mental model с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Redis mental model: отдельный пример

```text
SET lesson:19.1:s19_redis_mental_model value EX 60
GET lesson:19.1:s19_redis_mental_model
TTL lesson:19.1:s19_redis_mental_model
```

Определи key, value, TTL, invalidation, concurrency и outage fallback.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `in-memory data structure server` до запуска.

**B · Find the bug.** Найди нарушение `fast` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Redis mental model за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Redis mental model и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Redis mental model?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Redis mental model: это отдельный технический контракт

### Нормальный Junior answer

> Redis mental model — тема, в которой я сначала фиксирую `in-memory data structure server`, затем объясняю `fast` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Redis mental model?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- in-memory data structure server
- fast
- optional persistence modes
- not a relational source of truth by default

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Redis mental model?

## Задача

Сделай короткую письменную практику по теме **Redis mental model**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Redis mental model: это отдельный технический контракт
- **Механизм:** Для cache всегда определяй key, value, TTL, invalidation и fallback.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
