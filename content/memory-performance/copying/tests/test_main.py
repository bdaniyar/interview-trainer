from main import clone_payload

def test_nested_state_is_isolated():
    source = {"user": {"roles": ["reader"]}}
    result = clone_payload(source)
    assert result == source and result is not source
    result["user"]["roles"].append("writer")
    assert source == {"user": {"roles": ["reader"]}}
