import main


def test_magic_box_protocols():
    box = main.MagicBox("hello")
    assert str(box) == "Message: hello"
    assert repr(box) == "MagicBox(text='hello')"
    assert len(box) == 5
    assert bool(box) is True


def test_empty_box_is_falsy():
    assert bool(main.MagicBox("")) is False


def test_required_module_values():
    assert main.filled_str == "Message: Coding is magic"
    assert main.filled_repr == "MagicBox(text='Coding is magic')"
    assert main.filled_len == 15
    assert main.filled_bool is True
    assert main.empty_bool is False
