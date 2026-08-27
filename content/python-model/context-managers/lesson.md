# Context manager protocol

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- объяснить ``with`` своими словами и связать с backend-сценарием;
- объяснить ``__enter__`` своими словами и связать с backend-сценарием;
- объяснить ``__exit__`` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Итерация, исключения и context managers — протоколы управления потоком и освобождением ресурсов.

В теме **Context manager protocol** важно уверенно объяснять следующие части:

### `with`

Для ``with`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### `__enter__`

Для ``__enter__`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### `__exit__`

Для ``__exit__`` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### resource cleanup

Для `resource cleanup` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

### exception suppression

Для `exception suppression` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
from contextlib import contextmanager

@contextmanager
def transaction(session):
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Context manager protocol** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Покажи happy path, завершение протокола и поведение при исключении. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- `with`
- `__enter__`
- `__exit__`
- resource cleanup
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

- `with`
- `__enter__`
- `__exit__`
- resource cleanup
- exception suppression.

## Задача

### Transaction context manager

Создай Transaction: enter возвращает resource; success вызывает commit, error — rollback; исключение не подавляется.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### Context manager получает exception

```python
class Guard:
    def __enter__(self): return self
    def __exit__(self, kind, value, tb):
        print(kind.__name__)
        return True
with Guard():
    raise ValueError('x')
print('after')
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
ValueError
after
```

__exit__ получил тип ошибки и вернул True, поэтому исключение было подавлено.

Misconception: `context-manager-suppression`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Context manager protocol**;
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
