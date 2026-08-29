# Student schedule and availability

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Screening communication влияет на прохождение remote и local interviews.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Student schedule and availability**, а не только запомнить термин;
- прочитать и изменить короткий пример для `honest availability`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Student schedule and availability** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**honest availability.** `honest availability` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**part-time/flexible preference.** `part-time/flexible preference` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**clear commitment.** `clear commitment` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.

**no promises impossible to combine with study.** `no promises impossible to combine with study` раскрывается через context, личное действие, измеримый результат и конкретный follow-up без выдуманных деталей.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `honest availability` и `part-time/flexible preference` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `honest availability`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Используй STAR для поведения и context → decision → trade-off → verification для техники.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- honest availability
- part-time/flexible preference
- clear commitment
- no promises impossible to combine with study

### Полезно

- связать Student schedule and availability с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Student schedule and availability: отдельный пример

```text
Тема: Student schedule and availability

Фокус:
- honest availability
- part-time/flexible preference
- clear commitment
- no promises impossible to combine with study

Рабочая проверка:
Ответ строй как context → личное действие → результат → конкретный follow-up.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `honest availability` до запуска.

**B · Find the bug.** Найди нарушение `part-time/flexible preference` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Student schedule and availability за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Student schedule and availability и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Student schedule and availability?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Student schedule and availability: это отдельный технический контракт

### Нормальный Junior answer

> Student schedule and availability — тема, в которой я сначала фиксирую `honest availability`, затем объясняю `part-time/flexible preference` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Student schedule and availability?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- honest availability
- part-time/flexible preference
- clear commitment
- no promises impossible to combine with study

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Student schedule and availability?

## Задача

Сделай короткую письменную практику по теме **Student schedule and availability**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Student schedule and availability: это отдельный технический контракт
- **Механизм:** Используй STAR для поведения и context → decision → trade-off → verification для техники.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GitHub code review guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)

Последняя проверка версий: **2026-08-27**.
