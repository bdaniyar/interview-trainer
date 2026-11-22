from math import fsum,isfinite

def step(rows,w,b,rate):
    if not rows or not all(type(x) in (int,float) and isfinite(x) for x in (w,b,rate)) or rate <= 0:
        raise ValueError("Нужны данные и положительный конечный шаг")
    if any(len(row)!=2 or any(type(x) not in (int,float) or not isfinite(x) for x in row) for row in rows):
        raise ValueError("Нужны конечные пары")
    predictions=[w*x+b for x,_ in rows]
    errors=[p-y for p,(_,y) in zip(predictions,rows,strict=True)]
    n=len(rows)
    loss=fsum(e*e for e in errors)/n
    dw=2*fsum(e*x for e,(x,_) in zip(errors,rows,strict=True))/n
    db=2*fsum(errors)/n
    return dict(predictions=predictions,loss=loss,dw=dw,db=db,w=w-rate*dw,b=b-rate*db)

def train(rows,w,b,rate,steps):
    if type(steps) is not int or steps<0:
        raise ValueError("Некорректное число шагов")
    current=step(rows,w,b,rate)
    if steps==0:
        return w,b
    for _ in range(steps-1):
        current=step(rows,current["w"],current["b"],rate)
    return current["w"],current["b"]

if __name__ == "__main__":
    print(train([(0,1),(1,3),(2,5),(3,7)],0,0,0.1,20))
