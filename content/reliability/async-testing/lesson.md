# Async tests

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Async tests**, а не только запомнить термин;
- прочитать и изменить короткий пример для `event loop plugin/config`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**event loop plugin/config.** Event loop запускает ready callbacks/tasks и ждёт I/O; cooperative task уступает управление только в точка приостановки await.

**AsyncClient.** `AsyncClient` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**deterministic timeouts.** `deterministic timeouts` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**no sleep-heavy tests.** `no sleep-heavy tests` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `event loop plugin/config` и `AsyncClient` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `event loop plugin/config`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- event loop plugin/config
- AsyncClient
- deterministic timeouts
- no sleep-heavy tests

### Полезно

- связать Async tests с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Async tests: отдельный пример

```text
Сценарий: Test завершился, background task осталась.

Проверка:
Await/cancel tasks; deterministic event.
```

Это отдельный testing example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `event loop plugin/config` до запуска.

**B · Найди ошибку.** Найди нарушение `AsyncClient` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Async tests за 60 секунд: определение, механизм, пример, ограничение.

## Практика: Тестирование

### Async task leak

**Сценарий:** Test завершился, background task осталась.

**Критерии ответа:** Await/cancel tasks; deterministic event.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Async tests и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Async tests?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Async tests: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный ответ уровня Junior

> Async tests — тема, в которой я сначала фиксирую `event loop plugin/config`, затем объясняю `AsyncClient` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Async tests?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Критерии хорошего ответа

### Что обязательно упомянуть

- event loop plugin/config
- AsyncClient
- deterministic timeouts
- no sleep-heavy tests

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Async tests?

## Задача

Сделай короткую письменную практику по теме **Async tests**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Async tests: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
