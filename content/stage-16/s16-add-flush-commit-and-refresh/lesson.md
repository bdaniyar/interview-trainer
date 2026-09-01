# Add, flush, commit and refresh

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Add, flush, commit and refresh**, а не только запомнить термин;
- прочитать и изменить короткий пример для ``add``;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

`add` присоединяет новую entity, `flush` отправляет pending SQL внутри transaction, `commit` фиксирует её, `refresh` перечитывает значения из БД.

### Как работает

Autoflush может сработать перед query; generated первичный ключ часто доступен после flush без commit.


### Важный нюанс / ограничение

После commit objects могут стать expired в зависимости от конфигурацию; refresh не заменяет правильного transaction ownership.

## Модель понимания

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- `add`
- `flush` sends SQL inside transaction
- `commit` finalizes
- `refresh` reloads

### Полезно

- созданный идентификатор может появиться после синхронизации с БД

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Add, flush, commit and refresh: отдельный пример

```text
Сценарий: repository.save неожиданно commit-ит половину use case.

Проверка:
Transaction boundary принадлежит service/use case; repository делает add/flush, caller решает commit/rollback.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Типичные ошибки

### Ошибка 1

Commit только ради получения id ломает атомарный use case; внутри открытой transaction достаточно flush.

## Практика

**A · Предсказание результата.** Измени один input в примере ``add`` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий ``flush` sends SQL inside transaction`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие ``add``, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Add, flush, commit and refresh за 45–60 секунд и назови одно ограничение.

## Практика: Отладка

### Commit in repository

**Сценарий:** repository.save неожиданно commit-ит половину use case.

**Критерии ответа:** Transaction boundary принадлежит service/use case; repository делает add/flush, caller решает commit/rollback.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Вопросы с собеседований

### Основной вопрос

Что такое Add, flush, commit and refresh и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Add, flush, commit and refresh?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`add` присоединяет новую entity, `flush` отправляет pending SQL внутри transaction, `commit` фиксирует её, `refresh` перечитывает значения из БД.

### Нормальный ответ уровня Junior

> `add` присоединяет новую entity, `flush` отправляет pending SQL внутри transaction, `commit` фиксирует её, `refresh` перечитывает значения из БД. Autoflush может сработать перед query; generated первичный ключ часто доступен после flush без commit. Важное ограничение: После commit objects могут стать expired в зависимости от конфигурацию; refresh не заменяет правильного transaction ownership.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Add, flush, commit and refresh?**

Commit только ради получения id ломает атомарный use case; внутри открытой transaction достаточно flush.

## Критерии хорошего ответа

### Что обязательно упомянуть

- `add`
- `flush` sends SQL inside transaction
- `commit` finalizes
- `refresh` reloads

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Commit только ради получения id ломает атомарный use case; внутри открытой transaction достаточно flush.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Add, flush, commit and refresh?

## Задача

### Flush generated id

add_and_flush делает add+flush и возвращает entity; commit запрещён.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `add` присоединяет новую entity, `flush` отправляет pending SQL внутри transaction, `commit` фиксирует её, `refresh` перечитывает значения из БД.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Commit только ради получения id ломает атомарный use case; внутри открытой transaction достаточно flush.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
