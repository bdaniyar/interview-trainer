from datetime import date, datetime
import pytest
from pydantic import ValidationError
from main import TripRequest

GOOD={"city":"Тбилиси","check_in":"2028-02-29","check_out":"2028-03-02","guests":3}
def test_typed_fields():
    result=TripRequest.model_validate(GOOD)
    assert result.check_in==date(2028,2,29) and result.guests==3
    assert result.city=="Тбилиси"
def test_required_nullable():
    assert TripRequest.model_validate(dict.fromkeys(GOOD)).model_dump()==dict.fromkeys(GOOD)
    assert set(TripRequest.model_json_schema()["required"])==set(GOOD)
    with pytest.raises(ValidationError): TripRequest.model_validate({k:v for k,v in GOOD.items() if k!="city"})
@pytest.mark.parametrize("key,value", [("guests",False),("guests","1"),("guests",0),("guests",1.0),
                                       ("check_in","2027-02-29"),("check_out","2028-02-29"),("check_out","2028-02-20"),
                                       ("check_in",datetime(2028,2,29)),("check_in","10 December"),("city"," "),("notes","x")],
                         ids=["bool","string","zero","float","calendar","same","reverse","datetime","ambiguous","blank","extra"])
def test_invalid(key,value):
    with pytest.raises(ValidationError): TripRequest.model_validate({**GOOD,key:value})
