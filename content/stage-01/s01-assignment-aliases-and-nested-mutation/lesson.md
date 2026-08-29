# Assignment, aliases and nested mutation

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Assignment, aliases and nested mutation**, а не только запомнить термин;
- прочитать и изменить короткий пример для `aliases`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Aliases are multiple names or container slots referring to one object; nested mutation through any alias changes that same object.

### Как работает

Assignment and sequence repetition copy references. `[[]] * 3` repeats one inner-list reference three times, so mutating one visible row changes all three positions.


### Важный нюанс / limitation

Build independent nested values with a comprehension such as `[[] for _ in range(3)]`.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- aliases
- shared nested structures
- repeated references
- `[[]] * 3`

### Полезно

- passing objects into functions

### Можно не учить глубоко

- internal implementation details beyond common Junior follow-ups

## Code examples

### Assignment, aliases and nested mutation: отдельный пример

```python
matrix = [[0] * 2 for _ in range(3)]
alias = matrix[0]
alias.append(1)

print(matrix)
print(alias is matrix[0])
print(alias is matrix[1])
```

Comprehension создаёт независимые внутренние lists, а `alias` указывает только на первую строку.

## Common mistakes

### Ошибка 1

Using multiplication for mutable nested defaults creates shared state that is difficult to notice in tests with one element.

## Practice

**A · Code/result prediction.** Change one input in the `aliases` example and predict the result before running it.

**B · Find the bug.** Find code that violates `shared nested structures` and explain the concrete consequence.

**D · Small task.** Implement the smallest function/query that demonstrates `aliases` and add one edge-case test.

**E · Interview explanation.** Explain Assignment, aliases and nested mutation in 45–60 seconds and include one limitation.

## Code prediction

### Повтор вложенного списка

```python
rows = [[0]] * 3
rows[0].append(1)
print(rows)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[[0, 1], [0, 1], [0, 1]]
```

Оператор * повторил одну ссылку на внутренний список, а не создал три списка.

Misconception: `nested-aliasing`.

</details>

## Debugging practice

### Nested alias

**Сценарий:** [[]] * 3 меняет все строки после append.

**Rubric:** Повторяется одна reference; comprehension создаёт независимые lists.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Assignment, aliases and nested mutation и как это работает?

### Follow-up

Какая типичная ошибка связана с Assignment, aliases and nested mutation?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Aliases are multiple names or container slots referring to one object; nested mutation through any alias changes that same object.

### Нормальный Junior answer

> Aliases are multiple names or container slots referring to one object; nested mutation through any alias changes that same object. Assignment and sequence repetition copy references. `[[]] * 3` repeats one inner-list reference three times, so mutating one visible row changes all three positions. Важное ограничение: Build independent nested values with a comprehension such as `[[] for _ in range(3)]`.

### Углубление / follow-up

**Какая типичная ошибка связана с Assignment, aliases and nested mutation?**

Using multiplication for mutable nested defaults creates shared state that is difficult to notice in tests with one element.

## Expected answer rubric

### Must mention

- aliases
- shared nested structures
- repeated references
- `[[]] * 3`

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Using multiplication for mutable nested defaults creates shared state that is difficult to notice in tests with one element.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какая типичная ошибка связана с Assignment, aliases and nested mutation?

## Задача

Сделай короткую письменную практику по теме **Assignment, aliases and nested mutation**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Aliases are multiple names or container slots referring to one object; nested mutation through any alias changes that same object.
- **Механизм:** Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.
- **Ограничение:** Using multiplication for mutable nested defaults creates shared state that is difficult to notice in tests with one element.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
