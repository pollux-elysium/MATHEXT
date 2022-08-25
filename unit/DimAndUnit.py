from typing import Literal, Union
from ..typedef import *

BaseDim=Literal["T","L","M","N","I","J","H"]
DimensionResolvables = Union["Dimension","BaseUnit",str]
CompoundDimensionResolvables = Union["CompoundDimension","CompoundUnit",str]
CompoundUnitResolvables = Union["CompoundUnit","Unit",str]

def resolveDim(i:DimensionResolvables)->"Dimension":
    if isinstance(i,Dimension):
        return Dimension(i.dim)
    elif isinstance(i,str):
        if i in baseDim:
            return Dimension(i) # type: ignore
        else:raise ValueError("Not a base dimension")
    elif isinstance(i,BaseUnit):
        return Dimension(i.dim)
    else:
        raise TypeError("Not resolvable to dimension")
        
def resolveCompoundDim(i:CompoundDimensionResolvables)->"CompoundDimension":
    if isinstance(i,CompoundDimension):
        return i
    elif isinstance(i,str):
        num,den = i.split("/")
        return CompoundDimension(
            [resolveDim(j) for j in num if j in baseDim],
            [resolveDim(j) for j in den if j in baseDim]
        )
    elif isinstance(i,BaseUnit):
        return CompoundDimension(i.num,i.den)
    else:
        raise TypeError("Not resolvable to compound dimension")

baseDim=["T","L","M","N","I","J","H"]

class Dimension:
    """
    T : time
    L : length
    M : mass
    N : mol
    I : current
    J : luminosity
    H : temp
    """
    
    dim : BaseDim

    def __repr__(self) -> str:
        return self.dim

    def __init__(self,dim:BaseDim):
        if dim not in baseDim:
            raise ValueError("Not a base dimension")
        self.dim=dim

    def __hash__(self) -> int:
        return hash(self.dim)

    def __eq__(self, o:DimensionResolvables):
        o=resolveDim(o).dim
        if self.dim == o :return True
        else:return False

    def __mul__(self, o:DimensionResolvables) -> "CompoundDimension":
        o=resolveDim(o)
        return CompoundDimension([self,o],[])

    def __truediv__(self, o:DimensionResolvables) -> "CompoundDimension":
        o=resolveDim(o)
        return CompoundDimension([self],[o])

class CompoundDimension:
    numerator:list[Dimension]
    denominator:list[Dimension]

    def __init__(self,num:list[DimensionResolvables],den:list[DimensionResolvables]):
        self.numerator=list(map(resolveDim,num))
        self.denominator=list(map(resolveDim,den))
        self.onEdit()

    def __repr__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def onEdit(self):
        for i in self.numerator:
            for j in self.denominator:
                if i==j:
                    self.numerator.remove(i)
                    self.denominator.remove(j)
        for i in self.denominator:
            for j in self.numerator:
                if i==j:
                    self.numerator.remove(i)
                    self.denominator.remove(j)
        return

    def __mul__(self, o:CompoundDimensionResolvables) -> "CompoundDimension":
        o=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+o.numerator,self.denominator+o.denominator)  # type: ignore

    def __truediv__(self, o:CompoundDimensionResolvables) -> "CompoundDimension":
        o=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+o.denominator,self.denominator+o.numerator)  # type: ignore

class BaseUnit(Dimension):
    name:str
    mul:number = 1
    symbol:str

    def __init__(self,dim:DimensionResolvables,name:str,symbol:str,mul:number = 1):
        self.dim = resolveDim(dim).dim
        self.name=name
        self.mul=mul
        self.symbol=symbol

class Unit(BaseUnit):
    mul:number

class CompoundBaseUnit(BaseUnit,CompoundDimension):
    def __init__(self,num,den,name,symbol,mul):
        self.numerator=num
        self.denominator=den
        self.name=name
        self.mul=mul
        self.symbol=symbol

class CompoundUnit(CompoundBaseUnit):
    pass
