from math import factorial
def binomial(n:int,k:int):
    return factorial(n)/(factorial(k)*factorial(n-k))