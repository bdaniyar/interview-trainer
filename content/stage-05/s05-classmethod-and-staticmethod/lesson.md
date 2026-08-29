# `classmethod` and `staticmethod`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`classmethod` and `staticmethod`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `alternate constructors`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**alternate constructors.** `alternate constructors` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**class-aware behavior.** `class-aware behavior` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**namespace utility.** `namespace utility` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**when module-level function is simpler.** `when module-level function is simpler` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `alternate constructors` и `class-aware behavior` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- alternate constructors
- class-aware behavior
- namespace utility
- when module-level function is simpler

### Полезно

- связать `classmethod` and `staticmethod` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

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

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `alternate constructors` до запуска.

**B · Find the bug.** Найди нарушение `class-aware behavior` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `classmethod` and `staticmethod` за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое `classmethod` and `staticmethod` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `classmethod` and `staticmethod`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`classmethod` and `staticmethod`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> `classmethod` and `staticmethod` — тема, в которой я сначала фиксирую `alternate constructors`, затем объясняю `class-aware behavior` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `classmethod` and `staticmethod`?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- alternate constructors
- class-aware behavior
- namespace utility
- when module-level function is simpler

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `classmethod` and `staticmethod`?

## Задача

### Создать User из mapping

Реализуй staticmethod normalize_email и classmethod from_mapping. Поддержи subclass и проверь positive id/non-empty email.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `classmethod` and `staticmethod`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
