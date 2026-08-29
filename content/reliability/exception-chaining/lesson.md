# Exception chaining

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Exception chaining**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``raise ... from ...``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Как работает

Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception.

**`raise ... from ...`.** ``raise ... from ...`` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**preserving root cause.** `preserving root cause` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**translating infrastructure errors into domain/API errors.** `translating infrastructure errors into domain/API errors` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``raise ... from ...`` и `preserving root cause` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `raise ... from ...`
- preserving root cause
- translating infrastructure errors into domain/API errors

### Полезно

- связать Exception chaining с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Exception chaining: отдельный пример

```python
class InvalidUserId(ValueError):
    pass

def parse_user_id(raw):
    try:
        return int(raw)
    except ValueError as exc:
        raise InvalidUserId(raw) from exc
```

`raise from` добавляет domain context и сохраняет исходную причину в exception chain.

## Common mistakes

### Ошибка 1

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``raise ... from ...`` до запуска.

**B · Find the bug.** Найди нарушение `preserving root cause` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Exception chaining за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Exception chaining

```python
try:
    int('x')
except ValueError as exc:
    try:
        raise RuntimeError('bad input') from exc
    except RuntimeError as wrapped:
        print(type(wrapped.__cause__).__name__)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
ValueError
```

raise from записывает исходное исключение в __cause__ и делает цепочку явной.

Misconception: `exception-chaining`.

</details>

## Interview questions

### Основной вопрос

Что такое Exception chaining и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Exception chaining?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Exception chaining: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Нормальный Junior answer

> Exception chaining — тема, в которой я сначала фиксирую ``raise ... from ...``, затем объясняю `preserving root cause` на коротком примере. Ключевой механизм: Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception. Главная практическая ошибка — Забыть состояние protocol, сигнал завершения или cleanup при exception.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Exception chaining?**

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Expected answer rubric

### Must mention

- `raise ... from ...`
- preserving root cause
- translating infrastructure errors into domain/API errors

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Забыть состояние protocol, сигнал завершения или cleanup при exception.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Exception chaining?

## Задача

Сделай короткую письменную практику по теме **Exception chaining**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Exception chaining: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Забыть состояние protocol, сигнал завершения или cleanup при exception.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
