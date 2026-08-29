# Object, type, name and binding

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- объяснить `object` своими словами и связать с backend-сценарием;
- объяснить `type` своими словами и связать с backend-сценарием;
- объяснить `name` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Добро пожаловать в курс Python для опытных разработчиков. Здесь мы не учимся писать `if` и `for` — мы разбираем, почему Python ведёт себя именно так, и как использовать это в реальном backend-коде.

На платформе можно читать теорию и сразу применять её на практике, редактировать файлы в браузере, запускать решение и проверять его тестами.

### Как Python смотрит на объекты

В Python почти всё — объекты: числа, строки, функции, классы и даже сами классы классов.

```python
message = "Learn with Pythoria"
```

Переменная `message` не хранит строку внутри себя. Она связывает имя с объектом строки.

```python
a = [1, 2]
b = a  # b ссылается на тот же список
b.append(3)

print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3]
```

> [!NOTE]
> Имя связывается с объектом, а не «копирует значение» автоматически.

### Пространства имён

Пространство имён хранит соответствие между именем и объектом. Чаще всего встречаются локальное пространство функции, глобальное пространство модуля и встроенное пространство.

```python
title = "Backend powers the world"

def show():
    title = "Coding is magic"
    print(title)

show()
print(title)
```

### Mutability и immutability

`list`, `dict`, `set` изменяемы; `int`, `str`, `tuple` обычно неизменяемы.

| Тип | Изменяемость | Хешируемость |
| --- | --- | --- |
| `list` | да | нет |
| `dict` | да | нет |
| `str` | нет | да |
| `tuple` | нет | зависит от элементов |

### Data model и dunder-методы

Когда ты пишешь `len(obj)`, `print(obj)` или `obj[0]`, Python использует протоколы data model и специальные методы.

```python
class LessonBox:
    def __init__(self, topic):
        self.topic = topic

    def __repr__(self):
        return f"LessonBox(topic={self.topic!r})"

    def __str__(self):
        return f"Урок: {self.topic}"
```

### MRO и поиск атрибутов

MRO определяет порядок поиска методов при наследовании. Для `class D(B, C)` Python пройдёт цепочку `D -> B -> C -> A -> object` согласно C3-линеаризации.

### Дескрипторы

Дескриптор управляет доступом к атрибуту через `__get__`, `__set__` и `__delete__`. На этой идее построены `property`, методы и многие ORM.

### Метаклассы

Обычный объект создаётся классом, а класс обычно создаётся метаклассом `type`.

```python
class Event:
    pass

print(type(Event))    # <class 'type'>
print(type(Event()))  # <class '__main__.Event'>
```

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Object, type, name and binding: отдельный пример

```python
message = "Learn with Pythoria"
alias = message

print(type(message).__name__)
print(message is alias)

alias = alias.upper()
print(message, alias)
```

Имена `message` и `alias` сначала связаны с одним `str`; новый assignment переводит только `alias` на новый объект.

## Common mistakes

**Ошибка:** Объяснять переменную как коробку, которая всегда содержит независимое значение.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Object, type, name and binding** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи identity и состояние объекта после двух присваиваний и одной мутации. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- object
- type
- name
- binding
- Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Объяснять переменную как коробку, которая всегда содержит независимое значение.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- object
- type
- name
- binding
- переменная как имя, связанное с объектом
- assignment не копирует объект
- rebinding
- multiple names for one object.

## Задача

В `main.py` создай класс `MagicBox`:

- конструктор принимает строку `text`;
- `__str__` возвращает `Message: <text>`;
- `__repr__` возвращает `MagicBox(text='<text>')`;
- `__len__` возвращает длину `text`;
- `__bool__` возвращает `False` для пустой строки, иначе `True`.

Создай объекты `filled = MagicBox("Coding is magic")` и `empty = MagicBox("")`, затем переменные `filled_str`, `filled_repr`, `filled_len`, `filled_bool`, `empty_bool`. Ничего не печатай: тесты проверят переменные модуля.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Object, type, name and binding**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
