# Function annotations

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Function annotations**, а не только запомнить термин;
- прочитать и изменить короткий пример для `annotations are metadata`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**annotations are metadata.** `annotations are metadata` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**not runtime validation by default.** `not runtime validation by default` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**relationship with FastAPI/Pydantic.** `relationship with FastAPI/Pydantic` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**return annotations.** `return annotations` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `annotations are metadata` и `not runtime validation by default` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- annotations are metadata
- not runtime validation by default
- relationship with FastAPI/Pydantic
- return annotations

### Полезно

- связать Function annotations с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Function annotations: отдельный пример

```python
def find_user(user_id: int) -> dict[str, object] | None:
    return None

print(find_user.__annotations__)
print(find_user("runtime is still dynamic"))
```

Annotations доступны инструментам и runtime introspection, но сами не запрещают неверный тип аргумента.

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `annotations are metadata` до запуска.

**B · Find the bug.** Найди нарушение `not runtime validation by default` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Function annotations за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Function annotations и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Function annotations?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Function annotations: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> Function annotations — тема, в которой я сначала фиксирую `annotations are metadata`, затем объясняю `not runtime validation by default` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Function annotations?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- annotations are metadata
- not runtime validation by default
- relationship with FastAPI/Pydantic
- return annotations

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Function annotations?

## Задача

Сделай короткую письменную практику по теме **Function annotations**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Function annotations: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
