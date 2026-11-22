from pydantic import ValidationError
from fixtures import Envelope, ExtractionResult, demo

def parse_response(response,prompt_version,expected_revision="trip.schema.v1"):
    model=getattr(response,"model",None)
    if not isinstance(model,str) or not model.strip():
        model=None
    def result(status,trip=None):
        return ExtractionResult(status,model,prompt_version,expected_revision,trip)
    groups=getattr(response,"output",None)
    if not isinstance(groups,(tuple,list)) or model is None:
        return result("invalid")
    for item in groups:
        if not isinstance(getattr(item,"type",None),str):
            return result("invalid")
        if item.type=="message":
            parts=getattr(item,"content",None)
            if not isinstance(parts,(list,tuple)):
                return result("invalid")
            if any(getattr(part,"type",None)=="refusal" for part in parts):
                return result("refusal")
            if not all(isinstance(getattr(part,"type",None),str) for part in parts):
                return result("invalid")
    status=getattr(response,"status",None)
    if status=="incomplete":
        return result("incomplete")
    if status!="completed" or getattr(response,"schema_version",None)!=expected_revision:
        return result("invalid")
    try:
        parsed=Envelope.model_validate(getattr(response,"output_parsed",None))
    except ValidationError:
        return result("invalid")
    return result("completed",parsed.trip)
if __name__=="__main__":
    demo(parse_response)
