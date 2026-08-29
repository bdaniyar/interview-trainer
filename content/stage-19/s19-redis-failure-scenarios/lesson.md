# Redis failure scenarios

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Redis failure scenarios**, а не только запомнить термин;
- прочитать и изменить короткий пример для `cache unavailable → DB fallback`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Redis failure scenarios** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**cache unavailable → DB fallback.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

**rate limiter/session behavior depends on risk.** Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

**thundering herd basics.** `thundering herd basics` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**stale values.** `stale values` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `cache unavailable → DB fallback` и `rate limiter/session behavior depends on risk` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `cache unavailable → DB fallback`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- cache unavailable → DB fallback
- rate limiter/session behavior depends on risk
- thundering herd basics
- stale values

### Полезно

- связать Redis failure scenarios с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Redis failure scenarios: отдельный пример

```text
SET lesson:19.10:s19_redis_failure_scenarios value EX 60
GET lesson:19.10:s19_redis_failure_scenarios
TTL lesson:19.10:s19_redis_failure_scenarios
```

Определи key, value, TTL, invalidation, concurrency и outage fallback.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `cache unavailable → DB fallback` до запуска.

**B · Find the bug.** Найди нарушение `rate limiter/session behavior depends on risk` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Redis failure scenarios за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Redis failure scenarios и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Redis failure scenarios?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Redis failure scenarios: это отдельный технический контракт

### Нормальный Junior answer

> Redis failure scenarios — тема, в которой я сначала фиксирую `cache unavailable → DB fallback`, затем объясняю `rate limiter/session behavior depends on risk` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Redis failure scenarios?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- cache unavailable → DB fallback
- rate limiter/session behavior depends on risk
- thundering herd basics
- stale values

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Redis failure scenarios?

## Задача

Сделай короткую письменную практику по теме **Redis failure scenarios**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Redis failure scenarios: это отдельный технический контракт
- **Механизм:** Для cache всегда определяй key, value, TTL, invalidation и fallback.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
