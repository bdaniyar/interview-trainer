# Comprehensions

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- объяснить `list/dict/set comprehensions` своими словами и связать с backend-сценарием;
- объяснить `generator expressions` своими словами и связать с backend-сценарием;
- объяснить `nested comprehensions` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Коллекция выбирается по требуемым операциям: порядок, уникальность, доступ по ключу, мутабельность и стоимость поиска.

В теме **Comprehensions** важно уверенно объяснять следующие части:

### list/dict/set comprehensions

`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

### generator expressions

Generator хранит suspended execution frame и выдаёт значения лениво; после исчерпания он не перезапускается.

### nested comprehensions

Comprehension создаёт новую коллекцию из явного source/filter/expression; nested comprehensions стоит заменять обычным циклом, когда теряется читаемость.

### scope

LEGB ищет имя в local, enclosing, global и builtins; assignment делает имя local, если не объявлены `global` или `nonlocal`.

### readability

Для `readability` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### when a regular loop is better

Для `when a regular loop is better` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Comprehensions: отдельный пример

```python
rows = [
    {"id": 1, "active": True},
    {"id": 2, "active": False},
]
active_ids = [row["id"] for row in rows if row["active"]]

print(active_ids)
```

Comprehension объединяет преобразование и короткий filter без скрытых side effects.

## Common mistakes

**Ошибка:** Выбирать коллекцию по привычке и игнорировать порядок, дубликаты или хешируемость.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Comprehensions** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- list/dict/set comprehensions
- generator expressions
- nested comprehensions
- scope
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

- list/dict/set comprehensions
- generator expressions
- nested comprehensions
- scope
- readability
- when a regular loop is better.

## Задача

### Email активных пользователей

Верни lower-case email активных пользователей с непустым email. Не изменяй вход.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Comprehensions**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
