from main import make_multipliers

def test_captures_each_value():
    functions = make_multipliers([2, 3, 5])
    assert [function(4) for function in functions] == [8, 12, 20]
def test_empty(): assert make_multipliers([]) == []
