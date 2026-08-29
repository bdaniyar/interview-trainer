# Default arguments

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Default arguments**, а не только запомнить термин;
- прочитать и изменить короткий пример для `evaluation at function definition`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**evaluation at function definition.** `evaluation at function definition` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**mutable default bug.** Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.

**sentinel pattern.** `sentinel pattern` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**`None` pattern and its limitations.** ``None` pattern and its limitations` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `evaluation at function definition` и `mutable default bug` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- evaluation at function definition
- mutable default bug
- sentinel pattern
- `None` pattern and its limitations

### Полезно

- связать Default arguments с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Default arguments: отдельный пример

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags

print(add_tag("python"))
print(add_tag("sql"))
```

Sentinel/default `None` создаёт новый mutable list на каждый вызов и исключает shared state.

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `evaluation at function definition` до запуска.

**B · Find the bug.** Найди нарушение `mutable default bug` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Default arguments за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Default вычисляется один раз

```python
def add(value, bucket=[]):
    bucket.append(value)
    return bucket

print(add(1), add(2))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1] [1, 2]
```

Mutable default создаётся при выполнении def и переиспользуется следующими вызовами.

Misconception: `mutable-default`.

</details>

## Debugging practice

### Mutable default

**Сценарий:** Список tags растёт между независимыми вызовами.

**Rubric:** Default создаётся при def; None/sentinel и новый list; тест на два вызова.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Default arguments и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Default arguments?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Default arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> Default arguments — тема, в которой я сначала фиксирую `evaluation at function definition`, затем объясняю `mutable default bug` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Default arguments?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- evaluation at function definition
- mutable default bug
- sentinel pattern
- `None` pattern and its limitations

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Default arguments?

## Задача

Сделай короткую письменную практику по теме **Default arguments**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Default arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
