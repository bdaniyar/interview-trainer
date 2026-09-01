# Dataclasses

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; OOP/data model важны для чтения framework и domain code.

## Учебные цели

После урока ты сможешь:

- восстановить mental model темы **Dataclasses**, а не только запомнить термин;
- прочитать и изменить короткий пример для `generated methods`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Теория

### Что это

`@dataclass` генерирует `__init__`, `__repr__`, equality и другие методы по объявленным fields.

### Как работает

Fields обрабатываются по порядку; `field(default_factory=list)` создаёт новый mutable default для каждого instance. `frozen=True` запрещает обычное присваивание полям, но не даёт глубокой неизменяемости.


### Важный нюанс / ограничение

Dataclass подходит для внутренних data/value objects; Pydantic валидирует недоверенный input, а ORM models отвечают за persistence.

## Модель понимания

У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из теории.

## Что нужно знать на Junior

### Обязательно

- generated methods
- equality/repr
- mutable fields
- `field(default_factory=...)`

### Полезно

- frozen
- domain data vs ORM/Pydantic models

### Можно не учить глубоко

- внутренние детали реализации за пределами обычных Junior дополнительный вопрос

## Примеры кода

### Dataclasses: отдельный пример

```python
from dataclasses import dataclass, field

@dataclass(slots=True)
class User:
    email: str
    roles: list[str] = field(default_factory=list)

a, b = User("a@example.com"), User("b@example.com")
a.roles.append("admin")
print(b.roles)
```

`default_factory` создаёт независимый mutable default для каждого dataclass instance.

## Типичные ошибки

### Ошибка 1

Mutable default нужно задавать через `default_factory`, иначе instances получат общее состояние или dataclass отклонит объявление.

## Практика

**A · Предсказание результата.** Измени один input в примере `generated methods` и предскажи результат до запуска.

**B · Найди ошибку.** Найди код, нарушающий `equality/repr`, и объясни конкретное последствие.

**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `generated methods`, и добавь один граничный случай test.

**E · Ответ на собеседовании.** Объясни Dataclasses за 45–60 секунд и назови одно ограничение.

## Предсказание результата кода

### dataclass equality

```python
from dataclasses import dataclass
@dataclass
class Point:
    x: int
print(Point(1) == Point(1), Point(1) is Point(1))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Ожидаемый результат:

```text
True False
```

dataclass генерирует equality по полям, но каждый constructor call создаёт новый объект.

Типичная ошибка мышления: `dataclass-equality`.

</details>

## Вопросы с собеседований

### Основной вопрос

Что такое Dataclasses и как это работает?

### Дополнительный вопрос

Какая типичная ошибка связана с Dataclasses?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Хорошие ответы

### Короткий ответ

`@dataclass` генерирует `__init__`, `__repr__`, equality и другие методы по объявленным fields.

### Нормальный ответ уровня Junior

> `@dataclass` генерирует `__init__`, `__repr__`, equality и другие методы по объявленным fields. Fields обрабатываются по порядку; `field(default_factory=list)` создаёт новый mutable default для каждого instance. `frozen=True` запрещает обычное присваивание полям, но не даёт глубокой неизменяемости. Важное ограничение: Dataclass подходит для внутренних data/value objects; Pydantic валидирует недоверенный input, а ORM models отвечают за persistence.

### Углубление / дополнительный вопрос

**Какая типичная ошибка связана с Dataclasses?**

Mutable default нужно задавать через `default_factory`, иначе instances получат общее состояние или dataclass отклонит объявление.

## Критерии хорошего ответа

### Что обязательно упомянуть

- generated methods
- equality/repr
- mutable fields
- `field(default_factory=...)`

### Что улучшит ответ

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- пример из backend-разработки только при естественной связи.

### Частые неправильные ответы

- Mutable default нужно задавать через `default_factory`, иначе instances получат общее состояние или dataclass отклонит объявление.
- пересказ одного определения без механизма или примера.

### Дополнительный вопрос

- Какая типичная ошибка связана с Dataclasses?

## Задача

### Immutable BookingWindow

Создай frozen slots dataclass BookingWindow(start,end); end строго больше start; duration возвращает разницу.

Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок.
## Шпаргалка

Перед собеседованием запомни:

- **Что это:** `@dataclass` генерирует `__init__`, `__repr__`, equality и другие методы по объявленным fields.
- **Механизм:** У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.
- **Ограничение:** Mutable default нужно задавать через `default_factory`, иначе instances получат общее состояние или dataclass отклонит объявление.
- **Глубина для Junior:** знать обязательные пункты выше; внутренние детали реализации можно уточнить по документации.

## Источники

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [dataclasses](https://docs.python.org/3.12/library/dataclasses.html)

Последняя проверка версий: **2026-08-27**.
