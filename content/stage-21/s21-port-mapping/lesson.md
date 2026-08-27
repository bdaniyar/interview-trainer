# Port mapping

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- объяснить `host port` своими словами и связать с backend-сценарием;
- объяснить `container port` своими словами и связать с backend-сценарием;
- объяснить `service-to-service uses container port.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Docker image — неизменяемый шаблон filesystem, container — запущенный изолированный process с configuration runtime.

В теме **Port mapping** важно уверенно объяснять следующие части:

### host port

Для `host port` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.

### container port

Container — изолированный process из image, а не VM; сеть, environment и persistent volumes задаются отдельно при runtime.

### service-to-service uses container port

Container — изолированный process из image, а не VM; сеть, environment и persistent volumes задаются отдельно при runtime.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "app"]
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Использовать localhost между containers или считать depends_on проверкой readiness.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Port mapping** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Диагностируй container через logs, env, DNS, port и healthcheck по порядку. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- host port
- container port
- service-to-service uses container port.
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

- host port
- container port
- service-to-service uses container port.

## Задача

Разбери backend-сценарий: **Диагностируй container через logs, env, DNS, port и healthcheck по порядку.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Operations practice

### Wrong port

**Сценарий:** Host открывает 5433, какой port использует API container?

**Rubric:** service:5432; host mapping только для host client.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### Wrong Docker port

**Сценарий:** API container подключается к db:5433 из-за host mapping 5433:5432.

**Rubric:** Между containers использовать service DNS и container port 5432; host port нужен только host client.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Port mapping**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
