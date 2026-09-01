# Multiple decorators and order

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Multiple decorators and order**, а не только запомнить термин;
- прочитать и изменить короткий пример для `application bottom-up`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**application bottom-up.** `application bottom-up` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**execution nesting.** `execution nesting` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**предсказание результата tasks.** `dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `application bottom-up` и `execution nesting` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- application bottom-up
- execution nesting
- предсказание результата tasks

### Полезно

- связать Multiple decorators and order с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Multiple decorators and order: отдельный пример

```python
def mark(name):
    def decorate(function):
        def wrapper():
            return f"{name}({function()})"
        return wrapper
    return decorate

@mark("outer")
@mark("inner")
def value():
    return "core"

print(value())
```

Декораторы применяются снизу вверх, а wrappers вызываются снаружи внутрь.

## Типичные ошибки

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `application bottom-up` до запуска.

**B · Найди ошибку.** Найди нарушение `execution nesting` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Multiple decorators and order за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Multiple decorators and order и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Multiple decorators and order?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Multiple decorators and order: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный ответ уровня Junior

> Multiple decorators and order — тема, в которой я сначала фиксирую `application bottom-up`, затем объясняю `execution nesting` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Multiple decorators and order?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Критерии хорошего ответа

### Что обязательно упомянуть

- application bottom-up
- execution nesting
- предсказание результата tasks

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Multiple decorators and order?

## Задача

Сделай короткую письменную практику по теме **Multiple decorators and order**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Multiple decorators and order: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
