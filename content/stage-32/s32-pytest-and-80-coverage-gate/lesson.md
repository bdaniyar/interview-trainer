# pytest and 80% coverage gate

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **pytest and 80% coverage gate**, а не только запомнить термин;
- прочитать и изменить короткий пример для `unit vs integration`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **pytest and 80% coverage gate** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**unit vs integration.** `unit vs integration` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**critical failure cases.** `critical failure cases` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**coverage gate is not quality proof.** Coverage показывает исполненные строки/ветки, но не доказывает качество assertions и полноту failure scenarios.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `unit vs integration` и `critical failure cases` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `unit vs integration`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- unit vs integration
- critical failure cases
- coverage gate is not quality proof

### Полезно

- связать pytest and 80% coverage gate с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### pytest and 80% coverage gate: отдельный пример

```text
Тема: pytest and 80% coverage gate

Фокус:
- unit vs integration
- critical failure cases
- coverage gate is not quality proof

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `unit vs integration` до запуска.

**B · Find the bug.** Найди нарушение `critical failure cases` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про pytest and 80% coverage gate за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое pytest and 80% coverage gate и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме pytest and 80% coverage gate?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

pytest and 80% coverage gate: это отдельный технический контракт

### Нормальный Junior answer

> pytest and 80% coverage gate — тема, в которой я сначала фиксирую `unit vs integration`, затем объясняю `critical failure cases` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме pytest and 80% coverage gate?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- unit vs integration
- critical failure cases
- coverage gate is not quality proof

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме pytest and 80% coverage gate?

## Задача

Сделай короткую письменную практику по теме **pytest and 80% coverage gate**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** pytest and 80% coverage gate: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
