import numpy as np
from .typedef import *
char=str
def ldi(x: list[int]|None,i:int=0) ->list[int]: 
    """Load int into list"""
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = parse(*[int(j) for j in input().split(",")])
            x.extend(n)  # type: ignore
           
    else:
        n = parse(*[int(j) for j in input().split(",")])
        while n:
            x.extend(n)  # type: ignore
            n = parse(*[int(j) for j in input().split(",")])
    return x

def ldie(x: list[int]|None,i:int=0)->list[int]: 
    """Load int into list but evaluate"""
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = int(eval(input()))
            x.extend(n)#type:ignore
    else:
        n = int(eval(input()))
        while n:
            x.extend(n)#type:ignore
            n = int(eval(input()))
    return x


def ldf(x: list[float]|None,i:int=0)->list[float]:
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = parse(*[float(j) for j in input().split(",")])
            x.extend(n)  # type: ignore
    else:
        n = parse(*[float(j) for j in input().split(",")])
        while n:
            x.extend(n)  # type: ignore
            n = parse(*[float(j) for j in input().split(",")])
    return x

def ldfe(x: list[float]|None,i:int=0)->list[float]:
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = float(eval(input()))
            x.extend(n)  # type: ignore
    else:
        n = float(eval(input()))
        while n:
            x.extend(n)  # type: ignore
            n = float(eval(input()))
    return x


def ldc(x: list[char]|None,i:int=0)->list[char]:
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n=input()
            x.extend(n)
    else:
        n = input()
        while n:
            x.extend(n)
            n = input()
    return x


def ldw(x: list[str]|None,i:int=0)->list[str]:
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n=input()
            x.append(n)
    else:
        n = input()
        while n:
            x.append(n)
            n = input()
    return x


def lda(x: int, y: int)->np.ndarray:
    """Load csv(str) into 2d array"""
    return np.array([list(map(float, input().split(","))) for i in range(y)])


def ldae(x: int, y: int)->np.ndarray:
    """Load evaluated csv(str) into 2d array"""
    return np.array([list(map(float, map(eval, input().split(",")))) for i in range(y)])


def parse(x:T, f:number=1) -> list[T] | T:
    f=int(f)
    if x:
        return [x]*f
    else:
        return x
