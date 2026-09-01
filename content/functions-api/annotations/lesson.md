# Function annotations

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Function annotations**, а не только запомнить термин;
- прочитать и изменить короткий пример для `annotations are metadata`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**annotations are metadata.** `annotations are metadata` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**not runtime validation by default.** `not runtime validation by default` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**связь с FastAPI и Pydantic.** `relationship with FastAPI/Pydantic` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**return annotations.** `return annotations` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `annotations are metadata` и `not runtime validation by default` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- annotations are metadata
- not runtime validation by default
- связь с FastAPI и Pydantic
- return annotations

### Полезно

- связать Function annotations с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Function annotations: отдельный пример

```python
def find_user(user_id: int) -> dict[str, object] | None:
    return None

print(find_user.__annotations__)
print(find_user("runtime is still dynamic"))
```

Annotations доступны инструментам и runtime introspection, но сами не запрещают неверный тип аргумента.

## Типичные ошибки

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `annotations are metadata` до запуска.

**B · Найди ошибку.** Найди нарушение `not runtime validation by default` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Function annotations за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Function annotations и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Function annotations?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Function annotations: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный ответ уровня Junior

> Function annotations — тема, в которой я сначала фиксирую `annotations are metadata`, затем объясняю `not runtime validation by default` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Function annotations?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Критерии хорошего ответа

### Что обязательно упомянуть

- annotations are metadata
- not runtime validation by default
- связь с FastAPI и Pydantic
- return annotations

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Function annotations?

## Задача

Сделай короткую письменную практику по теме **Function annotations**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Function annotations: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
