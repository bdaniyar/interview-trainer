from main import make_counter

def test_state():
    counter = make_counter(10, 2)
    assert [counter(), counter(), counter()] == [12, 14, 16]
def test_independent():
    first, second = make_counter(), make_counter(100)
    assert first() == 1 and second() == 101 and first() == 2
