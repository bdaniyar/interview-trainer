# Positional-only and keyword-only parameters

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Positional-only and keyword-only parameters**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``/``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**`/`.** ``/`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**`*`.** ``*`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**API design.** `API design` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**readable signatures.** Signature — публичный контракт вызова: kinds параметров, defaults и annotations определяют допустимые positional/keyword arguments и помогают introspection.

**обратная совместимость.** `backward compatibility` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй ``/`` и ``*`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- `/`
- `*`
- API design
- readable signatures

### Полезно

- обратная совместимость

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Positional-only and keyword-only parameters: отдельный пример

```python
def paginate(resource, /, *, limit=20, offset=0):
    return resource[offset : offset + limit]

print(paginate([1, 2, 3], limit=2))
```

`resource` скрывает имя positional-only параметра, а параметры pagination требуют явных keywords.

## Типичные ошибки

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для ``/`` до запуска.

**B · Найди ошибку.** Найди нарушение ``*`` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Positional-only and keyword-only parameters за 60 секунд: определение, механизм, пример, ограничение.

## Предсказание результата кода

### Keyword-only argument

```python
def page(limit, *, offset=0):
    return limit, offset
print(page(10, offset=20))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Ожидаемый результат:

```text
(10, 20)
```

Параметр после * можно передать только по имени, что делает API вызова явным.

Типичная ошибка мышления: `keyword-only`.

</details>

## Вопросы с собеседований

### Основной вопрос

Что такое Positional-only and keyword-only parameters и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Positional-only and keyword-only parameters?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Positional-only and keyword-only parameters: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный ответ уровня Junior

> Positional-only and keyword-only parameters — тема, в которой я сначала фиксирую ``/``, затем объясняю ``*`` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Positional-only and keyword-only parameters?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Критерии хорошего ответа

### Что обязательно упомянуть

- `/`
- `*`
- API design
- readable signatures

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Positional-only and keyword-only parameters?

## Задача

### Явная сигнатура pagination helper

Реализуй build_page_query: resource positional-only; limit и offset keyword-only. Проверь resource, limit 1..100 и offset >= 0.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Positional-only and keyword-only parameters: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
