# Positional-only and keyword-only parameters

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Positional-only and keyword-only parameters**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``/``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**`/`.** ``/`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**`*`.** ``*`` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**API design.** `API design` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**readable signatures.** Signature — публичный контракт вызова: kinds параметров, defaults и annotations определяют допустимые positional/keyword arguments и помогают introspection.

**backward compatibility.** `backward compatibility` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``/`` и ``*`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `/`
- `*`
- API design
- readable signatures

### Полезно

- backward compatibility

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Positional-only and keyword-only parameters: отдельный пример

```python
def paginate(resource, /, *, limit=20, offset=0):
    return resource[offset : offset + limit]

print(paginate([1, 2, 3], limit=2))
```

`resource` скрывает имя positional-only параметра, а параметры pagination требуют явных keywords.

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``/`` до запуска.

**B · Find the bug.** Найди нарушение ``*`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Positional-only and keyword-only parameters за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Keyword-only argument

```python
def page(limit, *, offset=0):
    return limit, offset
print(page(10, offset=20))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
(10, 20)
```

Параметр после * можно передать только по имени, что делает API вызова явным.

Misconception: `keyword-only`.

</details>

## Interview questions

### Основной вопрос

Что такое Positional-only and keyword-only parameters и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Positional-only and keyword-only parameters?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Positional-only and keyword-only parameters: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> Positional-only and keyword-only parameters — тема, в которой я сначала фиксирую ``/``, затем объясняю ``*`` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Positional-only and keyword-only parameters?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- `/`
- `*`
- API design
- readable signatures

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Positional-only and keyword-only parameters?

## Задача

### Явная сигнатура pagination helper

Реализуй build_page_query: resource positional-only; limit и offset keyword-only. Проверь resource, limit 1..100 и offset >= 0.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Positional-only and keyword-only parameters: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
