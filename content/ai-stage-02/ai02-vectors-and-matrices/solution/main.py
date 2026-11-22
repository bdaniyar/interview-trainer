from math import fsum, hypot, isfinite

def checked(vector):
    if any(type(x) not in (int,float) or not isfinite(x) for x in vector):
        raise ValueError("Координаты должны быть конечными")
    return vector

def dot(left, right):
    return fsum(x*y for x,y in zip(checked(left), checked(right), strict=True))

def norm(vector):
    return hypot(*checked(vector))

def matvec(matrix, vector):
    checked(vector)
    return [dot(row, vector) for row in matrix]

if __name__ == "__main__":
    print(matvec([[2,0], [1,3], [-1,2]], [4,1]))
