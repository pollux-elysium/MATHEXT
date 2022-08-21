from .typedef import T


def percentile(x: list[int|float], p: int):
    """Return pth percentile of list x"""
    x.sort()
    l = p*(len(x)+1)/100
    return x[int(l) - 1]+(x[int(l)]-x[int(l)-1])*(l % 1)


def freq(x: list[T]) -> dict[T, int]:
    return {i: x.count(i)for i in undupe(x)}
    


def tree(x: list[float|int],sep:int=10):
    j = undupe([i//sep for i in x])
    return {i: [k for k in x if k//sep == i]for i in j}

def undupe(x: list[T]) -> list[T]:
    return list(dict.fromkeys(x))