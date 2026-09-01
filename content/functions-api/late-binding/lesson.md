# Late binding

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Late binding**, а не только запомнить термин;
- прочитать и изменить короткий пример для `closures inside loop`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

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


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `closures inside loop` и `lambdas` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

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

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Late binding: отдельный пример

```python
bad = [lambda: value for value in range(3)]
good = [lambda value=value: value for value in range(3)]

print([fn() for fn in bad])
print([fn() for fn in good])
```

Late binding разрешает free variable при вызове; default argument фиксирует значение при создании lambda.

## Типичные ошибки

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `closures inside loop` до запуска.

**B · Найди ошибку.** Найди нарушение `lambdas` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Late binding за 60 секунд: определение, механизм, пример, ограничение.

## Предсказание результата кода

### Late binding в цикле

```python
funcs = [lambda: i for i in range(3)]
print([fn() for fn in funcs])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Ожидаемый результат:

```text
[2, 2, 2]
```

Свободное имя i разрешается при вызове; после цикла оно равно 2.

Типичная ошибка мышления: `late-binding`.

</details>

## Практика: Отладка

### Late closure

**Сценарий:** Callbacks из цикла используют последнее id.

**Критерии ответа:** Free name resolved at call time; bind default/factory.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Late binding и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Late binding?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Late binding: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный ответ уровня Junior

> Late binding — тема, в которой я сначала фиксирую `closures inside loop`, затем объясняю `lambdas` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Late binding?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Критерии хорошего ответа

### Что обязательно упомянуть

- closures inside loop
- lambdas
- lookup at call time
- fix through default argument

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Late binding?

## Задача

### Исправить late binding

Верни функции, каждая умножает аргумент на собственный multiplier из входа.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Late binding: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
