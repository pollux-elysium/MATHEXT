from typing import Literal, Union
from .load import ldfe,ldf
from .listelemop import *
from .typedef import *

class Reg:
    x:list[number]
    fx:list[number]

    def __init__(self,x:Union[list[number],"Reg"],fx:list[number]|Literal[False]=False) -> None:
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

    @staticmethod
    def make(n: int = 0, eval: bool = False):
        return LinReg(Reg.make(n,eval))

    @property
    def c(self):
        return ((sum(self.fx)*sum(mul(self.x,self.x)) - sum(self.x)*sum(mul(self.x,self.fx)))
            /(len(self.x)*sum(mul(self.x,self.x))-sum(self.x)**2))

    @property
    def m(self):
        return ((
            len(self.x)*sum(mul(self.x,self.fx)) - sum(self.x)*sum(self.fx))
            /(len(self.x)*sum(mul(self.x,self.x))-sum(self.x)**2))

    def f(self,x:number):
        return self.m*x+self.c

    def xf(self,f:number):
        return (f-self.c)/self.m
