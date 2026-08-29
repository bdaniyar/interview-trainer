# Why async?

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Why async?**, а не только запомнить термин;
- прочитать и изменить короткий пример для `PostgreSQL/Redis/object storage/WebSocket are I/O-bound`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Why async?** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**PostgreSQL/Redis/object storage/WebSocket are I/O-bound.** WebSocket держит долгоживущее соединение; масштабирование требует shared fan-out, а durable history хранится отдельно.

**event loop serves other work while waiting.** Event loop запускает ready callbacks/tasks и ждёт I/O; cooperative task уступает управление только в await point.

**CPU-heavy work must leave event loop.** Event loop запускает ready callbacks/tasks и ждёт I/O; cooperative task уступает управление только в await point.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `PostgreSQL/Redis/object storage/WebSocket are I/O-bound` и `event loop serves other work while waiting` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `PostgreSQL/Redis/object storage/WebSocket are I/O-bound`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- PostgreSQL/Redis/object storage/WebSocket are I/O-bound
- event loop serves other work while waiting
- CPU-heavy work must leave event loop

### Полезно

- связать Why async? с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Why async?: отдельный пример

```text
Сценарий: Зачем async?

Проверка:
Concurrent I/O; not CPU speed; no blocking.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `PostgreSQL/Redis/object storage/WebSocket are I/O-bound` до запуска.

**B · Find the bug.** Найди нарушение `event loop serves other work while waiting` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Why async? за 60 секунд: определение, механизм, пример, ограничение.

## Architecture practice

### Why async

**Сценарий:** Зачем async?

**Rubric:** Concurrent I/O; not CPU speed; no blocking.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Why async? и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Why async??

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Why async?: это отдельный технический контракт

### Нормальный Junior answer

> Why async? — тема, в которой я сначала фиксирую `PostgreSQL/Redis/object storage/WebSocket are I/O-bound`, затем объясняю `event loop serves other work while waiting` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Why async??**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- PostgreSQL/Redis/object storage/WebSocket are I/O-bound
- event loop serves other work while waiting
- CPU-heavy work must leave event loop

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Why async??

## Задача

Сделай короткую письменную практику по теме **Why async?**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Why async?: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
