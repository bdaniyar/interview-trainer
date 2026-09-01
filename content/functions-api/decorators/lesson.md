# Basic decorators

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Basic decorators**, а не только запомнить термин;
- прочитать и изменить короткий пример для `wrapper`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

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

### Важный нюанс / ограничение

Используй `functools.wraps`, иначе теряются `__name__`, annotations, signature metadata и `__wrapped__`; это мешает FastAPI, introspection и debugging. Decorator не должен случайно проглатывать return value или exceptions.

### Где используется в backend

Декораторы естественны для регистрации routes и технического tracing; доменную авторизацию часто яснее выразить dependency/service policy.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

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

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Wrapper вызывает `fn(*args, **kwargs)`, но забывает `return`, поэтому caller получает `None`.

### Ошибка 2

Обычный sync wrapper вокруг `async def` возвращает coroutine object, но не ожидает его.

### Ошибка 3

Decorator скрывает signature без `@wraps(fn)`.

## Практика

**A · Предсказание результата кода.** Определи порядок `before/original/after`.

**B · Найди ошибку.** Верни потерянный результат из wrapper.

**C · Улучшение кода.** Добавь `@wraps` и async-compatible вариант.

**D · Небольшая задача.** Напиши decorator, считающий число вызовов.

## Вопросы с собеседований

### Основной вопрос

Как работает decorator функции и зачем нужен `functools.wraps`?

### Дополнительный вопрос

В каком порядке применяются два decorators?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Decorator заменяет функцию результатом `decorator(function)`; wraps сохраняет metadata и ссылку на исходную функцию.

### Нормальный ответ уровня Junior

> Запись `@audit` выполняется при определении функции и равна `handler = audit(handler)`. Audit возвращает wrapper, который принимает arguments, вызывает исходную функцию и возвращает результат. `functools.wraps` сохраняет имя, docstring, annotations и `__wrapped__`, поэтому framework и отладчик продолжают видеть исходный контракт.

### Углубление / дополнительный вопрос

**В каком порядке применяются два decorators?**

Применяются снизу вверх: `@a @b def f` даёт `f = a(b(f))`; при вызове внешний wrapper `a` начинает первым.

## Критерии хорошего ответа

### Что обязательно упомянуть

- эквивалентность `@decorator` присваиванию
- wrapper args/result
- definition time
- `functools.wraps`

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Wrapper вызывает `fn(*args, **kwargs)`, но забывает `return`, поэтому caller получает `None`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- В каком порядке применяются два decorators?

## Задача

### Decorator проверки роли

Реализуй require_role(role). Первый аргумент wrapped-функции — user с roles; иначе PermissionError. Сохрани metadata.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Decorator заменяет функцию результатом `decorator(function)`; wraps сохраняет metadata и ссылку на исходную функцию.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Wrapper вызывает `fn(*args, **kwargs)`, но забывает `return`, поэтому caller получает `None`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
