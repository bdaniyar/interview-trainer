# `classmethod` and `staticmethod`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **`classmethod` and `staticmethod`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `alternate constructors`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**alternate constructors.** `alternate constructors` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**class-aware behavior.** `class-aware behavior` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**namespace utility.** `namespace utility` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**когда функция уровня модуля проще.** `when module-level function is simpler` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `alternate constructors` и `class-aware behavior` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- alternate constructors
- class-aware behavior
- namespace utility
- когда функция уровня модуля проще

### Полезно

- связать `classmethod` and `staticmethod` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `alternate constructors` до запуска.

**B · Найди ошибку.** Найди нарушение `class-aware behavior` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про `classmethod` and `staticmethod` за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое `classmethod` and `staticmethod` и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме `classmethod` and `staticmethod`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`classmethod` and `staticmethod`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный ответ уровня Junior

> `classmethod` and `staticmethod` — тема, в которой я сначала фиксирую `alternate constructors`, затем объясняю `class-aware behavior` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме `classmethod` and `staticmethod`?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Критерии хорошего ответа

### Что обязательно упомянуть

- alternate constructors
- class-aware behavior
- namespace utility
- когда функция уровня модуля проще

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме `classmethod` and `staticmethod`?

## Задача

### Создать User из mapping

Реализуй staticmethod normalize_email и classmethod from_mapping. Поддержи subclass и проверь positive id/non-empty email.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `classmethod` and `staticmethod`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
