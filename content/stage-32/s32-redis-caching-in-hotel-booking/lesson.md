# Redis caching in Hotel Booking

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Redis caching in Hotel Booking**, а не только запомнить термин;
- прочитать и изменить короткий пример для `exact cached read`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Redis caching in Hotel Booking** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**exact cached read.** Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug.

**key.** `key` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**TTL.** `TTL` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**invalidation trigger.** `invalidation trigger` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**fallback.** `fallback` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `exact cached read` и `key` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `exact cached read`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- exact cached read
- key
- TTL
- invalidation trigger

### Полезно

- fallback

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Redis caching in Hotel Booking: отдельный пример

```text
Тема: Redis caching in Hotel Booking

Фокус:
- exact cached read
- key
- TTL
- invalidation trigger

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `exact cached read` до запуска.

**B · Find the bug.** Найди нарушение `key` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Redis caching in Hotel Booking за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Redis caching in Hotel Booking и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Redis caching in Hotel Booking?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Redis caching in Hotel Booking: это отдельный технический контракт

### Нормальный Junior answer

> Redis caching in Hotel Booking — тема, в которой я сначала фиксирую `exact cached read`, затем объясняю `key` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Redis caching in Hotel Booking?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- exact cached read
- key
- TTL
- invalidation trigger

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Redis caching in Hotel Booking?

## Задача

Сделай короткую письменную практику по теме **Redis caching in Hotel Booking**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Redis caching in Hotel Booking: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
