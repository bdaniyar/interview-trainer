# Exception hierarchy

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- объяснить ``BaseException`` своими словами и связать с backend-сценарием;
- объяснить ``Exception`` своими словами и связать с backend-сценарием;
- объяснить `common built-ins` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Итерация, исключения и context managers — протоколы управления потоком и освобождением ресурсов.

В теме **Exception hierarchy** важно уверенно объяснять следующие части:

### `BaseException`

Для ``BaseException`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### `Exception`

Для ``Exception`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### common built-ins

Для `common built-ins` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### why not catch bare `except`

Для `why not catch bare `except`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Exception hierarchy: отдельный пример

```python
try:
    int("not-a-number")
except ValueError as exc:
    print(isinstance(exc, Exception))
    print(type(exc).__mro__[:3])
```

Иерархия позволяет перехватывать ожидаемый узкий тип, не скрывая системные и неожиданные ошибки.

## Common mistakes

**Ошибка:** Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Exception hierarchy** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Покажи happy path, завершение протокола и поведение при исключении. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `BaseException`
- `Exception`
- common built-ins
- why not catch bare `except`.
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

- `BaseException`
- `Exception`
- common built-ins
- why not catch bare `except`.

## Задача

Разбери backend-сценарий: **Покажи happy path, завершение протокола и поведение при исключении.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Code prediction

### finally выполняется при return

```python
def run():
    try:
        return 'result'
    finally:
        print('cleanup')
print(run())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
cleanup
result
```

Перед фактическим выходом из функции Python выполняет finally.

Misconception: `finally`.

</details>

## Debugging practice

### Broad exception

**Сценарий:** except Exception превращает DB outage в 404.

**Rubric:** Перехватывать ожидаемую domain error; unexpected log/re-raise.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Exception hierarchy**;
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
