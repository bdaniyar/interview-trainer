from fixtures import demo
def normalize(embedding):
    raise NotImplementedError
def cosine(left,right):
    raise NotImplementedError
def rank(query,documents):
    raise NotImplementedError
if __name__=="__main__":
    demo(rank)
