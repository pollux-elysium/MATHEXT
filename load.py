import numpy as np
char=str
def ldi(x: list,i:int=0) ->list[int]: 
    """Load int into list"""
    if i:
        for j in range(i):
            n = parse(*[int(j) for j in input().split(",")])
            x.extend(n)
           
    else:
        n = parse(*[int(j) for j in input().split(",")])
        while n:
            x.extend(n)
            n = parse(*[int(j) for j in input().split(",")])


def ldie(x: list,i:int=0)->list[int]: 
    """Load int into list but evaluate"""
    if i:
        for j in range(i):
            n = int(eval(input()))
            x.extend(n)
    else:
        n = int(eval(input()))
        while n:
            x.extend(n)
            n = int(eval(input()))


def ldf(x: list,i:int=0)->list[float]:
    """Load float into list"""
    if i:
        for j in range(i):
            n = parse(*[float(j) for j in input().split(",")])
            x.extend(n)
    else:
        n = parse(*[float(j) for j in input().split(",")])
        while n:
            x.extend(n)
            n = parse(*[float(j) for j in input().split(",")])


def ldfe(x: list,i:int=0)->list[float]:
    """Load float into list but evaluate"""
    if i:
        for j in range(i):
            n = float(eval(input()))
            x.extend(n)
    else:
        n = float(eval(input()))
        while n:
            x.extend(n)
            n = float(eval(input()))


def ldc(x: list,i:int=0)->list[char]:
    """Load char into list"""
    if i:
        for j in range(i):
            n=input()
            x.extend(n)
    else:
        n = input()
        while n:
            x.extend(n)
            n = input()


def ldw(x: list,i:int=0)->list[str]:
    """Load word into list"""
    if i:
        for j in range(i):
            n=input()
            x.append(n)
    else:
        n = input()
        while n:
            x.append(n)
            n = input()


def lda(x: int, y: int)->np.ndarray:
    """Load csv(str) into 2d array"""
    return np.array([list(map(float, input().split(","))) for i in range(y)])


def ldae(x: int, y: int)->np.ndarray:
    """Load evaluated csv(str) into 2d array"""
    return np.array([list(map(float, map(eval, input().split(",")))) for i in range(y)])


def parse(x=0, f=1):
    if x:
        return [x]*f
    else:
        return f
