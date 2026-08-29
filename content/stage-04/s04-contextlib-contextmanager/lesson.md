# `contextlib.contextmanager`

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **`contextlib.contextmanager`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `generator-based context manager`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Как работает

Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception.

**generator-based context manager.** Context manager заключает acquire/use/release в `with`; `__exit__` получает exception info и подавляет ошибку только при truthy return.

**transaction/file/timer examples.** Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `generator-based context manager` и `transaction/file/timer examples` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- generator-based context manager
- transaction/file/timer examples

### Полезно

- связать `contextlib.contextmanager` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### `contextlib.contextmanager`: отдельный пример

```python
from contextlib import contextmanager

@contextmanager
def transaction(session):
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
```

`@contextmanager` превращает generator с одним `yield` в protocol `with`, сохраняя cleanup рядом с acquire.

## Common mistakes

### Ошибка 1

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `generator-based context manager` до запуска.

**B · Find the bug.** Найди нарушение `transaction/file/timer examples` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про `contextlib.contextmanager` за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое `contextlib.contextmanager` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме `contextlib.contextmanager`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

`contextlib.contextmanager`: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Нормальный Junior answer

> `contextlib.contextmanager` — тема, в которой я сначала фиксирую `generator-based context manager`, затем объясняю `transaction/file/timer examples` на коротком примере. Ключевой механизм: Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception. Главная практическая ошибка — Забыть состояние protocol, сигнал завершения или cleanup при exception.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме `contextlib.contextmanager`?**

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Expected answer rubric

### Must mention

- generator-based context manager
- transaction/file/timer examples

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Забыть состояние protocol, сигнал завершения или cleanup при exception.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме `contextlib.contextmanager`?

## Задача

Сделай короткую письменную практику по теме **`contextlib.contextmanager`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** `contextlib.contextmanager`: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Забыть состояние protocol, сигнал завершения или cleanup при exception.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
