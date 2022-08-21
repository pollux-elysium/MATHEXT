from itertools import count
from math import isclose, sqrt
from typing import Callable

from .combinatorics import binomial
from .typedef import *

class DiscreteDistribution:
    def __init__(self, values:list[number], probabilities:list[float]):
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

    def P(self,func:Callable):
        return sum([p for v, p in zip(self.values, self.probabilities) if func(v)])

class UniformDistribution(DiscreteDistribution):
    def __init__(self,n:int, maximum: number, minimum: number = 0):
        super().__init__([minimum+i*(maximum-minimum)/(n-1) for i in range(n)], [1/n]*n)
        self.min = minimum
        self.max = maximum
        self.step = (maximum-minimum)/(n-1)

    def __repr__(self):
        return f"Uniform Distribution: {self.min} to {self.max} in {self.length} steps of {self.step}"

class BinomialDistribution(DiscreteDistribution):
    def __init__(self, p: float,n: int):
        self.n = n
        self.p = p
        super().__init__([i for i in range(n+1)], [binomial(n,i)*p**i*(1-p)**(n-i) for i in range(n+1)])

    def __repr__(self):
        return f"Binomial Distribution: {self.n} trials with {self.p} probability"

class GeometricDistribution(DiscreteDistribution):
    def __init__(self, p: float):
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

    def P(self,func:Callable,n:int=100):#n limits the generator
        return sum([p for i, p in zip(range(n), self.probability) if func(i+1)]) #i+1 because the generator starts at 0

class HypergeometricDistribution(DiscreteDistribution):
    def __init__(self, choose: int, fail: int, suc: int):
        super().__init__([i for i in range(choose+1)], [binomial(suc,i)*binomial(fail,choose-i)/binomial(suc+fail,choose) for i in range(choose+1)])
        self.n = choose
        self.N = fail
        self.m = suc

    def __repr__(self):
        return f"Hypergeometric Distribution: {self.n} trials with {self.N} fail and {self.m} successes"
