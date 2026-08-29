# Chat/WebSocket design

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Junior system design связывает HTTP, DB, cache и failure modes в практический ответ.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Chat/WebSocket design**, а не только запомнить термин;
- прочитать и изменить короткий пример для `connection`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Chat/WebSocket design** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**connection.** `connection` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**live fan-out.** `live fan-out` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**history.** `history` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**reconnect.** `reconnect` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**multi-instance delivery.** `multi-instance delivery` является компонентом system design только при наличии требования, source of truth и измеримого failure mode.

**Redis Pub/Sub limitations.** Redis Pub/Sub доставляет только активным subscribers и не является durable очередью или историей.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `connection` и `live fan-out` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `connection`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- connection
- live fan-out
- history
- reconnect

### Полезно

- multi-instance delivery
- Redis Pub/Sub limitations

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Chat/WebSocket design: отдельный пример

```text
Сценарий: Fan-out между processes.

Проверка:
Redis Pub/Sub live + PostgreSQL history.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `connection` до запуска.

**B · Find the bug.** Найди нарушение `live fan-out` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Chat/WebSocket design за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### WebSocket scale

**Сценарий:** Fan-out между processes.

**Rubric:** Redis Pub/Sub live + PostgreSQL history.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Chat/WebSocket design и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Chat/WebSocket design?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Chat/WebSocket design: это отдельный технический контракт

### Нормальный Junior answer

> Chat/WebSocket design — тема, в которой я сначала фиксирую `connection`, затем объясняю `live fan-out` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Chat/WebSocket design?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- connection
- live fan-out
- history
- reconnect

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Chat/WebSocket design?

## Задача

Сделай короткую письменную практику по теме **Chat/WebSocket design**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Chat/WebSocket design: это отдельный технический контракт
- **Механизм:** Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [PostgreSQL high availability](https://www.postgresql.org/docs/current/high-availability.html)
- [Redis architecture](https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/)

Последняя проверка версий: **2026-08-27**.
