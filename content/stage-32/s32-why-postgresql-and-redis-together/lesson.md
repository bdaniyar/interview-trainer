# Why PostgreSQL and Redis together?

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Why PostgreSQL and Redis together?**, а не только запомнить термин;
- прочитать и изменить короткий пример для `PostgreSQL source of truth`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Why PostgreSQL and Redis together?** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**PostgreSQL source of truth.** `PostgreSQL source of truth` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**Redis ephemeral acceleration/coordination.** Redis хранит данные в памяти и полезен для cache/TTL/atomic counters, но durability, eviction и outage policy нужно проектировать явно.

**durable state survives Redis loss.** Redis хранит данные в памяти и полезен для cache/TTL/atomic counters, но durability, eviction и outage policy нужно проектировать явно.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `PostgreSQL source of truth` и `Redis ephemeral acceleration/coordination` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `PostgreSQL source of truth`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- PostgreSQL source of truth
- Redis ephemeral acceleration/coordination
- durable state survives Redis loss

### Полезно

- связать Why PostgreSQL and Redis together? с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Why PostgreSQL and Redis together?: отдельный пример

```text
Сценарий: Почему оба?

Проверка:
Durable truth vs cache/temp/fan-out.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `PostgreSQL source of truth` до запуска.

**B · Find the bug.** Найди нарушение `Redis ephemeral acceleration/coordination` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Why PostgreSQL and Redis together? за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### PostgreSQL plus Redis

**Сценарий:** Почему оба?

**Rubric:** Durable truth vs cache/temp/fan-out.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Why PostgreSQL and Redis together? и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Why PostgreSQL and Redis together??

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Why PostgreSQL and Redis together?: это отдельный технический контракт

### Нормальный Junior answer

> Why PostgreSQL and Redis together? — тема, в которой я сначала фиксирую `PostgreSQL source of truth`, затем объясняю `Redis ephemeral acceleration/coordination` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Why PostgreSQL and Redis together??**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- PostgreSQL source of truth
- Redis ephemeral acceleration/coordination
- durable state survives Redis loss

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Why PostgreSQL and Redis together??

## Задача

Сделай короткую письменную практику по теме **Why PostgreSQL and Redis together?**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Why PostgreSQL and Redis together?: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
