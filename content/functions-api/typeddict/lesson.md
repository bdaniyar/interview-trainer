# Literal and TypedDict

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Literal and TypedDict**, а не только запомнить термин;
- прочитать и изменить короткий пример для `constrained literals`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Как работает

Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation.

**constrained literals.** `constrained literals` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.

**typed dictionaries.** `dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.

**JSON-like structures.** `JSON-like structures` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `constrained literals` и `typed dictionaries` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- constrained literals
- typed dictionaries
- JSON-like structures

### Полезно

- связать Literal and TypedDict с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Literal and TypedDict: отдельный пример

```python
from typing import Literal, NotRequired, TypedDict

class UserPayload(TypedDict):
    email: str
    role: Literal["reader", "writer"]
    display_name: NotRequired[str]

payload: UserPayload = {"email": "a@example.com", "role": "reader"}
print(payload)
```

TypedDict проверяет статическую форму обычного dict, Literal сужает набор допустимых строк.

## Типичные ошибки

### Ошибка 1

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `constrained literals` до запуска.

**B · Найди ошибку.** Найди нарушение `typed dictionaries` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Literal and TypedDict за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Literal and TypedDict и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Literal and TypedDict?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Literal and TypedDict: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Нормальный ответ уровня Junior

> Literal and TypedDict — тема, в которой я сначала фиксирую `constrained literals`, затем объясняю `typed dictionaries` на коротком примере. Ключевой механизм: Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation. Главная практическая ошибка — Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Literal and TypedDict?**

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Критерии хорошего ответа

### Что обязательно упомянуть

- constrained literals
- typed dictionaries
- JSON-like structures

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Literal and TypedDict?

## Задача

Сделай короткую письменную практику по теме **Literal and TypedDict**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Literal and TypedDict: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.
- **Механизм:** Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.
- **Ограничение:** Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
