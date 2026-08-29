# Queue/deque

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Базовые structures/complexity проверяют на coding screen; competitive programming не приоритет.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Queue/deque**, а не только запомнить термин;
- прочитать и изменить короткий пример для `FIFO`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Queue/deque** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**FIFO.** `FIFO` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**BFS.** `BFS` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**task processing.** Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `FIFO` и `BFS` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Выбери структуру по операциям и оцени dominant time/space term.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- FIFO
- BFS
- task processing

### Полезно

- связать Queue/deque с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Queue/deque: отдельный пример

```python
values = [2, 1, 2, 3, 1]
print(list(dict.fromkeys(values)))
```

Expected: `[2, 1, 3]`. dict сохраняет порядок первого появления каждого hashable key.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `FIFO` до запуска.

**B · Find the bug.** Найди нарушение `BFS` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Queue/deque за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Dedup с сохранением порядка

```python
values = [2, 1, 2, 3, 1]
print(list(dict.fromkeys(values)))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[2, 1, 3]
```

dict сохраняет порядок первого появления каждого hashable key.

Misconception: `ordered-dedup`.

</details>

## Interview questions

### Основной вопрос

Что такое Queue/deque и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Queue/deque?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Queue/deque: это отдельный технический контракт

### Нормальный Junior answer

> Queue/deque — тема, в которой я сначала фиксирую `FIFO`, затем объясняю `BFS` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Queue/deque?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- FIFO
- BFS
- task processing

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Queue/deque?

## Задача

Сделай короткую письменную практику по теме **Queue/deque**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Queue/deque: это отдельный технический контракт
- **Механизм:** Выбери структуру по операциям и оцени dominant time/space term.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python collections](https://docs.python.org/3.12/library/collections.html)
- [Sorting HOWTO](https://docs.python.org/3.12/howto/sorting.html)

Последняя проверка версий: **2026-08-27**.
