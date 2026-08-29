# Parametrization

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Parametrization**, а не только запомнить термин;
- прочитать и изменить короткий пример для `edge cases`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**edge cases.** `edge cases` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**readable IDs.** `readable IDs` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**avoiding repeated tests.** `avoiding repeated tests` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `edge cases` и `readable IDs` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `edge cases`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- edge cases
- readable IDs
- avoiding repeated tests

### Полезно

- связать Parametrization с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Parametrization: отдельный пример

```python
import pytest
@pytest.mark.parametrize('value', [1, 2, 3])
def test_positive(value):
    assert value > 0
```

Expected: `3 passed`. pytest создаёт отдельный test case для каждого параметра; точное оформление строки зависит от verbosity.

## Common mistakes

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `edge cases` до запуска.

**B · Find the bug.** Найди нарушение `readable IDs` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Parametrization за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### parametrize создаёт отдельные cases

```python
import pytest
@pytest.mark.parametrize('value', [1, 2, 3])
def test_positive(value):
    assert value > 0
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
3 passed
```

pytest создаёт отдельный test case для каждого параметра; точное оформление строки зависит от verbosity.

Misconception: `pytest-parametrize`.

</details>

## Testing practice

### Parametrization

**Сценарий:** Пять копий теста отличаются input/result.

**Rubric:** parametrize cases с ids и boundaries.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Parametrization и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Parametrization?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Parametrization: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный Junior answer

> Parametrization — тема, в которой я сначала фиксирую `edge cases`, затем объясняю `readable IDs` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Parametrization?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Expected answer rubric

### Must mention

- edge cases
- readable IDs
- avoiding repeated tests

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Parametrization?

## Задача

Сделай короткую письменную практику по теме **Parametrization**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Parametrization: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
