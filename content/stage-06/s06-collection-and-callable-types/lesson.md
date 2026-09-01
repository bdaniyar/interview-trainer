# Collection and callable types

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Collection and callable types**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``list[str]``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Как работает

Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation.

**`list[str]`.** `list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

**`dict[str, int]`.** `dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.

**`Sequence`.** ``Sequence`` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.

**`Iterable`.** Iterable умеет создать iterator через `__iter__`; один iterable может создавать новые независимые iterators для повторных обходов.

**`Callable`.** ``Callable`` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй ``list[str]`` и ``dict[str, int]`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- `list[str]`
- `dict[str, int]`
- `Sequence`
- `Iterable`

### Полезно

- `Callable`

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Collection and callable types: отдельный пример

```python
from collections.abc import Callable, Iterable

def transform(values: Iterable[int], operation: Callable[[int], str]) -> list[str]:
    return [operation(value) for value in values]

print(transform((1, 2), lambda value: f"id:{value}"))
```

Types описывают не конкретный list/function, а iterable input и связь callable input/output.

## Типичные ошибки

### Ошибка 1

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для ``list[str]`` до запуска.

**B · Найди ошибку.** Найди нарушение ``dict[str, int]`` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Collection and callable types за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Collection and callable types и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Collection and callable types?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Collection and callable types: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Нормальный ответ уровня Junior

> Collection and callable types — тема, в которой я сначала фиксирую ``list[str]``, затем объясняю ``dict[str, int]`` на коротком примере. Ключевой механизм: Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation. Главная практическая ошибка — Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Collection and callable types?**

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Критерии хорошего ответа

### Что обязательно упомянуть

- `list[str]`
- `dict[str, int]`
- `Sequence`
- `Iterable`

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Collection and callable types?

## Задача

Сделай короткую письменную практику по теме **Collection and callable types**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Collection and callable types: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.
- **Механизм:** Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.
- **Ограничение:** Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
