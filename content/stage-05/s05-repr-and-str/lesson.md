# `__repr__` and `__str__`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`__repr__` and `__str__`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `debugging representation`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**debugging representation.** `debugging representation` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**user-facing text.** `user-facing text` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**unambiguous repr.** `unambiguous repr` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**avoiding secrets in logs.** `avoiding secrets in logs` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `debugging representation` и `user-facing text` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- debugging representation
- user-facing text
- unambiguous repr
- avoiding secrets in logs

### Полезно

- связать `__repr__` and `__str__` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `__repr__` and `__str__`: отдельный пример

```python
class User:
    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return f"User(email={self.email!r})"

    def __str__(self):
        return self.email

user = User("a@example.com")
print(str(user), repr(user))
```

`__repr__` помогает разработчику и отладке, `__str__` даёт удобное пользовательское представление.

## Common mistakes

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `debugging representation` до запуска.

**B · Find the bug.** Найди нарушение `user-facing text` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `__repr__` and `__str__` за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое `__repr__` and `__str__` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `__repr__` and `__str__`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`__repr__` and `__str__`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> `__repr__` and `__str__` — тема, в которой я сначала фиксирую `debugging representation`, затем объясняю `user-facing text` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `__repr__` and `__str__`?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- debugging representation
- user-facing text
- unambiguous repr
- avoiding secrets in logs

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `__repr__` and `__str__`?

## Задача

Сделай короткую письменную практику по теме **`__repr__` and `__str__`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `__repr__` and `__str__`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
