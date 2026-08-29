# Why Python and FastAPI?

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- объяснить `mature ecosystem and development speed` своими словами и связать с backend-сценарием;
- объяснить `type hints/Pydantic/OpenAPI` своими словами и связать с backend-сценарием;
- объяснить `async stack suits WebSockets and I/O waits` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Resume Defense проверяет каждую заявленную технологию через конкретную роль в StudyHub, Hotel Booking или Share Recipe.

В теме **Why Python and FastAPI?** важно уверенно объяснять следующие части:

### mature ecosystem and development speed

Для `mature ecosystem and development speed` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### type hints/Pydantic/OpenAPI

Type hint описывает контракт для checker/IDE; обычный Python не запрещает другое runtime-значение, а FastAPI/Pydantic отдельно используют annotation для schema и validation.

### async stack suits WebSockets and I/O waits

WebSocket держит долгоживущее соединение; масштабирование требует shared fan-out, а durable history хранится отдельно.

### FastAPI is not universally superior to Django

Для `FastAPI is not universally superior to Django` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### Django could reduce custom work for admin/content-heavy product

Для `Django could reduce custom work for admin/content-heavy product` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Why Python and FastAPI?: отдельный пример

```text
Тема: Why Python and FastAPI?

Фокус:
- mature ecosystem and development speed
- type hints/Pydantic/OpenAPI
- async stack suits WebSockets and I/O waits
- FastAPI is not universally superior to Django

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

**Ошибка:** Приписывать себе production scale, AWS, Kubernetes, Kafka или RabbitMQ без фактического опыта.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Why Python and FastAPI?** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Защити один claim, назвав точный flow, failure mode и способ проверки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- mature ecosystem and development speed
- type hints/Pydantic/OpenAPI
- async stack suits WebSockets and I/O waits
- FastAPI is not universally superior to Django
- Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Приписывать себе production scale, AWS, Kubernetes, Kafka или RabbitMQ без фактического опыта.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- mature ecosystem and development speed
- type hints/Pydantic/OpenAPI
- async stack suits WebSockets and I/O waits
- FastAPI is not universally superior to Django
- Django could reduce custom work for admin/content-heavy product.

## Задача

Разбери backend-сценарий: **Защити один claim, назвав точный flow, failure mode и способ проверки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Why Python and FastAPI?**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
