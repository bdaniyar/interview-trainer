# Instance vs class attributes

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Instance vs class attributes**, а не только запомнить термин;
- прочитать и изменить короткий пример для `shared mutable class attribute bug`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**ошибка общего изменяемого атрибута класса.** Class attribute разделяется instances до тех пор, пока instance не перекроет имя; mutable class state часто создаёт утечку между объектами.

**shadowing.** `shadowing` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**appropriate constants/config.** `appropriate constants/config` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `shared mutable class attribute bug` и `shadowing` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- ошибка общего изменяемого атрибута класса
- shadowing
- appropriate constants/config

### Полезно

- связать Instance vs class attributes с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `shared mutable class attribute bug` до запуска.

**B · Найди ошибку.** Найди нарушение `shadowing` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Instance vs class attributes за 60 секунд: определение, механизм, пример, ограничение.

## Предсказание результата кода

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

Ожидаемый результат:

```text
['admin']
```

До instance assignment оба объекта находят один mutable class attribute.

Типичная ошибка мышления: `class-attribute`.

</details>

## Практика: Отладка

### Shared class state

**Сценарий:** roles=[] class attribute делится между instances.

**Критерии ответа:** Mutable instance state создавать в __init__/default_factory.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Instance vs class attributes и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Instance vs class attributes?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Instance vs class attributes: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный ответ уровня Junior

> Instance vs class attributes — тема, в которой я сначала фиксирую `shared mutable class attribute bug`, затем объясняю `shadowing` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Instance vs class attributes?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Критерии хорошего ответа

### Что обязательно упомянуть

- ошибка общего изменяемого атрибута класса
- shadowing
- appropriate constants/config

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Instance vs class attributes?

## Задача

Сделай короткую письменную практику по теме **Instance vs class attributes**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Instance vs class attributes: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
