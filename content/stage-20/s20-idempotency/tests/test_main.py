from copy import deepcopy
import hashlib
import json
import pytest
from main import fingerprint_request

def test_canonical_utf8_and_no_mutation():
    value={'b':[1,True,None],'a':{'Я':'value'}};saved=deepcopy(value)
    expected=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    assert fingerprint_request(value)==expected
    assert fingerprint_request({'a':{'Я':'value'},'b':[1,True,None]})==expected
    assert value==saved

def test_list_order_and_boolean_identity():
    assert fingerprint_request({'x':[1,2]})!=fingerprint_request({'x':[2,1]})
    assert fingerprint_request({'x':True})!=fingerprint_request({'x':1})

@pytest.mark.parametrize('value',[[],None,{1:'x'},{'x':{2:'bad'}},{'x':{1,2}},{'x':float('nan')},{'x':float('inf')}], ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5', 'case-6', 'case-7'])
def test_invalid(value):
    with pytest.raises(ValueError):fingerprint_request(value)

def test_cycles_are_invalid_but_shared_references_are_valid():
    value={};value['self']=value
    with pytest.raises(ValueError):fingerprint_request(value)
    shared=[1];assert fingerprint_request({'a':shared,'b':shared})==fingerprint_request({'a':[1],'b':[1]})
