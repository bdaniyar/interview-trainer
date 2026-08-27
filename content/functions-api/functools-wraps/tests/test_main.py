import inspect
from main import traced

@traced
def add(left: int, right: int = 1) -> int:
    "Add values."
    return left + right

def test_behavior(): assert add(2, right=3) == 5
def test_metadata():
    assert add.__name__ == "add" and add.__doc__ == "Add values."
    assert str(inspect.signature(add)) == "(left: int, right: int = 1) -> int"
def test_marker(): assert add.traced is True
