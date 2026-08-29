# Encapsulation, abstraction and polymorphism

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Encapsulation, abstraction and polymorphism**, а не только запомнить термин;
- прочитать и изменить короткий пример для `practical Python meaning`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Encapsulation groups state and behavior, abstraction exposes a relevant contract, and polymorphism lets different objects satisfy that contract.

### Как работает

Python often uses duck typing: caller depends on available behavior rather than a concrete inheritance tree. ABC and Protocol can make the contract explicit when useful.


### Важный нюанс / limitation

Leading underscores communicate non-public API but are not access control; invariants still need methods/properties and tests.

### Где используется в backend

A service can accept any notifier implementing `send`, allowing a fake in tests and different providers in production.

## Mental model

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- practical Python meaning
- duck typing
- contracts
- avoid Java-style ceremony

### Полезно

- one short code/result example

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Encapsulation, abstraction and polymorphism: отдельный пример

```python
class JsonRenderable:
    def render(self):
        raise NotImplementedError

class User(JsonRenderable):
    def render(self):
        return {"type": "user"}

def response(item: JsonRenderable):
    return item.render()

print(response(User()))
```

Polymorphism позволяет caller работать через behavior contract, не проверяя конкретный класс.

## Common mistakes

### Ошибка 1

Checking `type(obj) is ConcreteClass` blocks valid substitutes and defeats polymorphism.

## Practice

**A · Code/result prediction.** Change one input in the `practical Python meaning` example and predict the result before running it.

**B · Find the bug.** Find code that violates `duck typing` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `practical Python meaning` and add one edge-case test.

**E · Interview explanation.** Explain Encapsulation, abstraction and polymorphism in 45–60 seconds and include one limitation.

## Code prediction

### super следует MRO

```python
class A:
    def name(self): return 'A'
class B(A):
    def name(self): return 'B>' + super().name()
class C(B): pass
print(C().name())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
B>A
```

super в B продолжает поиск после B в MRO фактического класса C.

Misconception: `mro`.

</details>

## Interview questions

### Основной вопрос

Что такое Encapsulation, abstraction and polymorphism и как это работает?

### Follow-up

Какая типичная ошибка связана с Encapsulation, abstraction and polymorphism?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Encapsulation groups state and behavior, abstraction exposes a relevant contract, and polymorphism lets different objects satisfy that contract.

### Нормальный Junior answer

> Encapsulation groups state and behavior, abstraction exposes a relevant contract, and polymorphism lets different objects satisfy that contract. Python often uses duck typing: caller depends on available behavior rather than a concrete inheritance tree. ABC and Protocol can make the contract explicit when useful. Важное ограничение: Leading underscores communicate non-public API but are not access control; invariants still need methods/properties and tests.

### Углубление / follow-up

**Какая типичная ошибка связана с Encapsulation, abstraction and polymorphism?**

Checking `type(obj) is ConcreteClass` blocks valid substitutes and defeats polymorphism.

## Expected answer rubric

### Must mention

- practical Python meaning
- duck typing
- contracts
- avoid Java-style ceremony

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Checking `type(obj) is ConcreteClass` blocks valid substitutes and defeats polymorphism.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Encapsulation, abstraction and polymorphism?

## Задача

Сделай короткую письменную практику по теме **Encapsulation, abstraction and polymorphism**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Encapsulation groups state and behavior, abstraction exposes a relevant contract, and polymorphism lets different objects satisfy that contract.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Checking `type(obj) is ConcreteClass` blocks valid substitutes and defeats polymorphism.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
