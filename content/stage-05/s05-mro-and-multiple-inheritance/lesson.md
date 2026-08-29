# MRO and multiple inheritance

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **MRO and multiple inheritance**, а не только запомнить термин;
- прочитать и изменить короткий пример для `C3 linearization intuition`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**C3 linearization intuition.** `C3 linearization intuition` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**`Class.__mro__`.** MRO задаёт детерминированный порядок поиска атрибутов при multiple inheritance; `super()` продолжает поиск по MRO фактического класса.

**diamond problem.** `diamond problem` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**cooperative `super`.** `cooperative `super`` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**common interview predictions.** `dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `C3 linearization intuition` и ``Class.__mro__`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- C3 linearization intuition
- `Class.__mro__`
- diamond problem
- cooperative `super`

### Полезно

- common interview predictions

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### MRO and multiple inheritance: отдельный пример

```python
class TraceMixin:
    def handle(self):
        return ["trace", *super().handle()]

class Handler:
    def handle(self):
        return ["handler"]

class ApiHandler(TraceMixin, Handler):
    pass

print(ApiHandler.__mro__)
print(ApiHandler().handle())
```

Cooperative `super()` следует MRO `ApiHandler → TraceMixin → Handler`, а не жёстко названному parent.

## Common mistakes

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `C3 linearization intuition` до запуска.

**B · Find the bug.** Найди нарушение ``Class.__mro__`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про MRO and multiple inheritance за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое MRO and multiple inheritance и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме MRO and multiple inheritance?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

MRO and multiple inheritance: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> MRO and multiple inheritance — тема, в которой я сначала фиксирую `C3 linearization intuition`, затем объясняю ``Class.__mro__`` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме MRO and multiple inheritance?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- C3 linearization intuition
- `Class.__mro__`
- diamond problem
- cooperative `super`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме MRO and multiple inheritance?

## Задача

Сделай короткую письменную практику по теме **MRO and multiple inheritance**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** MRO and multiple inheritance: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
