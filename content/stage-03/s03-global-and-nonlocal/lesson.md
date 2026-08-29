# `global` and `nonlocal`

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`global` and `nonlocal`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `rebinding`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**rebinding.** Binding — связь имени с объектом в namespace; assignment меняет связь имени, а mutation меняет состояние уже связанного объекта.

**enclosing state.** `enclosing state` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**why mutable global state is risky in backend services.** Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `rebinding` и `enclosing state` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- rebinding
- enclosing state
- why mutable global state is risky in backend services

### Полезно

- связать `global` and `nonlocal` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `global` and `nonlocal`: отдельный пример

```python
attempts = 0

def make_counter():
    count = 0
    def next_value():
        nonlocal count
        count += 1
        return count
    return next_value

counter = make_counter()
print(counter(), counter())
```

`nonlocal` меняет ближайший enclosing binding; global state для независимого counter не требуется.

## Common mistakes

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `rebinding` до запуска.

**B · Find the bug.** Найди нарушение `enclosing state` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `global` and `nonlocal` за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое `global` and `nonlocal` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `global` and `nonlocal`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`global` and `nonlocal`: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный Junior answer

> `global` and `nonlocal` — тема, в которой я сначала фиксирую `rebinding`, затем объясняю `enclosing state` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `global` and `nonlocal`?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Expected answer rubric

### Must mention

- rebinding
- enclosing state
- why mutable global state is risky in backend services

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `global` and `nonlocal`?

## Задача

Сделай короткую письменную практику по теме **`global` and `nonlocal`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `global` and `nonlocal`: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
