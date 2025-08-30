from .typedef import number
from typing import Callable, Concatenate
from sys import stderr

def nd1(func:Callable[[number],number],x:number,delta:number=1e-6,debug:bool=False) -> number:
    """
    Numerically differentiate a function using central difference method.

    Args:
        func (Callable[[number],number]): Function to differentiate
        x (number): Point at which to differentiate
        delta (number, optional): Step size. Defaults to 1e-6.
        debug (bool, optional): Print debug information. Defaults to False.

    Returns:
        number: Derivative of func at x
    """
    d = (func(x+delta)-func(x-delta))/(2*delta)
    if debug:
        print("f(x+delta):", func(x+delta), file=stderr)
        print("f(x-delta):", func(x-delta), file=stderr)
        print("Derivative:", d, file=stderr)
    return d

def nd2(func:Callable[[number],number],x:number,delta:number=1e-6,debug:bool=False) -> number:
    """
    Numerically differentiate a function using central difference method for second derivative.

    Args:
        func (Callable[[number],number]): Function to differentiate
        x (number): Point at which to differentiate
        delta (number, optional): Step size. Defaults to 1e-6.
        debug (bool, optional): Print debug information. Defaults to False.

    Returns:
        number: Second derivative of func at x
    """
    d2 = (func(x+delta) - 2*func(x) + func(x-delta)) / (delta**2)
    if debug:
        print("f(x+delta):", func(x+delta), file=stderr)
        print("f(x):", func(x), file=stderr)
        print("f(x-delta):", func(x-delta), file=stderr)
        print("Second Derivative:", d2, file=stderr)
    return d2

def invFuncSolve(func:Callable[[number],number],y:number,start:number=1,err:number=1e-6,debug:bool = False) -> number:
    """
    Solve for the inverse of a function using Newton's method.
    Uses numerical method for derivative

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
    while abs((fx:=func(x))-y)>err:
        dfx = nd1(func, x, err)
        if debug:
            print("x:", x,file=stderr)
            print("f(x):", fx,file=stderr)
            print("(f(x)-y):", fx-y,file=stderr)
            print("f(x+err):", func(x+err),file=stderr)
            print("(f(x+err)-f(x)):", func(x+err)-func(x),file=stderr)
            print("(f(x+err)-f(x))/err:", dfx,file=stderr)
            print("Delta x:", -(fx-y)/dfx,file=stderr)
            print("",file=stderr)
        x = x - (fx-y)/dfx
    return x

def invFuncSolveD(func:Callable[[number],number],dFunc:Callable[[number],number],y:number,start:number=1,err:number=1e-6,debug:bool = False) -> number:
    """
    Solve for the inverse of a function using Newton's method.
    Uses provided derivative function


    Args:
        func (Callable[[number],number]): Function to solve for
        dFunc (Callable[[number],number]): Derivative Function
        y (number): _description_
        start (number, optional): _description_. Defaults to 1.
        err (number, optional): _description_. Defaults to 1e-6.
        debug (bool, optional): _description_. Defaults to False.

    Returns:
        number: _description_
    """
    x = start
    while abs(func(x)-y)>err:
        if debug:
            print("x:", x,file=stderr)
            print("f(x):", func(x),file=stderr)
            print("(f(x)-y):", func(x)-y,file=stderr)
            print("f'(x):", dFunc(x),file=stderr)
            print("Delta x:", -(func(x)-y)/dFunc(x),file=stderr)
            print("",file=stderr)
        x = x - (func(x)-y)/dFunc(x)
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

def maximize(func:Callable[[number],number],a:number,b:number,err:number=1e-6,debug=False) -> number:
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
    fc = func(c)
    fd = func(d)
    while (d-c)>err:
        if debug:
            print("a:", a, "b:", b, "c:", c, "d:", d, file=stderr)
            print("f(c):", fc, "f(d):", fd, file=stderr)
            print("", file=stderr)
        if fc>fd:
            b = d
            d = c
            fd = fc
            c = b-gr*(b-a)
            fc = func(c)
        else:
            a = c
            c = d
            fc = fd
            d = a+gr*(b-a)
            fd = func(d)
    return (a+b)/2


def minimize(func:Callable[[number],number],a:number,b:number,err:number=1e-6,debug=False) -> number:
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
    fc = func(c)
    fd = func(d)
    while (d-c)>err:
        if debug:
            print("a:", a, "b:", b, "c:", c, "d:", d, file=stderr)
            print("f(c):", fc, "f(d):", fd, file=stderr)
            print("", file=stderr)
        if fc<fd:
            b = d
            d = c
            fd = fc
            c = b-gr*(b-a)
            fc = func(c)
        else:
            a = c
            c = d
            fc = fd
            d = a+gr*(b-a)
            fd = func(d)
        c = b-gr*(b-a)
        d = a+gr*(b-a)
    return (a+b)/2

def stationary_Newton_N(func:Callable[[number],number],start:number=0,err:number=1e-6,debug=False) -> number:
    """
    Find stationary point of a function using Newton's method.
    Derivatives are calculated numerically.

    Args:
        func (Callable[[number],number]): Function to maximize
        start (number): Initial guess
        err (number, optional): Error tolerance. Defaults to 1e-6.

    Returns:
        number: x such that func(x) is stationary
    """

    x = start
    d1 = nd1(func, x, err)
    d2 = nd2(func, x, err)
    dx = -(d1)/(d2)
    while abs(dx)>err:
        if debug:
            print("x:", x, file=stderr)
            print("f(x):", func(x), file=stderr)
            print("f'(x):", d1, file=stderr)
            print("f''(x):", d2, file=stderr)
            print("Delta x:", dx, file=stderr)
            print("", file=stderr)
        x += dx
        d1 = nd1(func, x, err)
        d2 = nd2(func, x, err)
        if abs(d2) < err:
            print("Second derivative is too small, cannot continue. x = ",x, file=stderr)
            return x
        dx = -(d1)/(d2)
    return x
    
def stationary_Newton_D(func:Callable[[number],number],dFunc:Callable[[number],number],d2Func:Callable[[number],number],start:number=0,err:number=1e-6,debug=False) -> number:
    """
    Find stationary point of a function using Newton's method.
    Uses provided derivative and second derivative functions.

    Args:
        func (Callable[[number],number]): Function to maximize
        dFunc (Callable[[number],number]): First derivative function
        d2Func (Callable[[number],number]): Second derivative function
        start (number): Initial guess
        err (number, optional): Error tolerance. Defaults to 1e-6.

    Returns:
        number: x such that func(x) is stationary
    """
    x = start
    dx = -dFunc(x)/d2Func(x)
    while abs(dx)>err:
        if debug:
            print("x:", x, file=stderr)
            print("f(x):", func(x), file=stderr)
            print("f'(x):", dFunc(x), file=stderr)
            print("f''(x):", d2Func(x), file=stderr)
            print("Delta x:", dx, file=stderr)
            print("", file=stderr)
        x += dx
        dx = -dFunc(x)/d2Func(x)
    return x

def stationary_Newton_N_2D(func:Callable[[number,number],number],start:tuple[number,number]=(0,0),err:number=1e-6,debug=False) -> tuple[number,number]:
    """
    Find stationary point of a function of two variables using Newton's method.
    Derivatives are calculated numerically.

    Args:
        func (Callable[[number,number],number]): Function to maximize
        start (tuple[number,number], optional): Starting coordinate. Defaults to (0,0).
        err (number, optional): Tolerance. Defaults to 1e-6.
        debug (bool, optional): Print debug. Defaults to False.

    Returns:
        tuple[number,number]: x,y such that func(x,y) is stationary
    """

    x, y = start
    fX = lambda x: func(x, y)
    fY = lambda y: func(x, y)
    d1x = nd1(fX, x, err)
    d1y = nd1(fY, y, err)
    d2xx = nd2(fX, x, err)
    d2yy = nd2(fY, y, err)
    d2xy = nd1(lambda x: nd1(lambda y: func(x, y), y, err), x, err)
    det = d2xx * d2yy - d2xy * d2xy
    inv_Hessian = [[d2yy/det, -d2xy/det], [-d2xy/det, d2xx/det]]
    dx = -(inv_Hessian[0][0] * d1x + inv_Hessian[0][1] * d1y)
    dy = -(inv_Hessian[1][0] * d1x + inv_Hessian[1][1] * d1y)
    while abs(dx) > err or abs(dy) > err:
        if debug:
            print("x:", x, "y:", y, file=stderr)
            print("f(x,y):", func(x, y), file=stderr)
            print("f'(x):", d1x, "f'(y):", d1y, file=stderr)
            print("f''(xx):", d2xx, "f''(yy):", d2yy, "f''(xy):",file=stderr)
            print("Determinant of Hessian:", det, file=stderr)
            print("Delta x:", dx, "Delta y:", dy, file=stderr)
            print("", file=stderr)

        x += dx
        y += dy
        fX = lambda x: func(x, y)
        fY = lambda y: func(x, y)
        # d1x = nd1(lambda x: func(x, y), x, err)
        # d1y = nd1(lambda y: func(x, y), y, err)
        # d2xx = nd2(lambda x: func(x, y), x, err)
        # d2yy = nd2(lambda y: func(x, y), y, err)
        d1x = nd1(fX, x, err)
        d1y = nd1(fY, y, err)
        d2xx = nd2(fX, x, err)
        d2yy = nd2(fY, y, err)
        d2xy = nd1(lambda x: nd1(lambda y: func(x, y), y, err), x, err)
        det = d2xx * d2yy - d2xy * d2xy
        inv_Hessian = [[d2yy/det, -d2xy/det], [-d2xy/det, d2xx/det]]
        dx = -(inv_Hessian[0][0] * d1x + inv_Hessian[0][1] * d1y)
        dy = -(inv_Hessian[1][0] * d1x + inv_Hessian[1][1] * d1y)
    return x, y

    


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