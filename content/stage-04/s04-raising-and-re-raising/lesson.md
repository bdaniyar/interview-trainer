# Raising and re-raising

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Raising and re-raising**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``raise``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Как работает

Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception.

**`raise`.** ``raise`` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**bare `raise`.** `bare `raise`` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**preserving traceback.** `preserving traceback` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**domain exceptions.** `domain exceptions` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй ``raise`` и `bare `raise`` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- `raise`
- bare `raise`
- preserving traceback
- domain exceptions

### Полезно

- связать Raising and re-raising с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Raising and re-raising: отдельный пример

```python
def load_id(raw):
    try:
        return int(raw)
    except ValueError:
        print("invalid id")
        raise

try:
    load_id("x")
except ValueError:
    print("caller decides")
```

Bare `raise` повторно поднимает текущую ошибку с исходным traceback.

## Common mistakes

### Ошибка 1

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для ``raise`` до запуска.

**B · Find the bug.** Найди нарушение `bare `raise`` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Raising and re-raising за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Raising and re-raising и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Raising and re-raising?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Raising and re-raising: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Нормальный Junior answer

> Raising and re-raising — тема, в которой я сначала фиксирую ``raise``, затем объясняю `bare `raise`` на коротком примере. Ключевой механизм: Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception. Главная практическая ошибка — Забыть состояние protocol, сигнал завершения или cleanup при exception.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Raising and re-raising?**

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Expected answer rubric

### Must mention

- `raise`
- bare `raise`
- preserving traceback
- domain exceptions

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Забыть состояние protocol, сигнал завершения или cleanup при exception.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Raising and re-raising?

## Задача

Сделай короткую письменную практику по теме **Raising and re-raising**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Raising and re-raising: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Забыть состояние protocol, сигнал завершения или cleanup при exception.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
