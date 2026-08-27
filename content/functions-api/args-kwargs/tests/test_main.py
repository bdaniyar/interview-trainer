from main import merge_options

def test_override(): assert merge_options({"limit": 20, "active": True}, limit=5) == {"limit": 5, "active": True}
def test_no_mutation():
    base = {"limit": 20}
    result = merge_options(base, offset=3)
    assert base == {"limit": 20} and result is not base
