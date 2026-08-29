# Redis-backed password reset

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- объяснить `short-lived one-time state/hashed token` своими словами и связать с backend-сценарием;
- объяснить `TTL` своими словами и связать с backend-сценарием;
- объяснить `atomic invalidation` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Resume Defense проверяет каждую заявленную технологию через конкретную роль в StudyHub, Hotel Booking или Share Recipe.

В теме **Redis-backed password reset** важно уверенно объяснять следующие части:

### short-lived one-time state/hashed token

Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

### TTL

Для `TTL` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### atomic invalidation

Для `atomic invalidation` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### do not reveal whether email exists

`EXISTS` проверяет наличие хотя бы одной строки correlated subquery и часто прямо выражает semi-join без размножения строк.

### revoke sessions when appropriate

Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Redis-backed password reset: отдельный пример

```text
Сценарий: Один reset URL меняет пароль повторно.

Проверка:
Random high-entropy token, server-side hash, TTL и atomic one-time invalidation; revoke sessions по policy.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Приписывать себе production scale, AWS, Kubernetes, Kafka или RabbitMQ без фактического опыта.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Redis-backed password reset** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Защити один claim, назвав точный flow, failure mode и способ проверки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- short-lived one-time state/hashed token
- TTL
- atomic invalidation
- do not reveal whether email exists
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

- short-lived one-time state/hashed token
- TTL
- atomic invalidation
- do not reveal whether email exists
- revoke sessions when appropriate.

## Задача

Разбери backend-сценарий: **Защити один claim, назвав точный flow, failure mode и способ проверки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Debugging practice

### Reusable reset token

**Сценарий:** Один reset URL меняет пароль повторно.

**Rubric:** Random high-entropy token, server-side hash, TTL и atomic one-time invalidation; revoke sessions по policy.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Redis-backed password reset**;
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
