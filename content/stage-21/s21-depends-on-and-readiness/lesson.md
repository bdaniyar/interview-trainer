# `depends_on` and readiness

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`depends_on` and readiness**, а не только запомнить термин;
- прочитать и изменить короткий пример для `start order is not application readiness`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **`depends_on` and readiness** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**start order is not application readiness.** `start order is not application readiness` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**healthcheck.** `healthcheck` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**retry/backoff.** Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `start order is not application readiness` и `healthcheck` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `start order is not application readiness`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- start order is not application readiness
- healthcheck
- retry/backoff

### Полезно

- связать `depends_on` and readiness с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `depends_on` and readiness: отдельный пример

```text
Сценарий: depends_on есть, migrations падают.

Проверка:
Healthcheck/ready retry; start order не readiness.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `start order is not application readiness` до запуска.

**B · Find the bug.** Найди нарушение `healthcheck` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `depends_on` and readiness за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Readiness

**Сценарий:** depends_on есть, migrations падают.

**Rubric:** Healthcheck/ready retry; start order не readiness.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### depends_on readiness

**Сценарий:** API стартует после container DB, но раньше готовности принимать SQL.

**Rubric:** Healthcheck/retry/backoff или entrypoint wait; start order не является readiness guarantee.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое `depends_on` and readiness и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `depends_on` and readiness?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`depends_on` and readiness: это отдельный технический контракт

### Нормальный Junior answer

> `depends_on` and readiness — тема, в которой я сначала фиксирую `start order is not application readiness`, затем объясняю `healthcheck` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `depends_on` and readiness?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- start order is not application readiness
- healthcheck
- retry/backoff

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `depends_on` and readiness?

## Задача

Сделай короткую письменную практику по теме **`depends_on` and readiness**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `depends_on` and readiness: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
