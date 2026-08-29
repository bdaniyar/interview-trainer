# Why Pub/Sub is not storage

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Why Pub/Sub is not storage**, а не только запомнить термин;
- прочитать и изменить короткий пример для `offline subscribers miss events`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Why Pub/Sub is not storage** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**offline subscribers miss events.** `offline subscribers miss events` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**no durable history.** `no durable history` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**no acknowledgement/replay.** `no acknowledgement/replay` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**history stored in PostgreSQL.** `history stored in PostgreSQL` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**reconnect fetches missed messages.** `reconnect fetches missed messages` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `offline subscribers miss events` и `no durable history` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `offline subscribers miss events`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- offline subscribers miss events
- no durable history
- no acknowledgement/replay
- history stored in PostgreSQL

### Полезно

- reconnect fetches missed messages

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Why Pub/Sub is not storage: отдельный пример

```text
Тема: Why Pub/Sub is not storage

Фокус:
- offline subscribers miss events
- no durable history
- no acknowledgement/replay
- history stored in PostgreSQL

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `offline subscribers miss events` до запуска.

**B · Find the bug.** Найди нарушение `no durable history` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Why Pub/Sub is not storage за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Why Pub/Sub is not storage и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Why Pub/Sub is not storage?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Why Pub/Sub is not storage: это отдельный технический контракт

### Нормальный Junior answer

> Why Pub/Sub is not storage — тема, в которой я сначала фиксирую `offline subscribers miss events`, затем объясняю `no durable history` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Why Pub/Sub is not storage?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- offline subscribers miss events
- no durable history
- no acknowledgement/replay
- history stored in PostgreSQL

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Why Pub/Sub is not storage?

## Задача

Сделай короткую письменную практику по теме **Why Pub/Sub is not storage**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Why Pub/Sub is not storage: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
