import inspect
import pytest
from main import build_page_query

def test_contract():
    assert build_page_query("users", limit=10, offset=5) == {"resource": "users", "limit": 10, "offset": 5}
def test_signature():
    kinds = [p.kind for p in inspect.signature(build_page_query).parameters.values()]
    assert kinds == [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.KEYWORD_ONLY]
def test_invalid():
    with pytest.raises(ValueError): build_page_query("users", limit=0)
