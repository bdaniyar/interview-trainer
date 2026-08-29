# Async tests

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Async tests**, а не только запомнить термин;
- прочитать и изменить короткий пример для `event loop plugin/config`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**event loop plugin/config.** Event loop запускает ready callbacks/tasks и ждёт I/O; cooperative task уступает управление только в await point.

**AsyncClient.** `AsyncClient` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**deterministic timeouts.** `deterministic timeouts` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**no sleep-heavy tests.** `no sleep-heavy tests` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `event loop plugin/config` и `AsyncClient` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `event loop plugin/config`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- event loop plugin/config
- AsyncClient
- deterministic timeouts
- no sleep-heavy tests

### Полезно

- связать Async tests с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Async tests: отдельный пример

```text
Сценарий: Test завершился, background task осталась.

Проверка:
Await/cancel tasks; deterministic event.
```

Это отдельный testing example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `event loop plugin/config` до запуска.

**B · Find the bug.** Найди нарушение `AsyncClient` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Async tests за 60 секунд: определение, механизм, пример, ограничение.

## Testing practice

### Async task leak

**Сценарий:** Test завершился, background task осталась.

**Rubric:** Await/cancel tasks; deterministic event.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Async tests и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Async tests?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Async tests: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный Junior answer

> Async tests — тема, в которой я сначала фиксирую `event loop plugin/config`, затем объясняю `AsyncClient` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Async tests?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Expected answer rubric

### Must mention

- event loop plugin/config
- AsyncClient
- deterministic timeouts
- no sleep-heavy tests

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Async tests?

## Задача

Сделай короткую письменную практику по теме **Async tests**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Async tests: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
