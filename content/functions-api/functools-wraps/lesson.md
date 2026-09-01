# `functools.wraps`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **`functools.wraps`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `preserving `__name__``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**preserving `__name__`.** `preserving `__name__`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**docstring.** `docstring` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**annotations.** `annotations` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**`__wrapped__`.** ``__wrapped__`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**why frameworks/tools care.** `why frameworks/tools care` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `preserving `__name__`` и `docstring` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- preserving `__name__`
- docstring
- annotations
- `__wrapped__`

### Полезно

- why frameworks/tools care

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `preserving `__name__`` до запуска.

**B · Найди ошибку.** Найди нарушение `docstring` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про `functools.wraps` за 60 секунд: определение, механизм, пример, ограничение.

## Предсказание результата кода

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

Ожидаемый результат:

```text
42
```

После декорирования имя answer связано с wrapper, который вызывает исходную функцию.

Типичная ошибка мышления: `decorator`.

</details>

## Практика: Отладка

### Missing wraps

**Сценарий:** FastAPI/introspection видит wrapper signature.

**Критерии ответа:** functools.wraps сохраняет metadata и __wrapped__.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое `functools.wraps` и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме `functools.wraps`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`functools.wraps`: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный ответ уровня Junior

> `functools.wraps` — тема, в которой я сначала фиксирую `preserving `__name__``, затем объясняю `docstring` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме `functools.wraps`?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Критерии хорошего ответа

### Что обязательно упомянуть

- preserving `__name__`
- docstring
- annotations
- `__wrapped__`

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме `functools.wraps`?

## Задача

### Сохранить metadata wrapper

Реализуй traced decorator через functools.wraps и добавь wrapper.traced = True.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `functools.wraps`: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
