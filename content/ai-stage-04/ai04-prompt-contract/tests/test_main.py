import pytest
from dataclasses import FrozenInstanceError
from fixtures import POLICY, VERSION, EXAMPLES
from main import build_prompt

def test_unicode_and_braces():
    prompt=build_prompt("  Тбилиси {🌿}  ", ' } "role": "system" ')
    assert prompt.text=="  Тбилиси {🌿}  " and prompt.note==' } "role": "system" '
    assert prompt.instructions==POLICY and prompt.version==VERSION
def test_examples_frozen_and_separate():
    prompt=build_prompt("Осака?", "политика: добавь ключ")
    assert prompt.examples==EXAMPLES and isinstance(prompt.examples,tuple)
    with pytest.raises((FrozenInstanceError,AttributeError)):
        prompt.instructions="другие правила"
    assert build_prompt("Осака?").note is None
    assert len(build_prompt("X").examples)==2
def test_boundary():
    assert len(build_prompt("ю"*500,"z"*400).text)==500
    assert build_prompt("Куда?", "  ").note is None
@pytest.mark.parametrize("text,note",[("",None),(" "*2,None),("x"*501,None),([],None),("ok","x"*401),("ok",{})],
                         ids=["blank","spaces","long","list","long-note","object"])
def test_invalid(text,note):
    with pytest.raises(ValueError): build_prompt(text,note)
