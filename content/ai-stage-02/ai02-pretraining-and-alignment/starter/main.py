def sequence_nll(tokens,distributions,masked=()):
    raise NotImplementedError
if __name__=="__main__":
    print(sequence_nll(["<s>","A","B"], [{"A":.8,"B":.2},{"A":.75,"B":.25}], [1]))
