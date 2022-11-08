from .load import ldf
from .typedef import T,number,NDArray
import statistics
import numpy as np

def lapprox(p1:tuple[number,number],p2:tuple[number,number],x:number)->float:
    """Return y value of a line approximated by two points"""
    return (p2[0]-p1[0])/(p2[1]-p1[1])*(x-p1[1])+p1[0]

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

class ANOVA:
    def __init__(self,data :NDArray[np.float64]):
        self.data = data
        self.k = len(data)
        self.n = len(data[0])
        self.N = self.n*self.k
        self.sum = np.sum(data)
        self.sumn = np.sum(data,axis=1)
        self.sum2 = np.sum(data**2)
        self.SST = self.sum2-self.sum**2/self.N
        self.SSTn = sum(self.sumn**2)/self.n-self.sum**2/self.N
        self.SSE = self.SST-self.SSTn
        self.MSn = self.SSTn/(self.k-1)
        self.MSe = self.SSE/(self.k*(self.n-1))
        self.F = self.MSn/self.MSe

    def __repr__(self):
        return f"ANOVA({self.data})"

    @property
    def result(self) -> str:
        return f"ANOVA Result {self.k=}\n{self.n=}\n{self.N=}\n{self.sum=}\n{self.sumn=}\n{self.sum2=}\n{self.SST=}\n{self.SSTn=}\n{self.SSE=}\n{self.MSn=}\n{self.MSe=}\n{self.F=}"

    @property
    def fmt(self):
        return f"ANOVA Result\n{self.SSTn:.2f}\t{self.n-1}\t{self.MSn:.2f}\t{self.F:.2f}\n{self.SSE:.2f}\t{self.k*(self.n-1)}\t{self.MSe:.2f}\n{self.SST:.2f}\t{self.N-1}"

class ANOVABlock(ANOVA):
    def __init__(self,data :NDArray[np.float64]):
        super().__init__(data)
        self.sumk = np.sum(data,axis=0)
        self.SSTk = sum(self.sumk**2)/self.k-self.sum**2/self.N
        self.SSE = self.SST-self.SSTn-self.SSTk
        self.MSk = self.SSTk/(self.n-1)
        self.MSe = self.SSE/((self.k-1)*(self.n-1))
        self.F0 = self.MSn/self.MSe
        self.F1 = self.MSk/self.MSe


    def __repr__(self):
        return f"ANOVABlock({self.data})"

    @property
    def result(self) -> str:
        return f"ANOVABlock Result {self.k=}\n{self.n=}\n{self.N=}\n{self.sum=}\n{self.sumn=}\n{self.sum2=}\n{self.SST=}\n{self.SSTn=}\n{self.sumk=}\n{self.SSTk=}\n{self.SSE=}\n{self.MSn=}\n{self.MSk=}\n{self.MSe=}\n{self.F0=}\n{self.F1=}"

    @property
    def fmt(self):
        return f"ANOVABlock Result\n{self.SSTn:.2f}\t{self.k-1}\t{self.MSn:.2f}\t{self.F0:.2f}\n{self.SSTk:.2f}\t{self.n-1}\t{self.MSk:.2f}\t{self.F1:.2f}\n{self.SSE:.2f}\t{(self.k-1)*(self.n-1)}\t{self.MSe:.2f}\n{self.SST:.2f}\t{self.N-1}"

class ANOVA2:
    def __init__(self,data :NDArray[np.float64]):
        self.data = data
        self.process()
        
    def process(self):
        data=self.data
        self.i=len(data)
        self.j=len(data[0])
        self.k=len(data[0][0])
        self.gsum = np.sum(data)
        self.sumi = np.sum(data,axis=(1,2))
        self.sumj = np.sum(data,axis=(0,2))
        self.sumij = np.sum(data,axis=2)
        self.SSt = np.sum(data**2)-self.gsum**2/(self.i*self.j*self.k)
        self.SSa = np.sum(self.sumi**2)/self.j/self.k-self.gsum**2/(self.i*self.j*self.k)
        self.SSb = np.sum(self.sumj**2)/self.i/self.k-self.gsum**2/(self.i*self.j*self.k)
        self.SSsub = np.sum(self.sumij**2)/self.k-self.gsum**2/(self.i*self.j*self.k)
        self.SSab = self.SSsub-self.SSa-self.SSb
        self.SSe = self.SSt-self.SSa-self.SSb-self.SSab
        self.MSa = self.SSa/(self.i-1)
        self.MSb = self.SSb/(self.j-1)
        self.MSab = self.SSab/(self.i-1)/(self.j-1)
        self.MSe = self.SSe/(self.i*self.j*(self.k-1))
        self.Fa = self.MSa/self.MSe
        self.Fb = self.MSb/self.MSe
        self.Fab = self.MSab/self.MSe

    def __repr__(self):
        return f"ANOVA2({self.data})"

    @property
    def result(self) -> str:
        return f"ANOVA2 Result {self.i=}\n{self.j=}\n{self.k=}\n{self.gsum=}\n{self.sumi=}\n{self.sumj=}\n{self.sumij=}\n{self.SSt=}\n{self.SSa=}\n{self.SSb=}\n{self.SSsub=}\n{self.SSab=}\n{self.SSe=}\n{self.MSa=}\n{self.MSb=}\n{self.MSab=}\n{self.MSe=}"

    @property
    def fmt(self):
        return f"ANOVA2 Result\n{self.SSa:.2f}\t{self.i-1}\t{self.MSa:.2f}\t{self.Fa:.2f}\n{self.SSb:.2f}\t{self.j-1}\t{self.MSb:.2f}\t{self.Fb:.2f}\n{self.SSab:.2f}\t{(self.i-1)*(self.j-1)}\t{self.MSab:.2f}\t{self.Fab:.2f}\n{self.SSe:.2f}\t{(self.i*self.j)*(self.k-1)}\t{self.MSe:.2f}\n{self.SSt:.2f}\t{(self.i-1)*(self.j-1)*(self.k-1)}"
