# Static hints vs runtime behavior

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Learning objectives

После урока ты сможешь:

- объяснить `type hints` своими словами и связать с backend-сценарием;
- объяснить `static checker` своими словами и связать с backend-сценарием;
- объяснить `Python remains dynamic` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Type hints улучшают статический анализ и контракты, но сами по себе не валидируют runtime-данные.

В теме **Static hints vs runtime behavior** важно уверенно объяснять следующие части:

### type hints

Type hint описывает контракт для checker/IDE; обычный Python не запрещает другое runtime-значение, а FastAPI/Pydantic отдельно используют annotation для schema и validation.

### static checker

Для `static checker` покажи, что видит static checker, что реально происходит runtime и где нужна отдельная validation.

### Python remains dynamic

Для `Python remains dynamic` покажи, что видит static checker, что реально происходит runtime и где нужна отдельная validation.

### FastAPI/Pydantic use hints at runtime

Для `FastAPI/Pydantic use hints at runtime` покажи, что видит static checker, что реально происходит runtime и где нужна отдельная validation.

## Mental model

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Static hints vs runtime behavior: отдельный пример

```python
def double(value: int) -> int:
    return value * 2

print(double(3))
print(double("a"))
```

Type checker отклонит второй вызов, но runtime Python выполнит operator строки без автоматической validation.

## Common mistakes

**Ошибка:** Считать Any безопасным escape hatch либо путать Optional с необязательным аргументом.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Static hints vs runtime behavior** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Опиши тип входа API helper так, чтобы mypy видел ошибочный вызов до запуска. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- type hints
- static checker
- Python remains dynamic
- FastAPI/Pydantic use hints at runtime.
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

- type hints
- static checker
- Python remains dynamic
- FastAPI/Pydantic use hints at runtime.

## Задача

Разбери backend-сценарий: **Опиши тип входа API helper так, чтобы mypy видел ошибочный вызов до запуска.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Code prediction

### Type hint не валидирует runtime

```python
def double(value: int) -> int:
    return value * 2
print(double('a'))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
aa
```

Обычная annotation не вставляет runtime type check; строка использует собственный operator *.

Misconception: `typing-runtime`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Static hints vs runtime behavior**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
