# Compose commands

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Compose commands**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``docker compose up``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Compose commands** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**`docker compose up`.** Container запускает изолированный process из image; данные вне writable layer сохраняют в volume.

**`up --build`.** ``up --build`` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**`build`.** ``build`` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**`ps`.** ``ps`` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**`logs`.** ``logs`` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**`exec`.** ``exec`` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``docker compose up`` и ``up --build`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``docker compose up``; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `docker compose up`
- `up --build`
- `build`
- `ps`

### Полезно

- `logs`
- `exec`

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Compose commands: отдельный пример

```yaml
# 21.15 · Compose commands
lesson:
  key: s21_compose_commands
  checks:
    - `docker compose up`
    - `up --build`
    - `build`
    - `ps`
```

Разделяй build-time image и runtime container: DNS, ports, mounts, env и readiness.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``docker compose up`` до запуска.

**B · Find the bug.** Найди нарушение ``up --build`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Compose commands за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Compose commands и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Compose commands?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Compose commands: это отдельный технический контракт

### Нормальный Junior answer

> Compose commands — тема, в которой я сначала фиксирую ``docker compose up``, затем объясняю ``up --build`` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Compose commands?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- `docker compose up`
- `up --build`
- `build`
- `ps`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Compose commands?

## Задача

Сделай короткую письменную практику по теме **Compose commands**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Compose commands: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
