# Literal and TypedDict

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Literal and TypedDict**, а не только запомнить термин;
- прочитать и изменить короткий пример для `constrained literals`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Как работает

Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation.

**constrained literals.** `constrained literals` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.

**typed dictionaries.** `dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract.

**JSON-like structures.** `JSON-like structures` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `constrained literals` и `typed dictionaries` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- constrained literals
- typed dictionaries
- JSON-like structures

### Полезно

- связать Literal and TypedDict с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

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

## Common mistakes

### Ошибка 1

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `constrained literals` до запуска.

**B · Find the bug.** Найди нарушение `typed dictionaries` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Literal and TypedDict за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Literal and TypedDict и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Literal and TypedDict?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Literal and TypedDict: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Нормальный Junior answer

> Literal and TypedDict — тема, в которой я сначала фиксирую `constrained literals`, затем объясняю `typed dictionaries` на коротком примере. Ключевой механизм: Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation. Главная практическая ошибка — Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Literal and TypedDict?**

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Expected answer rubric

### Must mention

- constrained literals
- typed dictionaries
- JSON-like structures

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Literal and TypedDict?

## Задача

Сделай короткую письменную практику по теме **Literal and TypedDict**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Literal and TypedDict: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.
- **Механизм:** Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.
- **Ограничение:** Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
