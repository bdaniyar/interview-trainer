# Decorator factory and decorator arguments

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Decorator factory and decorator arguments**, а не только запомнить термин;
- прочитать и изменить короткий пример для `three levels of functions`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**three levels of functions.** `three levels of functions` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**конфигурация, захваченная замыканием.** Closure хранит ссылки на enclosing bindings, а не snapshot каждого значения; late binding особенно заметен в callbacks, созданных в цикле.

**retry/timing/permission examples.** Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `three levels of functions` и `configuration captured by closure` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- three levels of functions
- конфигурация, захваченная замыканием
- retry/timing/permission examples

### Полезно

- связать Decorator factory and decorator arguments с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

Decorator factory сначала фиксирует конфигурацию, затем получает функцию и строит wrapper.

## Типичные ошибки

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `three levels of functions` до запуска.

**B · Найди ошибку.** Найди нарушение `configuration captured by closure` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Decorator factory and decorator arguments за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Decorator factory and decorator arguments и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Decorator factory and decorator arguments?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Decorator factory and decorator arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный ответ уровня Junior

> Decorator factory and decorator arguments — тема, в которой я сначала фиксирую `three levels of functions`, затем объясняю `configuration captured by closure` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Decorator factory and decorator arguments?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Критерии хорошего ответа

### Что обязательно упомянуть

- three levels of functions
- конфигурация, захваченная замыканием
- retry/timing/permission examples

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Decorator factory and decorator arguments?

## Задача

### Retry decorator

Реализуй retry(attempts, exceptions, on_retry). Повторяй только указанные errors, вызови hook перед retry и подними последнюю ошибку.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Decorator factory and decorator arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
