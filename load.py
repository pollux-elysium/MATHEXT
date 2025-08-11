import numpy as np
from .typedef import *
char=str

def _evalEnv(x:str,_env:dict|None)->str:
    """Evaluate string with environment FOR INTERNAL USE ONLY"""
    if _env:
        return eval(x,_env)
    else:
        return eval(x)

def ldi(x: list[int]|None = None,i:int=0) ->list[int]: 
    """Load int into list

    Args:
        x (list[int], optional): List to load into. Generates new list if None.
        i (int, optional): Number of inputs to load. Defaults to until error.

    Returns:
        list[int]: List with inputs loaded
    """
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

def ldie(x: list[int]|None = None,i:int=0,_env:dict|None=None)->list[int]: 
    """Load int into list and evaluate

    Args:
        x (list[int], optional): List to load into. Generates new list if None.
        i (int, optional): Number of inputs to load. Defaults to until error.
        
        _env (dict, optional): Environment to evaluate in. Used when calling from other functions.
            globals() may help.

    Returns:
        list[int]: List with inputs loaded
    """
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = int(_evalEnv(input(),_env))
            x.append(n)
    else:
        inp = input()
        while inp:
            n = int(_evalEnv(inp,_env))
            x.append(n)
            inp = input()
    return x


def ldf(x: list[float]|None = None,i:int=0)->list[float]:
    """Load float into list

    Args:
        x (list[float], optional): List to load into. Generates new list if None.
        i (int, optional): Number of inputs to load. Defaults to until error.

    Returns:
        list[float]: List with inputs loaded
    """

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

def ldfe(x: list[float]|None = None,i:int=0,_env:dict|None=None)->list[float]:
    """Load float into list and evaluate

    Args:
        x (list[float], optional): List to load into. Generates new list if None.
        i (int, optional): Number of inputs to load. Defaults to until error.

        _env (dict, optional): Environment to evaluate in. Used when calling from other functions.
            globals() may help.

    Returns:
        list[float]: List with inputs loaded
    """
    if not isinstance(x,list):x=[]
    if i:
        for j in range(i):
            n = float(_evalEnv(input(),_env))
            x.append(n)
    else:
        inp = input()
        while inp:
            n = float(_evalEnv(inp,_env))
            x.append(n)
            inp = input()
    return x

def ldc(x: list[char]|None = None,i:int=0)->list[char]:
    """Load char into list

    Args:
        x (list[char], optional): List to load into. Generates new list if None.
        i (int, optional): Number of inputs to load. Defaults to until error.

    Returns:
        list[char]: List with inputs loaded
    """
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


def ldw(x: list[str]|None = None,i:int=0)->list[str]:
    """Load word into list

    Args:
        x (list[str], optional): List to load into. Generates new list if None.
        i (int, optional): Number of inputs to load. Defaults to until error.

    Returns:
        list[str]: List with inputs loaded
    """

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
    """Load csv(str) into 2d array
    
    Args:
        x (int): Number of rows
        y (int): Number of columns
        
    Returns:
        np.ndarray: 2d array"""
    return np.array([list(map(float, input().split(","))) for i in range(y)])

def lda3d(i: int, j: int, k: int)->np.ndarray:
    """Load MATLAB formats into 3d array
    
    Args:
        i (int): Number of rows
        j (int): Number of columns
        k (int): Number of layers
        
    Returns:
        np.ndarray: 3d array"""
    return np.array([[list(map(float,i.split()))for i in input().split(";")]for k in range(i)])

def ldaM()->np.ndarray:
    """Load MATLAB formats into 2d array
        
    Returns:
        np.ndarray: 2d array"""
    return np.array([list(map(float,i.split())) for i in input().split(";")])


def ldae(x: int, y: int,_env:dict|None=None)->np.ndarray:
    """Load evaluated csv(str) into 2d array
    
    Args:
        x (int): Number of rows
        y (int): Number of columns
        
        _env (dict, optional): Environment to evaluate in. Used when calling from other functions.
            globals() may help.
            
    Returns:
        np.ndarray: 2d array"""
    return np.array([list(map(float, map(lambda a:_evalEnv(a,_env), input().split(",")))) for i in range(y)])


def parse(x:T, f:number=1) -> list[T]:
    """Parse input into list

    Args:
        x (T): Input
        f (number, optional): Number of times to repeat input. Defaults to 1.

    Returns:
        list[T]: List with input repeated f times
    """
    f=int(f)
    if x:
        return [x]*f
    else:
        return [x] # type: ignore

def ltsvf(i:str)->list[list[float]]:
    """Load tab separated values into 2d array as float

    Args:
        i (str): Input string

    Returns:
        list[list[float]]: 2d array
    """
    return [[float(k) for k in j.split("\t")]for j in i.split("\n")]

def ltsvi(i:str)->list[list[int]]:
    """Load tab separated values into 2d array as int

    Args:
        i (str): Input string

    Returns:
        list[list[int]]: 2d array
    """
    return [[int(k) for k in j.split("\t")]for j in i.split("\n")]

