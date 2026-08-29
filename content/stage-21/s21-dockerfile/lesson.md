# Dockerfile

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- объяснить `FROM` своими словами и связать с backend-сценарием;
- объяснить `WORKDIR` своими словами и связать с backend-сценарием;
- объяснить `COPY` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Docker image — неизменяемый шаблон filesystem, container — запущенный изолированный process с configuration runtime.

В теме **Dockerfile** важно уверенно объяснять следующие части:

### FROM

Для `FROM` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

### WORKDIR

Для `WORKDIR` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

### COPY

Для `COPY` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

### RUN

Для `RUN` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

### CMD

Для `CMD` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

### ENTRYPOINT

Для `ENTRYPOINT` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

### build context

Для `build context` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Dockerfile: отдельный пример

```yaml
# 21.2 · Dockerfile
lesson:
  key: s21_dockerfile
  checks:
    - FROM
    - WORKDIR
    - COPY
    - RUN
```

Разделяй build-time image и runtime container: DNS, ports, mounts, env и readiness.

## Common mistakes

**Ошибка:** Использовать localhost между containers или считать depends_on проверкой readiness.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Dockerfile** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Диагностируй container через logs, env, DNS, port и healthcheck по порядку. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- FROM
- WORKDIR
- COPY
- RUN
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

- FROM
- WORKDIR
- COPY
- RUN
- CMD
- ENTRYPOINT
- build context.

## Задача

Разбери backend-сценарий: **Диагностируй container через logs, env, DNS, port и healthcheck по порядку.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Dockerfile**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
