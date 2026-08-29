# `classmethod` and `staticmethod`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- объяснить `alternate constructors` своими словами и связать с backend-сценарием;
- объяснить `class-aware behavior` своими словами и связать с backend-сценарием;
- объяснить `namespace utility` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

ООП в backend полезно как способ выразить состояние, поведение и границы ответственности, а не как соревнование по наследованию.

В теме **`classmethod` and `staticmethod`** важно уверенно объяснять следующие части:

### alternate constructors

Для `alternate constructors` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### class-aware behavior

Для `class-aware behavior` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### namespace utility

Для `namespace utility` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

### when module-level function is simpler

Для `when module-level function is simpler` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### `classmethod` and `staticmethod`: отдельный пример

```python
class UserId:
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_text(cls, raw):
        return cls(int(raw))

    @staticmethod
    def is_valid(raw):
        return raw.isdigit()

print(UserId.from_text("7").value, UserId.is_valid("7"))
```

Classmethod создаёт объект через polymorphic `cls`; staticmethod — namespaced helper без implicit receiver.

## Common mistakes

**Ошибка:** Создавать глубокую иерархию ради переиспользования нескольких строк.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **`classmethod` and `staticmethod`** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сравни composition и inheritance для сервиса уведомлений и назови цену изменения. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- alternate constructors
- class-aware behavior
- namespace utility
- when module-level function is simpler.
- У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Создавать глубокую иерархию ради переиспользования нескольких строк.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- alternate constructors
- class-aware behavior
- namespace utility
- when module-level function is simpler.

## Задача

### Создать User из mapping

Реализуй staticmethod normalize_email и classmethod from_mapping. Поддержи subclass и проверь positive id/non-empty email.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **`classmethod` and `staticmethod`**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
