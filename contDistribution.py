from math import isclose, sqrt
from typing import Callable
import sympy as sym
from .typedef import *
from .stats import StatData
from statistics import NormalDist

oo=sym.oo
x = sym.Symbol('x')
y= sym.Symbol("y")

class ContinuousDistribution:
    """Continuous distribution class

    Call normally for sympy expression
    Call fromFunc for python function
    """
    
    def __init__(self,fx:sym.Expr,minimum:float,maximum:float):
        """Continuous distribution class

        Args:
            fx (sym.Expr): Function as a sympy expression
            minimum (float): minimum value
            maximum (float): maximum value
        """
        self.fx = fx
        self.minimum = minimum
        self.maximum = maximum
        self.expr: sym.Expr = fx
        self.sumProb = float(sym.integrate(self.expr,(x,self.minimum,self.maximum)))  # type: ignore
        if not isclose(self.sumProb,1):
            print("Sum of probabilities is not 1")

    @staticmethod
    def fromFunc(fx:Callable[[float],float],minimum:float,maximum:float):
        """Create a continuous distribution from a function

        Args:
            fx (Callable[[float],float]): Function
            minimum (float): minimum value
            maximum (float): maximum value

        Returns:
            ContinuousDistribution: Continuous distribution
        """
        return ContinuousDistribution(fx(x),minimum,maximum)#type:ignore 

    def __repr__(self):
        return f"{self.expr} in {self.minimum} to {self.maximum}"

    def P(self, minimum: float, maximum: float) :
        """Probability of a range

        Args:
            minimum (float): minimum value
            maximum (float): maximum value

        Returns:
            float: probability
        """
        return sym.integrate(self.expr,(x,minimum,maximum))

    def f(self,y:float) -> float:
        """Probability density function

        Args:
            y (float): value

        Returns:
            float: probability density
        """
        return self.expr.subs(x,y)  # type: ignore

    @property
    def mean(self) -> float:
        return sym.integrate(self.expr*x,(x,self.minimum,self.maximum)).__float__()  # type: ignore

    @property
    def variance(self) -> float:
        return sym.integrate(self.expr*x**2,(x,self.minimum,self.maximum)).__float__() - self.mean**2  # type: ignore

    @property
    def stdev(self) -> float:
        return sqrt(self.variance)

    def F(self,y:float):
        """Cumulative distribution function

        Args:
            y (float): value

        Returns:
            float: cumulative distribution
        """
        return sym.integrate(self.expr,(x,self.minimum,y))
        
    
class ContinuousUniformDistribution(ContinuousDistribution):
    """Continuous uniform distribution class"""
    def __init__(self,minimum:float,maximum:float):
        """Continuous uniform distribution class

        Args:
            minimum (float): minimum value
            maximum (float): maximum value
        """

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
    """Normal distribution class
    
    Wrapper for built in normal distribution"""
    def __init__(self,mean:float,stdev:float):
        """Normal distribution class

        Args:
            mean (float): mean
            stdev (float): standard deviation
        """
        self.mu = mean
        self.sigma = stdev
        self.dist = NormalDist(mean,stdev)

    def __repr__(self):
        return f"Normal distribution with mean {self.mean} and stdev {self.stdev}"

    def P(self, minimum: float, maximum: float) -> float:
        """Probability of a range

        Args:
            minimum (float): minimum value
            maximum (float): maximum value

        Returns:
            float: probability
        """
        return self.dist.cdf(maximum)-self.dist.cdf(minimum)

    @property
    def mean(self) -> float:
        return self.mu

    @property
    def variance(self) -> float:
        return self.sigma**2

    @property
    def stdev(self) -> float:
        return self.sigma

    @staticmethod
    def fromData(data:StatData):
        return NormalDistribution(data.mean,data.stdev)

    def toZ(self,x:float)->float:
        """Get Z score

        Args:
            x (float): value

        Returns:
            float: Z score
        """
        return (x-self.mean)/self.stdev

    def fromZ(self,z:float)->float:
        """Get value from Z score

        Args:
            z (float): Z score

        Returns:
            float: value
        """
        return z*self.stdev+self.mean

    def toP(self,x:float)->float:
        """Get cumilative probability from value

        Args:
            x (float): value

        Returns:
            float: probability
        """
        return self.dist.cdf(x)

    def fromP(self,p:float)->float:
        """Get value from cumilative probability

        Args:
            p (float): probability

        Returns:
            float: value
        """
        return self.dist.inv_cdf(p)

DefaultND = NormalDistribution(0,1)

def pZ(z:float)->float:
    """Probability of a Z score

    Args:
        z (float): Z score

    Returns:
        float: probability
    """
    return NormalDist().cdf(z)

def Zp(p:float)->float:
    """Z score of a probability

    Args:
        p (float): probability

    Returns:
        float: Z score
    """
    return NormalDist().inv_cdf(p)

def binomialZ(n:int,p:float,x:number)->float:
    """Z score of a binomial distribution

    Args:
        n (int): number of trials
        p (float): probability of success
        x (number): number of successes

    Returns:
        float: Z score
    """
    return (x-n*p+.5)/sqrt(n*p*(1-p))

def confidenceZ(confidence:float)->float:
    return Zp((1+confidence)/2)
    
def Tp(k:int,a:float)->float:
    """T score of a probability

    Args:
        k (int): degrees of freedom
        a (float): probability

    Returns:
        float: T score
    """
    T=sym.symbols('T')
    return sym.solve(sym.Eq(sym.integrate((sym.gamma((k+1)/2)/(sym.gamma(k/2)*sqrt(k*sym.pi))/(x**2/k+1)**((k+1)/2)),(x,-sym.oo,T)),a)) # type: ignore

