import pytest
from main import score

EXPECTED={"city":"Яссы","guests":4,"check_in":"2030-01-03","check_out":None}
C=[{"id":"q","status":"needs_clarification","trip":EXPECTED}]

def test_known_and_unknown_are_separate():
    result=score(C,{"q":{"status":"needs_clarification","trip":{**EXPECTED,"guests":5},
                         "schema_valid":True,"domain_valid":True}})
    assert result["metrics"]["field_accuracy"]["passed"]==2
    assert result["metrics"]["field_accuracy"]["total"]==3
    assert result["metrics"]["unknown_correctness"]=={"passed":1,"total":1,"rate":1}
    assert result["metrics"]["schema_validity"]["rate"]==1
    assert result["errors"]=={"q":["guests"]}

def test_missing_key_or_output_can_never_match_null():
    for out in ({},{"q":{"status":"needs_clarification","trip":{k:v for k,v in EXPECTED.items() if k!="check_out"}}}):
        result=score(C,out)
        assert result["metrics"]["unknown_correctness"]["rate"]==0
        assert result["metrics"]["exact_match"]["rate"]==0

def test_empty_returns_undefined():
    result=score([],{})
    assert all(row=={"passed":0,"total":0,"rate":None} for row in result["metrics"].values())
    assert result["errors"]=={}

def test_refusal_with_trip_is_an_error():
    cases=[{"id":"c","status":"refusal","trip":None}]
    result=score(cases,{"c":{"status":"refusal","trip":EXPECTED}})
    assert result["metrics"]["refusal_handling"]["rate"]==0
    assert result["errors"]=={"c":["refusal_payload"]}

def test_status_and_unexpected_payload():
    cases=[{"id":"x","status":"incomplete","trip":None}]
    result=score(cases,{"x":{"status":"completed","trip":EXPECTED,"schema_valid":True,"domain_valid":False}})
    assert result["errors"]=={"x":["status","unexpected_payload"]}
    assert result["metrics"]["outcome_accuracy"]["rate"]==0
    assert result["metrics"]["domain_validity"]["rate"]==0

def test_duplicate_case_errors():
    with pytest.raises(ValueError): score(C+C,{})

def test_boolean_is_not_an_integer_fact():
    expected={**EXPECTED,"guests":1}
    actual={**expected,"guests":True}
    result=score([{**C[0],"trip":expected}],{"q":{"status":"needs_clarification","trip":actual}})
    assert "guests" in result["errors"]["q"]
