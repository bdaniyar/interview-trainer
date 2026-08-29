# `monkeypatch`, Mock and AsyncMock

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`monkeypatch`, Mock and AsyncMock**, а не только запомнить термин;
- прочитать и изменить короткий пример для `environment`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**environment.** `environment` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**functions.** `functions` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**async dependencies.** `async dependencies` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**correct patch location.** `correct patch location` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `environment` и `functions` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `environment`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- environment
- functions
- async dependencies
- correct patch location

### Полезно

- связать `monkeypatch`, Mock and AsyncMock с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `monkeypatch`, Mock and AsyncMock: отдельный пример

```text
Сценарий: patch library.client не влияет на imported symbol.

Проверка:
Patch имя в module under test.
```

Это отдельный testing example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `environment` до запуска.

**B · Find the bug.** Найди нарушение `functions` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `monkeypatch`, Mock and AsyncMock за 60 секунд: определение, механизм, пример, ограничение.

## Testing practice

### Patch namespace

**Сценарий:** patch library.client не влияет на imported symbol.

**Rubric:** Patch имя в module under test.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое `monkeypatch`, Mock and AsyncMock и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `monkeypatch`, Mock and AsyncMock?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`monkeypatch`, Mock and AsyncMock: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный Junior answer

> `monkeypatch`, Mock and AsyncMock — тема, в которой я сначала фиксирую `environment`, затем объясняю `functions` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `monkeypatch`, Mock and AsyncMock?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Expected answer rubric

### Must mention

- environment
- functions
- async dependencies
- correct patch location

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `monkeypatch`, Mock and AsyncMock?

## Задача

Сделай короткую письменную практику по теме **`monkeypatch`, Mock and AsyncMock**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `monkeypatch`, Mock and AsyncMock: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
