# Parameters vs arguments

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Parameters vs arguments**, а не только запомнить термин;
- прочитать и изменить короткий пример для `parameter`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**parameter.** `parameter` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**argument.** `argument` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**positional.** `positional` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**keyword.** `keyword` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**binding process.** Binding — связь имени с объектом в namespace; assignment меняет связь имени, а mutation меняет состояние уже связанного объекта.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `parameter` и `argument` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- parameter
- argument
- positional
- keyword

### Полезно

- binding process

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Parameters vs arguments: отдельный пример

```python
def create_user(email, active=True):
    return {"email": email, "active": active}

user = create_user("a@example.com", active=False)
print(user)
```

`email` и `active` — parameters определения; переданные значения — arguments конкретного вызова.

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `parameter` до запуска.

**B · Find the bug.** Найди нарушение `argument` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Parameters vs arguments за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Parameters vs arguments и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Parameters vs arguments?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Parameters vs arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> Parameters vs arguments — тема, в которой я сначала фиксирую `parameter`, затем объясняю `argument` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Parameters vs arguments?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- parameter
- argument
- positional
- keyword

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Parameters vs arguments?

## Задача

Сделай короткую письменную практику по теме **Parameters vs arguments**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Parameters vs arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
