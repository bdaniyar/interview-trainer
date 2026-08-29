# Cache placement

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Cache placement**, а не только запомнить термин;
- прочитать и изменить короткий пример для `what to cache`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Cache placement** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**what to cache.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

**TTL.** `TTL` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**invalidation.** `invalidation` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**failure fallback.** `failure fallback` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `what to cache` и `TTL` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `what to cache`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- what to cache
- TTL
- invalidation
- failure fallback

### Полезно

- связать Cache placement с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Cache placement: отдельный пример

```text
Сценарий: Где cache profile read?

Проверка:
Auth-aware key; TTL/invalidation/fallback.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `what to cache` до запуска.

**B · Find the bug.** Найди нарушение `TTL` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Cache placement за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Cache placement

**Сценарий:** Где cache profile read?

**Rubric:** Auth-aware key; TTL/invalidation/fallback.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Cache placement и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Cache placement?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Cache placement: это отдельный технический контракт

### Нормальный Junior answer

> Cache placement — тема, в которой я сначала фиксирую `what to cache`, затем объясняю `TTL` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Cache placement?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- what to cache
- TTL
- invalidation
- failure fallback

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Cache placement?

## Задача

Сделай короткую письменную практику по теме **Cache placement**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Cache placement: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
