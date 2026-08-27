# Choosing a collection

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- объяснить `list vs tuple` своими словами и связать с backend-сценарием;
- объяснить `list vs set` своими словами и связать с backend-сценарием;
- объяснить `dict vs list of pairs` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Коллекция выбирается по требуемым операциям: порядок, уникальность, доступ по ключу, мутабельность и стоимость поиска.

В теме **Choosing a collection** важно уверенно объяснять следующие части:

### list vs tuple

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

### list vs set

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

### dict vs list of pairs

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

### queue/stack choices

Для `queue/stack choices` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### complexity trade-offs

Для `complexity trade-offs` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### practical backend examples

Для `practical backend examples` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

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

1. Объясни **Choosing a collection** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- list vs tuple
- list vs set
- dict vs list of pairs
- queue/stack choices
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

- list vs tuple
- list vs set
- dict vs list of pairs
- queue/stack choices
- complexity trade-offs
- practical backend examples.

## Задача

Разбери backend-сценарий: **Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Choosing a collection**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
