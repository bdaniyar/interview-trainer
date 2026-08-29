# Protocol

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Protocol**, а не только запомнить термин;
- прочитать и изменить короткий пример для `structural subtyping`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Как работает

Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation.

**structural subtyping.** `structural subtyping` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.

**dependency contracts.** Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

**testing/fakes.** `testing/fakes` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `structural subtyping` и `dependency contracts` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- structural subtyping
- dependency contracts
- testing/fakes

### Полезно

- связать Protocol с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Protocol: отдельный пример

```python
from typing import Protocol

class UserReader(Protocol):
    def get(self, user_id: int) -> dict | None: ...

class MemoryUsers:
    def get(self, user_id: int) -> dict | None:
        return {"id": user_id}

def load(repo: UserReader, user_id: int):
    return repo.get(user_id)

print(load(MemoryUsers(), 7))
```

Structural Protocol принимает объект по доступному behavior без общего base class.

## Common mistakes

### Ошибка 1

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `structural subtyping` до запуска.

**B · Find the bug.** Найди нарушение `dependency contracts` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Protocol за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Protocol и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Protocol?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Protocol: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Нормальный Junior answer

> Protocol — тема, в которой я сначала фиксирую `structural subtyping`, затем объясняю `dependency contracts` на коротком примере. Ключевой механизм: Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation. Главная практическая ошибка — Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Protocol?**

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Expected answer rubric

### Must mention

- structural subtyping
- dependency contracts
- testing/fakes

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Protocol?

## Задача

Сделай короткую письменную практику по теме **Protocol**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Protocol: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.
- **Механизм:** Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.
- **Ограничение:** Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
