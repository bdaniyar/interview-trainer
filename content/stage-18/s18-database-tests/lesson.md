# Database tests

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Database tests**, а не только запомнить термин;
- прочитать и изменить короткий пример для `isolated test DB/schema`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**isolated test DB/schema.** `isolated test DB/schema` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**transaction rollback or recreate.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.

**constraints.** Constraint хранит invariant рядом с данными и защищает его от всех writers; API переводит conflict в понятную domain/HTTP error.

**migrations.** `migrations` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**no production DB.** `no production DB` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `isolated test DB/schema` и `transaction rollback or recreate` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `isolated test DB/schema`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- isolated test DB/schema
- transaction rollback or recreate
- constraints
- migrations

### Полезно

- no production DB

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Database tests: отдельный пример

```text
Сценарий: Порядок tests влияет на rows.

Проверка:
Transaction rollback/recreated schema.
```

Это отдельный testing example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `isolated test DB/schema` до запуска.

**B · Find the bug.** Найди нарушение `transaction rollback or recreate` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Database tests за 60 секунд: определение, механизм, пример, ограничение.

## Testing practice

### Database isolation

**Сценарий:** Порядок tests влияет на rows.

**Rubric:** Transaction rollback/recreated schema.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Database tests и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Database tests?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Database tests: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный Junior answer

> Database tests — тема, в которой я сначала фиксирую `isolated test DB/schema`, затем объясняю `transaction rollback or recreate` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Database tests?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Expected answer rubric

### Must mention

- isolated test DB/schema
- transaction rollback or recreate
- constraints
- migrations

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Database tests?

## Задача

Сделай короткую письменную практику по теме **Database tests**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Database tests: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
