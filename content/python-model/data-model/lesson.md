# `__len__`, `__bool__`, `__contains__`, `__getitem__`

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`__len__`, `__bool__`, `__contains__`, `__getitem__`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `protocol-driven behavior`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**protocol-driven behavior.** `Protocol` задаёт structural contract: объект подходит по доступным методам и атрибутам, даже без наследования от общего base class.

**truthiness.** Truthiness определяется `__bool__`, затем `__len__`, а при отсутствии обоих объект считается truthy; это протокол, не проверка типа.

**membership.** `membership` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**indexing/iteration fallback.** Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `protocol-driven behavior` и `truthiness` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- protocol-driven behavior
- truthiness
- membership
- indexing/iteration fallback

### Полезно

- связать `__len__`, `__bool__`, `__contains__`, `__getitem__` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `__len__`, `__bool__`, `__contains__`, `__getitem__`: отдельный пример

```python
class Page:
    def __init__(self, items):
        self.items = tuple(items)

    def __len__(self): return len(self.items)
    def __bool__(self): return bool(self.items)
    def __contains__(self, item): return item in self.items
    def __getitem__(self, index): return self.items[index]

page = Page([10, 20])
print(len(page), bool(page), 20 in page, page[0])
```

Набор dunder methods подключает объект к независимым Python protocols длины, truthiness, membership и indexing.

## Common mistakes

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `protocol-driven behavior` до запуска.

**B · Find the bug.** Найди нарушение `truthiness` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `__len__`, `__bool__`, `__contains__`, `__getitem__` за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Property управляет записью

```python
class Score:
    def __init__(self): self._value = 0
    @property
    def value(self): return self._value
    @value.setter
    def value(self, value): self._value = max(0, value)
s = Score(); s.value = -3
print(s.value)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
0
```

Assignment проходит через property setter, который сохраняет нормализованное значение.

Misconception: `descriptor-property`.

</details>

## Interview questions

### Основной вопрос

Что такое `__len__`, `__bool__`, `__contains__`, `__getitem__` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `__len__`, `__bool__`, `__contains__`, `__getitem__`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`__len__`, `__bool__`, `__contains__`, `__getitem__`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> `__len__`, `__bool__`, `__contains__`, `__getitem__` — тема, в которой я сначала фиксирую `protocol-driven behavior`, затем объясняю `truthiness` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `__len__`, `__bool__`, `__contains__`, `__getitem__`?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- protocol-driven behavior
- truthiness
- membership
- indexing/iteration fallback

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `__len__`, `__bool__`, `__contains__`, `__getitem__`?

## Задача

Сделай короткую письменную практику по теме **`__len__`, `__bool__`, `__contains__`, `__getitem__`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `__len__`, `__bool__`, `__contains__`, `__getitem__`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
