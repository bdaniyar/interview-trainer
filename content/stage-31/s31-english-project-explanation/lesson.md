# English project explanation

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Screening communication влияет на прохождение remote и local interviews.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **English project explanation**, а не только запомнить термин;
- прочитать и изменить короткий пример для `self-introduction`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **English project explanation** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**self-introduction.** `self-introduction` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**StudyHub summary.** `StudyHub summary` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**explaining a bug.** `EXPLAIN (ANALYZE, BUFFERS)` сравнивает estimates с фактическими rows/time/I/O; запуск ANALYZE действительно выполняет statement.

**explaining async/transaction trade-off.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**PR description.** `PR description` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `self-introduction` и `StudyHub summary` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `self-introduction`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Используй STAR для поведения и context → decision → trade-off → verification для техники.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- self-introduction
- StudyHub summary
- explaining a bug
- explaining async/transaction trade-off

### Полезно

- PR description

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### English project explanation: отдельный пример

```text
Тема: English project explanation

Фокус:
- self-introduction
- StudyHub summary
- explaining a bug
- explaining async/transaction trade-off

Рабочая проверка:
Ответ строй как context → личное действие → результат → конкретный follow-up.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `self-introduction` до запуска.

**B · Find the bug.** Найди нарушение `StudyHub summary` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про English project explanation за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое English project explanation и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме English project explanation?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

English project explanation: это отдельный технический контракт

### Нормальный Junior answer

> English project explanation — тема, в которой я сначала фиксирую `self-introduction`, затем объясняю `StudyHub summary` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме English project explanation?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- self-introduction
- StudyHub summary
- explaining a bug
- explaining async/transaction trade-off

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме English project explanation?

## Задача

Сделай короткую письменную практику по теме **English project explanation**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** English project explanation: это отдельный технический контракт
- **Механизм:** Используй STAR для поведения и context → decision → trade-off → verification для техники.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub code review guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

Последняя проверка версий: **2026-08-27**.
