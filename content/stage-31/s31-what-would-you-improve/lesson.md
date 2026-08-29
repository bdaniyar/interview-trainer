# What would you improve?

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Screening communication влияет на прохождение remote и local interviews.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **What would you improve?**, а не только запомнить термин;
- прочитать и изменить короткий пример для `honest trade-off`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **What would you improve?** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**honest trade-off.** `honest trade-off` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**measured next step.** `measured next step` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**avoid pretending project is production-perfect.** `avoid pretending project is production-perfect` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `honest trade-off` и `measured next step` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `honest trade-off`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Используй STAR для поведения и context → decision → trade-off → verification для техники.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- honest trade-off
- measured next step
- avoid pretending project is production-perfect

### Полезно

- связать What would you improve? с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### What would you improve?: отдельный пример

```text
Тема: What would you improve?

Фокус:
- honest trade-off
- measured next step
- avoid pretending project is production-perfect

Рабочая проверка:
Ответ строй как context → личное действие → результат → конкретный follow-up.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `honest trade-off` до запуска.

**B · Find the bug.** Найди нарушение `measured next step` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про What would you improve? за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое What would you improve? и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме What would you improve??

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

What would you improve?: это отдельный технический контракт

### Нормальный Junior answer

> What would you improve? — тема, в которой я сначала фиксирую `honest trade-off`, затем объясняю `measured next step` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме What would you improve??**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- honest trade-off
- measured next step
- avoid pretending project is production-perfect

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме What would you improve??

## Задача

Сделай короткую письменную практику по теме **What would you improve?**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** What would you improve?: это отдельный технический контракт
- **Механизм:** Используй STAR для поведения и context → decision → trade-off → verification для техники.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub code review guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

Последняя проверка версий: **2026-08-27**.
