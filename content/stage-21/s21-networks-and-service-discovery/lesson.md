# Networks and service discovery

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- объяснить `service name` своими словами и связать с backend-сценарием;
- объяснить ``localhost` means current container` своими словами и связать с backend-сценарием;
- объяснить `common DB connection bug.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Docker image — неизменяемый шаблон filesystem, container — запущенный изолированный process с configuration runtime.

В теме **Networks and service discovery** важно уверенно объяснять следующие части:

### service name

Для `service name` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

### `localhost` means current container

Container — изолированный process из image, а не VM; сеть, environment и persistent volumes задаются отдельно при runtime.

### common DB connection bug

Для `common DB connection bug` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Networks and service discovery: отдельный пример

```text
Сценарий: API config содержит DB_HOST=localhost.

Проверка:
Compose service name; shared network/DNS.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

**Ошибка:** Использовать localhost между containers или считать depends_on проверкой readiness.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Networks and service discovery** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Диагностируй container через logs, env, DNS, port и healthcheck по порядку. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- service name
- `localhost` means current container
- common DB connection bug.
- Разделяй build-time layers, runtime config, network DNS и persistent volumes.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Использовать localhost между containers или считать depends_on проверкой readiness.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- service name
- `localhost` means current container
- common DB connection bug.

## Задача

Разбери backend-сценарий: **Диагностируй container через logs, env, DNS, port и healthcheck по порядку.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Operations practice

### Service discovery

**Сценарий:** API config содержит DB_HOST=localhost.

**Rubric:** Compose service name; shared network/DNS.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### Container localhost

**Сценарий:** API не видит PostgreSQL по localhost.

**Rubric:** localhost — тот же container; Compose DNS service name + container port.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Networks and service discovery**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
