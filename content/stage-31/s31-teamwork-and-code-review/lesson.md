# Teamwork and code review

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Screening communication влияет на прохождение remote и local interviews.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Teamwork and code review**, а не только запомнить термин;
- прочитать и изменить короткий пример для `accepting feedback`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Teamwork and code review** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**accepting feedback.** `accepting feedback` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**explaining trade-offs.** `EXPLAIN (ANALYZE, BUFFERS)` сравнивает estimates с фактическими rows/time/I/O; запуск ANALYZE действительно выполняет statement.

**focused PR.** `focused PR` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**conflict resolution.** `conflict resolution` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `accepting feedback` и `explaining trade-offs` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `accepting feedback`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Используй STAR для поведения и context → decision → trade-off → verification для техники.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- accepting feedback
- explaining trade-offs
- focused PR
- conflict resolution

### Полезно

- связать Teamwork and code review с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Teamwork and code review: отдельный пример

```text
Тема: Teamwork and code review

Фокус:
- accepting feedback
- explaining trade-offs
- focused PR
- conflict resolution

Рабочая проверка:
Ответ строй как context → личное действие → результат → конкретный follow-up.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `accepting feedback` до запуска.

**B · Find the bug.** Найди нарушение `explaining trade-offs` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Teamwork and code review за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Teamwork and code review и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Teamwork and code review?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Teamwork and code review: это отдельный технический контракт

### Нормальный Junior answer

> Teamwork and code review — тема, в которой я сначала фиксирую `accepting feedback`, затем объясняю `explaining trade-offs` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Teamwork and code review?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- accepting feedback
- explaining trade-offs
- focused PR
- conflict resolution

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Teamwork and code review?

## Задача

Сделай короткую письменную практику по теме **Teamwork and code review**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Teamwork and code review: это отдельный технический контракт
- **Механизм:** Используй STAR для поведения и context → decision → trade-off → verification для техники.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub code review guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

Последняя проверка версий: **2026-08-27**.
