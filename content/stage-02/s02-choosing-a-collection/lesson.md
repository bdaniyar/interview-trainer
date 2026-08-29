# Choosing a collection

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Choosing a collection**, а не только запомнить термин;
- прочитать и изменить короткий пример для `list vs tuple`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это операция или гарантия стандартной коллекции Python; выбор структуры зависит от порядка, уникальности и стоимости основных операций.

### Как работает

Сравни порядок, duplicates, mutability, lookup/membership и стоимость изменения; затем проверь edge cases коротким кодом.

**list vs tuple.** `tuple` — immutable sequence; hashability зависит от всех элементов, а неизменяемость контейнера не делает mutable элементы неизменяемыми.

**list vs set.** `list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

**dict vs list of pairs.** `list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

**queue/stack choices.** `queue/stack choices` является частью контракта collection: наблюдаемое поведение зависит от порядка, duplicates, mutability и стоимости доступа.

**complexity trade-offs.** `complexity trade-offs` является частью контракта collection: наблюдаемое поведение зависит от порядка, duplicates, mutability и стоимости доступа.

**practical backend examples.** `practical backend examples` является частью контракта collection: наблюдаемое поведение зависит от порядка, duplicates, mutability и стоимости доступа.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `list vs tuple` и `list vs set` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- list vs tuple
- list vs set
- dict vs list of pairs
- queue/stack choices

### Полезно

- complexity trade-offs
- practical backend examples

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Choosing a collection: отдельный пример

```python
ordered_ids = [5, 3, 5]          # порядок и повторы
unique_ids = set(ordered_ids)       # уникальность
user_by_id = {value: {} for value in unique_ids}  # lookup

print(ordered_ids, unique_ids, user_by_id.keys())
```

Коллекцию выбирают по инварианту: порядок, повторы и доступ по ключу требуют разных структур.

## Common mistakes

### Ошибка 1

Выбрать collection по привычке и не проверить duplicates, order или lookup cost.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `list vs tuple` до запуска.

**B · Find the bug.** Найди нарушение `list vs set` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Choosing a collection за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Choosing a collection и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Choosing a collection?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Choosing a collection: Это операция или гарантия стандартной коллекции Python; выбор структуры зависит от порядка, уникальности и стоимости основных операций.

### Нормальный Junior answer

> Choosing a collection — тема, в которой я сначала фиксирую `list vs tuple`, затем объясняю `list vs set` на коротком примере. Ключевой механизм: Сравни порядок, duplicates, mutability, lookup/membership и стоимость изменения; затем проверь edge cases коротким кодом. Главная практическая ошибка — Выбрать collection по привычке и не проверить duplicates, order или lookup cost.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Choosing a collection?**

Выбрать collection по привычке и не проверить duplicates, order или lookup cost.

## Expected answer rubric

### Must mention

- list vs tuple
- list vs set
- dict vs list of pairs
- queue/stack choices

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Выбрать collection по привычке и не проверить duplicates, order или lookup cost.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Choosing a collection?

## Задача

Сделай короткую письменную практику по теме **Choosing a collection**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Choosing a collection: Это операция или гарантия стандартной коллекции Python; выбор структуры зависит от порядка, уникальности и стоимости основных операций.
- **Механизм:** Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.
- **Ограничение:** Выбрать collection по привычке и не проверить duplicates, order или lookup cost.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
