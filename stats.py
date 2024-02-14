from .load import ldf
from .typedef import T,number,NDArray
import statistics
import numpy as np

def logmean(x: list[number]) -> float:
    """Return log mean of list x

    Args:
        x (list): List of numbers

    Returns:
        float: Log mean of list x
    """
    return (x[0]-x[1])/np.log(x[0]/x[1])
    

def lapprox(p1:tuple[number,number],p2:tuple[number,number],x:number)->float:
    """Return y value of a line approximated by two points

    Args:
        p1 (tuple): First point (y,x)
        p2 (tuple): Second point (y,x)
        x (number): x value of line
        
    Returns:
        float: y value of line"""
    return (p2[0]-p1[0])/(p2[1]-p1[1])*(x-p1[1])+p1[0]

def percentile(x: list[number], p: number):
    """Return pth percentile of list x
    
    Args:
        x (list): List of numbers
        p (number): Percentile
        
    Returns:
        float: pth percentile of list x
    """
    x.sort()
    l = p*(len(x)+1)/100
    return x[int(l) - 1]+(x[int(l)]-x[int(l)-1])*(l % 1)


def freq(x: list[T]) -> dict[T, int]:
    """Return frequency of each item in list x

    Args:
        x (list): List of items

    Returns:
        dict: Frequency of each item in list x
    """
    return {i: x.count(i)for i in undupe(x)}
    


def tree(x: list[number],sep:int=10):
    """Return a tree of the data in list x

    Args:
        x (list): List of numbers
        sep (int, optional): Separation between each tree level. Defaults to 10. recommended to be a multiple of 10

    Returns:
        dict: Tree of the data in list x
    """
    j= undupe([int(i//sep) for i in x])
    return {i: [k for k in x if k//sep == i]for i in j}

def undupe(x: list[T]) -> list[T]:
    """Return list with duplicates removed"""
    return list(dict.fromkeys(x))

def iqr(x: list[float|int]) -> float:
    """Return interquartile range of list x"""
    return percentile(x,75)-percentile(x,25)

def indexClose(x: list[number], n: number) -> int:
    """Return index of number in list x closest to n"""
    return x.index(min(x, key=lambda i: abs(i-n)))

def cumCount(x: list[number],mode:bool = False) -> dict[number,int]:
    """Return cumulative count of each number in list x
    
    Args:
        x (list): List of numbers
        mode (bool, optional): False: Less Than.
    """
    x.sort()
    if mode:
        return {i: len([k for k in x if k <= i]) for i in undupe(x)}
    else:
        return {i: len([k for k in x if k >= i]) for i in undupe(x)}
    
def cumFreq(x: list[number],mode:bool = False) -> dict[number,float]:
    """Return cumulative frequency of each number in list x
    
    Args:
        x (list): List of numbers
        mode (bool, optional): False: Less Than.
    """
    x.sort()
    if mode:
        return {i: len([k for k in x if k <= i])/len(x) for i in undupe(x)}
    else:
        return {i: len([k for k in x if k >= i])/len(x) for i in undupe(x)}

class StatData:
    """Wrapper for list to be used with statistics module"""
    data:list[number]
    isSample:bool = False

    def __init__(self, data: list[number],sample:bool=False):
        """Initialize StatData
        
        Args:
            data (list): List of numbers
            sample (bool, optional): Whether data is a sample or population. Defaults to False.
        """
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
        """Percentile of number p"""
        return percentile(self.data, p)

    @staticmethod
    def make():
        """Macro for creating StatData with ldf"""
        return StatData(ldf([]))

    def __add__(self, other: 'StatData') -> 'StatData':
        return StatData(self.data + other.data)

    def trimMean(self, p: number) -> float:
        """Return mean of data with p% trimmed off each side"""
        return statistics.mean([i for i in self.data if self.percentile(p) <= i <= self.percentile(100-p)])

    def freq(self) -> dict[number, int]:
        """Frequency of each number in data"""
        return freq(self.data)

    def tree(self,sep:int=10) -> dict[int, list[number]]:
        """Return a tree of the data in list x

    Args:
        x (list): List of numbers
        sep (int, optional): Separation between each tree level. Defaults to 10. recommended to be a multiple of 10

    Returns:
        dict: Tree of the data in list x
    """
        return tree(self.data,sep)

    @property
    def sigmaXbar(self) -> float:
        """Standard error of the mean"""
        return self.stdev/(len(self.data)**0.5)
    
    def __getitem__(self, key: int) -> float:
        return self.data[key]
    
    def __setitem__(self, key: int, value: float):
        self.data[key] = value

    def __len__(self) -> int:
        return len(self.data)
    
    

