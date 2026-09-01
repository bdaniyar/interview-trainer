# Networks and service discovery

> [!IMPORTANT]
> **P1 · вероятность на интервью: very_high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Networks and service discovery**, а не только запомнить термин;
- прочитать и изменить короткий пример для `service name`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Тема **Networks and service discovery** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы сценарий ошибки.

**service name.** `service name` относится либо к во время сборки image, либо к runtime container и наблюдается через DNS, ports, mounts и жизненный цикл процесса.

**`localhost` means current container.** Container — изолированный process из image, а не VM; сеть, окружением и persistent volumes задаются отдельно при runtime.

**common DB connection bug.** `common DB connection bug` относится либо к во время сборки image, либо к runtime container и наблюдается через DNS, ports, mounts и жизненный цикл процесса.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `service name` и ``localhost` means current container` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `service name`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Разделяй во время сборки layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- service name
- `localhost` means current container
- common DB connection bug

### Полезно

- связать Networks and service discovery с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Networks and service discovery: отдельный пример

```text
Сценарий: API config содержит DB_HOST=localhost.

Проверка:
Compose service name; shared network/DNS.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Игнорировать ограничение механизма и проверять только основной сценарий.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `service name` до запуска.

**B · Найди ошибку.** Найди нарушение ``localhost` means current container` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Networks and service discovery за 60 секунд: определение, механизм, пример, ограничение.

## Практика: Эксплуатация

### Service discovery

**Сценарий:** API config содержит DB_HOST=localhost.

**Критерии ответа:** Compose service name; shared network/DNS.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Практика: Отладка

### Container localhost

**Сценарий:** API не видит PostgreSQL по localhost.

**Критерии ответа:** localhost — тот же container; Compose DNS service name + container port.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Networks and service discovery и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Networks and service discovery?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Networks and service discovery: это отдельный технический контракт

### Нормальный ответ уровня Junior

> Networks and service discovery — тема, в которой я сначала фиксирую `service name`, затем объясняю ``localhost` means current container` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Networks and service discovery?**

Нужно назвать конкретный сценарий ошибки и способ его проверить.

## Критерии хорошего ответа

### Что обязательно упомянуть

- service name
- `localhost` means current container
- common DB connection bug

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Игнорировать ограничение механизма и проверять только основной сценарий.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Networks and service discovery?

## Задача

Сделай короткую письменную практику по теме **Networks and service discovery**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Networks and service discovery: это отдельный технический контракт
- **Механизм:** Разделяй во время сборки layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только основной сценарий.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
