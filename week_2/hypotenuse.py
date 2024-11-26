from math import sqrt

def hypotenuse(a: float, b: float):
    return sqrt(a**2 + b**2)

print(hypotenuse(3,4)) # 5.0
print(hypotenuse(5,12)) # 13.0
print(hypotenuse(1,1)) # 1.4142135623730951
