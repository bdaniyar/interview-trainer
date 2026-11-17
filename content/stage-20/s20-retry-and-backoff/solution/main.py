import math

def backoff(attempt, base=1.0, cap=8.0):
    if isinstance(attempt,bool) or not isinstance(attempt,int) or not 1<=attempt<=8:
        raise ValueError('invalid attempt')
    for value in (base,cap):
        if isinstance(value,bool) or not isinstance(value,(int,float)) or (isinstance(value,float) and not math.isfinite(value)) or value<=0:
            raise ValueError('invalid delay')
    if base>cap:raise ValueError('base exceeds cap')
    return min(cap,base*2**(attempt-1))
