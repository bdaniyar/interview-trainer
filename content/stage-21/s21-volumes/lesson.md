# Volumes

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Volumes**, а не только запомнить термин;
- прочитать и изменить короткий пример для `named volume`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Volumes** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**named volume.** `named volume` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**bind mount.** `bind mount` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**persistence.** `persistence` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.

**source mount pitfalls.** `source mount pitfalls` относится либо к build-time image, либо к runtime container и наблюдается через DNS, ports, mounts и process lifecycle.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `named volume` и `bind mount` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `named volume`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- named volume
- bind mount
- persistence
- source mount pitfalls

### Полезно

- связать Volumes с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Volumes: отдельный пример

```text
Сценарий: После recreate DB данные исчезли.

Проверка:
Named volume; backups; down -v destructive.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `named volume` до запуска.

**B · Find the bug.** Найди нарушение `bind mount` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Volumes за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Lost data

**Сценарий:** После recreate DB данные исчезли.

**Rubric:** Named volume; backups; down -v destructive.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### Bind mount hides files

**Сценарий:** Mount ./app:/app скрыл dependencies, созданные в image path.

**Rubric:** Проверить mount target; отделить source и dependency paths, использовать named volume где уместно.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### No database volume

**Сценарий:** После compose down/recreate PostgreSQL пуст.

**Rubric:** Named volume и backup/restore; документировать, что down -v удаляет данные.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Volumes и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Volumes?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Volumes: это отдельный технический контракт

### Нормальный Junior answer

> Volumes — тема, в которой я сначала фиксирую `named volume`, затем объясняю `bind mount` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Volumes?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- named volume
- bind mount
- persistence
- source mount pitfalls

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Volumes?

## Задача

Сделай короткую письменную практику по теме **Volumes**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Volumes: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
