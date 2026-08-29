# Custom exceptions

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Custom exceptions**, а не только запомнить термин;
- прочитать и изменить короткий пример для `hierarchy`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Как работает

Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception.

**hierarchy.** `hierarchy` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**useful context.** `useful context` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**mapping to HTTP errors.** `mapping to HTTP errors` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**avoiding exception-driven normal flow.** `avoiding exception-driven normal flow` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `hierarchy` и `useful context` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- hierarchy
- useful context
- mapping to HTTP errors
- avoiding exception-driven normal flow

### Полезно

- связать Custom exceptions с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Custom exceptions: отдельный пример

```python
class BookingConflict(Exception):
    def __init__(self, room_id):
        self.room_id = room_id
        super().__init__(f"room {room_id} is already booked")

try:
    raise BookingConflict(42)
except BookingConflict as exc:
    print(exc.room_id)
```

Custom exception несёт стабильный domain type и данные, а не заставляет caller разбирать строку.

## Common mistakes

### Ошибка 1

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `hierarchy` до запуска.

**B · Find the bug.** Найди нарушение `useful context` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Custom exceptions за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Custom exceptions и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Custom exceptions?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Custom exceptions: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Нормальный Junior answer

> Custom exceptions — тема, в которой я сначала фиксирую `hierarchy`, затем объясняю `useful context` на коротком примере. Ключевой механизм: Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception. Главная практическая ошибка — Забыть состояние protocol, сигнал завершения или cleanup при exception.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Custom exceptions?**

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Expected answer rubric

### Must mention

- hierarchy
- useful context
- mapping to HTTP errors
- avoiding exception-driven normal flow

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Забыть состояние protocol, сигнал завершения или cleanup при exception.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Custom exceptions?

## Задача

Сделай короткую письменную практику по теме **Custom exceptions**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Custom exceptions: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Забыть состояние protocol, сигнал завершения или cleanup при exception.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
