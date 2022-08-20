from math import exp, log, sqrt
from typing import Literal, Union
from .load import ldfe,ldf
from .listelemop import *
from .typedef import *
from .matrix import AugMat
import numpy as np

class Reg:
    x:list[number]
    fx:list[number]

    def __init__(self,x:Union[list[number],"Reg"],fx:list[number]|None=None) -> None:
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
    def make(n:int=0,eval:bool=False):
        if eval:
            x:list[number]=[]
            print("Enter x:\n")
            ldfe(x,n)
            fx:list[number]=[]
            print("Enter f(x):\n")
            ldfe(fx,n)
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
        x:list[number] =[]; fx:list[number]= []
        for i in n:
            a,b=i
            x.append(a)
            fx.append(b)
        return Reg(x,fx)

    def loadReg(self,reg:"Reg"):
        self.x=reg.x
        self.fx=reg.fx
        return self

class LinReg(Reg):

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.m}x+{self.c}"

    @staticmethod
    def make(n: int = 0, eval: bool = False):
        return LinReg(Reg.make(n,eval))

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
        return self.m*x+self.c

    def xf(self,f:number):
        return (f-self.c)/self.m

class QuadReg(Reg):

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.a}x^2+{self.b}x+{self.c}"

    @staticmethod
    def make(n: int = 0, eval: bool = False):
        return QuadReg(Reg.make(n,eval))

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
        return self.a*x**2+self.b*x+self.c

    def xf(self,f:number):
        return (-self.b+sqrt(self.b**2-4*self.a*(self.c-f)))/(2*self.a)

class CubReg(Reg):

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.a}x^3+{self.b}x^2+{self.c}x+{self.d}"

    @staticmethod
    def make(n: int = 0, eval: bool = False):
        return CubReg(Reg.make(n,eval))

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
        return self.a*x**3+self.b*x**2+self.c*x+self.d 

    def xf(self,f:number):
        return (-self.c+sqrt(self.c**2-3*self.b*(self.d-f)))/(3*self.b)

class ExpReg(Reg):

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.a}e^({self.b}x)"

    @staticmethod
    def make(n: int = 0, eval: bool = False):
        return ExpReg(Reg.make(n,eval))

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        return ExpReg(Reg.lot(n))

    @property
    def logx(self):
        return [log(i) for i in self.x]

    @property
    def logfx(self):
        return [log(i) for i in self.fx]

    @property
    def solArray(self):
        return AugMat(
            np.array([[sum(mul(self.logx,self.logx)),sum(self.logx)],
            [sum(self.logx),len(self.logx)]]),
            [sum(mul(self.logx,self.logfx)),sum(self.logfx)]
        ).asolve()

    @property
    def a(self) -> number:
        return self.solArray[0]

    @property
    def b(self) -> number:
        return self.solArray[1]

    def f(self,x:number):
        return self.a*exp(self.b*x)

    def xf(self,f:number):
        return log(f/self.a)/self.b

class LogReg(Reg):

    def __repr__(self) -> str:
        return f"{self.x=}\n{self.fx=}\ny~{self.a}ln(x)+{self.b}"

    @staticmethod
    def make(n: int = 0, eval: bool = False):
        return LogReg(Reg.make(n,eval))

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        return LogReg(Reg.lot(n))

    @property
    def expx(self):
        return [exp(i) for i in self.x]

    @property
    def expfx(self):
        return [exp(i) for i in self.fx]

    @property
    def solArray(self):
        return AugMat(
            np.array([[sum(mul(self.expx,self.expx)),sum(self.expx)],
            [sum(self.expx),len(self.expx)]]),
            [sum(mul(self.expx,self.expfx)),sum(self.expfx)]
        ).asolve()

    @property
    def a(self) -> number:
        return self.solArray[0]

    @property
    def b(self) -> number:
        return self.solArray[1]

    def f(self,x:number):
        return self.a*log(x)+self.b

    def xf(self,f:number):
        return exp((f-self.b)/self.a)
