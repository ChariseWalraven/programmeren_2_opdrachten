class Fraction:
    def __init__(self, n: int, d: int):
        self.n = n
        self.d = d


    # how do I add the class as a type hint? rn I get an unresolved reference
    def add(self, fraction) -> str:
        n = self.n * fraction.d + fraction.n * self.d
        d = self.d * fraction.d
        return f'{n}/{d}'

    def multiply(self, fraction) -> str:
        n = self.n * fraction.n
        d = self.d * fraction.d
        return f'{n}/{d}'

    def __str__(self):
        return f'{self.n}/{self.d}'


one_third = Fraction(1,3)
one_fourth = Fraction(1,4)

add_result = one_third.add(one_fourth)

print(add_result)
# 7/12

mul_result = one_third.multiply(one_fourth)

print(mul_result)
# 1/12

print(one_third)