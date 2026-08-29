# Outbox design

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Outbox design**, а не только запомнить термин;
- прочитать и изменить короткий пример для `atomic write`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Outbox design** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**atomic write.** `atomic write` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**worker claim.** `worker claim` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**retry.** Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.

**idempotency.** Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.

**locking.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `atomic write` и `worker claim` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `atomic write`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- atomic write
- worker claim
- retry
- idempotency

### Полезно

- locking

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Outbox design: отдельный пример

```text
Сценарий: Commit прошёл, publish упал.

Проверка:
Same transaction outbox; retry/idempotency.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `atomic write` до запуска.

**B · Find the bug.** Найди нарушение `worker claim` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Outbox design за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Outbox

**Сценарий:** Commit прошёл, publish упал.

**Rubric:** Same transaction outbox; retry/idempotency.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Outbox design и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Outbox design?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Outbox design: это отдельный технический контракт

### Нормальный Junior answer

> Outbox design — тема, в которой я сначала фиксирую `atomic write`, затем объясняю `worker claim` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Outbox design?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- atomic write
- worker claim
- retry
- idempotency

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Outbox design?

## Задача

Сделай короткую письменную практику по теме **Outbox design**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Outbox design: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
