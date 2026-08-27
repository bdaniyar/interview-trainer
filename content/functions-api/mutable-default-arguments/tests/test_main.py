from main import add_tag


def test_calls_do_not_share_state():
    assert add_tag("python") == ["python"]
    assert add_tag("backend") == ["backend"]


def test_mutates_explicit_list():
    tags = ["api"]
    result = add_tag("async", tags)
    assert result is tags
    assert tags == ["api", "async"]


def test_signature_default_is_safe():
    assert add_tag.__defaults__ == (None,)
