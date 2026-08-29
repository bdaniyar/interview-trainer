# `functools.wraps`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`functools.wraps`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `preserving `__name__``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**preserving `__name__`.** `preserving `__name__`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**docstring.** `docstring` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**annotations.** `annotations` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**`__wrapped__`.** ``__wrapped__`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**why frameworks/tools care.** `why frameworks/tools care` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `preserving `__name__`` и `docstring` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- preserving `__name__`
- docstring
- annotations
- `__wrapped__`

### Полезно

- why frameworks/tools care

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `functools.wraps`: отдельный пример

```python
from functools import wraps

def traced(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper

@traced
def health() -> dict[str, str]:
    return {"status": "ok"}

print(health.__name__, health.__annotations__)
```

`wraps` сохраняет metadata и `__wrapped__`, нужные introspection и framework-коду.

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `preserving `__name__`` до запуска.

**B · Find the bug.** Найди нарушение `docstring` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `functools.wraps` за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Decorator меняет вызываемый объект

```python
def twice(fn):
    def wrapper():
        return fn() * 2
    return wrapper

@twice
def answer():
    return 21
print(answer())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
42
```

После декорирования имя answer связано с wrapper, который вызывает исходную функцию.

Misconception: `decorator`.

</details>

## Debugging practice

### Missing wraps

**Сценарий:** FastAPI/introspection видит wrapper signature.

**Rubric:** functools.wraps сохраняет metadata и __wrapped__.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое `functools.wraps` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `functools.wraps`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`functools.wraps`: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> `functools.wraps` — тема, в которой я сначала фиксирую `preserving `__name__``, затем объясняю `docstring` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `functools.wraps`?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- preserving `__name__`
- docstring
- annotations
- `__wrapped__`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `functools.wraps`?

## Задача

### Сохранить metadata wrapper

Реализуй traced decorator через functools.wraps и добавь wrapper.traced = True.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `functools.wraps`: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
