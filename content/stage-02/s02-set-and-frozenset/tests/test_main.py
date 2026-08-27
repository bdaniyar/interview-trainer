from main import normalize_scopes

def test_normalizes(): assert normalize_scopes([" Read ", "WRITE", "read"]) == frozenset({"read", "write"})
def test_empty_values(): assert normalize_scopes(["", "  "]) == frozenset()
def test_immutable(): assert isinstance(normalize_scopes(["read"]), frozenset)
