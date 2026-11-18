import math

def can_commit(state,current_generation,worker_generation,lease_until,now):
    if not isinstance(state,str) or state not in {'queued','running','succeeded','failed','cancelled'}:raise ValueError('invalid state')
    for value in (current_generation,worker_generation):
        if isinstance(value,bool) or not isinstance(value,int) or value<0:raise ValueError('invalid generation')
    for value in (lease_until,now):
        if isinstance(value,bool) or not isinstance(value,(int,float)) or (isinstance(value,float) and not math.isfinite(value)):raise ValueError('invalid time')
    return state=='running' and current_generation==worker_generation and now<lease_until
