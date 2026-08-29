# Test pyramid and test types

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Test pyramid and test types**, а не только запомнить термин;
- прочитать и изменить короткий пример для `unit`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**unit.** `unit` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**integration.** `integration` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**end-to-end.** `end-to-end` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**contract awareness.** `contract awareness` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**correct boundary choice.** `correct boundary choice` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `unit` и `integration` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `unit`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- unit
- integration
- end-to-end
- contract awareness

### Полезно

- correct boundary choice

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Test pyramid and test types: отдельный пример

```text
Сценарий: Раздели booking flow на unit, integration и API tests.

Проверка:
Unit domain decision; integration DB constraint; API status/body.
```

Это отдельный testing example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `unit` до запуска.

**B · Find the bug.** Найди нарушение `integration` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Test pyramid and test types за 60 секунд: определение, механизм, пример, ограничение.

## Testing practice

### Test boundary

**Сценарий:** Раздели booking flow на unit, integration и API tests.

**Rubric:** Unit domain decision; integration DB constraint; API status/body.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Test pyramid and test types и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Test pyramid and test types?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Test pyramid and test types: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный Junior answer

> Test pyramid and test types — тема, в которой я сначала фиксирую `unit`, затем объясняю `integration` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Test pyramid and test types?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Expected answer rubric

### Must mention

- unit
- integration
- end-to-end
- contract awareness

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Test pyramid and test types?

## Задача

Сделай короткую письменную практику по теме **Test pyramid and test types**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Test pyramid and test types: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
