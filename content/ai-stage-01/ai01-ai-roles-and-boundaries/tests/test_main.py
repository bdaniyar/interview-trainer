import pytest
from main import choose_approach


@pytest.mark.parametrize(("requirements", "expected"), [
    ({"database", "new_text"}, "sql"),
    ({"existing_document", "learned_prediction"}, "retrieval"),
    ({"fixed_rules", "new_text"}, "llm"),
    ({"database"}, "sql"),
    ({"existing_document"}, "retrieval"),
])
def test_new_combinations(requirements, expected):
    before = set(requirements)
    assert choose_approach(requirements) == expected
    assert requirements == before


@pytest.mark.parametrize("requirements", [
    set(), {"python"}, {"database", "unknown"},
    {"database", "existing_document"}, {"learned_prediction", "new_text"},
])
def test_ambiguous_or_unknown_requirements(requirements):
    with pytest.raises(ValueError):
        choose_approach(requirements)
