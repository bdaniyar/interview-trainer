from types import SimpleNamespace as NS
import pytest
from fixtures import Envelope
from main import parse_response

PAYLOAD={"trip":{"city":"Риддер","check_in":None,"check_out":"2028-03-01","guests":None}}

def provider(**changes):
    return NS(**({"model":"mock-3","schema_version":"trip.schema.v1","status":"completed",
                  "output":[NS(type="reasoning"),NS(type="message",content=[NS(type="output_text")])],
                  "output_parsed":PAYLOAD}|changes))
@pytest.mark.parametrize("typed",[False,True])
def test_typed_nested_and_versions(typed):
    parsed=Envelope.model_validate(PAYLOAD) if typed else PAYLOAD
    result=parse_response(provider(output_parsed=parsed),"trip.prompt.v4")
    assert (result.model,result.prompt_version,result.schema_version)==("mock-3","trip.prompt.v4","trip.schema.v1")
    assert result.status=="completed" and result.trip.model_dump()==PAYLOAD["trip"]
def test_refusal_ignores_partial():
    refusal=NS(type="message",content=[NS(type="refusal",refusal="private")])
    result=parse_response(provider(status="incomplete",output=[refusal]),"p")
    assert result.status=="refusal" and result.trip is None and "private" not in repr(result)
def test_incomplete_ignores_valid_payload():
    result=parse_response(provider(status="incomplete"),"p")
    assert result.status=="incomplete" and result.trip is None
@pytest.mark.parametrize("changes",[{"output_parsed":None},{"output_parsed":"{}"},{"output_parsed":{"trip":{"city":None}}},
                                   {"schema_version":"trip.schema.v0"},{"output":None},{"model":3},{"status":"unknown"},
                                   {"output":[NS(type="message",content=[None])]}],
                          ids=["missing","raw","nested","revision","envelope","model","status","part"])
def test_invalid(changes):
    result=parse_response(provider(**changes),"p")
    assert result.status=="invalid" and result.trip is None
