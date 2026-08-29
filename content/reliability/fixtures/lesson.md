# Fixtures

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Fixtures**, а не только запомнить термин;
- прочитать и изменить короткий пример для `setup/teardown`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**setup/teardown.** `setup/teardown` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**dependency injection.** Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

**yield fixture.** Fixture создаёт dependency теста и управляет cleanup; scope выбирают по требуемой изоляции, а не ради скорости любой ценой.

**avoiding giant fixture graphs.** Fixture создаёт dependency теста и управляет cleanup; scope выбирают по требуемой изоляции, а не ради скорости любой ценой.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `setup/teardown` и `dependency injection` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `setup/teardown`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- setup/teardown
- dependency injection
- yield fixture
- avoiding giant fixture graphs

### Полезно

- связать Fixtures с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Fixtures: отдельный пример

```text
Сценарий: Resource остаётся после failed test.

Проверка:
yield fixture, cleanup in finally, narrow scope.
```

Это отдельный testing example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `setup/teardown` до запуска.

**B · Find the bug.** Найди нарушение `dependency injection` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Fixtures за 60 секунд: определение, механизм, пример, ограничение.

## Testing practice

### Fixture cleanup

**Сценарий:** Resource остаётся после failed test.

**Rubric:** yield fixture, cleanup in finally, narrow scope.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Fixtures и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Fixtures?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Fixtures: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный Junior answer

> Fixtures — тема, в которой я сначала фиксирую `setup/teardown`, затем объясняю `dependency injection` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Fixtures?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Expected answer rubric

### Must mention

- setup/teardown
- dependency injection
- yield fixture
- avoiding giant fixture graphs

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Fixtures?

## Задача

Сделай короткую письменную практику по теме **Fixtures**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Fixtures: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
