# List

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **List**, а не только запомнить термин;
- прочитать и изменить короткий пример для `order`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`list` — упорядоченная изменяемая последовательность. Она хранит references на элементы, поддерживает индексы, срезы и дубликаты; один список может содержать объекты разных типов.

### Как работает

`append(x)` добавляет один элемент, `extend(iterable)` добавляет элементы iterable, `insert(i, x)` сдвигает хвост. Доступ по индексу обычно O(1), поиск значения и удаление по значению — O(n), вставка в начало — O(n). Срез создаёт новый внешний list, но остаётся shallow copy.


### Пример

```python
items = ["created", "paid"]
items.append("shipped")
items.extend(["delivered", "closed"])

print(items[1:3])
# ['paid', 'shipped']
```

### Важный нюанс / limitation

Методы `append`, `extend`, `sort` меняют список на месте и возвращают `None`. Во время обхода не стоит менять размер того же списка: элементы можно пропустить. Для очереди с частым удалением слева лучше `collections.deque`.

### Где используется в backend

Список естественен для упорядоченного JSON-массива результатов API; для быстрого поиска по id дополнительно строят dict.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- append vs extend
- индексы и срезы
- mutability и aliases
- базовая сложность операций

### Полезно

- deque для очереди
- stable sort и key function

### Можно не учить глубоко

- стратегия over-allocation CPython в точных коэффициентах

## Code examples

### List: отдельный пример

```python
events = ["created", "paid"]
events.append("sent")
last = events.pop()

print(events)
print(last)
```

List сохраняет порядок, поддерживает mutation и удобен для последовательного набора событий.

## Common mistakes

### Ошибка 1

`items = items.append(value)` заменит переменную на `None`.

### Ошибка 2

`matrix = [[0] * 3] * 3` создаёт три ссылки на одну строку, поэтому изменение одной строки видно во всех.

## Practice

**A · Code prediction.** Что произойдёт после `rows = [[0]] * 3; rows[0].append(1)`?

**B · Find the bug.** Исправь `items = items.sort(key=...)`.

**C · Rewrite.** Замени цикл накопления квадратов простой читаемой comprehension.

**D · Small task.** Верни уникальные элементы списка с сохранением порядка.

## Code prediction

### Срез создаёт новый list

```python
items = [1, 2, 3]
part = items[:]
part.append(4)
print(items, part)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
[1, 2, 3] [1, 2, 3, 4]
```

Срез создаёт новый внешний список; для immutable int этого достаточно для независимости.

Misconception: `slice-copy`.

</details>

### Unpacking со starred target

```python
first, *middle, last = [1, 2, 3, 4]
print(first, middle, last)
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
1 [2, 3] 4
```

Starred target собирает промежуточные элементы в новый list.

Misconception: `unpacking`.

</details>

## Interview questions

### Основной вопрос

Что такое list, какие у него основные операции и их сложность?

### Follow-up

Когда вместо list выбрать set, dict или deque?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

List — ordered mutable sequence; индекс и append обычно O(1), поиск и вставка в начало — O(n).

### Нормальный Junior answer

> `list` хранит упорядоченную последовательность references, допускает дубликаты и меняется на месте. Доступ по индексу и append обычно O(1), а поиск значения, удаление по значению и вставка в начало — O(n). `append` добавляет один объект, `extend` — все элементы iterable. Срез создаёт новый внешний список, но копия остаётся shallow.

### Углубление / follow-up

**Когда вместо list выбрать set, dict или deque?**

Set — для уникальности и быстрого membership, dict — для lookup по ключу, deque — для частых операций с обоих концов.

## Expected answer rubric

### Must mention

- append vs extend
- индексы и срезы
- mutability и aliases
- базовая сложность операций

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- `items = items.append(value)` заменит переменную на `None`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Когда вместо list выбрать set, dict или deque?

## Задача

Сделай короткую письменную практику по теме **List**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** List — ordered mutable sequence; индекс и append обычно O(1), поиск и вставка в начало — O(n).
- **Механизм:** Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.
- **Ограничение:** `items = items.append(value)` заменит переменную на `None`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
