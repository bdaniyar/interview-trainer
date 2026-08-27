import pytest
from main import index_by_id

def test_builds_index():
    rows = [{"id": 2}, {"id": 1}]
    assert index_by_id(rows) == {2: rows[0], 1: rows[1]}
def test_duplicate():
    with pytest.raises(ValueError, match="duplicate id: 1"):
        index_by_id([{"id": 1}, {"id": 1}])
def test_empty(): assert index_by_id([]) == {}
