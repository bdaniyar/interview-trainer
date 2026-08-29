# What to test

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **What to test**, а не только запомнить термин;
- прочитать и изменить короткий пример для `happy path`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**happy path.** `happy path` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**validation.** `validation` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**permissions.** `permissions` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**not found.** `not found` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**duplicates/conflicts.** `duplicates/conflicts` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**rollback.** Rollback отменяет текущую transaction и возвращает Session в usable state; после flush error продолжать без rollback нельзя.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `happy path` и `validation` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `happy path`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- happy path
- validation
- permissions
- not found

### Полезно

- duplicates/conflicts
- rollback

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### What to test: отдельный пример

```python
def example_s18_what_to_test() -> tuple[str, ...]:
    # What to test: проверяем отдельный contract урока.
    return ('happy path', 'validation', 'permissions', 'not found',)

assert example_s18_what_to_test()
```

Тестируй observable contract, failure path и изоляцию между cases.

## Common mistakes

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `happy path` до запуска.

**B · Find the bug.** Найди нарушение `validation` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про What to test за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое What to test и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме What to test?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

What to test: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный Junior answer

> What to test — тема, в которой я сначала фиксирую `happy path`, затем объясняю `validation` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме What to test?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Expected answer rubric

### Must mention

- happy path
- validation
- permissions
- not found

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме What to test?

## Задача

Сделай короткую письменную практику по теме **What to test**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** What to test: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
