from typing import Literal, Union
from ..typedef import *

BaseDim=Literal["T","L","M","N","I","J","H"]
DimensionResolvables = Union["Dimension","BaseUnit","Unit",str]
CompoundDimensionResolvables = Union["CompoundDimension","CompoundUnit",DimensionResolvables,str]
CompoundUnitResolvables = Union["CompoundUnit","Unit"]
UnitResolvables = Union["Unit","BaseUnit"]

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
        return CompoundDimension([resolveDim(i)],[])
    elif isinstance(i,Dimension):
        return CompoundDimension([i],[])
    else:
        raise TypeError("Not resolvable to compound dimension")

def resolveCompoundUnit(i:CompoundUnitResolvables)->"CompoundUnit":
    if isinstance(i,CompoundUnit):
        return i
    elif isinstance(i,BaseUnit):
        return CompoundUnit([resolveDim(i.dim)],[],i.name,i.symbol,i.mul,i.offset)
    else:
        raise TypeError("Not resolvable to compound unit")

def resolveUnit(i:UnitResolvables)->"Unit":
    if isinstance(i,Unit):
        return i
    elif isinstance(i,BaseUnit):
        return Unit(resolveDim(i.dim),i.name,i.symbol,i.mul,i.offset)
    else:
        raise TypeError("Not resolvable to unit")

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

    @staticmethod
    def resolve(i:CompoundDimensionResolvables)->"CompoundDimension":
        return resolveCompoundDim(i)

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

    # def __rmul__(self, o:CompoundDimensionResolvables) -> "CompoundDimension":
    #     o=resolveCompoundDim(o)
    #     return CompoundDimension(self.numerator+o.numerator,self.denominator+o.denominator)  # type: ignore

    def __truediv__(self, o:CompoundDimensionResolvables) -> "CompoundDimension":
        o=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+o.denominator,self.denominator+o.numerator)  # type: ignore

class BaseUnit(Dimension):
    name:str
    mul:number = 1
    symbol:str
    offset:number = 0.

    def __init__(self,dim:DimensionResolvables,name:str,symbol:str,mul:number = 1,offset:number = 0.):
        self.dim = resolveDim(dim).dim
        self.name=name
        self.mul=mul
        self.symbol=symbol
        self.offset=offset

    def __repr__(self) -> str:
        default = DefaultUnit[resolveDim(self.dim)]
        return f'{self.dim}: {self.name} = {self.mul/default.mul} {default.symbol} {self.offset:+.4}'

    def __mul__(self, o: UnitResolvables) -> "CompoundUnit":
        res=resolveDim(o)
        o = resolveUnit(o)
        ret = CompoundDimension.resolve(resolveDim(self.dim)*res)
        return CompoundUnit(ret.numerator,ret.denominator,self.name + "*" + o.name,self.symbol,self.mul*o.mul,self.offset+o.offset)


class Unit(BaseUnit):
    mul:number

class CompoundBaseUnit(BaseUnit,CompoundDimension):
    def __init__(self,num:list[Dimension],den:list[Dimension],name:str,symbol:str,mul:number,offset:number):
        self.numerator=num
        self.denominator=den
        self.name=name
        self.mul=mul
        self.symbol=symbol
        self.offset=offset



class CompoundUnit(CompoundBaseUnit):
    pass





sec = BaseUnit("T","Second","s")
meter=BaseUnit("L","Meter","m")
kilogram = BaseUnit("M","Kilogram","g",1000)
mol=BaseUnit("N","mol","mol")
kelvin = BaseUnit("H","Kelvin","K")
amp = BaseUnit("I","Ampere","A")
cd = BaseUnit("J","Candela","cd")

DefaultUnit = {
    Dimension("T"):sec,
    Dimension("L"):meter,
    Dimension("M"):kilogram,
    Dimension("N"):mol,
    Dimension("H"):kelvin,
    Dimension("I"):amp,
    Dimension("J"):cd
}

foot = Unit("L","foot","ft",0.3048)
inch = Unit("L","inch","in",0.0254)
pound = Unit("M","pound","lbm",0.45359237)
ounce = Unit("M","ounce","oz",0.028349523125)
gram = Unit("M","gram","g",1)
minutes = Unit("T","minutes","min",60)
hour=Unit("T","hour","hr",3600)
day=Unit("T","day","d",86400)
week=Unit("T","week","wk",604800)
year=Unit("T","year","yr",31536000)
month = Unit("T","month","mo",2628000)
celsius = Unit("H","celsius","C",1,-273.15)
fahrenheit = Unit("H","fahrenheit","F",1.8,-459.67)
rankine = Unit("H","rankine","R",1.8)