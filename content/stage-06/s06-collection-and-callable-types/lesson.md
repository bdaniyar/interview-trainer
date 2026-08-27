# Collection and callable types

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Learning objectives

После урока ты сможешь:

- объяснить ``list[str]`` своими словами и связать с backend-сценарием;
- объяснить ``dict[str, int]`` своими словами и связать с backend-сценарием;
- объяснить ``Sequence`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Type hints улучшают статический анализ и контракты, но сами по себе не валидируют runtime-данные.

В теме **Collection and callable types** важно уверенно объяснять следующие части:

### `list[str]`

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

### `dict[str, int]`

`dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.

### `Sequence`

Для ``Sequence`` покажи, что видит static checker, что реально происходит runtime и где нужна отдельная validation.

### `Iterable`

Iterable умеет создать iterator через `__iter__`; один iterable может создавать новые независимые iterators для повторных обходов.

### `Callable`

Для ``Callable`` покажи, что видит static checker, что реально происходит runtime и где нужна отдельная validation.

## Mental model

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
from typing import Protocol

class UserReader(Protocol):
    def get(self, user_id: int) -> dict | None: ...

def load_name(repo: UserReader, user_id: int) -> str | None:
    user = repo.get(user_id)
    return user["name"] if user else None
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Считать Any безопасным escape hatch либо путать Optional с необязательным аргументом.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Collection and callable types** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Опиши тип входа API helper так, чтобы mypy видел ошибочный вызов до запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `list[str]`
- `dict[str, int]`
- `Sequence`
- `Iterable`
- Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Считать Any безопасным escape hatch либо путать Optional с необязательным аргументом.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- `list[str]`
- `dict[str, int]`
- `Sequence`
- `Iterable`
- `Callable`.

## Задача

Разбери backend-сценарий: **Опиши тип входа API helper так, чтобы mypy видел ошибочный вызов до запуска.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Collection and callable types**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
