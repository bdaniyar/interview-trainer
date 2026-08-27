# Mutability and references

Переменные в Python — имена, связанные с объектами. Если два имени ссылаются на изменяемый объект, мутация наблюдается через обе ссылки.

```python
original = {"roles": ["reader"]}
alias = original
alias["roles"].append("writer")
assert original["roles"] == ["reader", "writer"]
```

Переприсваивание имени не меняет прежний объект, а связывает имя с новым. Мутация, напротив, сохраняет identity объекта.

## Задача

Реализуй `append_marker(items, marker)`: добавь marker в переданный список и верни **тот же** список. Не создавай копию.
