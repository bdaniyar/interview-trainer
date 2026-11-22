from math import fsum, inf, isclose, isfinite, log

def sequence_nll(tokens,distributions,masked=()):
    masked=tuple(masked)
    if len(distributions)!=max(len(tokens)-1,0) or any(type(i) is not int or not 1<=i<len(tokens) for i in masked):
        raise ValueError("Несовместимые позиции")
    hidden=set(masked)
    losses=[]
    for i,(target,row) in enumerate(zip(tokens[1:],distributions,strict=True),1):
        if i in hidden:
            continue
        if not all(type(p) in (float,int) and isfinite(p) and 0<=p<=1 for p in row.values()):
            raise ValueError("Некорректная вероятность")
        if not isclose(fsum(row.values()),1,rel_tol=0,abs_tol=1e-9):
            raise ValueError("Вероятности должны давать сумму один")
        p=row.get(target,0)
        losses.append(-log(p) if p>0 else inf)
    return fsum(losses)/len(losses) if losses else None
if __name__=="__main__":
    print(sequence_nll(["<s>","A","B"], [{"A":.8,"B":.2},{"A":.75,"B":.25}], [1]))
