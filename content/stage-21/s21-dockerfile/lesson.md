# Dockerfile

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Dockerfile**, а не только запомнить термин;
- прочитать и изменить короткий пример для `FROM`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Dockerfile** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**FROM.** `FROM` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**WORKDIR.** `WORKDIR` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**COPY.** `COPY` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**RUN.** `RUN` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**CMD.** `CMD` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**ENTRYPOINT.** `ENTRYPOINT` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `FROM` и `WORKDIR` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `FROM`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- FROM
- WORKDIR
- COPY
- RUN

### Полезно

- CMD
- ENTRYPOINT

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

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

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `FROM` до запуска.

**B · Find the bug.** Найди нарушение `WORKDIR` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Dockerfile за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Dockerfile и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Dockerfile?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Dockerfile: это отдельный технический контракт

### Нормальный Junior answer

> Dockerfile — тема, в которой я сначала фиксирую `FROM`, затем объясняю `WORKDIR` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Dockerfile?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- FROM
- WORKDIR
- COPY
- RUN

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Dockerfile?

## Задача

Сделай короткую письменную практику по теме **Dockerfile**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Dockerfile: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
