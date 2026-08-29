# `.dockerignore`

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Docker/containers явно встречались в 11/18 — обязательный P1 practical skill.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`.dockerignore`**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``.dockerignore``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **`.dockerignore`** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**`.dockerignore`.** Container запускает изолированный process из image; данные вне writable layer сохраняют в volume.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``.dockerignore`` и ``.dockerignore`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется ``.dockerignore``; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Разделяй build-time layers, runtime config, network DNS и persistent volumes.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `.dockerignore`

### Полезно

- связать `.dockerignore` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `.dockerignore`: отдельный пример

```text
Сценарий: COPY . . добавил .env.

Проверка:
dockerignore, rotation, runtime secrets.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``.dockerignore`` до запуска.

**B · Find the bug.** Найди нарушение ``.dockerignore`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `.dockerignore` за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Secret in image

**Сценарий:** COPY . . добавил .env.

**Rubric:** dockerignore, rotation, runtime secrets.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Debugging practice

### Secret copied into image

**Сценарий:** COPY . . сохранил .env в старом image layer.

**Rubric:** Rotate secret, .dockerignore, runtime injection/secrets; удаление в следующем layer не очищает историю.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое `.dockerignore` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `.dockerignore`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`.dockerignore`: это отдельный технический контракт

### Нормальный Junior answer

> `.dockerignore` — тема, в которой я сначала фиксирую ``.dockerignore``, затем объясняю ``.dockerignore`` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `.dockerignore`?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- `.dockerignore`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `.dockerignore`?

## Задача

Сделай короткую письменную практику по теме **`.dockerignore`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `.dockerignore`: это отдельный технический контракт
- **Механизм:** Разделяй build-time layers, runtime config, network DNS и persistent volumes.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Docker concepts](https://docs.docker.com/get-started/docker-concepts/)
- [Compose reference](https://docs.docker.com/reference/compose-file/)

Последняя проверка версий: **2026-08-27**.
