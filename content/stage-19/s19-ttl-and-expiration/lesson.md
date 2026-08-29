# TTL and expiration

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **TTL and expiration**, а не только запомнить термин;
- прочитать и изменить короткий пример для `expiry`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **TTL and expiration** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**expiry.** `expiry` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**renewal.** `renewal` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**stale/missing keys.** `stale/missing keys` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**memory policy awareness.** `memory policy awareness` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `expiry` и `renewal` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `expiry`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- expiry
- renewal
- stale/missing keys
- memory policy awareness

### Полезно

- связать TTL and expiration с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### TTL and expiration: отдельный пример

```text
Сценарий: Reset state навсегда остаётся в Redis.

Проверка:
Установить короткий TTL атомарно при записи и тестировать expiration policy.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `expiry` до запуска.

**B · Find the bug.** Найди нарушение `renewal` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про TTL and expiration за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Missing TTL

**Сценарий:** Reset state навсегда остаётся в Redis.

**Rubric:** Установить короткий TTL атомарно при записи и тестировать expiration policy.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое TTL and expiration и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме TTL and expiration?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

TTL and expiration: это отдельный технический контракт

### Нормальный Junior answer

> TTL and expiration — тема, в которой я сначала фиксирую `expiry`, затем объясняю `renewal` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме TTL and expiration?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- expiry
- renewal
- stale/missing keys
- memory policy awareness

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме TTL and expiration?

## Задача

Сделай короткую письменную практику по теме **TTL and expiration**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** TTL and expiration: это отдельный технический контракт
- **Механизм:** Для cache всегда определяй key, value, TTL, invalidation и fallback.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
