# JWT refresh sessions

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- объяснить `short access token` своими словами и связать с backend-сценарием;
- объяснить `server-side refresh session` своими словами и связать с backend-сценарием;
- объяснить `hashed token identifier` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Resume Defense проверяет каждую заявленную технологию через конкретную роль в StudyHub, Hotel Booking или Share Recipe.

В теме **JWT refresh sessions** важно уверенно объяснять следующие части:

### short access token

Для `short access token` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### server-side refresh session

Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

### hashed token identifier

Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

### rotation

Для `rotation` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### revocation

Для `revocation` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

### reuse detection

Для `reuse detection` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### JWT refresh sessions: отдельный пример

```text
Сценарий: Отозвать stolen refresh.

Проверка:
Server session, rotation/revocation, short access.
```

Это отдельный architecture example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Приписывать себе production scale, AWS, Kubernetes, Kafka или RabbitMQ без фактического опыта.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **JWT refresh sessions** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Защити один claim, назвав точный flow, failure mode и способ проверки. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- short access token
- server-side refresh session
- hashed token identifier
- rotation
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

- short access token
- server-side refresh session
- hashed token identifier
- rotation
- revocation
- reuse detection.

## Задача

Разбери backend-сценарий: **Защити один claim, назвав точный flow, failure mode и способ проверки.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Architecture practice

### JWT sessions

**Сценарий:** Отозвать stolen refresh.

**Rubric:** Server session, rotation/revocation, short access.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **JWT refresh sessions**;
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
