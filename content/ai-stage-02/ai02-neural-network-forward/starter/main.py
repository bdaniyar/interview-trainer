def forward(x,w1,b1,w2,b2):
    raise NotImplementedError
def sensitivity(x,w1,b1,w2,b2,output,hidden,feature):
    raise NotImplementedError
if __name__ == "__main__":
    print(forward([3],[[2]],[0],[[5]],[0]))
