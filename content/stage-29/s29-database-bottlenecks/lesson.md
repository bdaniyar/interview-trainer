# Database bottlenecks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Database bottlenecks**, а не только запомнить термин;
- прочитать и изменить короткий пример для `slow query`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Database bottlenecks** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**slow query.** `slow query` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**missing index.** Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.

**N+1.** N+1 возникает, когда список загружается одним query, а relationship каждого объекта — отдельным; query-count test и eager-loading делают проблему видимой.

**too many connections.** `too many connections` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**lock contention.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

**measure first.** `measure first` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `slow query` и `missing index` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `slow query`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- slow query
- missing index
- N+1
- too many connections

### Полезно

- lock contention
- measure first

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Database bottlenecks: отдельный пример

```text
Сценарий: p95 вырос, DB CPU высокий.

Проверка:
Slow queries, pool, plans, indexes, N+1.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `slow query` до запуска.

**B · Find the bug.** Найди нарушение `missing index` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Database bottlenecks за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### DB bottleneck

**Сценарий:** p95 вырос, DB CPU высокий.

**Rubric:** Slow queries, pool, plans, indexes, N+1.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Database bottlenecks и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Database bottlenecks?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Database bottlenecks: это отдельный технический контракт

### Нормальный Junior answer

> Database bottlenecks — тема, в которой я сначала фиксирую `slow query`, затем объясняю `missing index` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Database bottlenecks?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- slow query
- missing index
- N+1
- too many connections

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Database bottlenecks?

## Задача

Сделай короткую письменную практику по теме **Database bottlenecks**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Database bottlenecks: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
