# Dependency injection with `Depends`

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Dependency injection with `Depends`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `dependency graph`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Dependency Injection — передача нужной зависимости извне вместо создания её внутри handler. В FastAPI `Depends` описывает dependency graph, который framework разрешает для каждого request.

### Как работает

FastAPI читает signature endpoint и dependencies, вызывает их в правильном порядке и передаёт результаты дальше. Одинаковая dependency по умолчанию кэшируется один раз в рамках request. Dependency может зависеть от другой dependency; yield-вариант выполняет setup до handler и cleanup после response/error.


### Пример

```python
from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def require_admin(x_role: Annotated[str | None, Header()] = None) -> str:
    if x_role != "admin":
        raise HTTPException(403, "admin role required")
    return x_role

@app.get("/admin")
def admin(role: Annotated[str, Depends(require_admin)]):
    return {"role": role}
```

### Важный нюанс / limitation

Request-scoped cache не является глобальным cache. Не храни request-specific Session или user в module global. Dependencies удобны для границ framework — auth, session, settings — но сложные business rules лучше оставить service.

### Где используется в backend

`get_current_user` может зависеть от token parser, а endpoint получает уже проверенного user; dependency override упрощает тест.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- зачем DI
- dependency graph
- per-request cache
- yield cleanup
- test overrides

### Полезно

- `Annotated` aliases
- `use_cache=False`
- граница dependency/service

### Можно не учить глубоко

- внутренние классы решения dependency graph FastAPI

## Code examples

### Dependency injection with `Depends`: отдельный пример

```python
from fastapi import FastAPI

app = FastAPI()
# Добавь dependency и endpoint.
```

Это публичный starter contract практики «Authorization dependency». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Вызвать dependency вручную как обычную функцию и ожидать, что FastAPI разрешит её sub-dependencies.

### Ошибка 2

Создать глобальную SQLAlchemy Session и возвращать её всем requests.

### Ошибка 3

Поместить всю бизнес-логику в огромную dependency graph, которую трудно тестировать отдельно.

## Practice

**A · Flow prediction.** Расположи вызовы parent dependency, child dependency, endpoint и cleanup.

**B · Find the bug.** Найди глобальную Session в dependency module.

**C · Rewrite.** Вынеси чтение X-Role в `require_admin`.

**D · Small task.** Реализуй защищённый `/admin` endpoint с hidden tests.

## Interview questions

### Основной вопрос

Как работает `Depends` в FastAPI и каков lifecycle dependency?

### Follow-up

Чем request cache dependency отличается от singleton?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Depends объявляет dependency graph; FastAPI разрешает его на request, кэширует одинаковые dependencies и выполняет cleanup yield-dependency.

### Нормальный Junior answer

> `Depends` позволяет endpoint явно объявить, что ему нужны user, Session или settings. FastAPI строит graph по signatures, вызывает dependencies и передаёт результаты в handler. Внутри одного request одинаковая dependency обычно выполняется один раз. Если dependency использует `yield`, код после yield работает как cleanup. В тестах dependency можно override-нуть.

### Углубление / follow-up

**Чем request cache dependency отличается от singleton?**

Результат переиспользуется только внутри одного request; следующий request разрешает dependency заново. Singleton живёт между requests на уровне приложения.

## Expected answer rubric

### Must mention

- зачем DI
- dependency graph
- per-request cache
- yield cleanup

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Вызвать dependency вручную как обычную функцию и ожидать, что FastAPI разрешит её sub-dependencies.
- пересказ одного определения без механизма или примера.

### Follow-up

- Чем request cache dependency отличается от singleton?

## Задача

### Authorization dependency

require_admin читает X-Role: не admin → 403; GET /admin использует Depends.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Depends объявляет dependency graph; FastAPI разрешает его на request, кэширует одинаковые dependencies и выполняет cleanup yield-dependency.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Вызвать dependency вручную как обычную функцию и ожидать, что FastAPI разрешит её sub-dependencies.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
