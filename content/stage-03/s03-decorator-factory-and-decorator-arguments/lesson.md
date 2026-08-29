# Decorator factory and decorator arguments

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Decorator factory and decorator arguments**, а не только запомнить термин;
- прочитать и изменить короткий пример для `three levels of functions`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**three levels of functions.** `three levels of functions` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**configuration captured by closure.** Closure хранит ссылки на enclosing bindings, а не snapshot каждого значения; late binding особенно заметен в callbacks, созданных в цикле.

**retry/timing/permission examples.** Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `three levels of functions` и `configuration captured by closure` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- three levels of functions
- configuration captured by closure
- retry/timing/permission examples

### Полезно

- связать Decorator factory and decorator arguments с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Decorator factory and decorator arguments: отдельный пример

```python
def retry(*, attempts):
    def decorate(function):
        def wrapper(*args, **kwargs):
            for number in range(attempts):
                try:
                    return function(*args, **kwargs)
                except TimeoutError:
                    if number + 1 == attempts:
                        raise
        return wrapper
    return decorate
```

Decorator factory сначала фиксирует configuration, затем получает функцию и строит wrapper.

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `three levels of functions` до запуска.

**B · Find the bug.** Найди нарушение `configuration captured by closure` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Decorator factory and decorator arguments за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Decorator factory and decorator arguments и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Decorator factory and decorator arguments?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Decorator factory and decorator arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> Decorator factory and decorator arguments — тема, в которой я сначала фиксирую `three levels of functions`, затем объясняю `configuration captured by closure` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Decorator factory and decorator arguments?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- three levels of functions
- configuration captured by closure
- retry/timing/permission examples

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Decorator factory and decorator arguments?

## Задача

### Retry decorator

Реализуй retry(attempts, exceptions, on_retry). Повторяй только указанные errors, вызови hook перед retry и подними последнюю ошибку.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Decorator factory and decorator arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
