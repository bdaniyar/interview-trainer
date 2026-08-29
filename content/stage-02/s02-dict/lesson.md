# Dict

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Dict**, а не только запомнить термин;
- прочитать и изменить короткий пример для `keys/values/items`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`dict` — изменяемое отображение пар key-value. Ключи уникальны и должны быть hashable; значения могут быть любыми. С Python 3.7 insertion order гарантирован языком.

### Как работает

Dict использует hash table: по hash ключа ищется позиция, затем equality подтверждает совпадение. Lookup, insert и delete в среднем O(1). `keys()`, `values()` и `items()` возвращают динамические views. Обновление существующего ключа меняет value, но не перемещает ключ в порядке.


### Пример

```python
user = {"id": 1, "name": "Daniyar"}

print(user.get("name"))              # Daniyar
print(user.get("email"))             # None
print(user.get("email", "unknown"))  # unknown

roles = user.setdefault("roles", [])
roles.append("reader")
print(user["roles"])                 # ['reader']
```

### Важный нюанс / limitation

`data[key]` поднимает `KeyError`, `.get(key)` возвращает `None`, `.get(key, default)` — default и не меняет dict. `.setdefault(key, default)` при отсутствии вставляет default и всегда возвращает итоговое значение. Для накопления многих групп часто яснее `defaultdict(list)`.

### Где используется в backend

Dict удобен для индексирования ORM/DTO объектов по id и для чтения необязательных HTTP headers или JSON fields.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- hashable и уникальные keys
- `.get` vs `[]`
- `.setdefault`
- insertion order
- средняя O(1) lookup

### Полезно

- merge через `|` и `update`
- views и безопасная итерация
- когда выбрать defaultdict

### Можно не учить глубоко

- размер таблицы, perturb algorithm и layout CPython

## Code examples

### Dict: отдельный пример

```python
users = {
    7: {"name": "Aida"},
    9: {"name": "Daniyar"},
}
users[7]["active"] = True

print(users.get(8))
print(users[7])
```

Dict моделирует lookup по уникальному ключу; `.get` явно выражает допустимое отсутствие.

## Common mistakes

### Ошибка 1

`user['email']` падает с `KeyError`, если поле действительно необязательное; используй `.get` только когда отсутствие допустимо.

### Ошибка 2

`data[[1, 2]] = 'value'` падает с `TypeError: unhashable type: 'list'`.

### Ошибка 3

`bucket = data.setdefault('roles', [])` изменяет dict при отсутствующем ключе — в отличие от `.get`.

## Practice

**A · Code prediction.** Обнови существующий ключ и предскажи `list(data)`.

**B · Find the bug.** Исправь чтение необязательного `Authorization` без сокрытия обязательных полей.

**C · Rewrite.** Перепиши ручное группирование сначала с `setdefault`, затем сравни с `defaultdict(list)`.

**D · Small task.** Построй индекс пользователей по id и отклони дубликаты.

**F · Backend scenario.** Выбери структуру для ответа API, где важны порядок и lookup по id.

## Code prediction

### dict сохраняет insertion order

```python
data = {'b': 2, 'a': 1}
data['b'] = 3
print(list(data))
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
['b', 'a']
```

Замена значения существующего ключа не переносит ключ в конец.

Misconception: `dict-order`.

</details>

## Interview questions

### Основной вопрос

Что такое `dict`, как работает lookup и чем `.get()` отличается от `[]` и `.setdefault()`?

### Follow-up

Когда `.setdefault()` лучше заменить на `defaultdict(list)`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Dict — mutable mapping на hash table; lookup в среднем O(1), keys hashable. `[]` даёт KeyError, `.get` не меняет dict, `setdefault` может вставить default.

### Нормальный Junior answer

> `dict` хранит пары key-value; keys уникальны и hashable. В среднем lookup работает за O(1), потому что сначала используется hash, а затем equality. `data[key]` нужен, когда ключ обязателен, и поднимет `KeyError` при ошибке. `.get` удобен для допустимо отсутствующего значения и не меняет dict. `.setdefault` возвращает значение, но при отсутствии ещё и вставляет default. Dict сохраняет insertion order, а замена value не перемещает ключ.

### Углубление / follow-up

**Когда `.setdefault()` лучше заменить на `defaultdict(list)`?**

Когда код систематически группирует много значений по keys: defaultdict убирает повторяющееся создание bucket. Для единичной вставки setdefault проще и не меняет тип mapping.

## Expected answer rubric

### Must mention

- mutable mapping
- hashable unique keys
- average O(1)
- insertion order
- get/setdefault semantics

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- `user['email']` падает с `KeyError`, если поле действительно необязательное; используй `.get` только когда отсутствие допустимо.
- пересказ одного определения без механизма или примера.

### Follow-up

- Когда `.setdefault()` лучше заменить на `defaultdict(list)`?

## Задача

### Индекс без тихих дублей

Построй dict записей по id. Повторный id должен вызвать ValueError; входной list не изменяй.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Dict — mutable mapping на hash table; lookup в среднем O(1), keys hashable. `[]` даёт KeyError, `.get` не меняет dict, `setdefault` может вставить default.
- **Механизм:** Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.
- **Ограничение:** `user['email']` падает с `KeyError`, если поле действительно необязательное; используй `.get` только когда отсутствие допустимо.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
