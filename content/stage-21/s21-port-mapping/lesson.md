# Port mapping

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Port mapping**, а не только запомнить термин;
- прочитать и изменить короткий пример для `host port`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Port mapping** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**host port.** `host port` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**container port.** Container — изолированный process из image, а не VM; сеть, environment и persistent volumes задаются отдельно при runtime.

**service-to-service uses container port.** Container — изолированный process из image, а не VM; сеть, environment и persistent volumes задаются отдельно при runtime.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `host port` и `container port` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `host port`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- host port
- container port
- service-to-service uses container port

### Полезно

- связать Port mapping с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Port mapping: отдельный пример

```text
Сценарий: Host открывает 5433, какой port использует API container?

Проверка:
service:5432; host mapping только для host client.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `host port` до запуска.

**B · Find the bug.** Найди нарушение `container port` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Port mapping за 60 секунд: определение, механизм, пример, ограничение.

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

## Interview questions

### Основной вопрос

Что такое Port mapping и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Port mapping?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Port mapping: это отдельный технический контракт

### Нормальный Junior answer

> Port mapping — тема, в которой я сначала фиксирую `host port`, затем объясняю `container port` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Port mapping?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- host port
- container port
- service-to-service uses container port

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Port mapping?

## Задача

Сделай короткую письменную практику по теме **Port mapping**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Port mapping: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
