# Inheritance vs composition

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Inheritance vs composition**, а не только запомнить термин;
- прочитать и изменить короткий пример для `is-a vs has-a`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Inheritance models an is-a relationship; composition models has-a by giving an object explicit collaborators.

### Как работает

Inheritance reuses and overrides behavior through MRO. Composition delegates to injected objects, reducing coupling and making substitutions local.


### Важный нюанс / limitation

Prefer composition for services/repositories. Inheritance is justified for a stable substitutable hierarchy or framework contract, not only code reuse.

### Где используется в backend

A notification service composed with an email provider is easier to test than a deep service subclass tree.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- is-a vs has-a
- coupling
- testability
- service composition

### Полезно

- when inheritance is justified

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Inheritance vs composition: отдельный пример

```python
class EmailSender:
    def send(self, message):
        return f"sent: {message}"

class RegistrationService:
    def __init__(self, sender):
        self.sender = sender

    def register(self, email):
        return self.sender.send(email)

print(RegistrationService(EmailSender()).register("a@example.com"))
```

Composition передаёт collaborator явно и не заставляет service наследоваться от sender.

## Common mistakes

### Ошибка 1

Adding subclasses for every combination of behavior creates a fragile hierarchy and unclear MRO.

## Practice

**A · Code/result prediction.** Change one input in the `is-a vs has-a` example and predict the result before running it.

**B · Find the bug.** Find code that violates `coupling` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `is-a vs has-a` and add one edge-case test.

**E · Interview explanation.** Explain Inheritance vs composition in 45–60 seconds and include one limitation.

## Interview questions

### Основной вопрос

Что такое Inheritance vs composition и как это работает?

### Follow-up

Какая типичная ошибка связана с Inheritance vs composition?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Inheritance models an is-a relationship; composition models has-a by giving an object explicit collaborators.

### Нормальный Junior answer

> Inheritance models an is-a relationship; composition models has-a by giving an object explicit collaborators. Inheritance reuses and overrides behavior through MRO. Composition delegates to injected objects, reducing coupling and making substitutions local. Важное ограничение: Prefer composition for services/repositories. Inheritance is justified for a stable substitutable hierarchy or framework contract, not only code reuse.

### Углубление / follow-up

**Какая типичная ошибка связана с Inheritance vs composition?**

Adding subclasses for every combination of behavior creates a fragile hierarchy and unclear MRO.

## Expected answer rubric

### Must mention

- is-a vs has-a
- coupling
- testability
- service composition

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Adding subclasses for every combination of behavior creates a fragile hierarchy and unclear MRO.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Inheritance vs composition?

## Задача

Сделай короткую письменную практику по теме **Inheritance vs composition**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Inheritance models an is-a relationship; composition models has-a by giving an object explicit collaborators.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Adding subclasses for every combination of behavior creates a fragile hierarchy and unclear MRO.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
