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
def localMax(x: list[number],n: int=1) -> list[number]:
    ...
@overload
def localMax(x: dict[T,number],n: int=1) -> dict[T,number]:
    ...
def localMax(x: list[number]|dict[T,number],n: int=1) -> list[number]|dict[T,number]:
    """Return list or dict of local maxima of x

    Args:
        x (list): List of numbers
        n (int, optional): Number of local maxima to return. Defaults to 1.

    Returns:
        list: List of local maxima of x
    """
    if isinstance(x,list):
        arr=x.copy()
        ret=[]
        for i in range(n):
            ret.append(max(arr))
            arr.remove(max(arr))
        return ret
    else:
        dic = x.copy()
        ret={}
        for i in range(n):
            ret[max(dic,key=dic.get)]=max(dic.values()) #type: ignore
            del dic[max(dic,key=dic.get)] #type: ignore
        return ret

@overload
def localMin(x: list[number],n: int=1) -> list[number]:
    ...
@overload
def localMin(x: dict[T,number],n: int=1) -> dict[T,number]:
    ...
def localMin(x: list[number]|dict[T,number],n: int=1) -> list[number]|dict[T,number]:
    """Return list or dict of local minima of x

    Args:
        x (list): List of numbers
        n (int, optional): Number of local minima to return. Defaults to 1.

    Returns:
        list: List of local minima of x
    """
    if isinstance(x,list):
        arr=x.copy()
        ret=[]
        for i in range(n):
            ret.append(min(arr))
            arr.remove(min(arr))
        return ret
    else:
        dic = x.copy()
        ret={}
        for i in range(n):
            ret[min(dic,key=dic.get)]=min(dic.values()) #type: ignore
            del dic[min(dic,key=dic.get)] #type: ignore
        return ret

def percentError(real: number,theory: number) -> number:
    """Return the percent error of approx from real

    Args:
        real (number): Real value or measurement
        theory (number): Theoretical value

    Returns:
        number: Percent error of approx from real
    """
    return abs((real-theory)/theory)*100