from itertools import count
from math import isclose, sqrt
from typing import Callable

from .combinatorics import binomial
from .typedef import *

class DiscreteDistribution:
    """Discrete Distribution Class"""
    def __init__(self, values:list[number], probabilities:list[float]):
        """Discrete Distribution Class

        Args:
            values (list[number]): List of values
            probabilities (list[float]): List of probabilities
        """
        self.values = values
        self.probabilities = probabilities
        self.length = len(values)

    def __repr__(self):
        return f"values: {self.values}, probabilities: {self.probabilities}"

    @property
    def mu(self):
        return sum([v * p for v, p in zip(self.values, self.probabilities)])

    @property
    def variance(self):
        return sum([p * (v - self.mu)**2 for v, p in zip(self.values, self.probabilities)])

    @property
    def std(self):
        return sqrt(self.variance)

    @property
    def sumProb(self):
        p=sum(self.probabilities)
        if not isclose(p,1):
            raise ValueError("Sum of probabilities is not 1")
        return p

    def P(self,func:Callable[[number],bool]):
        """Probability of a function

        Args:
            func (Callable[[number],bool]): Function

        Returns:
            float: Probability
        """
        return sum([p for v, p in zip(self.values, self.probabilities) if func(v)])

    

class UniformDistribution(DiscreteDistribution):
    """Uniform Distribution Class"""
    def __init__(self,n:int, maximum: number, minimum: number = 0):
        """Uniform Distribution Class

        Args:
            n (int): Number of steps
            maximum (number): Maximum value
            minimum (number, optional): Minimum value. Defaults to 0.
        """
        super().__init__([minimum+i*(maximum-minimum)/(n-1) for i in range(n)], [1/n]*n)
        self.min = minimum
        self.max = maximum
        self.step = (maximum-minimum)/(n-1)

    def __repr__(self):
        return f"Uniform Distribution: {self.min} to {self.max} in {self.length} steps of {self.step}"

class BinomialDistribution(DiscreteDistribution):
    """Binomial Distribution Class"""
    def __init__(self, p: float,n: int):
        """Binomial Distribution Class

        Args:
            p (float): Probability
            n (int): Number of trials
        """
        self.n = n
        self.p = p
        super().__init__([i for i in range(n+1)], [binomial(n,i)*p**i*(1-p)**(n-i) for i in range(n+1)])

    def __repr__(self):
        return f"Binomial Distribution: {self.n} trials with {self.p} probability"

class GeometricDistribution(DiscreteDistribution):
    """Geometric Distribution Class"""
    def __init__(self, p: float):
        """Geometric Distribution Class

        Args:
            p (float): Probability
        """
        self.p=p

    def __repr__(self):
        return f"Geometric Distribution: {self.p} probability"

    @property
    def mu(self):
        return 1/self.p

    @property
    def variance(self):
        return (1-self.p)/(self.p**2)

    @property
    def std(self):
        return sqrt(self.variance)

    @property
    def values(self):
        return count(1)

    @property
    def probability(self):
        return (self.p*(1-self.p)**(i-1) for i in count(1))

    @property
    def sumProb(self):
        return 1

    def P(self,func:Callable[[float],float],n:int=100):#n limits the generator
        """Probability of a function

        Args:
            func (Callable[[float],float]): Function
            n (int, optional): Number of steps. Defaults to 100.

        Returns:
            float: Probability
        """
        return sum([p for i, p in zip(range(n), self.probability) if func(i+1)]) #i+1 because the generator starts at 0

class HypergeometricDistribution(DiscreteDistribution):
    """Hypergeometric Distribution Class"""
    def __init__(self, choose: int, fail: int, suc: int):
        """Hypergeometric Distribution Class

        Args:
            choose (int): Number of trials
            fail (int): Number of failures
            suc (int): Number of successes
        """
        super().__init__([i for i in range(choose+1)], [binomial(suc,i)*binomial(fail,choose-i)/binomial(suc+fail,choose) for i in range(choose+1)])
        self.n = choose
        self.N = fail
        self.m = suc

    def __repr__(self):
        return f"Hypergeometric Distribution: {self.n} trials with {self.N} fail and {self.m} successes"

class JointDiscreteDistribution:
    """Joint Discrete Distribution Class"""
    def __init__(self,point:list[tuple[number,number]],probabilities:list[float]):
        """Joint Discrete Distribution Class

        Args:
            point (list[tuple[number,number]]): List of points
            probabilities (list[float]): List of probabilities
        """
        self.point=point
        self.probabilities=probabilities
        self.length=len(point)

    @property
    def mux(self):
        return sum([x[0]*p for x,p in zip(self.point,self.probabilities)])

    @property
    def muy(self):
        return sum([x[1]*p for x,p in zip(self.point,self.probabilities)])

    @property
    def muxy(self):
        return sum([x[0]*x[1]*p for x,p in zip(self.point,self.probabilities)])

    @property
    def varx(self):
        return sum([p*(x[0]-self.mux)**2 for x,p in zip(self.point,self.probabilities)])

    @property
    def vary(self):
        return sum([p*(x[1]-self.muy)**2 for x,p in zip(self.point,self.probabilities)])

    @property
    def stdx(self):
        return sqrt(self.varx)

    @property
    def stdy(self):
        return sqrt(self.vary)

    @property
    def sumProb(self):
        p=sum(self.probabilities)
        if not isclose(p,1):
            raise ValueError("Sum of probabilities is not 1")
        return p

    @property
    def cov(self):
        return sum([p*(x[0]-self.mux)*(x[1]-self.muy) for x,p in zip(self.point,self.probabilities)])

    @property
    def corr(self):
        return self.cov/(self.stdx*self.stdy)

    def P(self,func:Callable[[number,number],bool]):
        """Probability of a function

        Args:
            func (Callable[[number,number],bool]): Function with input X,Y

        Returns:
            float: Probability
        """
        return sum([p for x, p in zip(self.point, self.probabilities) if func(x[0],x[1])])

    @staticmethod
    def from2dist(dist1:DiscreteDistribution,dist2:DiscreteDistribution):
        """Joint Distribution from 2 distributions

        Args:
            dist1 (DiscreteDistribution): Distribution 1
            dist2 (DiscreteDistribution): Distribution 2

        Returns:
            JointDiscreteDistribution: Joint Distribution
        """
        return JointDiscreteDistribution([(x,y) for x in dist1.values for y in dist2.values],[p1*p2 for p1 in dist1.probabilities for p2 in dist2.probabilities])