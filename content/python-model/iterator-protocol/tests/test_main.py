import pytest
from main import Countdown


def test_iterator_protocol():
    countdown = Countdown(3)
    assert iter(countdown) is countdown


def test_iteration_order():
    assert list(Countdown(4)) == [4, 3, 2, 1]


def test_stop_iteration_is_stable():
    countdown = Countdown(1)
    assert next(countdown) == 1
    with pytest.raises(StopIteration):
        next(countdown)
    with pytest.raises(StopIteration):
        next(countdown)


def test_empty_input():
    assert list(Countdown(0)) == []
