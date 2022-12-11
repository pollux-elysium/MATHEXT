from math import exp, log, sqrt
from typing import Literal, Union

from .poly import solvePoly
from .load import ldfe,ldf
from .listelemop import *
from .typedef import *
from .matrix import AugMat
import numpy as np

class Reg:
    """Base Regression class template.
    
    Should not be used directly, use the subclasses instead or make your own."""
    x:list[number]
    fx:list[number]

    def __init__(self,x:Union[list[number],"Reg"],fx:list[number]|None=None) -> None:
        """Initialise a regression object.
        
        Args:
            x (list[number]|Reg): The x values of the regression.
                If a Reg object is passed, the x and fx values of the Reg object will be used.
            fx (list[number]|None): The f(x) values of the regression.
            
        Raises:
            ValueError: If the length of x and fx are not equal.
        """

        if not fx:
            fx=[]
        if isinstance(x,Reg):
            self.x=x.x
            self.fx=x.fx
        elif len(x) == len(fx):
            self.x=x
            self.fx=fx
        else:
            raise ValueError

    @staticmethod
    def make(n:int=0,eval:bool=False,env:dict|None=None):
        """Macro to make a regression object.

        Args:
            n (int, optional): The number of points. Defaults to 0.
            eval (bool, optional): Whether to evaluate the input. Defaults to False.
            env (dict|None, optional): The environment to evaluate the input in. Defaults to None.
                globals() can be useful.

        Returns:
            Reg: The regression object.
        """
        if eval:
            x:list[number]=[]
            print("Enter x:\n")
            ldfe(x,n,env)
            fx:list[number]=[]
            print("Enter f(x):\n")
            ldfe(fx,n,env)
            return Reg(x,fx)
        else:
            x=[]
            print("Enter x:\n")
            ldf(x,n)
            fx=[]
            print("Enter f(x):\n")
            ldf(fx,n)
            return Reg(x,fx)

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        """Regression object from a list of tuples.
        
        Args:
            n (list[tuple[number,number]]): The list of tuples. (x,fx)
            
        Returns:
            Reg: The regression object.
        """
        x:list[number] =[]; fx:list[number]= []
        for i in n:
            a,b=i
            x.append(a)
            fx.append(b)
        return Reg(x,fx)

    def loadReg(self,reg:"Reg"):
        """Load the x and fx values of another regression object.

        Args:
            reg (Reg): The regression object to load from.

        Returns:
            Reg: The regression object.(self)
        """
        self.x=reg.x
        self.fx=reg.fx
        return self

class LinReg(Reg):
    """Linear Regression class.
    
    In the form y = mx + c."""

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.m}x+{self.c}"

    @staticmethod
    def make(n: int = 0, eval: bool = False, env: dict | None = None):
        return LinReg(Reg.make(n,eval,env))

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        return LinReg(Reg.lot(n))

    @property
    def solArray(self):
        return AugMat(np.array([[sum(mul(self.x,self.x)),sum(self.x)]
        ,[sum(self.x),len(self.x)]]),
        [sum(mul(self.x,self.fx)),sum(self.fx)]).asolve()

    @property
    def m(self) -> number:
        return self.solArray[0]

    @property
    def c(self) -> number:
        return self.solArray[1]

    def f(self,x:number):
        """f(x) for the regression line.
        
        Args:
            x (number): The x value.
            
        Returns:
            number: The f(x) value."""
        return self.m*x+self.c

    def xf(self,f:number):
        """x for the regression line.

        Args:
            f (number): The f(x) value.

        Returns:
            number: The x value.
        """
        return (f-self.c)/self.m

class QuadReg(Reg):
    """Quadratic Regression class.
    
    In the form y = ax^2 + bx + c."""

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.a}x^2+{self.b}x+{self.c}"

    @staticmethod
    def make(n: int = 0, eval: bool = False, env: dict | None = None):
        return QuadReg(Reg.make(n,eval,env))

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        return QuadReg(Reg.lot(n))

    @property
    def solArray(self):
        return AugMat(
            np.array([[sum([i**4 for i in self.x]),sum([i**3 for i in self.x]),sum([i**2 for i in self.x])],
            [sum([i**3 for i in self.x]),sum([i**2 for i in self.x]),sum(self.x)],
            [sum([i**2 for i in self.x]),sum(self.x),len(self.x)]]),
            [sum(mul([i**2 for i in self.x],self.fx)),sum(mul(self.x,self.fx)),sum(self.fx)]
        ).asolve()

    @property
    def a(self) -> number:
        return self.solArray[0]

    @property
    def b(self) -> number:
        return self.solArray[1]

    @property
    def c(self) -> number:
        return self.solArray[2]

    def f(self,x:number):
        """f(x) for the regression line.
        
        Args:
            x (number): The x value.
            
        Returns:
            number: The f(x) value."""
        return self.a*x**2+self.b*x+self.c

    def xf(self,f:number):
        """x for the regression line.

        Args:
            f (number): The f(x) value.

        Returns:
            list[complex]: The x values.
        """
        return solvePoly(self.a,self.b,self.c-f)

class CubReg(Reg):
    """Cubic Regression class.
    
    In the form y = ax^3 + bx^2 + cx + d."""

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.a}x^3+{self.b}x^2+{self.c}x+{self.d}"

    @staticmethod
    def make(n: int = 0, eval: bool = False, env: dict | None = None):
        return CubReg(Reg.make(n,eval,env))

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        return CubReg(Reg.lot(n))

    @property
    def solArray(self):
        return AugMat(
            np.array([[sum([i**6 for i in self.x]),sum([i**5 for i in self.x]),sum([i**4 for i in self.x]),sum([i**3 for i in self.x])],
            [sum([i**5 for i in self.x]),sum([i**4 for i in self.x]),sum([i**3 for i in self.x]),sum([i**2 for i in self.x])],
            [sum([i**4 for i in self.x]),sum([i**3 for i in self.x]),sum([i**2 for i in self.x]),sum(self.x)],
            [sum([i**3 for i in self.x]),sum([i**2 for i in self.x]),sum(self.x),len(self.x)]]),
            [sum(mul([i**3 for i in self.x],self.fx)),sum(mul([i**2 for i in self.x],self.fx)),sum(mul(self.x,self.fx)),sum(self.fx)]
        ).asolve()

    @property
    def a(self) -> number:
        return self.solArray[0]

    @property
    def b(self) -> number:
        return self.solArray[1]

    @property
    def c(self) -> number:
        return self.solArray[2]

    @property
    def d(self) -> number:
        return self.solArray[3]

    def f(self,x:number):
        """f(x) for the regression line.

        Args:
            x (number): The x value.

        Returns:
            number: The f(x) value."""

        return self.a*x**3+self.b*x**2+self.c*x+self.d 

    def xf(self,f:number):
        """x for the regression line.

        Args:
            f (number): The f(x) value.

        Returns:
            list[complex]: The x values.
        """
        return solvePoly(self.a,self.b,self.c,self.d-f)

class ExpReg(Reg):
    """Exponential Regression class.
    
    In the form y = e^(bx)."""

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.a}e^({self.b}x)"

    @staticmethod
    def make(n: int = 0, eval: bool = False, env: dict | None = None):
        return ExpReg(Reg.make(n,eval,env))

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        return ExpReg(Reg.lot(n))

    @property
    def logfx(self):
        return [log(i) for i in self.fx]

    @property
    def solArray(self):
        return AugMat(
            np.array([[sum([i**2 for i in self.x]),sum(self.x)],
            [sum(self.x),len(self.x)]]),
            [sum(mul(self.x,self.logfx)),sum(self.logfx)]
        ).asolve()

    @property
    def b(self) -> number:
        return self.solArray[0]

    @property
    def a(self) -> number:
        return exp(self.solArray[1])

    def f(self,x:number):
        """f(x) for the regression line.

        Args:
            x (number): The x value.

        Returns:
            number: The f(x) value."""

        return self.a*exp(self.b*x)

    def xf(self,f:number):
        """x for the regression line.

        Args:
            f (number): The f(x) value.

        Returns:
            number: The x value.
        """
        return log(f/self.a)/self.b

class LogReg(Reg):
    """Logarithmic Regression class.

    In the form y = a*ln(x) + b."""

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.a}ln(x)+{self.b}"

    @staticmethod
    def make(n: int = 0, eval: bool = False, env: dict | None = None):
        return LogReg(Reg.make(n,eval,env))

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        return LogReg(Reg.lot(n))
    
    @property
    def logx(self):
        return [log(i) for i in self.x]

    @property
    def solArray(self):
        return AugMat(
            np.array([[sum([i**2 for i in self.logx]),sum(self.logx)],
            [sum(self.logx),len(self.logx)]]),
            [sum(mul(self.logx,self.fx)),sum(self.fx)]
        ).asolve()

    @property
    def a(self) -> number:
        return self.solArray[0]

    @property
    def b(self) -> number:
        return self.solArray[1]

    def f(self,x:number):
        """f(x) for the regression line.

        Args:
            x (number): The x value.

        Returns:
            number: The f(x) value."""
        return self.a*log(x)+self.b

    def xf(self,f:number):
        """x for the regression line.

        Args:
            f (number): The f(x) value.

        Returns:
            number: The x value.
        """
        return exp((f-self.b)/self.a)
