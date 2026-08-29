# Abstract base classes

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Abstract base classes**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``ABC``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**`ABC`.** ``ABC`` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**`abstractmethod`.** ``abstractmethod`` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**contract.** `contract` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**ABC vs Protocol.** `Protocol` задаёт structural contract: объект подходит по доступным методам и атрибутам, даже без наследования от общего base class.

**repository interface example.** `repository interface example` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``ABC`` и ``abstractmethod`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `ABC`
- `abstractmethod`
- contract
- ABC vs Protocol

### Полезно

- repository interface example

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Abstract base classes: отдельный пример

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get(self, item_id): ...

class MemoryRepository(Repository):
    def get(self, item_id):
        return {"id": item_id}

print(MemoryRepository().get(1))
```

ABC запрещает создать неполную реализацию и документирует nominal interface.

## Common mistakes

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``ABC`` до запуска.

**B · Find the bug.** Найди нарушение ``abstractmethod`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Abstract base classes за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Abstract base classes и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Abstract base classes?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Abstract base classes: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> Abstract base classes — тема, в которой я сначала фиксирую ``ABC``, затем объясняю ``abstractmethod`` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Abstract base classes?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- `ABC`
- `abstractmethod`
- contract
- ABC vs Protocol

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Abstract base classes?

## Задача

Сделай короткую письменную практику по теме **Abstract base classes**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Abstract base classes: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
