# WebSockets + Redis Pub/Sub

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **WebSockets + Redis Pub/Sub**, а не только запомнить термин;
- прочитать и изменить короткий пример для `WebSocket connects client to one process`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **WebSockets + Redis Pub/Sub** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**WebSocket connects client to one process.** WebSocket держит долгоживущее соединение; масштабирование требует shared fan-out, а durable history хранится отдельно.

**Pub/Sub distributes live events between instances.** Redis Pub/Sub доставляет только активным subscribers и не является durable очередью или историей.

**API instances fan out to local clients.** `API instances fan out to local clients` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `WebSocket connects client to one process` и `Pub/Sub distributes live events between instances` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `WebSocket connects client to one process`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- WebSocket connects client to one process
- Pub/Sub distributes live events between instances
- API instances fan out to local clients

### Полезно

- связать WebSockets + Redis Pub/Sub с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### WebSockets + Redis Pub/Sub: отдельный пример

```text
Сценарий: Cross-instance flow.

Проверка:
Persist, publish, fan-out; offline reads DB.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `WebSocket connects client to one process` до запуска.

**B · Find the bug.** Найди нарушение `Pub/Sub distributes live events between instances` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про WebSockets + Redis Pub/Sub за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### WebSocket Pub/Sub

**Сценарий:** Cross-instance flow.

**Rubric:** Persist, publish, fan-out; offline reads DB.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое WebSockets + Redis Pub/Sub и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме WebSockets + Redis Pub/Sub?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

WebSockets + Redis Pub/Sub: это отдельный технический контракт

### Нормальный Junior answer

> WebSockets + Redis Pub/Sub — тема, в которой я сначала фиксирую `WebSocket connects client to one process`, затем объясняю `Pub/Sub distributes live events between instances` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме WebSockets + Redis Pub/Sub?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- WebSocket connects client to one process
- Pub/Sub distributes live events between instances
- API instances fan out to local clients

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме WebSockets + Redis Pub/Sub?

## Задача

Сделай короткую письменную практику по теме **WebSockets + Redis Pub/Sub**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** WebSockets + Redis Pub/Sub: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
