from main import first_or_default

def test_list(): assert first_or_default([3, 4]) == 3
def test_lazy():
    touched = []
    def values():
        touched.append(1); yield "first"
        touched.append(2); yield "second"
    assert first_or_default(values()) == "first" and touched == [1]
def test_empty(): assert first_or_default(iter(()), "none") == "none"
