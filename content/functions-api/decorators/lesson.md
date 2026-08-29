# Basic decorators

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Basic decorators**, а не только запомнить термин;
- прочитать и изменить короткий пример для `wrapper`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Decorator — callable, который получает декорируемый объект и возвращает объект-замену. Для функции заменой обычно служит wrapper, добавляющий поведение до и после исходного вызова.

### Как работает

`@audit` над `def save` эквивалентен `save = audit(save)` и выполняется при definition/import time. Wrapper должен принять совместимые arguments, вызвать исходную функцию и вернуть её результат. Для async function нужен async wrapper с await.


### Пример

```python
from functools import wraps

def audit(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@audit
def total(values):
    return sum(values)

print(total([2, 3]))  # 5
```

### Важный нюанс / limitation

Используй `functools.wraps`, иначе теряются `__name__`, annotations, signature metadata и `__wrapped__`; это мешает FastAPI, introspection и debugging. Decorator не должен случайно проглатывать return value или exceptions.

### Где используется в backend

Декораторы естественны для регистрации routes и технического tracing; доменную авторизацию часто яснее выразить dependency/service policy.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- эквивалентность `@decorator` присваиванию
- wrapper args/result
- definition time
- `functools.wraps`

### Полезно

- различать decorator и decorator factory
- порядок нескольких decorators

### Можно не учить глубоко

- переписывание signatures через `inspect.Signature`

## Code examples

### Basic decorators: отдельный пример

```python
def require_active(function):
    def wrapper(user):
        if not user["active"]:
            raise PermissionError
        return function(user)
    return wrapper

@require_active
def profile(user):
    return user["name"]
```

Decorator заменяет имя `profile` на wrapper, который проверяет условие перед исходным вызовом.

## Common mistakes

### Ошибка 1

Wrapper вызывает `fn(*args, **kwargs)`, но забывает `return`, поэтому caller получает `None`.

### Ошибка 2

Обычный sync wrapper вокруг `async def` возвращает coroutine object, но не ожидает его.

### Ошибка 3

Decorator скрывает signature без `@wraps(fn)`.

## Practice

**A · Code prediction.** Определи порядок `before/original/after`.

**B · Find the bug.** Верни потерянный результат из wrapper.

**C · Rewrite.** Добавь `@wraps` и async-compatible вариант.

**D · Small task.** Напиши decorator, считающий число вызовов.

## Interview questions

### Основной вопрос

Как работает decorator функции и зачем нужен `functools.wraps`?

### Follow-up

В каком порядке применяются два decorators?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Decorator заменяет функцию результатом `decorator(function)`; wraps сохраняет metadata и ссылку на исходную функцию.

### Нормальный Junior answer

> Запись `@audit` выполняется при определении функции и равна `handler = audit(handler)`. Audit возвращает wrapper, который принимает arguments, вызывает исходную функцию и возвращает результат. `functools.wraps` сохраняет имя, docstring, annotations и `__wrapped__`, поэтому framework и отладчик продолжают видеть исходный контракт.

### Углубление / follow-up

**В каком порядке применяются два decorators?**

Применяются снизу вверх: `@a @b def f` даёт `f = a(b(f))`; при вызове внешний wrapper `a` начинает первым.

## Expected answer rubric

### Must mention

- эквивалентность `@decorator` присваиванию
- wrapper args/result
- definition time
- `functools.wraps`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Wrapper вызывает `fn(*args, **kwargs)`, но забывает `return`, поэтому caller получает `None`.
- пересказ одного определения без механизма или примера.

### Follow-up

- В каком порядке применяются два decorators?

## Задача

### Decorator проверки роли

Реализуй require_role(role). Первый аргумент wrapped-функции — user с roles; иначе PermissionError. Сохрани metadata.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Decorator заменяет функцию результатом `decorator(function)`; wraps сохраняет metadata и ссылку на исходную функцию.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Wrapper вызывает `fn(*args, **kwargs)`, но забывает `return`, поэтому caller получает `None`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
