# Parameters vs arguments

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Parameters vs arguments**, а не только запомнить термин;
- прочитать и изменить короткий пример для `parameter`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**parameter.** `parameter` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**argument.** `argument` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**positional.** `positional` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**keyword.** `keyword` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**binding process.** Binding — связь имени с объектом в namespace; assignment меняет связь имени, а mutation меняет состояние уже связанного объекта.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `parameter` и `argument` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- parameter
- argument
- positional
- keyword

### Полезно

- binding process

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Parameters vs arguments: отдельный пример

```python
def create_user(email, active=True):
    return {"email": email, "active": active}

user = create_user("a@example.com", active=False)
print(user)
```

`email` и `active` — parameters определения; переданные значения — arguments конкретного вызова.

## Типичные ошибки

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `parameter` до запуска.

**B · Найди ошибку.** Найди нарушение `argument` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Parameters vs arguments за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Parameters vs arguments и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Parameters vs arguments?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Parameters vs arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный ответ уровня Junior

> Parameters vs arguments — тема, в которой я сначала фиксирую `parameter`, затем объясняю `argument` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Parameters vs arguments?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Критерии хорошего ответа

### Что обязательно упомянуть

- parameter
- argument
- positional
- keyword

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Parameters vs arguments?

## Задача

Сделай короткую письменную практику по теме **Parameters vs arguments**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Parameters vs arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
