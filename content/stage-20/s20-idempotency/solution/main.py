import hashlib
import json
import math

def fingerprint_request(payload):
    active=set()
    def validate(value):
        if value is None or isinstance(value,(str,bool,int)):return
        if isinstance(value,float) and math.isfinite(value):return
        if isinstance(value,(list,dict)):
            if id(value) in active:raise ValueError('cyclic input')
            if isinstance(value,dict) and not all(isinstance(k,str) for k in value):raise ValueError('string keys required')
            active.add(id(value))
            for item in (value.values() if isinstance(value,dict) else value):validate(item)
            active.remove(id(value))
            return
        raise ValueError('not supported JSON')
    if not isinstance(payload,dict):raise ValueError('dictionary required')
    validate(payload)
    wire=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(wire).hexdigest()
