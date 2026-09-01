# BackgroundTasks

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **BackgroundTasks**, а не только запомнить термин;
- прочитать и изменить короткий пример для `runs after response in same application process`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

FastAPI `BackgroundTasks` запускает небольшую in-process работу после отправки response.

### Как работает

Task работает в том же application process и не имеет гарантий durable delivery, distributed retry или восстановления после crash.


### Важный нюанс / ограничение

Используй механизм для небольших некритичных действий; durable jobs требуют queue/worker и idempotency.

## Модель понимания

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- выполняется после ответа в том же процессе приложения
- small non-critical work
- not durable
- lost on crash

### Полезно

- не является заменой Celery или шаблону outbox

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### BackgroundTasks: отдельный пример

```python
def example_s14_backgroundtasks() -> tuple[str, ...]:
    # BackgroundTasks: проверяем отдельный contract урока.
    return ('runs after response in same application process', 'small non-critical work', 'not durable', 'lost on crash',)

assert example_s14_backgroundtasks()
```

Проследи request через router, validation, dependency, service и response model.

## Типичные ошибки

### Ошибка 1

Критическое письмо или payment только через BackgroundTasks может потеряться при restart process.

## Практика

**A · Предсказание результата.** Измени один input в примере `runs after response in same application process` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `small non-critical work`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `runs after response in same application process`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни BackgroundTasks за 45–60 секунд и назови одно ограничение.

## Вопросы с собеседований

### Основной вопрос

Что такое BackgroundTasks и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с BackgroundTasks?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

FastAPI `BackgroundTasks` запускает небольшую in-process работу после отправки response.

### Нормальный ответ уровня Junior

> FastAPI `BackgroundTasks` запускает небольшую in-process работу после отправки response. Task работает в том же application process и не имеет гарантий durable delivery, distributed retry или восстановления после crash. Важное ограничение: Используй механизм для небольших некритичных действий; durable jobs требуют queue/worker и idempotency.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с BackgroundTasks?**

Критическое письмо или payment только через BackgroundTasks может потеряться при restart process.

## Критерии хорошего ответа

### Что обязательно упомянуть

- выполняется после ответа в том же процессе приложения
- small non-critical work
- not durable
- lost on crash

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Критическое письмо или payment только через BackgroundTasks может потеряться при restart process.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с BackgroundTasks?

## Задача

Сделай короткую письменную практику по теме **BackgroundTasks**: реши один пункт из раздела «Практика», затем сравни своё объяснение с хорошим ответом уровня Junior. Для этого урока автоматические скрытые тесты не требуются.

## Шпаргалка

Перед собеседованием запомни:

- **Что это:** FastAPI `BackgroundTasks` запускает небольшую in-process работу после отправки response.
- **Механизм:** Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.
- **Ограничение:** Критическое письмо или payment только через BackgroundTasks может потеряться при restart process.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
