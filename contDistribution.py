from math import isclose, sqrt
from typing import Callable
import sympy as sym
from .typedef import *

oo=sym.oo
x = sym.Symbol('x')

class ContinuousDistribution:
    
    def __init__(self,fx:sym.Expr,minimum:float,maximum:float):
        self.fx = fx
        self.minimum = minimum
        self.maximum = maximum
        self.expr: sym.Expr = fx
        self.sumProb = float(sym.integrate(self.expr,(x,self.minimum,self.maximum)))
        if not isclose(self.sumProb,1):
            print("Sum of probabilities is not 1")

    @staticmethod
    def fromFunc(fx:Callable[[float],float],minimum:float,maximum:float):
        return ContinuousDistribution(fx(x),minimum,maximum)#type:ignore 

    def __repr__(self):
        return f"{self.expr} in {self.minimum} to {self.maximum}"

    def P(self, minimum: float, maximum: float) :
        return sym.integrate(self.expr,(x,minimum,maximum))

    def f(self,y:float) -> float:
        return self.expr.subs(x,y)

    @property
    def mean(self) -> float:
        return sym.integrate(self.expr*x,(x,self.minimum,self.maximum)).__float__()

    @property
    def variance(self) -> float:
        return float(sym.integrate(self.expr*x**2,(x,self.minimum,self.maximum))).__float__() - self.mean**2

    @property
    def stdev(self) -> float:
        return sqrt(self.variance)

    def F(self,y:float):
        return sym.integrate(self.expr,(x,self.minimum,y))
        
    
class ContinuousUniformDistribution(ContinuousDistribution):
    def __init__(self,minimum:float,maximum:float):
        super().fromFunc(lambda x: 1/(maximum-minimum),minimum,maximum)
        self.minimum = minimum
        self.maximum = maximum
        self.expr = sym.Symbol('1')/(maximum-minimum)
        self.sumProb = 1
    
    @property
    def mean(self) -> float:
        return (self.maximum+self.minimum)/2

    @property
    def variance(self) -> float:
        return (self.maximum-self.minimum)**2/12

    @property
    def stdev(self) -> float:
        return sqrt(self.variance)

class NormalDistribution:
    def __init__(self,mean:float,stdev:float):
        self.mu = mean
        self.sigma = stdev
        self.expr = sym.exp(-((x-self.mu)**2)/(2*self.sigma**2))/(self.sigma*sqrt(2*sym.pi))
        self.sumProb = float(sym.integrate(self.expr,(x,-sym.oo,sym.oo)))
        if not isclose(self.sumProb,1):
            print("Sum of probabilities is not 1")

    def __repr__(self):
        return f"{self.expr} with mean {self.mean} and stdev {self.stdev}"

    def P(self, minimum: float, maximum: float) -> float:
        return float(sym.integrate(self.expr,(x,minimum,maximum)))

    @property
    def mean(self) -> float:
        return self.mu

    @property
    def variance(self) -> float:
        return self.sigma**2

    @property
    def stdev(self) -> float:
        return self.sigma

    def toZ(self,x:float) -> float:
        return (x-self.mu)/self.sigma

    def fromZ(self,z:float) -> float:
        return z*self.sigma+self.mu

DefaultND = NormalDistribution(0,1)

def pZ(z:float)->float:
    return float(sym.integrate(sym.exp(-(x**2)/(2))/(sqrt(2*sym.pi)),(x,-sym.oo,z)))  # type: ignore

def Zp(p:float)->float:#find z from p
    z=sym.symbols('z')
    return sym.solve(sym.Eq(sym.integrate(sym.exp(-(x**2)/(2))/(sqrt(2*sym.pi)),(x,-sym.oo,z)),p)) # type: ignore

def binomialZ(n:int,p:float,x:number)->float:
    return (x-n*p+.5)/sqrt(n*p*(1-p))