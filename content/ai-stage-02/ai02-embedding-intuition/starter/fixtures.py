from dataclasses import dataclass

@dataclass(frozen=True)
class Embedding:
    model: str
    dimensions: int
    values: tuple[float,...]

def demo(rank):
    phrases={"a":"деньги обратно","b":"оплату подтвердить"}
    query="вернуть оплату"
    def jaccard(text):
        words=set(query.split())
        other=set(text.split())
        return len(words & other)/len(words | other)
    print("Слова", sorted(phrases,key=lambda key:-jaccard(phrases[key])))
    vectors={"a": Embedding("toy-v1",3,(3,1,0)), "b": Embedding("toy-v1",3,(0,2,0))}
    print("Toy-векторы", rank(Embedding("toy-v1",3,(1,0,0)),vectors))
