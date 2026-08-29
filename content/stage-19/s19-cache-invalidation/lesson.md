# Cache invalidation

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Cache invalidation**, а не только запомнить термин;
- прочитать и изменить короткий пример для `update/delete invalidation`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Cache invalidation** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**update/delete invalidation.** `update/delete invalidation` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**TTL.** `TTL` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**stale cache.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

**race windows.** Window function считает значение по partition, не сворачивая строки как GROUP BY; порядок внутри `OVER` задаёт frame/ranking semantics.

**versioned keys.** `versioned keys` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**GET обычно read-heavy и повторяемый.** `GET обычно read-heavy и повторяемый` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `update/delete invalidation` и `TTL` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `update/delete invalidation`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- update/delete invalidation
- TTL
- stale cache
- race windows

### Полезно

- versioned keys
- GET обычно read-heavy и повторяемый

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Cache invalidation: отдельный пример

```text
Сценарий: PUT commit успешен, GET отдаёт старое.

Проверка:
Invalidate/update after commit; key ownership, TTL, race.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `update/delete invalidation` до запуска.

**B · Find the bug.** Найди нарушение `TTL` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Cache invalidation за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Stale cache

**Сценарий:** PUT commit успешен, GET отдаёт старое.

**Rubric:** Invalidate/update after commit; key ownership, TTL, race.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Cache invalidation и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Cache invalidation?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Cache invalidation: это отдельный технический контракт

### Нормальный Junior answer

> Cache invalidation — тема, в которой я сначала фиксирую `update/delete invalidation`, затем объясняю `TTL` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Cache invalidation?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- update/delete invalidation
- TTL
- stale cache
- race windows

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Cache invalidation?

## Задача

Сделай короткую письменную практику по теме **Cache invalidation**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Cache invalidation: это отдельный технический контракт
- **Механизм:** Для cache всегда определяй key, value, TTL, invalidation и fallback.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
