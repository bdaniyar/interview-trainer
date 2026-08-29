# Alembic

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Alembic**, а не только запомнить термин;
- прочитать и изменить короткий пример для `versioned schema`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Alembic** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**versioned schema.** `versioned schema` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**autogenerate review.** `autogenerate review` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**expand/contract.** `expand/contract` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**data migration/rollback awareness.** Rollback отменяет текущую transaction и возвращает Session в usable state; после flush error продолжать без rollback нельзя.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `versioned schema` и `autogenerate review` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `versioned schema`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- versioned schema
- autogenerate review
- expand/contract
- data migration/rollback awareness

### Полезно

- связать Alembic с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Alembic: отдельный пример

```text
Тема: Alembic

Фокус:
- versioned schema
- autogenerate review
- expand/contract
- data migration/rollback awareness

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `versioned schema` до запуска.

**B · Find the bug.** Найди нарушение `autogenerate review` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Alembic за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Alembic и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Alembic?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Alembic: это отдельный технический контракт

### Нормальный Junior answer

> Alembic — тема, в которой я сначала фиксирую `versioned schema`, затем объясняю `autogenerate review` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Alembic?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- versioned schema
- autogenerate review
- expand/contract
- data migration/rollback awareness

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Alembic?

## Задача

Сделай короткую письменную практику по теме **Alembic**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Alembic: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
