# `try/except/else/finally`

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- объяснить `control flow` своими словами и связать с backend-сценарием;
- объяснить `cleanup` своими словами и связать с backend-сценарием;
- объяснить `return inside try/finally` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Итерация, исключения и context managers — протоколы управления потоком и освобождением ресурсов.

В теме **`try/except/else/finally`** важно уверенно объяснять следующие части:

### control flow

Для `control flow` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### cleanup

Для `cleanup` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### return inside try/finally

`finally` выполняет cleanup при normal return и exception; он не должен без необходимости подавлять исходную ошибку новым return/raise.

### narrow exception scope

LEGB ищет имя в local, enclosing, global и builtins; assignment делает имя local, если не объявлены `global` или `nonlocal`.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### `try/except/else/finally`: отдельный пример

```python
def parse(value):
    try:
        result = int(value)
    except ValueError:
        return None
    else:
        return result
    finally:
        print("parse finished")

print(parse("7"))
```

`else` выполняется только без exception, `finally` — при любом пути выхода.

## Common mistakes

**Ошибка:** Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **`try/except/else/finally`** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Покажи happy path, завершение протокола и поведение при исключении. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- control flow
- cleanup
- return inside try/finally
- narrow exception scope.
- Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- control flow
- cleanup
- return inside try/finally
- narrow exception scope.

## Задача

### Разобрать optional integer

None и пустая строка дают None; str/int преобразуются в int; bool и мусор дают ValueError с explicit cause.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **`try/except/else/finally`**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
