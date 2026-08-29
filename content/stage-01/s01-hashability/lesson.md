# Hashability

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Hashability**, а не только запомнить термин;
- прочитать и изменить короткий пример для `hashable object`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

A hashable object has a stable hash and equality behavior, so it can be a dict key or set element.

### Как работает

A hash table uses `hash(key)` to find candidates and `==` to confirm a match. Objects that compare equal must have equal hashes; state involved in equality must not change while used as a key.


### Важный нюанс / limitation

A tuple is hashable only when all elements are hashable. Custom equality often requires an explicit, consistent `__hash__` decision.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- hashable object
- dict key/set member
- equality/hash contract
- mutable object as key

### Полезно

- tuple hashability
- custom `__hash__`

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Hashability: отдельный пример

```python
keys = {(1, 2): "point"}
print(keys[(1, 2)])

try:
    {[1, 2]: "broken"}
except TypeError as exc:
    print(type(exc).__name__)
```

Tuple из hashable элементов допустим как ключ, mutable list — нет.

## Common mistakes

### Ошибка 1

Using list or dict as a key raises `TypeError: unhashable type`; making mutable state hashable can corrupt lookup semantics.

## Practice

**A · Code/result prediction.** Change one input in the `hashable object` example and predict the result before running it.

**B · Find the bug.** Find code that violates `dict key/set member` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `hashable object` and add one edge-case test.

**E · Interview explanation.** Explain Hashability in 45–60 seconds and include one limitation.

## Code prediction

### Равные ключи dict

```python
data = {True: 'yes', 1: 'one'}
print(len(data), data[True])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
1 one
```

True == 1 и их hashes равны, поэтому второй assignment заменяет значение того же ключа.

Misconception: `hash-equality-contract`.

</details>

## Interview questions

### Основной вопрос

Что такое Hashability и как это работает?

### Follow-up

Какая типичная ошибка связана с Hashability?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

A hashable object has a stable hash and equality behavior, so it can be a dict key or set element.

### Нормальный Junior answer

> A hashable object has a stable hash and equality behavior, so it can be a dict key or set element. A hash table uses `hash(key)` to find candidates and `==` to confirm a match. Objects that compare equal must have equal hashes; state involved in equality must not change while used as a key. Важное ограничение: A tuple is hashable only when all elements are hashable. Custom equality often requires an explicit, consistent `__hash__` decision.

### Углубление / follow-up

**Какая типичная ошибка связана с Hashability?**

Using list or dict as a key raises `TypeError: unhashable type`; making mutable state hashable can corrupt lookup semantics.

## Expected answer rubric

### Must mention

- hashable object
- dict key/set member
- equality/hash contract
- mutable object as key

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Using list or dict as a key raises `TypeError: unhashable type`; making mutable state hashable can corrupt lookup semantics.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Hashability?

## Задача

Сделай короткую письменную практику по теме **Hashability**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** A hashable object has a stable hash and equality behavior, so it can be a dict key or set element.
- **Механизм:** Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.
- **Ограничение:** Using list or dict as a key raises `TypeError: unhashable type`; making mutable state hashable can corrupt lookup semantics.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
