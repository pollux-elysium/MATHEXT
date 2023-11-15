from .typedef import number
from typing import Callable

def invFuncSolve(func:Callable[[number],number],y:number,start:number=1,err:number=1e-6) -> number:
    """
    Solve for the inverse of a function using Newton's method.
    """
    x = start
    while abs(func(x)-y)>err:
        x = x - (func(x)-y)/((func(x+err)-func(x))/err)
    return x
