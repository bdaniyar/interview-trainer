# Multiple decorators and order

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Multiple decorators and order**, а не только запомнить термин;
- прочитать и изменить короткий пример для `application bottom-up`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**application bottom-up.** `application bottom-up` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**execution nesting.** `execution nesting` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**prediction tasks.** `dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `application bottom-up` и `execution nesting` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- application bottom-up
- execution nesting
- prediction tasks

### Полезно

- связать Multiple decorators and order с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

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

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `application bottom-up` до запуска.

**B · Find the bug.** Найди нарушение `execution nesting` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Multiple decorators and order за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Multiple decorators and order и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Multiple decorators and order?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Multiple decorators and order: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> Multiple decorators and order — тема, в которой я сначала фиксирую `application bottom-up`, затем объясняю `execution nesting` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Multiple decorators and order?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- application bottom-up
- execution nesting
- prediction tasks

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Multiple decorators and order?

## Задача

Сделай короткую письменную практику по теме **Multiple decorators and order**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Multiple decorators and order: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
