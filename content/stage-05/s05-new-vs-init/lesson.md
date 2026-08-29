# `__new__` vs `__init__`

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`__new__` vs `__init__`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `object creation vs initialization`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**object creation vs initialization.** `object creation vs initialization` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**immutable subclasses.** Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.

**avoid unnecessary custom `__new__`.** `avoid unnecessary custom `__new__`` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `object creation vs initialization` и `immutable subclasses` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- object creation vs initialization
- immutable subclasses
- avoid unnecessary custom `__new__`

### Полезно

- связать `__new__` vs `__init__` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `__new__` vs `__init__`: отдельный пример

```python
class PositiveInt(int):
    def __new__(cls, value):
        parsed = int(value)
        if parsed <= 0:
            raise ValueError("positive value required")
        return super().__new__(cls, parsed)

print(PositiveInt("7"))
```

Для immutable base создание и validation значения выполняют в `__new__`; `__init__` уже получает созданный объект.

## Common mistakes

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `object creation vs initialization` до запуска.

**B · Find the bug.** Найди нарушение `immutable subclasses` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `__new__` vs `__init__` за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое `__new__` vs `__init__` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `__new__` vs `__init__`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`__new__` vs `__init__`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> `__new__` vs `__init__` — тема, в которой я сначала фиксирую `object creation vs initialization`, затем объясняю `immutable subclasses` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `__new__` vs `__init__`?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- object creation vs initialization
- immutable subclasses
- avoid unnecessary custom `__new__`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `__new__` vs `__init__`?

## Задача

Сделай короткую письменную практику по теме **`__new__` vs `__init__`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `__new__` vs `__init__`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
