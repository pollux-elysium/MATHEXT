import math
import numpy as np
from .typedef import *
from typing import overload

def fft(x: list[number]) :
    """Return the discrete fourier transform of x

    Args:
        x (list): List of numbers

    Returns:
        ndarray[complex]: Discrete fourier transform of x
    """
    return np.fft.fft(x)

def ifft(x: list[number]) :
    """Return the inverse discrete fourier transform of x

    Args:
        x (list): List of numbers

    Returns:
        ndarray[number]: Inverse discrete fourier transform of x
    """
    return np.fft.ifft(x)

@overload
def localMax(x: list[number],n: int=1) -> tuple[list[number],list[number]]:
    ...
@overload
def localMax(x: dict[T,number],n: int=1) -> dict[T,number]:
    ...
def localMax(x: list[number]|dict[T,number],n: int=1) -> tuple[list[number],list[number]]|dict[T,number]:
    """Return list or dict of local maxima of x

    Args:
        x (list): List of numbers
        n (int, optional): Number of local maxima to return. Defaults to 1.

    Returns:
        list: List of local maxima of x
    """
    if isinstance(x,list):
        arr=x.copy()
        filtered:list[number]=[]
        index:list[number] = []
        for i in range(len(arr)):
            if i==0:
                if arr[i]>arr[i+1]:
                    filtered.append(arr[i])
                    index.append(i)
            elif i==len(arr)-1:
                if arr[i]>arr[i-1]:
                    filtered.append(arr[i])
                    index.append(i)
            else:
                if arr[i-1]<arr[i]>arr[i+1]:
                    filtered.append(arr[i])
                    index.append(i)
        arr=filtered.copy()        
        retL:list[number]=[]
        for i in range(n):
            retL.append(max(arr))
            arr.remove(max(arr))
        return retL,index
    elif isinstance(x,dict):
        dic = x.copy()
        retD:dict[T,number]={}
        for i in range(n):
            retD[max(dic,key=dic.get)]=max(dic.values()) #type: ignore
            del dic[max(dic,key=dic.get)] #type: ignore
        return retD

@overload
def localMin(x: list[number],n: int=1) -> tuple[list[number],list[number]]:
    ...
@overload
def localMin(x: dict[T,number],n: int=1) -> dict[T,number]:
    ...
def localMin(x: list[number]|dict[T,number],n: int=1) -> tuple[list[number],list[number]]|dict[T,number]:
    """Return list or dict of local minima of x

    Args:
        x (list): List of numbers
        n (int, optional): Number of local minima to return. Defaults to 1.

    Returns:
        list: List of local minima of x
    """
    if isinstance(x,list):
        arr=x.copy()
        filtered:list[number]=[]
        index:list[number] = []
        for i in range(len(arr)):
            if i==0:
                if arr[i]<arr[i+1]:
                    filtered.append(arr[i])
                    index.append(i)
            elif i==len(arr)-1:
                if arr[i]<arr[i-1]:
                    filtered.append(arr[i])
                    index.append(i)
            else:
                if arr[i-1]>arr[i]<arr[i+1]:
                    filtered.append(arr[i])
                    index.append(i)
        arr=filtered.copy()
        retL:list[number]=[]
        for i in range(n):
            retL.append(min(arr))
            arr.remove(min(arr))
        return retL,index
    elif isinstance(x,dict):
        dic = x.copy()
        retD:dict[T,number]={}
        for i in range(n):
            retD[min(dic,key=dic.get)]=min(dic.values()) #type: ignore
            del dic[min(dic,key=dic.get)] #type: ignore
        return retD

def percentError(real: number,theory: number) -> number:
    """Return the percent error of approx from real

    Args:
        real (number): Real value or measurement
        theory (number): Theoretical value

    Returns:
        number: Percent error of real from theory
    """
    return abs((real-theory)/theory)*100

def indexList(x: list[T])-> dict[int,T]:
    """Return dictionary of index:element pairs from list x

    Args:
        x (list): List of elements

    Returns:
        dict: Dictionary of index:element pairs
    """
    return {i:x[i] for i in range(len(x))}

def clampMax(x: list[number],maxVal: number = -math.inf) -> list[number]:
    """Return list x with elements clamped to maxVal

    Args:
        x (list): List of numbers
        maxVal (number): Maximum value

    Returns:
        list: List x with elements clamped to maxVal
    """
    return [(maxVal:=i) if i>maxVal else maxVal for i in x]

def clampMin(x: list[number],minVal: number = math.inf) -> list[number]:
    """Return list x with elements clamped to minVal

    Args:
        x (list): List of numbers
        minVal (number): Minimum value

    Returns:
        list: List x with elements clamped to minVal
    """
    return [(minVal:=i) if i<minVal else minVal for i in x]