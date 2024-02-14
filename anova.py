import numpy as np
from .typedef import NDArray

class ANOVA:
    """ANOVA class for one-way ANOVA"""
    def __init__(self,data :NDArray[np.float64]):
        """Initialize ANOVA

        Args:
            data (NDArray): 2D array of data
                i: Factor
                j: Replication

        Raises:
            ValueError: If data is not 2D
        """
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
        return f"ANOVA Result\n{self.SSTn:.2f}\t{self.k-1}\t{self.MSn:.2f}\t{self.F:.2f}\n{self.SSE:.2f}\t{self.k*(self.n-1)}\t{self.MSe:.2f}\n{self.SST:.2f}\t{self.N-1}"

class ANOVABlock(ANOVA):
    """ANOVA class for two-way ANOVA (block)"""
    def __init__(self,data :NDArray[np.float64]):
        """Initialize ANOVABlock

        Args:
            data (NDArray): 2D array of data
                i: Factor 1
                j: Block

        Raises:
            ValueError: If data is not 2D
        """
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

class ANOVA2Single(ANOVABlock):
    """ANOVA class for two-way ANOVA (single)"""
    def __init__(self,data :NDArray[np.float64]):
        """Initialize ANOVA2Single

        Args:
            data (NDArray): 2D array of data
                i: Factor 1
                j: Factor 2

        Raises:
            ValueError: If data is not 2D
        """
        super().__init__(data)
        self.SSN = ((self.data * self.sumn[:,None] *self.sumk).sum() - self.sum*(self.SSTk+self.SSTn+self.sum**2/self.N))**2/self.N/self.SSTk/self.SSTn
        self.SSE = self.SST-self.SSTn-self.SSTk-self.SSN
        self.MSN = self.SSN
        self.MSe = self.SSE/((self.k-1)*(self.n-1)-1)
        self.F2 = self.MSN/self.MSe

        self.F0 = self.MSn/self.MSe
        self.F1 = self.MSk/self.MSe

    def __repr__(self):
        return f"ANOVA2Single({self.data})"

    @property
    def result(self) -> str:
        return f"ANOVA2Single Result {self.k=}\n{self.n=}\n{self.N=}\n{self.sum=}\n{self.sumn=}\n{self.sum2=}\n{self.SST=}\n{self.SSTn=}\n{self.sumk=}\n{self.SSTk=}\n{self.SSE=}\n{self.MSn=}\n{self.MSk=}\n{self.MSe=}\n{self.F0=}\n{self.F1=}\n{self.SSN=}"

    @property
    def fmt(self) -> str:
        return f"ANOVA2Single Result\
            \n{self.SSTn:.2f}\t{self.k-1}\t{self.MSn:.2f}\t{self.F0:.2f}\
            \n{self.SSTk:.2f}\t{self.n-1}\t{self.MSk:.2f}\t{self.F1:.2f}\
            \n{self.SSN:.4f}\t{1}\t{self.MSN:.4f}\t{self.F2:.2f}\
            \n{self.SSE:.2f}\t{(self.k-1)*(self.n-1)-1}\t{self.MSe:.2f}\
            \n{self.SST:.2f}\t{self.N-1}"

class ANOVA2:
    """ANOVA class for two-way ANOVA (factorial)"""
    def __init__(self,data :NDArray[np.float64]):
        """Initialize ANOVA2

        Args:
            data (NDArray): 3D array of data
                i: Factor 1
                j: Factor 2
                k: Replication

        Raises:
            ValueError: If data is not 3D
        """
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
        return f"ANOVA2 Result\n{self.SSa:.2f}\t{self.i-1}\t{self.MSa:.2f}\t{self.Fa:.2f}\n{self.SSb:.2f}\t{self.j-1}\t{self.MSb:.2f}\t{self.Fb:.2f}\n{self.SSab:.2f}\t{(self.i-1)*(self.j-1)}\t{self.MSab:.2f}\t{self.Fab:.2f}\n{self.SSe:.2f}\t{(self.i*self.j)*(self.k-1)}\t{self.MSe:.2f}\n{self.SSt:.2f}\t{(self.i)*(self.j)*(self.k)-1}"
        

class ANOVA2Block(ANOVA2):
    """ANOVA class for three-way ANOVA (block)"""
    def __init__(self,data :NDArray[np.float64]):
        """Initialize ANOVA2Block

        Args:
            data (NDArray): 3D array of data
                i: Factor 1
                j: Factor 2
                k: Block

        Raises:
            ValueError: If data is not 3D
        """
        super().__init__(data)
        self.sumk = np.sum(data,axis=(0,1))
        self.SSk = np.sum(self.sumk**2)/self.i/self.j-self.gsum**2/(self.i*self.j*self.k)
        self.SSE = self.SSt-self.SSa-self.SSb-self.SSab-self.SSk
        self.MSk = self.SSk/(self.k-1)
        self.MSe = self.SSE/(self.i*self.j-1)/(self.k-1)
        self.Fa = self.MSa/self.MSe
        self.Fb = self.MSb/self.MSe
        self.Fab = self.MSab/self.MSe
        self.Fk = self.MSk/self.MSe

    def __repr__(self):
        return f"ANOVA2Block({self.data})"

    @property
    def result(self) -> str:
        return f"ANOVA2Block Result {self.i=}\n{self.j=}\n{self.k=}\n{self.gsum=}\n{self.sumi=}\n{self.sumj=}\n{self.sumk=}\n{self.SSt=}\n{self.SSa=}\n{self.SSb=}\n{self.SSk=}\n{self.SSab=}\n{self.SSE=}\n{self.MSa=}\n{self.MSb=}\n{self.MSk=}\n{self.MSe=}\n{self.Fa=}\n{self.Fb=}\n{self.Fk=}"

    @property
    def fmt(self):
        return f"ANOVA2Block Result\n{self.SSa:.2f}\t{self.i-1}\t{self.MSa:.2f}\t{self.Fa:.2f}\n{self.SSb:.2f}\t{self.j-1}\t{self.MSb:.2f}\t{self.Fb:.2f}\n{self.SSk:.2f}\t{self.k-1}\t{self.MSk:.2f}\t{self.Fk:.2f}\n{self.SSab:.2f}\t{(self.i-1)*(self.j-1)}\t{self.MSab:.2f}\t{self.Fab:.2f}\n{self.SSE:.2f}\t{(self.i*self.j)*(self.k-1)}\t{self.MSe:.2f}\n{self.SSt:.2f}\t{(self.i)*(self.j)*(self.k)-1}"

class LatinSquare:
    """Latin Square class

    Args:
        block (NDArray): Block data
            i:Error 1
            j:Error 2
        factor (NDArray): Factor data [Factor][Count]
            i: Factor
            j: Replication
    """

    def __init__(self,block:NDArray[np.float64],factor:NDArray[np.float64]):
        """Initialize LatinSquare

        Args:
            block (NDArray): Block data
            factor (NDArray): Factor data [Factor][Count]
        """
        self.block = block
        self.factor = factor
        self.process()

    def process(self):
        block = self.block
        factor = self.factor
        self.i = len(block)
        self.j = len(block[0])
        self.k = len(factor)
        self.gsum = np.sum(block)
        self.sumi = np.sum(block,axis=1)
        self.sumj = np.sum(block,axis=0)
        self.sumk = np.sum(factor,axis=1)
        self.SSt = np.sum(block**2)-self.gsum**2/self.i/self.j
        self.SSi = np.sum(self.sumi**2)/self.j-self.gsum**2/self.i/self.j
        self.SSj = np.sum(self.sumj**2)/self.i-self.gsum**2/self.i/self.j
        self.SSk = np.sum(self.sumk**2)/self.i-self.gsum**2/self.i/self.j
        self.SSe = self.SSt-self.SSi-self.SSj-self.SSk
        self.MSi = self.SSi/(self.i-1)
        self.MSj = self.SSj/(self.j-1)
        self.MSk = self.SSk/(self.k-1)
        self.MSe = self.SSe/((self.i-2)*(self.k-1))
        self.Fi = self.MSi/self.MSe
        self.Fj = self.MSj/self.MSe
        self.Fk = self.MSk/self.MSe



    def __repr__(self):
        return f"LatinSquare({self.block},{self.factor})"

    @property
    def result(self) -> str:
        return f"LatinSquare Result {self.i=}\n{self.j=}\n{self.k=}\n{self.gsum=}\n{self.sumi=}\n{self.sumj=}\n{self.sumk=}\n{self.SSt=}\n{self.SSi=}\n{self.SSj=}\n{self.SSk=}\n{self.SSe=}\n{self.MSi=}\n{self.MSj=}\n{self.MSk=}\n{self.MSe=}\n{self.Fi=}\n{self.Fj=}\n{self.Fk=}"
    
    @property
    def fmt(self):
        return f"LatinSquare Result\n{self.SSi:.2f}\t{self.i-1}\t{self.MSi:.2f}\t{self.Fi:.2f}\n{self.SSj:.2f}\t{self.j-1}\t{self.MSj:.2f}\t{self.Fj:.2f}\n{self.SSk:.2f}\t{self.k-1}\t{self.MSk:.2f}\t{self.Fk:.2f}\n{self.SSe:.2f}\t{(self.i-2)*(self.k-1)}\t{self.MSe:.2f}\n{self.SSt:.2f}\t{(self.i)*(self.j)-1}"