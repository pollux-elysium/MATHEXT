from math import factorial
def binomial(n:int,k:int):
    return factorial(n)/(factorial(k)*factorial(n-k))

def perm(n:int,k:int):
    return factorial(n)/factorial(n-k)

def comb(n:int,k:int):
    return perm(n,k)/factorial(k)