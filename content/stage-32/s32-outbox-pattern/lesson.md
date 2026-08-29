# Outbox pattern

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Outbox pattern**, а не только запомнить термин;
- прочитать и изменить короткий пример для `business change and outbox row in one transaction`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Outbox pattern** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**business change and outbox row in one transaction.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**worker processes rows.** Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.

**closes dual-write gap.** `closes dual-write gap` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**at-least-once.** `at-least-once` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**idempotency/retry.** Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `business change and outbox row in one transaction` и `worker processes rows` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `business change and outbox row in one transaction`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- business change and outbox row in one transaction
- worker processes rows
- closes dual-write gap
- at-least-once

### Полезно

- idempotency/retry

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Outbox pattern: отдельный пример

```text
Сценарий: Почему outbox?

Проверка:
Atomicity gap; at-least-once/idempotency.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `business change and outbox row in one transaction` до запуска.

**B · Find the bug.** Найди нарушение `worker processes rows` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Outbox pattern за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Outbox defense

**Сценарий:** Почему outbox?

**Rubric:** Atomicity gap; at-least-once/idempotency.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Outbox pattern и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Outbox pattern?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Outbox pattern: это отдельный технический контракт

### Нормальный Junior answer

> Outbox pattern — тема, в которой я сначала фиксирую `business change and outbox row in one transaction`, затем объясняю `worker processes rows` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Outbox pattern?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- business change and outbox row in one transaction
- worker processes rows
- closes dual-write gap
- at-least-once

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Outbox pattern?

## Задача

Сделай короткую письменную практику по теме **Outbox pattern**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Outbox pattern: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
