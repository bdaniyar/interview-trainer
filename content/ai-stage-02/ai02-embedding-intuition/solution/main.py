from math import fsum, hypot, isfinite
from fixtures import demo

def normalize(embedding):
    xs=embedding.values
    if not xs or len(xs)!=embedding.dimensions or not all(type(x) in (int,float) and isfinite(x) for x in xs):
        raise ValueError("Несовместимые координаты")
    scale=max(abs(x) for x in xs)
    if not scale:
        raise ValueError("Нулевое направление")
    scaled=[x/scale for x in xs]
    length=hypot(*scaled)
    return tuple(x/length for x in scaled)

def cosine(left,right):
    if left.model!=right.model or left.dimensions!=right.dimensions:
        raise ValueError("Разные пространства")
    score=fsum(x*y for x,y in zip(normalize(left),normalize(right),strict=True))
    return min(1,max(-1,score))

def rank(query,documents):
    normalize(query)
    return sorted(((key,cosine(query,value)) for key,value in documents.items()),key=lambda item:(-item[1],item[0]))
if __name__=="__main__":
    demo(rank)
