# Late binding

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Late binding**, а не только запомнить термин;
- прочитать и изменить короткий пример для `closures inside loop`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**closures inside loop.** Closure хранит ссылки на enclosing bindings, а не snapshot каждого значения; late binding особенно заметен в callbacks, созданных в цикле.

**lambdas.** `lambdas` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**lookup at call time.** `lookup at call time` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**fix through default argument.** `fix through default argument` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**factory function.** `factory function` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**`functools.partial`.** ``functools.partial`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `closures inside loop` и `lambdas` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- closures inside loop
- lambdas
- lookup at call time
- fix through default argument

### Полезно

- factory function
- `functools.partial`

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Late binding: отдельный пример

```python
bad = [lambda: value for value in range(3)]
good = [lambda value=value: value for value in range(3)]

print([fn() for fn in bad])
print([fn() for fn in good])
```

Late binding разрешает free variable при вызове; default argument фиксирует значение при создании lambda.

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `closures inside loop` до запуска.

**B · Find the bug.** Найди нарушение `lambdas` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Late binding за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Late binding в цикле

```python
funcs = [lambda: i for i in range(3)]
print([fn() for fn in funcs])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[2, 2, 2]
```

Свободное имя i разрешается при вызове; после цикла оно равно 2.

Misconception: `late-binding`.

</details>

## Debugging practice

### Late closure

**Сценарий:** Callbacks из цикла используют последнее id.

**Rubric:** Free name resolved at call time; bind default/factory.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Late binding и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Late binding?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Late binding: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> Late binding — тема, в которой я сначала фиксирую `closures inside loop`, затем объясняю `lambdas` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Late binding?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- closures inside loop
- lambdas
- lookup at call time
- fix through default argument

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Late binding?

## Задача

### Исправить late binding

Верни функции, каждая умножает аргумент на собственный multiplier из входа.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Late binding: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
