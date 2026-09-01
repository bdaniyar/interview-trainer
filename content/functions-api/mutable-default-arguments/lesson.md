# Default arguments

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; functions/scope/decorators регулярно проверяют на screening.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Default arguments**, а не только запомнить термин;
- прочитать и изменить короткий пример для `evaluation at function definition`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Как работает

Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.

**вычисление в момент определения функции.** `evaluation at function definition` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**mutable default bug.** Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.

**sentinel pattern.** `sentinel pattern` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.

**`None` pattern and its limitations.** ``None` pattern and its limitations` влияет на function contract; результат определяется definition time, argument binding при вызове и разрешением names.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `evaluation at function definition` и `mutable default bug` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- вычисление в момент определения функции
- mutable default bug
- sentinel pattern
- `None` pattern and its limitations

### Полезно

- связать Default arguments с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

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

## Типичные ошибки

### Ошибка 1

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `evaluation at function definition` до запуска.

**B · Найди ошибку.** Найди нарушение `mutable default bug` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Default arguments за 60 секунд: определение, механизм, пример, ограничение.

## Предсказание результата кода

### Default вычисляется один раз

```python
def add(value, bucket=[]):
    bucket.append(value)
    return bucket

print(add(1), add(2))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Ожидаемый результат:

```text
[1] [1, 2]
```

Mutable default создаётся при выполнении def и переиспользуется следующими вызовами.

Типичная ошибка мышления: `mutable-default`.

</details>

## Практика: Отладка

### Mutable default

**Сценарий:** Список tags растёт между независимыми вызовами.

**Критерии ответа:** Default создаётся при def; None/sentinel и новый list; тест на два вызова.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Default arguments и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Default arguments?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Default arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.

### Нормальный ответ уровня Junior

> Default arguments — тема, в которой я сначала фиксирую `evaluation at function definition`, затем объясняю `mutable default bug` на коротком примере. Ключевой механизм: Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB. Главная практическая ошибка — Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Default arguments?**

Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.

## Критерии хорошего ответа

### Что обязательно упомянуть

- вычисление в момент определения функции
- mutable default bug
- sentinel pattern
- `None` pattern and its limitations

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Default arguments?

## Задача

Сделай короткую письменную практику по теме **Default arguments**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Default arguments: Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.
- **Механизм:** Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.
- **Ограничение:** Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python function definitions](https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions)
- [functools](https://docs.python.org/3.12/library/functools.html)

Последняя проверка версий: **2026-08-27**.
