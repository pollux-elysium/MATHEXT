from .typedef import number
from typing import Callable, Concatenate
from sys import stderr

def invFuncSolve(func:Callable[[number],number],y:number,start:number=1,err:number=1e-6,debug:bool = False) -> number:
    """
    Solve for the inverse of a function using Newton's method.

    Args:
        func (Callable[[number],number]): Function to solve for the inverse of
        y (number): Value to solve for
        start (number, optional): Initial guess. Defaults to 1.
        err (number, optional): Error tolerance and step size. Defaults to 1e-6.
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

def maximize(func:Callable[[number],number],a:number,b:number,err:number=1e-6) -> number:
    """
    Find the maximum of a function using the golden section search.

    Args:
        func (Callable[[number],number]): Function to maximize
        a (number): Lower bound
        b (number): Upper bound
        err (number, optional): Error tolerance. Defaults to 1e-6.

    Returns:
        number: x such that func(x) is maximized
    """
    gr = (5**0.5-1)/2
    c = b-gr*(b-a)
    d = a+gr*(b-a)
    while abs(c-d)>err:
        if func(c)>func(d):
            b = d
        else:
            a = c
        c = b-gr*(b-a)
        d = a+gr*(b-a)
    return (a+b)/2


def minimize(func:Callable[[number],number],a:number,b:number,err:number=1e-6) -> number:
    """
    Find the minimum of a function using the golden section search.

    Args:
        func (Callable[[number],number]): Function to minimize
        a (number): Lower bound
        b (number): Upper bound
        err (number, optional): Error tolerance. Defaults to 1e-6.

    Returns:
        number: x such that func(x) is minimized
    """
    gr = (5**0.5-1)/2
    c = b-gr*(b-a)
    d = a+gr*(b-a)
    while abs(c-d)>err:
        if func(c)<func(d):
            b = d
        else:
            a = c
        c = b-gr*(b-a)
        d = a+gr*(b-a)
    return (a+b)/2

def ODE1(dydt : Callable[[number,number],number],y0:number,t0:number,t1:number,n:int) -> number:
    """
    Solve a first order ordinary differential equation using Euler's method.

    Args:
        dydt (Callable[[number,number],number]): Function (t,y) representing the derivative of y
        y0 (number): Initial value of y
        t0 (number): Initial value of t
        t1 (number): Final value of t
        n (int): Number of steps

    Returns:
        number: Approximate value of y at t1
    """
    h = (t1-t0)/n
    t = t0
    y = y0
    for i in range(n):
        y += h*dydt(t,y)
        t += h
    return y

def ODE1A(dydt : Callable[[number,number],number],y0:number,t0:number,t1:number,n:int) -> tuple[list[number],list[number]]:
    """
    Solve a first order ordinary differential equation using Euler's method.
    Returns all steps, time.

    Args:
        dydt (Callable[[number,number],number]): Function (t,y) representing the derivative of y
        y0 (number): Initial value of y
        t0 (number): Initial value of t
        t1 (number): Final value of t
        n (int): Number of steps

    Returns:
        tuple[list[number],list[number]]: [time[], y[]]
    """
    h = (t1-t0)/n
    t = t0
    y = y0
    outy = [None]*(n+1)
    outt = [None]*(n+1)
    outy[0] = y0
    outt[0] = t0
    for i in range(n):
        y += h*dydt(t,y)
        t += h
        outy[i+1] = y
        outt[i+1] = t
    return outt,outy

def ODEx(dfunc : Callable[...,number],iv:list[number],t0:number,t1:number,n:int):
    """
    Solve a nth order ordinary differential equation using Euler's method.

    Args:
        dfunc (Callable[[number,...],number]): Function representing the highest order derivative of y (t,*y and its derivatives in increasing order)
        iv (list[number]): Initial values of y and its derivatives in increasing order
        t0 (number): Initial value of t
        t1 (number): Final value of t
        n (int): Number of steps

    Returns:
        number: Approximate value of y at t1
    """
    h = (t1-t0)/n
    t = t0
    cv = iv.copy()
    for i in range(n):
        for j in range(0,len(cv)-1):
            cv[j] += h*cv[j+1]
        cv[-1] += h*dfunc(t,*cv)
        t += h
    return cv[0]

def ODExA(dfunc : Callable[...,number],iv:list[number],t0:number,t1:number,n:int):
    """
    Solve a nth order ordinary differential equation using Euler's method.
    Returns all steps, time.

    Args:
        dfunc (Callable[[number,...],number]): Function representing the highest order derivative of y (t,*y and its derivatives in increasing order)
        iv (list[number]): Initial values of y and its derivatives in increasing order
        t0 (number): Initial value of t
        t1 (number): Final value of t
        n (int): Number of steps
    
    Returns:
        tuple[list[number],list[list[number]]]: time[], degree[y[]] in increasing order
    """

    h = (t1-t0)/n
    t = t0
    cv = iv.copy()
    out = [[x for x in cv]]
    outt = [t0]
    for i in range(n):
        curr = cv.copy()
        for j in range(0,len(cv)-1):
            cv[j] += h*cv[j+1]
        cv[-1] += h*dfunc(t,*curr)
        t += h
        out.append([x for x in cv])
        outt.append(t)
    return outt,out

def SODE1(fs: list[Callable[...,number]], iv: list[number], t0:number, t1:number, n:int) -> list[number]:
    """
    Solve a system of first order ordinary differential equations using Euler's method.
    Function input order is important.

    [
        dx/dt = f1(t,x,y,z,...)
        dy/dt = f2(t,x,y,z,...)
        dz/dt = f3(t,x,y,z,...)
    ]

    Args:
        fs (list[Callable[...,number]]): List of functions representing the derivatives 
        iv (list[number]): Initial values
        t0 (number): Initial value of t
        t1 (number): Final value of t
        n (int): Number of steps

    Returns:
        list[number]: Approximate values at t1
    """

    h = (t1-t0)/n
    t = t0
    cv = iv.copy()
    for i in range(n):
        for j in range(len(cv)):
            cv[j] += h*fs[j](t,*cv)
        t += h
    return cv