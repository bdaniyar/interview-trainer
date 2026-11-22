def softmax(logits):
    raise NotImplementedError
def attention(q,k,v,causal=True):
    raise NotImplementedError
if __name__ == "__main__":
    print(attention([[1],[2],[1]],[[0],[1],[2]],[[3],[6],[9]]))
