# Lazy loading

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Lazy loading**, а не только запомнить термин;
- прочитать и изменить короткий пример для `implicit query`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**implicit query.** `implicit query` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**session dependency.** Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

**async pitfalls.** `async pitfalls` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `implicit query` и `session dependency` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `implicit query`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- implicit query
- session dependency
- async pitfalls

### Полезно

- связать Lazy loading с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Lazy loading: отдельный пример

```text
Сценарий: Доступ к relationship запускает SQL в serializer.

Проверка:
Загрузить данные явно, запретить accidental lazy load и не прятать I/O за attribute access.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `implicit query` до запуска.

**B · Find the bug.** Найди нарушение `session dependency` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Lazy loading за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Unexpected lazy load

**Сценарий:** Доступ к relationship запускает SQL в serializer.

**Rubric:** Загрузить данные явно, запретить accidental lazy load и не прятать I/O за attribute access.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

### Detached instance

**Сценарий:** После закрытия Session serializer читает unloaded relationship и падает.

**Rubric:** Сформировать DTO внутри session boundary или eager-load нужное; не возвращать live ORM entity наружу.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Lazy loading и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Lazy loading?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Lazy loading: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Нормальный Junior answer

> Lazy loading — тема, в которой я сначала фиксирую `implicit query`, затем объясняю `session dependency` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Lazy loading?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Expected answer rubric

### Must mention

- implicit query
- session dependency
- async pitfalls

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Lazy loading?

## Задача

Сделай короткую письменную практику по теме **Lazy loading**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Lazy loading: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
