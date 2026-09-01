# Generator expression vs list comprehension

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; iteration/exceptions/resource cleanup нужны в production code.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Generator expression vs list comprehension**, а не только запомнить термин;
- прочитать и изменить короткий пример для `eager vs lazy`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Как работает

Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception.

**eager vs lazy.** `eager vs lazy` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**single-use.** `single-use` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**performance/memory.** `performance/memory` участвует в protocol управления потоком: объект хранит state, consumer делает шаги, а завершение и error path имеют явный сигнал.

**when list is preferable.** `list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `eager vs lazy` и `single-use` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Модель понимания

Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- eager vs lazy
- single-use
- performance/memory
- when list is preferable

### Полезно

- связать Generator expression vs list comprehension с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Generator expression vs list comprehension: отдельный пример

```python
source = range(1_000_000)
lazy_squares = (value * value for value in source)
eager_squares = [value * value for value in range(3)]

print(next(lazy_squares))
print(eager_squares)
```

Generator expression вычисляет элементы по запросу; list comprehension сразу материализует результат.

## Типичные ошибки

### Ошибка 1

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `eager vs lazy` до запуска.

**B · Найди ошибку.** Найди нарушение `single-use` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Generator expression vs list comprehension за 60 секунд: определение, механизм, пример, ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое Generator expression vs list comprehension и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Generator expression vs list comprehension?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Generator expression vs list comprehension: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.

### Нормальный ответ уровня Junior

> Generator expression vs list comprehension — тема, в которой я сначала фиксирую `eager vs lazy`, затем объясняю `single-use` на коротком примере. Ключевой механизм: Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception. Главная практическая ошибка — Забыть состояние protocol, сигнал завершения или cleanup при exception.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Generator expression vs list comprehension?**

Забыть состояние protocol, сигнал завершения или cleanup при exception.

## Критерии хорошего ответа

### Что обязательно упомянуть

- eager vs lazy
- single-use
- performance/memory
- when list is preferable

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Забыть состояние protocol, сигнал завершения или cleanup при exception.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Generator expression vs list comprehension?

## Задача

Сделай короткую письменную практику по теме **Generator expression vs list comprehension**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Generator expression vs list comprehension: Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.
- **Механизм:** Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.
- **Ограничение:** Забыть состояние protocol, сигнал завершения или cleanup при exception.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Iterator types](https://docs.python.org/3.12/library/stdtypes.html#iterator-types)
- [Exceptions](https://docs.python.org/3.12/tutorial/errors.html)
- [contextlib](https://docs.python.org/3.12/library/contextlib.html)

Последняя проверка версий: **2026-08-27**.
