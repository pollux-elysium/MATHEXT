import numpy as np
from .typedef import *
char=str

def evalEnv(x:str,env:dict|None)->str:
    if env:
        return eval(x,env)
    else:
        return eval(x)

def ldi(x: list[int]|None,i:int=0) ->list[int]: 
    """Load int into list"""
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = parse(*[int(i)for i in input().split(",")])
            x.extend(n)
    else:
        inp = input()
        while inp:
            n = parse(*[int(i)for i in inp.split(",")])
            x.extend(n)
            inp = input()
    return x

def ldie(x: list[int]|None,i:int=0,env:dict|None=None)->list[int]: 
    """Load int into list but evaluate"""
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = int(evalEnv(input(),env))
            x.append(n)
    else:
        inp = input()
        while inp:
            n = int(evalEnv(inp,env))
            x.append(n)
            inp = input()
    return x


def ldf(x: list[float]|None,i:int=0)->list[float]:
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = parse(*[float(j) for j in input().split(",")])
            x.extend(n) 
    else:
        inp = input()
        while inp:
            n = parse(*[float(j) for j in inp.split(",")])
            x.extend(n)
            inp = input()
    return x

def ldfe(x: list[float]|None,i:int=0,env:dict|None=None)->list[float]:
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = float(evalEnv(input(),env))
            x.append(n)
    else:
        inp = input()
        while inp:
            n = float(evalEnv(inp,env))
            x.append(n)
            inp = input()
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


def ldae(x: int, y: int,env:dict|None=None)->np.ndarray:
    """Load evaluated csv(str) into 2d array"""
    return np.array([list(map(float, map(lambda a:evalEnv(a,env), input().split(",")))) for i in range(y)])


def parse(x:T, f:number=1) -> list[T]:
    f=int(f)
    if x:
        return [x]*f
    else:
        return [x]
