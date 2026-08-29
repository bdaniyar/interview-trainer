# Booking endpoint

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Booking endpoint**, а не только запомнить термин;
- прочитать и изменить короткий пример для `availability check`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Booking endpoint** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**availability check.** `availability check` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**transaction.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**DB invariant.** `DB invariant` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**concurrent requests.** `concurrent requests` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**idempotency.** Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.

**conflict response.** `conflict response` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `availability check` и `transaction` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `availability check`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- availability check
- transaction
- DB invariant
- concurrent requests

### Полезно

- idempotency
- conflict response

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Booking endpoint: отдельный пример

```text
Сценарий: Спроектируй POST booking.

Проверка:
Validation, auth, transaction, 201/409, idempotency.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `availability check` до запуска.

**B · Find the bug.** Найди нарушение `transaction` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Booking endpoint за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Booking endpoint

**Сценарий:** Спроектируй POST booking.

**Rubric:** Validation, auth, transaction, 201/409, idempotency.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Booking endpoint и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Booking endpoint?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Booking endpoint: это отдельный технический контракт

### Нормальный Junior answer

> Booking endpoint — тема, в которой я сначала фиксирую `availability check`, затем объясняю `transaction` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Booking endpoint?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- availability check
- transaction
- DB invariant
- concurrent requests

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Booking endpoint?

## Задача

Сделай короткую письменную практику по теме **Booking endpoint**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Booking endpoint: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
