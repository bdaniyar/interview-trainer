# Sorting

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Sorting**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``sorted` vs `.sort``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это операция или гарантия стандартной коллекции Python; выбор структуры зависит от порядка, уникальности и стоимости основных операций.

### Как работает

Сравни порядок, duplicates, mutability, lookup/membership и стоимость изменения; затем проверь edge cases коротким кодом.

**`sorted` vs `.sort`.** ``sorted` vs `.sort`` является частью контракта collection: наблюдаемое поведение зависит от порядка, duplicates, mutability и стоимости доступа.

**`key`.** ``key`` является частью контракта collection: наблюдаемое поведение зависит от порядка, duplicates, mutability и стоимости доступа.

**stability.** `stability` является частью контракта collection: наблюдаемое поведение зависит от порядка, duplicates, mutability и стоимости доступа.

**multiple fields.** `multiple fields` является частью контракта collection: наблюдаемое поведение зависит от порядка, duplicates, mutability и стоимости доступа.

**`reverse`.** ``reverse`` является частью контракта collection: наблюдаемое поведение зависит от порядка, duplicates, mutability и стоимости доступа.

**sorting dictionaries/objects.** Python sort стабилен и использует key один раз на элемент; `sorted` создаёт новый list, а `.sort()` меняет существующий и возвращает `None`.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``sorted` vs `.sort`` и ``key`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `sorted` vs `.sort`
- `key`
- stability
- multiple fields

### Полезно

- `reverse`
- sorting dictionaries/objects

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Sorting: отдельный пример

```python
users = [
    {"id": 2, "score": 10},
    {"id": 1, "score": 10},
    {"id": 3, "score": 7},
]
result = sorted(users, key=lambda user: (-user["score"], user["id"]))
print([user["id"] for user in result])
```

Tuple key задаёт основной порядок и детерминированный tie-breaker.

## Common mistakes

### Ошибка 1

Выбрать collection по привычке и не проверить duplicates, order или lookup cost.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``sorted` vs `.sort`` до запуска.

**B · Find the bug.** Найди нарушение ``key`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Sorting за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Sorting и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Sorting?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Sorting: Это операция или гарантия стандартной коллекции Python; выбор структуры зависит от порядка, уникальности и стоимости основных операций.

### Нормальный Junior answer

> Sorting — тема, в которой я сначала фиксирую ``sorted` vs `.sort``, затем объясняю ``key`` на коротком примере. Ключевой механизм: Сравни порядок, duplicates, mutability, lookup/membership и стоимость изменения; затем проверь edge cases коротким кодом. Главная практическая ошибка — Выбрать collection по привычке и не проверить duplicates, order или lookup cost.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Sorting?**

Выбрать collection по привычке и не проверить duplicates, order или lookup cost.

## Expected answer rubric

### Must mention

- `sorted` vs `.sort`
- `key`
- stability
- multiple fields

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Выбрать collection по привычке и не проверить duplicates, order или lookup cost.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Sorting?

## Задача

### Стабильно отсортировать события

Верни новый list событий по created_at по убыванию. Равные timestamps сохрани в исходном порядке.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Sorting: Это операция или гарантия стандартной коллекции Python; выбор структуры зависит от порядка, уникальности и стоимости основных операций.
- **Механизм:** Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.
- **Ограничение:** Выбрать collection по привычке и не проверить duplicates, order или lookup cost.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
