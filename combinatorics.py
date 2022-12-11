from math import factorial
def binomial(n:int,k:int) -> float:
    """Binomial coefficient

    Args:
        n (int): top number
        k (int): bottom number

    Returns:
        float : binomial coefficient
    """
    return factorial(n)/(factorial(k)*factorial(n-k))

def perm(n:int,k:int) -> float:
    """Permutation number

    Args:
        n (int): top number
        k (int): bottom number

    Returns:
        float: permutation
    """
    return factorial(n)/factorial(n-k)

def comb(n:int,k:int) -> float:
    """Combination number

    Args:
        n (int): top number
        k (int): bottom number

    Returns:
        float: combination
    """
    return perm(n,k)/factorial(k)