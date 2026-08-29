# Cache-aside

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Cache-aside**, а не только запомнить термин;
- прочитать и изменить короткий пример для `read cache`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Cache-aside** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**read cache.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

**miss → DB → cache.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

**source of truth remains DB.** `source of truth remains DB` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `read cache` и `miss → DB → cache` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `read cache`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- read cache
- miss → DB → cache
- source of truth remains DB

### Полезно

- связать Cache-aside с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Cache-aside: отдельный пример

```text
SET lesson:19.4:s19_cache_aside value EX 60
GET lesson:19.4:s19_cache_aside
TTL lesson:19.4:s19_cache_aside
```

Определи key, value, TTL, invalidation, concurrency и outage fallback.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `read cache` до запуска.

**B · Find the bug.** Найди нарушение `miss → DB → cache` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Cache-aside за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Cache-aside и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Cache-aside?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Cache-aside: это отдельный технический контракт

### Нормальный Junior answer

> Cache-aside — тема, в которой я сначала фиксирую `read cache`, затем объясняю `miss → DB → cache` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Cache-aside?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- read cache
- miss → DB → cache
- source of truth remains DB

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Cache-aside?

## Задача

Сделай короткую письменную практику по теме **Cache-aside**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Cache-aside: это отдельный технический контракт
- **Механизм:** Для cache всегда определяй key, value, TTL, invalidation и fallback.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
