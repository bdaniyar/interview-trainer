# Raising and re-raising

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- объяснить ``raise`` своими словами и связать с backend-сценарием;
- объяснить `bare `raise`` своими словами и связать с backend-сценарием;
- объяснить `preserving traceback` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Итерация, исключения и context managers — протоколы управления потоком и освобождением ресурсов.

В теме **Raising and re-raising** важно уверенно объяснять следующие части:

### `raise`

Для ``raise`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### bare `raise`

Для `bare `raise`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### preserving traceback

Для `preserving traceback` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### domain exceptions

Для `domain exceptions` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Raising and re-raising: отдельный пример

```python
def load_id(raw):
    try:
        return int(raw)
    except ValueError:
        print("invalid id")
        raise

try:
    load_id("x")
except ValueError:
    print("caller decides")
```

Bare `raise` повторно поднимает текущую ошибку с исходным traceback.

## Common mistakes

**Ошибка:** Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Raising and re-raising** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Покажи happy path, завершение протокола и поведение при исключении. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `raise`
- bare `raise`
- preserving traceback
- domain exceptions.
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

- `raise`
- bare `raise`
- preserving traceback
- domain exceptions.

## Задача

Разбери backend-сценарий: **Покажи happy path, завершение протокола и поведение при исключении.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Raising and re-raising**;
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
