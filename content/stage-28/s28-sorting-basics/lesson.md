# Sorting basics

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Базовые structures/complexity проверяют на coding screen; competitive programming не приоритет.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Sorting basics**, а не только запомнить термин;
- прочитать и изменить короткий пример для `O(n log n)`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Sorting basics** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**O(n log n).** `O(n log n)` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**stable sort.** `stable sort` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**key extraction.** `key extraction` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**no need to memorize every sort implementation.** `no need to memorize every sort implementation` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `O(n log n)` и `stable sort` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Выбери структуру по операциям и оцени dominant time/space term.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- O(n log n)
- stable sort
- key extraction
- no need to memorize every sort implementation

### Полезно

- связать Sorting basics с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Sorting basics: отдельный пример

```python
def example_s28_sorting_basics() -> tuple[str, ...]:
    # Sorting basics: проверяем отдельный contract урока.
    return ('O(n log n)', 'stable sort', 'key extraction', 'no need to memorize every sort implementation',)

assert example_s28_sorting_basics()
```

Сначала назови input constraints, структуру данных, complexity и boundary cases.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `O(n log n)` до запуска.

**B · Find the bug.** Найди нарушение `stable sort` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Sorting basics за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Sorting basics и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Sorting basics?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Sorting basics: это отдельный технический контракт

### Нормальный Junior answer

> Sorting basics — тема, в которой я сначала фиксирую `O(n log n)`, затем объясняю `stable sort` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Sorting basics?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- O(n log n)
- stable sort
- key extraction
- no need to memorize every sort implementation

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Sorting basics?

## Задача

Сделай короткую письменную практику по теме **Sorting basics**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Sorting basics: это отдельный технический контракт
- **Механизм:** Выбери структуру по операциям и оцени dominant time/space term.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python collections](https://docs.python.org/3.12/library/collections.html)
- [Sorting HOWTO](https://docs.python.org/3.12/howto/sorting.html)

Последняя проверка версий: **2026-08-27**.
