def step(rows,w,b,rate):
    raise NotImplementedError
def train(rows,w,b,rate,steps):
    raise NotImplementedError
if __name__ == "__main__":
    print(train([(0,1),(1,3),(2,5),(3,7)],0,0,0.1,20))
