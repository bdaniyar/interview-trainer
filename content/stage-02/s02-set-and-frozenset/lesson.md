# Set and frozenset

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- объяснить `uniqueness` своими словами и связать с backend-сценарием;
- объяснить `membership` своими словами и связать с backend-сценарием;
- объяснить `union/intersection/difference` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Коллекция выбирается по требуемым операциям: порядок, уникальность, доступ по ключу, мутабельность и стоимость поиска.

В теме **Set and frozenset** важно уверенно объяснять следующие части:

### uniqueness

Для `uniqueness` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### membership

Для `membership` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### union/intersection/difference

Для `union/intersection/difference` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### deduplication

Для `deduplication` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### set vs list

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

### frozenset

`frozenset` — immutable hashable set и подходит как key или элемент другого set, если требуется множество без mutations.

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

1. Объясни **Set and frozenset** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- uniqueness
- membership
- union/intersection/difference
- deduplication
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

- uniqueness
- membership
- union/intersection/difference
- deduplication
- set vs list
- frozenset.

## Задача

### Нормализовать scopes

Верни frozenset непустых scopes в lower-case без пробелов и дублей.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Code prediction

### set удаляет дубликаты

```python
values = {3, 1, 3, 2}
print(len(values), sorted(values))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
3 [1, 2, 3]
```

set хранит уникальные hashable значения; порядок вывода делают явным через sorted.

Misconception: `set-order`.

</details>

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Set and frozenset**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
