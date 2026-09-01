# Test pyramid and test types

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Testing явно встречался в 6/18 и часто подразумевается; pytest — P0/P1 рабочий навык.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Test pyramid and test types**, а не только запомнить термин;
- прочитать и изменить короткий пример для `unit`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Как работает

Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.

**unit.** `unit` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**integration.** `integration` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**end-to-end.** `end-to-end` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**contract awareness.** `contract awareness` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.

**correct boundary choice.** `correct boundary choice` помогает проверить observable contract; test задаёт isolation boundary, конкретный input и ожидаемый success/failure result.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `unit` и `integration` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `unit`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- unit
- integration
- end-to-end
- contract awareness

### Полезно

- correct boundary choice

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Test pyramid and test types: отдельный пример

```text
Сценарий: Раздели booking flow на unit, integration и API tests.

Проверка:
Unit domain decision; integration DB constraint; API status/body.
```

Это отдельный testing example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `unit` до запуска.

**B · Найди ошибку.** Найди нарушение `integration` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Test pyramid and test types за 60 секунд: определение, механизм, пример, ограничение.

## Практика: Тестирование

### Test boundary

**Сценарий:** Раздели booking flow на unit, integration и API tests.

**Критерии ответа:** Unit domain decision; integration DB constraint; API status/body.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Test pyramid and test types и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Test pyramid and test types?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Test pyramid and test types: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.

### Нормальный ответ уровня Junior

> Test pyramid and test types — тема, в которой я сначала фиксирую `unit`, затем объясняю `integration` на коротком примере. Ключевой механизм: Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression. Главная практическая ошибка — Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Test pyramid and test types?**

Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.

## Критерии хорошего ответа

### Что обязательно упомянуть

- unit
- integration
- end-to-end
- contract awareness

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Test pyramid and test types?

## Задача

Сделай короткую письменную практику по теме **Test pyramid and test types**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Test pyramid and test types: Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.
- **Механизм:** Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.
- **Ограничение:** Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Последняя проверка версий: **2026-08-27**.
