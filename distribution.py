from math import sqrt

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

class UniformDistribution(DiscreteDistribution):
    def __init__(self,n:int, max: number, min: number = 0):
        super().__init__([min+i*(max-min)/(n-1) for i in range(n)], [1/n]*n)
        self.min = min
        self.max = max
        self.step = (max-min)/(n-1)

    def __repr__(self):
        return f"Uniform Distribution: {min} to {max} in {self.length} steps of {self.step}"

class BinomialDistribution(DiscreteDistribution):
    def __init__(self, p: float,n: int):
        self.n = n
        self.p = p
        super().__init__([i for i in range(n+1)], [binomial(n,i)*p**i*(1-p)**(n-i) for i in range(n+1)])

    def __repr__(self):
        return f"Binomial Distribution: {self.n} trials with {self.p} probability"

class GeometricDistribution(DiscreteDistribution):
    def __init__(self, p: float,n:int = 10):
        super().__init__([i for i in range(1,n)], [p*(1-p)**(i-1) for i in range(1,n)])
        self.p = p

    def __repr__(self):
        return f"Geometric Distribution: {self.p} probability"

    def extended(self,n:int):
        return GeometricDistribution(self.p,n)

class HypergeometricDistribution(DiscreteDistribution):
    def __init__(self, n: int, N: int, m: int):
        super().__init__([i for i in range(m+1)], [binomial(m,i)*binomial(N-m,n-i)/binomial(N,n) for i in range(m+1)])
        self.n = n
        self.N = N
        self.m = m

    def __repr__(self):
        return f"Hypergeometric Distribution: {self.n} trials with {self.N} total and {self.m} successes"
