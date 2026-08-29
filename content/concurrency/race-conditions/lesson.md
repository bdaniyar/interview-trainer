# Race conditions and locks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; CPython details приоритетны только там, где объясняют реальные bugs.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Race conditions and locks**, а не только запомнить термин;
- прочитать и изменить короткий пример для `check-then-act`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это практическая модель CPython для lifetime, памяти или конкурентности; детали реализации нужно отделять от спецификации языка.

### Как работает

Сначала измерь lifetime, allocations или contention и только затем связывай symptom с особенностью CPython.

**check-then-act.** `check-then-act` относится к поведению CPython; практический вывод подтверждают измерением lifetime, allocations или contention.

**shared mutable state.** Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию.

**`Lock`.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

**deadlock basics.** Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания.

**database race conditions are separate from Python GIL.** CPython GIL допускает выполнение Python bytecode одним thread за раз, но отпускается вокруг части I/O/native calls и не защищает бизнес-инварианты от races.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `check-then-act` и `shared mutable state` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Разделяй спецификацию Python и конкретную реализацию CPython; GIL относится к выполнению bytecode, не к бизнес-инвариантам.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- check-then-act
- shared mutable state
- `Lock`
- deadlock basics

### Полезно

- database race conditions are separate from Python GIL

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Race conditions and locks: отдельный пример

```python
from threading import Lock

lock = Lock()
balance = 0

def deposit(amount):
    global balance
    with lock:
        current = balance
        balance = current + amount
```

Lock защищает всю read-modify-write critical section; отдельные операции чтения и записи недостаточны.

## Common mistakes

### Ошибка 1

Принять деталь CPython за гарантию языка или оптимизировать без измерения.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `check-then-act` до запуска.

**B · Find the bug.** Найди нарушение `shared mutable state` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Race conditions and locks за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Race conditions and locks и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Race conditions and locks?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Race conditions and locks: Это практическая модель CPython для lifetime, памяти или конкурентности; детали реализации нужно отделять от спецификации языка.

### Нормальный Junior answer

> Race conditions and locks — тема, в которой я сначала фиксирую `check-then-act`, затем объясняю `shared mutable state` на коротком примере. Ключевой механизм: Сначала измерь lifetime, allocations или contention и только затем связывай symptom с особенностью CPython. Главная практическая ошибка — Принять деталь CPython за гарантию языка или оптимизировать без измерения.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Race conditions and locks?**

Принять деталь CPython за гарантию языка или оптимизировать без измерения.

## Expected answer rubric

### Must mention

- check-then-act
- shared mutable state
- `Lock`
- deadlock basics

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Принять деталь CPython за гарантию языка или оптимизировать без измерения.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Race conditions and locks?

## Задача

Сделай короткую письменную практику по теме **Race conditions and locks**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Race conditions and locks: Это практическая модель CPython для lifetime, памяти или конкурентности; детали реализации нужно отделять от спецификации языка.
- **Механизм:** Разделяй спецификацию Python и конкретную реализацию CPython; GIL относится к выполнению bytecode, не к бизнес-инвариантам.
- **Ограничение:** Принять деталь CPython за гарантию языка или оптимизировать без измерения.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [gc](https://docs.python.org/3.12/library/gc.html)
- [threading](https://docs.python.org/3.12/library/threading.html)

Последняя проверка версий: **2026-08-27**.
