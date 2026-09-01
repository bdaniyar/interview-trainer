# Async lazy-loading pitfalls

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Async lazy-loading pitfalls**, а не только запомнить термин;
- прочитать и изменить короткий пример для `unexpected I/O`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**unexpected I/O.** `unexpected I/O` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**missing greenlet-style problems.** `missing greenlet-style problems` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**explicit eager loading.** `explicit eager loading` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `unexpected I/O` и `missing greenlet-style problems` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `unexpected I/O`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- unexpected I/O
- missing greenlet-style problems
- explicit eager loading

### Полезно

- связать Async lazy-loading pitfalls с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Async lazy-loading pitfalls: отдельный пример

```text
Сценарий: Response validation выполняет queries после service return.

Проверка:
Map ORM to response data при открытой session; query-count test обнаруживает hidden I/O.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `unexpected I/O` до запуска.

**B · Найди ошибку.** Найди нарушение `missing greenlet-style problems` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Async lazy-loading pitfalls за 60 секунд: определение, механизм, пример, ограничение.

## Практика: Отладка

### Serialization hits DB

**Сценарий:** Response validation выполняет queries после service return.

**Критерии ответа:** Map ORM to response data при открытой session; query-count test обнаруживает hidden I/O.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Async lazy-loading pitfalls и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Async lazy-loading pitfalls?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Async lazy-loading pitfalls: Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.

### Нормальный ответ уровня Junior

> Async lazy-loading pitfalls — тема, в которой я сначала фиксирую `unexpected I/O`, затем объясняю `missing greenlet-style problems` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Async lazy-loading pitfalls?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Критерии хорошего ответа

### Что обязательно упомянуть

- unexpected I/O
- missing greenlet-style problems
- explicit eager loading

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Async lazy-loading pitfalls?

## Задача

Сделай короткую письменную практику по теме **Async lazy-loading pitfalls**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Async lazy-loading pitfalls: Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
