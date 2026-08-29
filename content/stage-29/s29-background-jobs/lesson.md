# Background jobs

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Background jobs**, а не только запомнить термин;
- прочитать и изменить короткий пример для `latency`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Background jobs** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**latency.** `latency` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**durability.** `durability` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**retries.** `retries` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**idempotency.** Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `latency` и `durability` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `latency`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- latency
- durability
- retries
- idempotency

### Полезно

- связать Background jobs с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Background jobs: отдельный пример

```text
Сценарий: Email без latency/loss.

Проверка:
Outbox/durable queue, retry, idempotency.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `latency` до запуска.

**B · Find the bug.** Найди нарушение `durability` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Background jobs за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Background email

**Сценарий:** Email без latency/loss.

**Rubric:** Outbox/durable queue, retry, idempotency.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Background jobs и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Background jobs?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Background jobs: это отдельный технический контракт

### Нормальный Junior answer

> Background jobs — тема, в которой я сначала фиксирую `latency`, затем объясняю `durability` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Background jobs?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- latency
- durability
- retries
- idempotency

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Background jobs?

## Задача

Сделай короткую письменную практику по теме **Background jobs**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Background jobs: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
