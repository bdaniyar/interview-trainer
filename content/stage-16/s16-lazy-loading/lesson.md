# Lazy loading

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Lazy loading**, а не только запомнить термин;
- прочитать и изменить короткий пример для `implicit query`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**implicit query.** `implicit query` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**session dependency.** Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

**async pitfalls.** `async pitfalls` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.


### Важный нюанс / ограничение

Граница Junior: уверенно объясняй `implicit query` и `session dependency` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `implicit query`; проверяй именно наблюдаемый contract, а не название инструмента.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- implicit query
- session dependency
- async pitfalls

### Полезно

- связать Lazy loading с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview дополнительный вопрос

## Примеры кода

### Lazy loading: отдельный пример

```text
Сценарий: Доступ к relationship запускает SQL в serializer.

Проверка:
Загрузить данные явно, запретить accidental lazy load и не прятать I/O за attribute access.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Практика

**A · Предсказание результата/reasoning.** Предскажи результат минимального примера для `implicit query` до запуска.

**B · Найди ошибку.** Найди нарушение `session dependency` и объясни конкретное последствие.

**E · Ответ на собеседовании.** Дай ответ про Lazy loading за 60 секунд: определение, механизм, пример, ограничение.

## Практика: Отладка

### Unexpected lazy load

**Сценарий:** Доступ к relationship запускает SQL в serializer.

**Критерии ответа:** Загрузить данные явно, запретить accidental lazy load и не прятать I/O за attribute access.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### Detached instance

**Сценарий:** После закрытия Session serializer читает unloaded relationship и падает.

**Критерии ответа:** Сформировать DTO внутри session boundary или eager-load нужное; не возвращать live ORM entity наружу.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Lazy loading и какой механизм здесь важно понимать Junior-разработчику?

### Дополнительный вопрос

Какое ограничение или типичная ошибка относится именно к теме Lazy loading?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

Lazy loading: Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.

### Нормальный ответ уровня Junior

> Lazy loading — тема, в которой я сначала фиксирую `implicit query`, затем объясняю `session dependency` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / дополнительный вопрос

**Какое ограничение или типичная ошибка относится именно к теме Lazy loading?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Критерии хорошего ответа

### Что обязательно упомянуть

- implicit query
- session dependency
- async pitfalls

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какое ограничение или типичная ошибка относится именно к теме Lazy loading?

## Задача

Сделай короткую письменную практику по теме **Lazy loading**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** Lazy loading: Это часть SQLAlchemy 2.x процесс доступа к данным: statement, Session, identity map и жизненный цикл транзакции.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
