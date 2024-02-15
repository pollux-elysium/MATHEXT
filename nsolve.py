from .typedef import number
from typing import Callable
from sys import stderr

def invFuncSolve(func:Callable[[number],number],y:number,start:number=1,err:number=1e-6,debug:bool = False) -> number:
    """
    Solve for the inverse of a function using Newton's method.
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
