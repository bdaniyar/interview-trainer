# FastAPI tests

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **FastAPI tests**, а не только запомнить термин;
- прочитать и изменить короткий пример для `request/response`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**request/response.** `request/response` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**auth.** `auth` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**validation.** `validation` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**dependency overrides.** Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

**lifespan.** Lifespan управляет ресурсами уровня приложения: код до `yield` создаёт client/pool, код после `yield` гарантированно закрывает их при shutdown.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `request/response` и `auth` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `request/response`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- request/response
- auth
- validation
- dependency overrides

### Полезно

- lifespan

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### FastAPI tests: отдельный пример

```text
Сценарий: FastAPI test ходит в real DB.

Проверка:
app.dependency_overrides и cleanup.
```

Это отдельный testing example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `request/response` до запуска.

**B · Find the bug.** Найди нарушение `auth` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про FastAPI tests за 60 секунд: определение, механизм, пример, ограничение.

## Testing practice

### Dependency override

**Сценарий:** FastAPI test ходит в real DB.

**Rubric:** app.dependency_overrides и cleanup.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое FastAPI tests и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме FastAPI tests?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

FastAPI tests: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный Junior answer

> FastAPI tests — тема, в которой я сначала фиксирую `request/response`, затем объясняю `auth` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме FastAPI tests?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Expected answer rubric

### Must mention

- request/response
- auth
- validation
- dependency overrides

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме FastAPI tests?

## Задача

Сделай короткую письменную практику по теме **FastAPI tests**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** FastAPI tests: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
