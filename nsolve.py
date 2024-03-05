from .typedef import number
from typing import Callable
from sys import stderr

def invFuncSolve(func:Callable[[number],number],y:number,start:number=1,err:number=1e-6,debug:bool = False) -> number:
    """
    Solve for the inverse of a function using Newton's method.

    Args:
        func (Callable[[number],number]): Function to solve for the inverse of
        y (number): Value to solve for
        start (number, optional): Initial guess. Defaults to 1.
        err (number, optional): Error tolerance. Defaults to 1e-6.
        debug (bool, optional): Print debug information. Defaults to False.
            
    Returns:
        number: x such that func(x) = y
    """
    x = start
    while abs(func(x)-y)>err:
        if debug:
            print("x:", x,file=stderr)
            print("f(x):", func(x),file=stderr)
            print("(f(x)-y):", func(x)-y,file=stderr)
            print("f(x+err):", func(x+err),file=stderr)
            print("(f(x+err)-f(x)):", func(x+err)-func(x),file=stderr)
            print("(f(x+err)-f(x))/err:", (func(x+err)-func(x))/err,file=stderr)
            print("Delta x:", -(func(x)-y)/((func(x+err)-func(x))/err),file=stderr)
            print("",file=stderr)
        x = x - (func(x)-y)/((func(x+err)-func(x))/err)
    return x

def numIntTrap(func:Callable[[number],number],a:number,b:number,n:int) -> number:
    """
    Numerically integrate a function using the trapezoidal rule.

    Args:
        func (Callable[[number],number]): Function to integrate
        a (number): Lower bound
        b (number): Upper bound
        n (int): Number of trapezoids

    Returns:
        number: Approximate integral of func from a to b
    """
    h = (b-a)/n
    s = 0.5*(func(a)+func(b))
    for i in range(1,n):
        s += func(a+i*h)
    return s*h
