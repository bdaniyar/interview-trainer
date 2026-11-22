from math import fsum, isfinite

def layer(x, weights, biases):
    if not x or not weights or len(weights)!=len(biases):
        raise ValueError("Несогласованная форма слоя")
    values = [*x,*biases,*(v for row in weights for v in row)]
    if not all(type(v) in (int,float) and isfinite(v) for v in values):
        raise ValueError("Требуются конечные числа")
    return [bias+fsum(a*b for a,b in zip(row,x,strict=True))
            for row,bias in zip(weights,biases,strict=True)]

def forward(x,w1,b1,w2,b2):
    hidden=layer(x,w1,b1)
    return layer([max(0,z) for z in hidden],w2,b2)

def sensitivity(x,w1,b1,w2,b2,output,hidden,feature):
    forward(x,w1,b1,w2,b2)
    if any(type(j) is not int or not 0<=j<n for j,n in
           ((output,len(w2)),(hidden,len(w1)),(feature,len(x)))):
        raise ValueError("Индекс за пределами слоя")
    z=layer(x,w1,b1)[hidden]
    if z==0:
        raise ValueError("ReLU в точке излома")
    return w2[output][hidden]*x[feature] if z>0 else 0
if __name__ == "__main__":
    print(forward([3],[[2]],[0],[[5]],[0]))
