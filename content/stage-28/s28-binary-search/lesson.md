# Binary search

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Базовые structures/complexity проверяют на coding screen; competitive programming не приоритет.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Binary search**, а не только запомнить термин;
- прочитать и изменить короткий пример для `sorted invariant`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Binary search** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**sorted invariant.** `sorted invariant` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**boundaries.** `boundaries` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**O(log n).** `O(log n)` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `sorted invariant` и `boundaries` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Выбери структуру по операциям и оцени dominant time/space term.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- sorted invariant
- boundaries
- O(log n)

### Полезно

- связать Binary search с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Binary search: отдельный пример

```python
from collections import Counter
counts = Counter('aba')
print(counts['a'], counts['x'])
```

Expected: `2 0`. Counter возвращает ноль для отсутствующего ключа вместо KeyError.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `sorted invariant` до запуска.

**B · Find the bug.** Найди нарушение `boundaries` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Binary search за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Счётчик частот

```python
from collections import Counter
counts = Counter('aba')
print(counts['a'], counts['x'])
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
2 0
```

Counter возвращает ноль для отсутствующего ключа вместо KeyError.

Misconception: `counter`.

</details>

## Interview questions

### Основной вопрос

Что такое Binary search и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Binary search?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Binary search: это отдельный технический контракт

### Нормальный Junior answer

> Binary search — тема, в которой я сначала фиксирую `sorted invariant`, затем объясняю `boundaries` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Binary search?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- sorted invariant
- boundaries
- O(log n)

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Binary search?

## Задача

Сделай короткую письменную практику по теме **Binary search**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Binary search: это отдельный технический контракт
- **Механизм:** Выбери структуру по операциям и оцени dominant time/space term.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python collections](https://docs.python.org/3.12/library/collections.html)
- [Sorting HOWTO](https://docs.python.org/3.12/howto/sorting.html)

Последняя проверка версий: **2026-08-27**.
