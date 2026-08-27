import inspect
import pytest
from main import batched


def test_is_generator_function():
    assert inspect.isgeneratorfunction(batched)


def test_groups_values():
    assert list(batched(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_is_lazy():
    seen = []
    source = (seen.append(i) or i for i in range(5))
    result = batched(source, 2)
    assert seen == []
    assert next(result) == [0, 1]
    assert seen == [0, 1]


def test_rejects_invalid_size():
    with pytest.raises(ValueError):
        next(batched([1], 0))
