from dataclasses import FrozenInstanceError
import pytest
from main import BookingWindow

def test_contract(): assert BookingWindow(10, 15).duration == 5
def test_validation():
    with pytest.raises(ValueError): BookingWindow(10, 10)
def test_frozen_slots():
    value = BookingWindow(1, 2)
    with pytest.raises((FrozenInstanceError, AttributeError)): value.start = 0
    assert not hasattr(value, "__dict__")
