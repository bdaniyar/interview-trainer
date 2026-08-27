# Iterator protocol

Iterable возвращает iterator из `__iter__`. Iterator хранит состояние обхода, возвращает себя из `__iter__` и выдаёт элементы через `__next__`. Когда элементы закончились, он поднимает `StopIteration`.

```python
iterator = iter([10, 20])
next(iterator)  # 10
next(iterator)  # 20
```

Цикл `for` скрывает эти вызовы, но использует тот же протокол.

## Задача

Создай iterator-класс `Countdown(start)`, который выдаёт числа от `start` до `1`. После окончания каждый следующий `next()` должен поднимать `StopIteration`.
