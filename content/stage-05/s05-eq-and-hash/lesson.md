# `__eq__` and `__hash__`

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`__eq__` and `__hash__`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `equality contract`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**equality contract.** `equality contract` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**hash consistency.** Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе.

**mutable fields.** Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.

**dataclass behavior.** `dataclass` генерирует init/repr/equality по объявленным fields; mutable defaults задают через `default_factory`, а invariants — в `__post_init__`.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `equality contract` и `hash consistency` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- equality contract
- hash consistency
- mutable fields
- dataclass behavior

### Полезно

- связать `__eq__` and `__hash__` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `__eq__` and `__hash__`: отдельный пример

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class UserId:
    value: int

left, right = UserId(7), UserId(7)
print(left == right)
print({left: "Aida"}[right])
```

Равные immutable value objects имеют согласованные equality и hash и безопасны как dict keys.

## Common mistakes

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `equality contract` до запуска.

**B · Find the bug.** Найди нарушение `hash consistency` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `__eq__` and `__hash__` за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Broken hash

**Сценарий:** Mutable field участвует в __hash__, set не находит object.

**Rubric:** Hash/equality contract; immutable key or unhashable entity.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое `__eq__` and `__hash__` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `__eq__` and `__hash__`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`__eq__` and `__hash__`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> `__eq__` and `__hash__` — тема, в которой я сначала фиксирую `equality contract`, затем объясняю `hash consistency` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `__eq__` and `__hash__`?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- equality contract
- hash consistency
- mutable fields
- dataclass behavior

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `__eq__` and `__hash__`?

## Задача

Сделай короткую письменную практику по теме **`__eq__` and `__hash__`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `__eq__` and `__hash__`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
