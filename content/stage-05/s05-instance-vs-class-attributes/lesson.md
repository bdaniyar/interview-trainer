# Instance vs class attributes

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Instance vs class attributes**, а не только запомнить термин;
- прочитать и изменить короткий пример для `shared mutable class attribute bug`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**shared mutable class attribute bug.** Class attribute разделяется instances до тех пор, пока instance не перекроет имя; mutable class state часто создаёт утечку между объектами.

**shadowing.** `shadowing` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**appropriate constants/config.** `appropriate constants/config` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `shared mutable class attribute bug` и `shadowing` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- shared mutable class attribute bug
- shadowing
- appropriate constants/config

### Полезно

- связать Instance vs class attributes с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Instance vs class attributes: отдельный пример

```python
class BadCart:
    items = []

class Cart:
    def __init__(self):
        self.items = []

a, b = Cart(), Cart()
a.items.append(1)
print(b.items)
```

Mutable instance state создают в `__init__`; иначе class attribute разделяется всеми instances.

## Common mistakes

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `shared mutable class attribute bug` до запуска.

**B · Find the bug.** Найди нарушение `shadowing` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Instance vs class attributes за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Class attribute общий

```python
class User:
    roles = []
a = User(); b = User()
a.roles.append('admin')
print(b.roles)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
['admin']
```

До instance assignment оба объекта находят один mutable class attribute.

Misconception: `class-attribute`.

</details>

## Debugging practice

### Shared class state

**Сценарий:** roles=[] class attribute делится между instances.

**Rubric:** Mutable instance state создавать в __init__/default_factory.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Instance vs class attributes и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Instance vs class attributes?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Instance vs class attributes: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> Instance vs class attributes — тема, в которой я сначала фиксирую `shared mutable class attribute bug`, затем объясняю `shadowing` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Instance vs class attributes?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- shared mutable class attribute bug
- shadowing
- appropriate constants/config

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Instance vs class attributes?

## Задача

Сделай короткую письменную практику по теме **Instance vs class attributes**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Instance vs class attributes: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
