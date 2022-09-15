from .load import ldf
from .typedef import T,number
import statistics

def percentile(x: list[int|float], p: number):
    """Return pth percentile of list x"""
    x.sort()
    l = p*(len(x)+1)/100
    return x[int(l) - 1]+(x[int(l)]-x[int(l)-1])*(l % 1)


def freq(x: list[T]) -> dict[T, int]:
    return {i: x.count(i)for i in undupe(x)}
    


def tree(x: list[number],sep:int=10):
    j= undupe([int(i//sep) for i in x])
    return {i: [k for k in x if k//sep == i]for i in j}

def undupe(x: list[T]) -> list[T]:
    return list(dict.fromkeys(x))

def iqr(x: list[float|int]) -> float:
    return percentile(x,75)-percentile(x,25)



class StatData:
    data:list[number]
    isSample:bool = False

    def __init__(self, data: list[number],sample:bool=False):
        self.data = data
        self.isSample = sample

    def __repr__(self):
        return f"StatData({self.data})"

    @property
    def mean(self) -> float:
        return statistics.mean(self.data)

    @property
    def median(self) -> float:
        return statistics.median(self.data)

    @property
    def mode(self) -> list[float]:
        return [i for i in undupe(self.data) if self.data.count(i) == max([self.data.count(i) for i in undupe(self.data)])]

    @property
    def stdev(self) -> float:
        if self.isSample:
            return statistics.stdev(self.data)
        else:
            return statistics.pstdev(self.data)

    @property
    def variance(self) -> float:
        if self.isSample:
            return statistics.variance(self.data)
        else:
            return statistics.pvariance(self.data)

    @property
    def range(self) -> float:
        return max(self.data)-min(self.data)

    @property
    def iqr(self) -> float:
        return percentile(self.data,75)-percentile(self.data,25)

    def percentile(self, p: number) -> float:
        return percentile(self.data, p)

    @staticmethod
    def make():
        return StatData(ldf([]))

    def __add__(self, other: 'StatData') -> 'StatData':
        return StatData(self.data + other.data)

    def trimMean(self, p: number) -> float:
        return statistics.mean([i for i in self.data if self.percentile(p) <= i <= self.percentile(100-p)])

    def freq(self) -> dict[number, int]:
        return freq(self.data)

    def tree(self,sep:int=10) -> dict[int, list[number]]:
        return tree(self.data,sep)

    @property
    def sigmaXbar(self) -> float:
        return self.stdev/(len(self.data)**0.5)

    
    