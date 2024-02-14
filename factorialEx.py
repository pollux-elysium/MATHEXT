from .typedef import T,number,NDArray
import numpy as np

class fac22:
    
    def __init__(self,arr:NDArray[np.float64]):
        """2^2 factorial design
        
        Args:
            arr (NDArray): 3D array
                i:Factor B
                j:Factor A
                k:Replicate
        """

        self.arr = arr
        self.main()

    def main(self):
        self.f:NDArray[np.float64] = np.sum(self.arr,axis=-1)
        self.n = len(self.arr[0,0])


    @property
    def CA(self) ->float:
        """Contrast A"""
        f= self.f
        return f[1,1]+f[0,1]-f[1,0]-f[0,0]
    
    @property
    def CB(self) ->float:
        """Contrast B"""
        f= self.f
        return f[1,1]+f[1,0]-f[0,1]-f[0,0]
    
    @property
    def CAB(self) ->float:
        """Contrast AB"""
        f= self.f
        return f[1,1]-f[0,1]-f[1,0]+f[0,0]
    @property
    def A(self):
        """Effect A"""
        return self.CA/self.n/2
    
    @property
    def B(self):
        """Effect B"""
        return self.CB/self.n/2
    
    @property
    def AB(self):
        """Effect AB"""
        return self.CAB/self.n/2
    
    @property
    def SSA(self):
        """Sum of squares A"""
        return self.CA**2/(4*self.n)
    
    @property
    def SSB(self):
        """Sum of squares B"""
        return self.CB**2/(4*self.n)

    @property
    def SSAB(self):
        """Sum of squares AB"""
        return self.CAB**2/(4*self.n)
    
    @property
    def SST(self) -> float:
        """Total sum of squares"""
        return np.sum(self.arr**2)-np.sum(self.f)**2/(4*self.n) #type:ignore
    
    @property
    def SSe(self) -> float:
        """Sum of squares error"""
        return self.SST-self.SSA-self.SSB-self.SSAB
    
    @property
    def MSe(self) -> float:
        """Mean square error"""
        return self.SSe/(4*self.n-4)
    
    @property
    def RMSE(self) -> float:
        """Root mean square error"""
        return np.sqrt(self.MSe)

    @property
    def regCoef(self) -> NDArray[np.float64]:
        """Regression Coefficients"""
        return np.array([np.mean(self.arr),self.A,self.B,self.AB])/2
    
    def printReg(self):
        print("I".ljust(10) + "A".ljust(10) + "B".ljust(10) + "AB".ljust(10))
        print(f"{self.regCoef[0]:.3f}".ljust(10) + f"{self.regCoef[1]:.3f}".ljust(10) + f"{self.regCoef[2]:.3f}".ljust(10) + f"{self.regCoef[3]:.3f}".ljust(10))

    def anova(self) :
        """ANOVA Table"""
        MS = [self.SSA,self.SSB,self.SSAB,(self.SST-self.SSA-self.SSB-self.SSAB)/(4*self.n-1)]
        F = [MS[i]/MS[3] for i in range(3)]
        return {"Source":["A","B","AB","Error","Total"],
                "DF":[1,1,1,4*self.n-4,4*self.n-1],
                "SS":[self.SSA,self.SSB,self.SSAB,self.SST-self.SSA-self.SSB-self.SSAB,self.SST],
                "MS":MS + [np.nan]*2,
                "F":F + [np.nan]*2,
                "P":[np.nan,np.nan,np.nan,np.nan,np.nan]}

    def printAnova(self):
        """Print ANOVA Table"""
        anova = self.anova()
        print("Source".rjust(16) + "DF".rjust(10) + "SS".rjust(10) + "MS".rjust(10) + "F".rjust(10) + "P".rjust(10))
        for i in range(5):
            print(anova["Source"][i].rjust(16) + f"{anova['DF'][i]:.3f}".rjust(10) + f"{anova['SS'][i]:.3f}".rjust(10) + f"{anova['MS'][i]:.3f}".rjust(10) + f"{anova['F'][i]:.3f}".rjust(10) + f"{anova['P'][i]:.3f}".rjust(10))