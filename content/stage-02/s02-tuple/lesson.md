# Tuple

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- объяснить `immutability` своими словами и связать с backend-сценарием;
- объяснить `packing/unpacking` своими словами и связать с backend-сценарием;
- объяснить `single-element tuple` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Коллекция выбирается по требуемым операциям: порядок, уникальность, доступ по ключу, мутабельность и стоимость поиска.

В теме **Tuple** важно уверенно объяснять следующие части:

### immutability

Для `immutability` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### packing/unpacking

Для `packing/unpacking` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.

### single-element tuple

`tuple` — immutable sequence; hashability зависит от всех элементов, а неизменяемость контейнера не делает mutable элементы неизменяемыми.

### tuple as key

`tuple` — immutable sequence; hashability зависит от всех элементов, а неизменяемость контейнера не делает mutable элементы неизменяемыми.

### named structured data vs dataclass

`dataclass` генерирует init/repr/equality по объявленным fields; mutable defaults задают через `default_factory`, а invariants — в `__post_init__`.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Tuple: отдельный пример

```python
point = (43.2389, 76.8897)
latitude, longitude = point
locations = {point: "Almaty"}

print(latitude, longitude)
print(locations[point])
```

Tuple выражает фиксированную запись и может быть dict key, если все элементы hashable.

## Common mistakes

**Ошибка:** Выбирать коллекцию по привычке и игнорировать порядок, дубликаты или хешируемость.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Tuple** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- immutability
- packing/unpacking
- single-element tuple
- tuple as key
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

- immutability
- packing/unpacking
- single-element tuple
- tuple as key
- named structured data vs dataclass.

## Задача

Разбери backend-сценарий: **Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Tuple**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
