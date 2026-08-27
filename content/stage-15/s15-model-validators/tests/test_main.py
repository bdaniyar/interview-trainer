import pytest
from pydantic import ValidationError
from main import BookingPeriod

def test_valid(): assert BookingPeriod(start=2, end=5).end == 5
def test_invalid():
    with pytest.raises(ValidationError, match="end must be after start"):
        BookingPeriod(start=5, end=5)
