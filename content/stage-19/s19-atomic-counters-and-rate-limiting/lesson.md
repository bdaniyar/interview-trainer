# Atomic counters and rate limiting

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Atomic counters and rate limiting**, а не только запомнить термин;
- прочитать и изменить короткий пример для `INCR`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Atomic counters and rate limiting** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**INCR.** `INCR` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**TTL.** `TTL` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**race-free command/script.** `race-free command/script` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**distributed instances.** `distributed instances` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `INCR` и `TTL` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `INCR`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- INCR
- TTL
- race-free command/script
- distributed instances

### Полезно

- связать Atomic counters and rate limiting с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Atomic counters and rate limiting: отдельный пример

```text
Сценарий: Два API process дают вдвое больший лимит.

Проверка:
Shared Redis counter + atomic operation/Lua, window semantics, TTL и fail-open/fail-closed policy.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `INCR` до запуска.

**B · Find the bug.** Найди нарушение `TTL` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Atomic counters and rate limiting за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Local rate limit

**Сценарий:** Два API process дают вдвое больший лимит.

**Rubric:** Shared Redis counter + atomic operation/Lua, window semantics, TTL и fail-open/fail-closed policy.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Atomic counters and rate limiting и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Atomic counters and rate limiting?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Atomic counters and rate limiting: это отдельный технический контракт

### Нормальный Junior answer

> Atomic counters and rate limiting — тема, в которой я сначала фиксирую `INCR`, затем объясняю `TTL` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Atomic counters and rate limiting?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- INCR
- TTL
- race-free command/script
- distributed instances

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Atomic counters and rate limiting?

## Задача

Сделай короткую письменную практику по теме **Atomic counters and rate limiting**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Atomic counters and rate limiting: это отдельный технический контракт
- **Механизм:** Для cache всегда определяй key, value, TTL, invalidation и fallback.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
