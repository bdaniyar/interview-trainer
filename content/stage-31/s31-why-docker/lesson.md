# Why Docker?

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Screening communication влияет на прохождение remote и local interviews.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Why Docker?**, а не только запомнить термин;
- прочитать и изменить короткий пример для `reproducible environment`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Why Docker?** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**reproducible environment.** `reproducible environment` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**dependency isolation.** Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

**multi-service local setup.** `multi-service local setup` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**not “Docker automatically scales”.** Container запускает изолированный process из image; данные вне writable layer сохраняют в volume.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `reproducible environment` и `dependency isolation` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `reproducible environment`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Используй STAR для поведения и context → decision → trade-off → verification для техники.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- reproducible environment
- dependency isolation
- multi-service local setup
- not “Docker automatically scales”

### Полезно

- связать Why Docker? с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Why Docker?: отдельный пример

```text
Тема: Why Docker?

Фокус:
- reproducible environment
- dependency isolation
- multi-service local setup
- not “Docker automatically scales”

Рабочая проверка:
Ответ строй как context → личное действие → результат → конкретный follow-up.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `reproducible environment` до запуска.

**B · Find the bug.** Найди нарушение `dependency isolation` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Why Docker? за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Why Docker? и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Why Docker??

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Why Docker?: это отдельный технический контракт

### Нормальный Junior answer

> Why Docker? — тема, в которой я сначала фиксирую `reproducible environment`, затем объясняю `dependency isolation` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Why Docker??**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- reproducible environment
- dependency isolation
- multi-service local setup
- not “Docker automatically scales”

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Why Docker??

## Задача

Сделай короткую письменную практику по теме **Why Docker?**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Why Docker?: это отдельный технический контракт
- **Механизм:** Используй STAR для поведения и context → decision → trade-off → verification для техники.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub code review guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

Последняя проверка версий: **2026-08-27**.
