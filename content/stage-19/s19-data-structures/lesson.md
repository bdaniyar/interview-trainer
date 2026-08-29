# Data structures

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Redis явно встречался в 6/18 и входит в фактические проекты кандидата.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Data structures**, а не только запомнить термин;
- прочитать и изменить короткий пример для `strings`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Data structures** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**strings.** `strings` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**hashes.** Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

**lists.** `list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

**sets.** `sets` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**sorted sets.** `sorted sets` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.

**streams awareness.** `streams awareness` влияет на Redis key/value lifecycle; корректная схема заранее определяет TTL, invalidation, concurrency и outage fallback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `strings` и `hashes` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `strings`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Для cache всегда определяй key, value, TTL, invalidation и fallback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- strings
- hashes
- lists
- sets

### Полезно

- sorted sets
- streams awareness

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Data structures: отдельный пример

```text
Сценарий: profile:42 разных tenants возвращает чужие данные.

Проверка:
Key включает namespace/version/tenant/entity; authorization остаётся server-side.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `strings` до запуска.

**B · Find the bug.** Найди нарушение `hashes` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Data structures за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Cache key collision

**Сценарий:** profile:42 разных tenants возвращает чужие данные.

**Rubric:** Key включает namespace/version/tenant/entity; authorization остаётся server-side.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Data structures и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Data structures?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Data structures: это отдельный технический контракт

### Нормальный Junior answer

> Data structures — тема, в которой я сначала фиксирую `strings`, затем объясняю `hashes` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Data structures?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- strings
- hashes
- lists
- sets

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Data structures?

## Задача

Сделай короткую письменную практику по теме **Data structures**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Data structures: это отдельный технический контракт
- **Механизм:** Для cache всегда определяй key, value, TTL, invalidation и fallback.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Redis data types](https://redis.io/docs/latest/develop/data-types/)
- [Redis caching](https://redis.io/docs/latest/develop/use/client-side-caching/)

Последняя проверка версий: **2026-08-27**.
