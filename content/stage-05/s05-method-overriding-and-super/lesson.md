# Method overriding and `super()`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Method overriding and `super()`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `cooperative calls`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Как работает

Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.

**cooperative calls.** `cooperative calls` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**avoiding direct parent naming.** `avoiding direct parent naming` определяет, где хранится object state, как идёт attribute lookup и насколько сильно тип зависит от collaborators.

**inheritance chains.** Inheritance выражает отношение is-a и участвует в MRO; если нужно только переиспользовать collaborator, composition обычно делает зависимость яснее.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `cooperative calls` и `avoiding direct parent naming` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- cooperative calls
- avoiding direct parent naming
- inheritance chains

### Полезно

- связать Method overriding and `super()` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Method overriding and `super()`: отдельный пример

```python
class Serializer:
    def dump(self, value):
        return str(value)

class JsonSerializer(Serializer):
    def dump(self, value):
        base = super().dump(value)
        return f'{{"value": "{base}"}}'

print(JsonSerializer().dump(7))
```

Override заменяет behavior, а `super()` продолжает реализацию по MRO.

## Common mistakes

### Ошибка 1

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `cooperative calls` до запуска.

**B · Find the bug.** Найди нарушение `avoiding direct parent naming` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Method overriding and `super()` за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Method overriding and `super()` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Method overriding and `super()`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Method overriding and `super()`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.

### Нормальный Junior answer

> Method overriding and `super()` — тема, в которой я сначала фиксирую `cooperative calls`, затем объясняю `avoiding direct parent naming` на коротком примере. Ключевой механизм: Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами. Главная практическая ошибка — Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Method overriding and `super()`?**

Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.

## Expected answer rubric

### Must mention

- cooperative calls
- avoiding direct parent naming
- inheritance chains

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Method overriding and `super()`?

## Задача

Сделай короткую письменную практику по теме **Method overriding and `super()`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Method overriding and `super()`: Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
