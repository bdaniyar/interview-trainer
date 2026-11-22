from math import exp, fsum, isfinite, sqrt

def finite(values):
    return all(type(x) in (int,float) and isfinite(x) for x in values)

def softmax(logits):
    if not logits or not finite(logits):
        raise ValueError("Требуются конечные логиты")
    largest=max(logits)
    exps=[exp(x-largest) for x in logits]
    total=fsum(exps)
    return [x/total for x in exps]

def width(matrix):
    if not matrix or not matrix[0] or any(len(row)!=len(matrix[0]) or not finite(row) for row in matrix):
        raise ValueError("Требуется непустая прямоугольная матрица")
    return len(matrix[0])

def attention(q,k,v,causal=True):
    d_k=width(q)
    d_v=width(v)
    if width(k)!=d_k or len(q)!=len(k) or len(q)!=len(v):
        raise ValueError("Несогласованные формы")
    output=[]
    weights=[]
    scale=sqrt(d_k)
    for i,query in enumerate(q):
        available=k[:i+1] if causal else k
        scores=[fsum(a*b for a,b in zip(query,key,strict=True))/scale for key in available]
        fitted=softmax(scores)
        row=fitted+[0]*(len(k)-len(fitted))
        weights.append(row)
        output.append([fsum(p*value[j] for p,value in zip(row,v,strict=True)) for j in range(d_v)])
    return output, weights
if __name__ == "__main__":
    print(attention([[1],[2],[1]],[[0],[1],[2]],[[3],[6],[9]]))
