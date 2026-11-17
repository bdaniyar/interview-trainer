def periodic_key(name,epoch,period):
    if not isinstance(name,str) or not 1<=len(name)<=64:raise ValueError('invalid name')
    if any(isinstance(v,bool) or not isinstance(v,int) for v in (epoch,period)) or epoch<0 or period<1:
        raise ValueError('invalid clock')
    return f'periodic:{name}:{epoch//period}'
