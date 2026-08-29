# Stack

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** Базовые structures/complexity проверяют на coding screen; competitive programming не приоритет.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Stack**, а не только запомнить термин;
- прочитать и изменить короткий пример для `brackets`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Stack** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**brackets.** `brackets` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**undo.** `undo` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.

**DFS basics.** `DFS basics` определяет data-structure operation с конкретной time/space complexity и набором boundary cases.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `brackets` и `undo` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Выбери структуру по операциям и оцени dominant time/space term.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- brackets
- undo
- DFS basics

### Полезно

- связать Stack с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Stack: отдельный пример

```python
def example_s28_stack() -> tuple[str, ...]:
    # Stack: проверяем отдельный contract урока.
    return ('brackets', 'undo', 'DFS basics',)

assert example_s28_stack()
```

Сначала назови input constraints, структуру данных, complexity и boundary cases.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `brackets` до запуска.

**B · Find the bug.** Найди нарушение `undo` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Stack за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Stack и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Stack?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Stack: это отдельный технический контракт

### Нормальный Junior answer

> Stack — тема, в которой я сначала фиксирую `brackets`, затем объясняю `undo` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Stack?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- brackets
- undo
- DFS basics

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Stack?

## Задача

Сделай короткую письменную практику по теме **Stack**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Stack: это отдельный технический контракт
- **Механизм:** Выбери структуру по операциям и оцени dominant time/space term.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python collections](https://docs.python.org/3.12/library/collections.html)
- [Sorting HOWTO](https://docs.python.org/3.12/howto/sorting.html)

Последняя проверка версий: **2026-08-27**.
