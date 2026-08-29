# Tuple

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; collections — ежедневная data transformation работа backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Tuple**, а не только запомнить термин;
- прочитать и изменить короткий пример для `immutability`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`tuple` — упорядоченная неизменяемая последовательность. После создания нельзя заменить, добавить или удалить элемент, но tuple может содержать mutable object, состояние которого всё ещё меняется.

### Как работает

Запятые создают tuple: `(value,)` — tuple из одного элемента, а `(value)` — просто value в скобках. Packing собирает значения, unpacking распределяет их по именам. Tuple может быть dict key, только если каждый его элемент hashable.


### Пример

```python
point = (43.2389, 76.8897)
latitude, longitude = point
locations = {point: "Almaty"}

print(latitude, locations[point])
# 43.2389 Almaty
```

### Важный нюанс / limitation

Immutability контейнера не гарантирует deep immutability: `([1],)` нельзя хешировать, а внутренний list можно менять. Для сущности с именованными полями и поведением dataclass обычно понятнее позиционного tuple.

### Где используется в backend

Tuple удобен для внутренней фиксированной пары `(host, port)` или составного hashable key; JSON всё равно сериализует его как array.

## Mental model

Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- immutability
- packing/unpacking
- одиночный tuple
- условия hashability

### Полезно

- понимать, когда dataclass яснее tuple

### Можно не учить глубоко

- memory layout tuple в CPython

## Code examples

### Tuple: отдельный пример

```python
point = (43.2389, 76.8897)
latitude, longitude = point
locations = {point: "Almaty"}

print(latitude, longitude)
print(locations[point])
```

Tuple выражает фиксированную запись и может быть dict key, если все элементы hashable.

## Common mistakes

### Ошибка 1

`single = (42)` создаёт int, не tuple; нужна запятая: `(42,)`.

### Ошибка 2

Считать любой tuple hashable: `([1],)` содержит unhashable list.

## Practice

**A · Code prediction.** Определи тип `(1)` и `(1,)`.

**B · Find the bug.** Объясни `TypeError` для `{([1],): 'value'}`.

**C · Rewrite.** Замени нечитабельный 6-позиционный tuple на dataclass.

## Interview questions

### Основной вопрос

Чем tuple отличается от list и когда tuple можно использовать как ключ dict?

### Follow-up

Почему tuple с list внутри не является hashable?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Tuple неизменяем и может быть ключом dict, если все его элементы hashable; list изменяем и не hashable.

### Нормальный Junior answer

> Tuple — ordered immutable sequence. Его структуру нельзя изменить после создания, поэтому tuple из hashable элементов сам hashable и может быть ключом dict. Но tuple с list внутри уже не hashable, и внутренний list можно мутировать. Одноэлементный tuple записывается с запятой: `(value,)`.

### Углубление / follow-up

**Почему tuple с list внутри не является hashable?**

Hash ключа должен оставаться стабильным; list меняется и не имеет hash, поэтому содержащий его tuple тоже нельзя хешировать.

## Expected answer rubric

### Must mention

- immutability
- packing/unpacking
- одиночный tuple
- условия hashability

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- `single = (42)` создаёт int, не tuple; нужна запятая: `(42,)`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Почему tuple с list внутри не является hashable?

## Задача

Сделай короткую письменную практику по теме **Tuple**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Tuple неизменяем и может быть ключом dict, если все его элементы hashable; list изменяем и не hashable.
- **Механизм:** Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.
- **Ограничение:** `single = (42)` создаёт int, не tuple; нужна запятая: `(42,)`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python built-in types](https://docs.python.org/3.12/library/stdtypes.html)

Последняя проверка версий: **2026-08-27**.
