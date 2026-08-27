# List

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- объяснить `order` своими словами и связать с backend-сценарием;
- объяснить `mutability` своими словами и связать с backend-сценарием;
- объяснить `indexing/slicing` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Коллекция выбирается по требуемым операциям: порядок, уникальность, доступ по ключу, мутабельность и стоимость поиска.

В теме **List** важно уверенно объяснять следующие части:

### order

Для `order` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### mutability

Для `mutability` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### indexing/slicing

Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.

### append/extend/insert

Для `append/extend/insert` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### remove/pop

Для `remove/pop` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### membership

Для `membership` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### common time complexity

Для `common time complexity` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

```python
records = [{"id": 2}, {"id": 1}, {"id": 2}]
by_id = {record["id"]: record for record in records}
ordered = sorted(by_id.values(), key=lambda row: row["id"] )
```

Разбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path.

## Common mistakes

**Ошибка:** Выбирать коллекцию по привычке и игнорировать порядок, дубликаты или хешируемость.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **List** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- order
- mutability
- indexing/slicing
- append/extend/insert
- Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Выбирать коллекцию по привычке и игнорировать порядок, дубликаты или хешируемость.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- order
- mutability
- indexing/slicing
- append/extend/insert
- remove/pop
- membership
- common time complexity
- copying

## Задача

Разбери backend-сценарий: **Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Code prediction

### Срез создаёт новый list

```python
items = [1, 2, 3]
part = items[:]
part.append(4)
print(items, part)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1, 2, 3] [1, 2, 3, 4]
```

Срез создаёт новый внешний список; для immutable int этого достаточно для независимости.

Misconception: `slice-copy`.

</details>

### Unpacking со starred target

```python
first, *middle, last = [1, 2, 3, 4]
print(first, middle, last)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
1 [2, 3] 4
```

Starred target собирает промежуточные элементы в новый list.

Misconception: `unpacking`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **List**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
