# Networks and service discovery

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Networks and service discovery**, а не только запомнить термин;
- прочитать и изменить короткий пример для `service name`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Networks and service discovery** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**service name.** `service name` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**`localhost` means current container.** Container — изолированный process из image, а не VM; сеть, environment и persistent volumes задаются отдельно при runtime.

**common DB connection bug.** `common DB connection bug` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `service name` и ``localhost` means current container` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `service name`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- service name
- `localhost` means current container
- common DB connection bug

### Полезно

- связать Networks and service discovery с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Networks and service discovery: отдельный пример

```text
Сценарий: API config содержит DB_HOST=localhost.

Проверка:
Compose service name; shared network/DNS.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `service name` до запуска.

**B · Find the bug.** Найди нарушение ``localhost` means current container` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Networks and service discovery за 60 секунд: определение, механизм, пример, ограничение.

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

## Interview questions

### Основной вопрос

Что такое Networks and service discovery и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Networks and service discovery?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Networks and service discovery: это отдельный технический контракт

### Нормальный Junior answer

> Networks and service discovery — тема, в которой я сначала фиксирую `service name`, затем объясняю ``localhost` means current container` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Networks and service discovery?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- service name
- `localhost` means current container
- common DB connection bug

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Networks and service discovery?

## Задача

Сделай короткую письменную практику по теме **Networks and service discovery**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Networks and service discovery: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
