import sys
from typing import Generic, Literal, TypeAlias, Union, overload , ParamSpec
from typing_extensions import TypeVarTuple,Unpack
from ..typedef import *
from ..stats import freq



BaseDim = Literal["T","L","H","N","M","I","J"]

BaseDIM  = Union["Dimension[Literal['T']]", "Dimension[Literal['L']]", "Dimension[Literal['H']]", "Dimension[Literal['N']]", "Dimension[Literal['M']]", "Dimension[Literal['I']]", "Dimension[Literal['J']]","Dimension[BaseDim]"]


D = TypeVar("D",bound = Literal["T","L","H","N","M","I","J"])
D1 = TypeVar("D1",bound = Literal["T","L","H","N","M","I","J"])

RDs = TypeVar("RDs",bound=tuple[BaseDim,...])
RDs1 = TypeVar("RDs1",bound=tuple[BaseDim,...])

DsN = TypeVar("DsN",bound=tuple[BaseDIM,...])
DsD = TypeVar("DsD",bound=tuple[BaseDIM,...])
Ds1N = TypeVar("Ds1N",bound=tuple[BaseDIM,...])
Ds1D = TypeVar("Ds1D",bound=tuple[BaseDIM,...])



CompoundUnitResolvables = Union["CompoundUnit","Unit","BaseUnit"]
UnitResolvables = Union["Unit","BaseUnit"]

@overload
def resolveDim(i:"Dimension[D]")->"Dimension[D]":
    ...
@overload
def resolveDim(i:D)->"Dimension[D]":
    ...
def resolveDim(i:"Dimension[D]"|D) -> "Dimension[D]":
    if isinstance(i,Dimension):
        return Dimension(i.dim)
    elif isinstance(i,str):
        if i in baseDim:
            return Dimension(i) 
        else:raise ValueError("Not a base dimension")
    else:
        raise TypeError("Not resolvable to dimension")


@overload
def resolveCompoundDim(i:"CompoundDimension[DsN,DsD]")->"CompoundDimension[DsN,DsD]":
    ...
@overload
def resolveCompoundDim(i:"Dimension[D]")->"CompoundDimension[tuple[Dimension[D]],tuple[()]]":
    ...
def resolveCompoundDim(i:"CompoundDimension[DsN,DsD] | Dimension[D] "):
    if isinstance(i,CompoundBaseUnit):
        return CompoundDimension(i.numerator,i.denominator)  # type: ignore
    elif isinstance(i,Dimension):
        return CompoundDimension((i,),())
    if isinstance(i,CompoundDimension):
        return i
    else:
        raise TypeError("Not resolvable to compound dimension")

@overload
def resolveCompoundUnit(i:"CompoundBaseUnit[DsN,DsD]")->"CompoundBaseUnit[DsN,DsD]":
    ...
@overload
def resolveCompoundUnit(i:"BaseUnit[D]")->"CompoundUnit[tuple[Dimension[D]],tuple[()]]":
    ...
def resolveCompoundUnit(i:"CompoundBaseUnit[DsN,DsD] | BaseUnit[D]") -> "CompoundBaseUnit[DsN,DsD]|CompoundUnit[tuple[Dimension[D]],tuple[()]]":
    if isinstance(i,CompoundBaseUnit):
        return i
    elif isinstance(i,BaseUnit):
        return CompoundUnit((resolveDim(i.dim),),(),i.name,i.symbol,i.mul,i.offset)
    else:
        raise TypeError("Not resolvable to compound unit")

def resolveUnit(i:UnitResolvables)->"Unit":
    if isinstance(i,Unit):
        return i
    elif isinstance(i,BaseUnit):
        return Unit(resolveDim(i.dim),i.name,i.symbol,i.mul,i.offset)
    else:
        raise TypeError("Not resolvable to unit")

def parseSymbol(s:str) ->str:
    n,d = s.split("/")
    fn,fd = freq(n.split(".")),freq(d.split("."))
    return f"{'*'.join([f'{i}^{fn[i]}'if fn[i]>1 else i for i in fn  ])} / {'*'.join([f'{i}^{fd[i]}'if fd[i]>1 else i for i in fd  ])}"

baseDim=["T","L","M","N","I","J","H"]

class Dimension(Generic[D]):
    """
    T : time
    L : length
    M : mass
    N : mol
    I : current
    J : luminosity
    H : temp
    """
    
    dim : D

    def __repr__(self) -> str:
        return self.dim

    def __init__(self,dim:D):
        if dim not in baseDim:
            raise ValueError("Not a base dimension")
        self.dim=dim

    def __hash__(self) -> int:
        return hash(self.dim)

    def __eq__(self, o:"Dimension[D1]"):
        dim: D1=resolveDim(o).dim
        if self.dim == dim :return True
        else:return False

    def __mul__(self, o:"Dimension[D1]") -> "CompoundDimension[tuple[Dimension[D],Dimension[D1]],tuple[()]]":
        o=resolveDim(o)
        return CompoundDimension((self,o),())

    def __truediv__(self, o:"Dimension[D1]") -> "CompoundDimension[tuple[Dimension[D]],tuple[Dimension[D1]]]":
        o=resolveDim(o)
        return CompoundDimension((self,),(o,))

class CompoundDimension(Generic[DsN,DsD]):
    numerator:DsN
    denominator:DsD

    def __init__(self,num:DsN,den:DsD):
        numerator = [resolveDim(i) for i in num]
        denominator = [resolveDim(i) for i in den]

        #Remove duplicates
        fnum = freq(numerator)
        fden = freq(denominator)

        fnum_new: dict[BaseDIM,int] = {}
        fden_new: dict[BaseDIM,int] = {}
        for i in fnum:
            if i in fden:
                if fnum[i]>fden[i]:
                    fnum_new[i]=fnum[i]-fden[i]

            else:
                fnum_new[i]=fnum[i]

        for i in fden:
            if i in fnum:
                if fden[i]>fnum[i]:
                    fden_new[i]=fden[i]-fnum[i]

            else:
                fden_new[i]=fden[i]

        num_new = [i for i in fnum_new for _ in range(fnum_new[i])]
        den_new = [i for i in fden_new for _ in range(fden_new[i])]
        

        tup_numerator = tuple(num_new)
        tup_denominator = tuple(den_new)

        self.numerator = tup_numerator 
        self.denominator=tup_denominator
        # self.onEdit(True)


    def __repr__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.numerator,key=lambda x: x.dim))+tuple(sorted(self.denominator,key=lambda x: x.dim)))

    def __eq__(self, o:"CompoundDimension[Ds1N,Ds1D]") -> bool:
        o=resolveCompoundDim(o)
        return sorted(self.numerator,key=lambda x: x.dim)==sorted(o.numerator,key=lambda x: x.dim) and sorted(self.denominator,key=lambda x: x.dim)==sorted(o.denominator,key=lambda x: x.dim)

    resolve = resolveCompoundDim

    # def onEdit(self,callback=False):
    #     num = [*self.numerator]
    #     den = [*self.denominator]

    #     for i in num:
    #         for j in den:
    #             if i==j:
    #                 num.remove(i)
    #                 den.remove(j)
    #                 break
    #     for i in den:
    #         for j in num:
    #             if i==j:
    #                 num.remove(i)
    #                 den.remove(j)
    #                 break

    #     self.numerator = tuple(num)
    #     self.denominator = tuple(den)

    #     if callback:
    #         self.onEdit()
    #     return self

    def __mul__(self, o:"CompoundDimension[DsN,DsD] | Dimension[D] "):
        new=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+new.numerator,self.denominator+new.denominator)  

    def __rmul__(self, o:"CompoundDimension[DsN,DsD] | Dimension[D] "):
        new=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+new.numerator,self.denominator+new.denominator)  

    def __truediv__(self, o:"CompoundDimension[DsN,DsD] | Dimension[D] "):
        new=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+new.denominator,self.denominator+new.numerator)  

    @overload
    def __rtruediv__(self, o:"CompoundDimension[DsN,DsD] | Dimension[D]") -> "CompoundDimension":
        ...
    @overload
    def __rtruediv__(self, o:Literal[1]) -> "CompoundDimension[DsD,DsN]":
        ...
    def __rtruediv__(self, o:"CompoundDimension[DsN,DsD] | Dimension[D] |Literal[1]") -> "CompoundDimension":
        if o ==1:
            return CompoundDimension(self.denominator,self.numerator) 
        else:
            new=resolveCompoundDim(o)
            return CompoundDimension(self.numerator+new.denominator,self.denominator+new.numerator)

class BaseUnit(Dimension[D]):
    name:str
    mul:number = 1
    symbol:str
    offset:number = 0.
    dim:D

    def __init__(self,dim:Dimension[D]|D,name:str,symbol:str,mul:number = 1,offset:number = 0.):
        self.dim = resolveDim(dim).dim
        self.name=name
        self.mul=mul
        self.symbol=symbol
        self.offset=offset

    def __repr__(self) -> str:
        default = DefaultUnit[Dimension(self.dim)]
        return f'{self.dim}: {self.name} = {self.mul/default.mul} {default.symbol} {self.offset:+.4}'

    def __mul__(self, o: "BaseUnit[D1]") -> "CompoundUnit[tuple[Dimension[D], Dimension[D1]], tuple[()]]":
        dim=resolveDim(o)
        o = resolveUnit(o)
        ret = resolveDim(self.dim)*dim
        offset = (self.offset*self.mul + o.offset*o.mul)/(self.mul*o.mul)
        return CompoundUnit(ret.numerator,ret.denominator,self.name + "*" + o.name,self.symbol+"."+o.symbol,self.mul*o.mul,offset)  # type: ignore

    def __truediv__(self, o: "BaseUnit[D1]") -> "CompoundUnit[tuple[Dimension[D]], tuple[Dimension[D1]]]":
        dim=resolveDim(o)
        o = resolveUnit(o)
        ret = resolveDim(self.dim)/dim
        offset = (self.offset*self.mul - o.offset*o.mul)/(self.mul*o.mul)
        return CompoundUnit(ret.numerator,ret.denominator,self.name + "/" + o.name,self.symbol+"/"+o.symbol,self.mul/o.mul,offset)  # type: ignore

    def __rmul__(self, o:number) -> "Value[tuple[Dimension[D]],tuple[()]]":
        return Value(o,self)
    
    def __rtruediv__(self, o:number) -> "Value":
        dim = resolveDim(self.dim)
        return Value(o,CompoundUnit([],[dim],"/"+self.name,"/"+self.symbol,1/self.mul,-self.offset/self.mul)) 
    
    def __pow__(self,o:int) :
        return CompoundUnit((self,)*o,(),self.name+f"^{o}",self.symbol+f"^{o}",self.mul**o,self.offset*o)

class Unit(BaseUnit[D]):
    mul:number


class CompoundBaseUnit(BaseUnit,CompoundDimension[DsN,DsD]):
    num:DsN
    den:DsD

    def __init__(self,num:DsN,den:DsD,name:str,symbol:str,mul:number=1.,offset:number=0.):
        numerator = [resolveDim(i) for i in num]
        denominator = [resolveDim(i) for i in den]

        #Remove duplicates
        fnum = freq(numerator)
        fden = freq(denominator)

        fnum_new: dict[BaseDIM,int] = {}
        fden_new: dict[BaseDIM,int] = {}
        for i in fnum:
            if i in fden:
                if fnum[i]>fden[i]:
                    fnum_new[i]=fnum[i]-fden[i]

            else:
                fnum_new[i]=fnum[i]

        for i in fden:
            if i in fnum:
                if fden[i]>fnum[i]:
                    fden_new[i]=fden[i]-fnum[i]

            else:
                fden_new[i]=fden[i]

        num_new = [i for i in fnum_new for _ in range(fnum_new[i])]
        den_new = [i for i in fden_new for _ in range(fden_new[i])]

        tup_numerator = tuple(num_new)
        tup_denominator = tuple(den_new)

        self.numerator = tup_numerator 
        self.denominator=tup_denominator
        self.name=name
        self.mul=mul
        self.symbol=symbol
        self.offset=offset
        self.baseSymbol = f'{".".join(DefaultUnit[i].symbol for i in self.numerator)}/{".".join(DefaultUnit[i].symbol for i in self.denominator)}'

    def __repr__(self) -> str:
        return f"{[i.dim for i in self.numerator]}/{[i.dim for i in self.denominator]} : {self.name} = {self.mul} {parseSymbol(self.baseSymbol)} {self.offset:+.4}"

    def __mul__(self, o: "CompoundUnit[Ds1N,Ds1D]|BaseUnit[D1]") :
        o=resolveCompoundUnit(o)
        return CompoundUnit((*self.numerator,*o.numerator),(*self.denominator,*o.denominator),self.name + "*" + o.name,self.symbol+"."+o.symbol,self.mul*o.mul,self.offset+o.offset)  # type: ignore

    def __truediv__(self, o: "CompoundUnit[Ds1N,Ds1D]|BaseUnit[D1]"):
        o=resolveCompoundUnit(o)
        return CompoundUnit((*self.numerator,*o.denominator),(*self.denominator,*o.numerator),self.name + "/" + o.name,self.symbol+"/"+o.symbol,self.mul/o.mul,self.offset-o.offset)  # type: ignore

    def __pow__(self, o: int) :
        return CompoundUnit(self.numerator*o,self.denominator*o,self.name+f"^{o}",self.symbol+f"^{o}",self.mul**o,self.offset*o) 

    def sameDim(self,o:"CompoundBaseUnit")->bool:
        return sorted(self.numerator,key = lambda x:x.dim)==sorted(o.numerator,key = lambda x:x.dim) and sorted(self.denominator,key = lambda x:x.dim)==sorted(o.denominator,key = lambda x:x.dim)

    def ratio(self,o:"CompoundBaseUnit")->number:
        """Ratio of 1 self to n other"""
        if self.sameDim(o):
            return self.mul/o.mul
        else:
            raise Exception("Cannot find ratio of units with different dimensions")

    def base(self)->"CompoundBaseUnit[DsN,DsD]":
        dim=resolveCompoundDim(self)
        if dim in DefaultCompoundUnit:
            return DefaultCompoundUnit[dim]
        else:
            raise NotImplementedError("Not implemented dynamic base unit")

    def __eq__(self, o: "CompoundBaseUnit"):
        return sorted(self.numerator,key = lambda x:x.dim)==sorted(o.numerator,key = lambda x:x.dim) and sorted(self.denominator,key = lambda x:x.dim)==sorted(o.denominator,key = lambda x:x.dim) and self.mul==o.mul and self.offset==o.offset

    @overload
    def __rmul__(self, o: number) -> "Value[DsN,DsD]":
        ...
    @overload
    def __rmul__(self, o: "CompoundBaseUnit[Ds1N,Ds1D]"):
        ...
    def __rmul__(self, o: "CompoundBaseUnit[Ds1N,Ds1D]|number") :
        if isinstance(o,number):
            return Value(o,self)
        else:
            o=resolveCompoundUnit(o)
            return CompoundUnit(self.numerator+o.numerator,self.denominator+o.denominator,self.name + "*" + o.name,self.symbol+"."+o.symbol,self.mul,self.offset) 

class CompoundUnit(CompoundBaseUnit[DsN,DsD]):
    pass

class prefix:
    def __init__(self,name:str,symbol:str,mul:number):
        self.name=name
        self.symbol=symbol
        self.mul=mul
    def __repr__(self)->str:
        return f"{self.name} : {self.symbol} = 10^{self.mul}"

    def __mul__(self, o: CompoundUnitResolvables) -> "CompoundUnit":
        o=resolveCompoundUnit(o)
        return CompoundUnit(o.numerator,o.denominator,self.name + o.name,self.symbol+o.symbol,(10**self.mul)*o.mul,o.offset/10**o.mul) 

    def __rmul__(self, o: number) -> number:
            return o*10**self.mul

class Value(Generic[DsN,DsD]):
    unit: CompoundUnit[DsN,DsD]
    value:number

    def __init__(self,value:number,unit:CompoundBaseUnit[DsN,DsD]|BaseUnit[D]):
        self.value=value
        resunit = resolveCompoundUnit(unit)
        self.unit=resunit
        self.__doc__ = str([self.unit.numerator,self.unit.denominator])

    def __repr__(self) -> str:
        return f"{self.value} {self.unit.symbol}"

    @overload
    def __mul__(self, o: "Value[Ds1N,Ds1D]") -> "Value[tuple[Unpack[DsN],Unpack[Ds1N]],tuple[Unpack[DsD],Unpack[Ds1D]]]":
        ...
    @overload
    def __mul__(self, o: CompoundBaseUnit[Ds1N,Ds1D]) -> "Value[tuple[Unpack[DsN],Unpack[Ds1N]],tuple[Unpack[DsD],Unpack[Ds1D]]]":
        ...
    @overload
    def __mul__(self, o: BaseUnit[D1]) -> "Value[tuple[Unpack[DsN],Dimension[D1]],DsD]":
        ...
    @overload
    def __mul__(self, o: number) -> "Value[DsN,DsD]":
        ...
    def __mul__(self, o: "Value[Ds1N,Ds1D]" | CompoundBaseUnit[Ds1N,Ds1D]|BaseUnit[D1]|number) :
        if isinstance(o,Value):
            return Value(self.value*o.value,self.unit*o.unit)
        elif isinstance(o,number):
            return Value(self.value*o,self.unit)
        elif isinstance(o,BaseUnit):
            return Value(self.value,resolveCompoundUnit(o)*self.unit)

    def __rmul__(self, o: "Value[Ds1N,Ds1D]" |  CompoundBaseUnit[Ds1N,Ds1D]|BaseUnit[D1]|number):
        if isinstance(o,Value):
            return Value(self.value*o.value,self.unit*o.unit)
        elif isinstance(o,number):
            return Value(self.value*o,self.unit)
        elif isinstance(o,BaseUnit):
            return Value(self.value,resolveCompoundUnit(o)*self.unit)

    def __truediv__(self, o: "Value[Ds1N,Ds1D]" | CompoundBaseUnit[Ds1N,Ds1D]|BaseUnit[D1]|number):
        if isinstance(o,Value):
            return Value(self.value/o.value,self.unit/o.unit)
        elif isinstance(o,number):
            return Value(self.value/o,self.unit)
        elif isinstance(o,BaseUnit):
            return Value(self.value,self.unit/resolveCompoundUnit(o))
        
    def __rtruediv__(self, o: "Value[Ds1N,Ds1D]" | CompoundBaseUnit[Ds1N,Ds1D]|BaseUnit[D1]|number):
        if isinstance(o,Value):
            return Value(o.value/self.value,o.unit/self.unit)
        elif isinstance(o,number):
            return o/self
        elif isinstance(o,BaseUnit):
            return Value(self.value,resolveCompoundUnit(o)/self.unit)

    def __add__(self, o: "Value[DsN,DsD]") -> "Value[DsN,DsD]":
        if self.unit == o.unit:
            return Value(self.value+o.value,self.unit)
        elif self.unit.sameDim(o.unit):
            return Value(self.value + ((o.value-o.unit.offset)*o.unit.mul/self.unit.mul +self.unit.offset),self.unit)
        else:
            raise Exception("Unit mismatch")

    def __sub__(self, o: "Value[DsN,DsD]") -> "Value[DsN,DsD]":
        if self.unit == o.unit:
            return Value(self.value-o.value,self.unit)
        elif self.unit.sameDim(o.unit):
            return Value(self.value - ((o.value-o.unit.offset)*o.unit.mul/self.unit.mul +self.unit.offset),self.unit)
        else:
            raise Exception("Unit mismatch")

    def __neg__(self) -> "Value[DsN,DsD]":
        return Value(-self.value,self.unit)
    
    def __pow__(self, o: int) :
        return Value(self.value**o,self.unit**o)

    def inUnit(self,unit:CompoundUnitResolvables)->"Value":
        unit=resolveCompoundUnit(unit)
        # if self.unit == unit:
        #     return self
        if self.unit.sameDim(unit):
            return Value((self.value-self.unit.offset)*self.unit.mul/unit.mul + unit.offset,unit)
        else:
            raise Exception("Unit mismatch")

    @property
    def inBase(self)->"Value":
        return self.inUnit(self.unit.base())

    def __eq__(self, o: "Value") -> bool:
        if self.unit == o.unit:
            return self.value==o.value
        elif self.unit.sameDim(o.unit):
            return self.value == ((o.value-o.unit.offset)*o.unit.mul/self.unit.mul +self.unit.offset)
        else:
            raise Exception("Unit mismatch")

    to = inUnit
    toBase = inBase

#Sync with unitdef.py

#Sync with DimeAndUnit.py

TIME = Dimension("T")
LENGTH = Dimension("L")
MASS = Dimension("M")
TEMP = Dimension("H")
MOL = Dimension("N")
CURRENT = Dimension("I")
LUMINOSITY = Dimension("J")

sec = BaseUnit("T","Second","s")
meter=BaseUnit("L","Meter","m")
kilogram = BaseUnit("M","gram","kg")
mol=BaseUnit("N","Mole","mol")
kelvin = BaseUnit("H","Kelvin","K")
amp = BaseUnit("I","Ampere","A")
cd = BaseUnit("J","Candela","cd")


DefaultUnit: dict[BaseDIM,BaseUnit]  = {
    Dimension("T"):sec,
    Dimension("L"):meter,
    Dimension("M"):kilogram,
    Dimension("N"):mol,
    Dimension("H"):kelvin,
    Dimension("I"):amp,
    Dimension("J"):cd
}
#LENGTH
foot = Unit("L","foot","ft",0.3048)
inch = Unit("L","inch","in",0.0254)
miles = Unit("L","miles","mi",1609.344)
yard = Unit("L","yard","yd",0.9144)
angstrom = Unit("L","angstrom","A",1e-10)

#MASS
lbm = pound = Unit("M","pound","lbm",.45359237)
ounce = Unit("M","ounce","oz",.028349523125)
gram = Unit("M","gram","g",.001)
ton = Unit("M","metricTon","ton",1000)

#TIME
minutes = Unit("T","minutes","min",60)
hour=Unit("T","hour","hr",3600)
day=Unit("T","day","d",86400)
week=Unit("T","week","wk",604800)
year=Unit("T","year","yr",31536000)
month = Unit("T","month","mo",2628000)

#TEMP
celsius = Unit("H","celsius","C",1,-273.15)
fahrenheit = Unit("H","fahrenheit","F",1/1.8,-459.67)
rankine = Unit("H","rankine","R",1/1.8)

#Prefix
deca = prefix("deca","da",1)
hecto = prefix("hecto","h",2)
kilo = prefix("Kilo","k",3)
mega = prefix("Mega","M",6)
giga = prefix("Giga","G",9)
tera = prefix("Tera","T",12)
peta = prefix("Peta","P",15)
exa = prefix("Exa","E",18)
zetta = prefix("Zetta","Z",21)
yotta = prefix("Yotta","Y",24)

deci = prefix("deci","d",-1)
centi = prefix("centi","c",-2)
milli = prefix("milli","m",-3)
micro = prefix("micro","u",-6)
nano = prefix("nano","n",-9)
pico = prefix("pico","p",-12)
femto = prefix("femto","f",-15)
atto = prefix("atto","a",-18)
zepto = prefix("zepto","z",-21)
yocto = prefix("yocto","y",-24)
#Compound Units

DimLes = CompoundUnit((),(),"","",1)

#Speed
meterPerSecond = CompoundUnit((meter,),(sec,),"meter/sec","m/s",1)
kilometerPerHour = CompoundUnit((meter,),(hour,),"kilometer/hour","km/h",1/3.6)
milesPerHour = CompoundUnit((miles,),(hour,),"miles/hour","mph",1/2.237)

#Acceleration
meterPerSecondSquared = CompoundUnit((meter,),(sec,sec),"meter/sec^2","m/s.s",1)
kilometerPerHourSquared = CompoundUnit((meter,),(hour,hour),"kilometer/hour^2","km/hr.hr",1/1.944**2)

#Area
squareMeter = CompoundUnit((meter,meter),(),"square meter","m.m",1)
squareKilometer = CompoundUnit((meter,meter),(),"square kilometer","m.km",1e6)
squareMiles = CompoundUnit((miles,miles),(),"square miles","mi.mi",2.58999e6)
squareYard = CompoundUnit((yard,yard),(),"square yard","yd.yd",0.836127)
squareFoot = CompoundUnit((foot,foot),(),"square foot","ft.ft",0.09290304)
squareInch = CompoundUnit((inch,inch),(),"square inch","in.in",0.00064516)
acre = CompoundUnit((meter,meter),(),"acre","acre",4046.8564224)
hectre = CompoundUnit((meter,meter),(),"hectre","hectre",1e4)
วา = CompoundUnit((meter,meter),(),"วา","วา",4)
ไร่ = CompoundUnit((meter,meter),(),"ไร่","ไร่",1600)
งาน = CompoundUnit((meter,meter),(),"งาน","งาน",400)
darcy = CompoundUnit((meter,meter),(),"darcy","darcy",9.869233e-13)

#Volume
liter = CompoundUnit((meter,meter,meter),(),"liter","l",1e-3)
cubicMeter = CompoundUnit((meter,meter,meter),(),"cubic meter","m.m.m",1)
gallon = CompoundUnit((meter,meter,meter),(),"gallon","gal",0.0037854118)
cubicFoot = CompoundUnit((foot,foot,foot),(),"cubic foot","ft.ft.ft",0.028316846592)
cubicInch = CompoundUnit((inch,inch,inch),(),"cubic inch","in.in.in",0.000016387064)
fluidOunce = CompoundUnit((inch,inch,inch),(),"fluid ounce","fl.oz",0.0000295735295625)
cup = CompoundUnit((inch,inch,inch),(),"cup","cup",0.0002365882365)
pint = CompoundUnit((inch,inch,inch),(),"pint","pt",0.000473176473)
quart = CompoundUnit((inch,inch,inch),(),"quart","qt",0.000946352946)
cc = CompoundUnit((inch,inch,inch),(),"CC","CC",0.001)

#Density
kilogramPerCubicMeter = CompoundUnit((kilogram,),(meter,meter,meter),"kilogram/cubic meter","kg/m.m.m",1)
gramPerCubicMeter = CompoundUnit((gram,),(meter,meter,meter),"gram/cubic meter","g/m.m.m",1e-3)
poundPerCubicFoot = CompoundUnit((pound,),(foot,foot,foot),"pound/cubic foot","lbm/ft.ft.ft",16.01846337)
poundPerCubicInch = CompoundUnit((pound,),(inch,inch,inch),"pound/cubic inch","lbm/in.in.in",27679.9047)
gramPerCc = CompoundUnit((gram,),(inch,inch,inch),"gram/cc","g/cc",1000)
kilogramPerLiter = CompoundUnit((kilogram,),(meter,meter,meter),"kilogram/liter","kg/l",1e3)
gramPerLiter = CompoundUnit((gram,),(meter,meter,meter),"gram/liter","g/l",1)

#Force
newton = CompoundUnit((kilogram,meter),(sec,sec),"newton","N",1)
dyne = CompoundUnit((kilogram,meter),(sec,sec),"dyne","dyn",1e-5)
poundForce = CompoundUnit((pound,foot),(sec,sec),"pound force","lbf",4.4482216152605)

#Pressure
pascal = CompoundUnit((kilogram,),(meter,sec,sec),"pascal","Pa",1)
bar = CompoundUnit((kilogram,),(meter,sec,sec),"bar","bar",1e5)
atm = CompoundUnit((kilogram,),(meter,sec,sec),"atmosphere","atm",101325)
psi = CompoundUnit((kilogram,),(meter,sec,sec),"pound/square inch","psi",6894.757293168)
mmHg = CompoundUnit((kilogram,),(meter,sec,sec),"millimeter of mercury","mmHg",133.322)
torr = CompoundUnit((kilogram,),(meter,sec,sec),"torr","torr",133.322)

#Energy
joule = CompoundUnit((kilogram,meter,meter),(sec,sec),"joule","J",1)
eV = CompoundUnit((kilogram,meter,meter),(sec,sec),"electron volt","eV",1.602176634e-19)
kWh = CompoundUnit((kilogram,meter,meter),(sec,sec),"kilowatt hour","kWh",3600000)
calorie = CompoundUnit((kilogram,meter,meter),(sec,sec),"calorie","cal",4.1868)
btu = CompoundUnit((kilogram,meter,meter),(sec,sec),"British thermal unit","btu",1055.05585262)

#Energy Density
joulePerKilogram = CompoundUnit((meter,meter),(sec,sec),"joule/kilogram","J/kg",1)
btuPerPound = CompoundUnit((foot,foot),(sec,sec),"British thermal unit/pound","btu/lbm",2326)
caloriePerGram = CompoundUnit((meter,meter),(sec,sec),"calorie/gram","cal/g",4186.8)

#Power
watt = CompoundUnit((kilogram,meter,meter),(sec,sec,sec),"watt","W",1)
horsepower = CompoundUnit((kilogram,meter,meter),(sec,sec,sec),"horsepower","hp",745.699871582270)

#Charge
coulomb = CompoundUnit((amp,sec),(),"coulomb","C",1)
faraday = CompoundUnit((amp,sec),(),"faraday","F",96485.3399)
electron = CompoundUnit((amp,sec),(),"electron charge","e",1.602176634e-19)

#Electric Potential
volt = CompoundUnit((kilogram,meter,meter),(sec,sec,sec,amp),"volt","V",1)

#Electric Field
voltPerMeter = CompoundUnit((kilogram,meter),(sec,sec,sec,amp),"volt/meter","V/m",1)

#Chemical.14
amu = CompoundUnit((kilogram,),(),"atomic mass unit","amu",1.66053906660e-27)
gpm = CompoundUnit((kilogram,),(mol,),"gram per mole","gpm",1e-3)

#Viscosity
poise = CompoundUnit((kilogram,),(meter,sec),"poise","P",0.1)
pascalSecond = CompoundUnit((kilogram,),(meter,sec),"pascal second","Pa.s",1)
centipoise = CompoundUnit((kilogram,),(meter,sec),"centipoise","cP",1e-3)
micropoise = CompoundUnit((kilogram,),(meter,sec),"micropoise","uP",1e-7)
millipoise = CompoundUnit((kilogram,),(meter,sec),"millipoise","mP",1e-4)

#Mass Diffusivity
sqfPs = CompoundUnit((meter,meter),(sec,),"square foot per second","ft.ft/s",0.09290304)
sqmPs = CompoundUnit((meter,meter),(sec,),"square meter per second","m.m/s",1)
sqcmPs = CompoundUnit((meter,meter),(sec,),"square centimeter per second","cm.cm/s",1e-4)

DefaultCompoundUnit = {
    Dimension("T"):sec,
    Dimension("L"):meter,
    Dimension("M"):kilogram,
    Dimension("N"):mol,
    Dimension("H"):kelvin,
    Dimension("I"):amp,
    Dimension("J"):cd,
    CompoundDimension((),()):DimLes,
    CompoundDimension((LENGTH,),(TIME,)):meterPerSecond, #Speed
    CompoundDimension((LENGTH,),(TIME,TIME)):meterPerSecondSquared,#Acceleration
    CompoundDimension((LENGTH,LENGTH),()):squareMeter,#Area
    CompoundDimension((LENGTH,LENGTH,LENGTH),()):cubicMeter,#Volume
    CompoundDimension((MASS,),(LENGTH,LENGTH,LENGTH)):gramPerCubicMeter,#Density
    CompoundDimension((LENGTH,MASS),(TIME,TIME)):newton,#Force
    CompoundDimension((MASS,),(LENGTH,TIME,TIME)):pascal,#Pressure
    CompoundDimension((MASS,LENGTH,LENGTH),(TIME,TIME)):joule,#Energy
    CompoundDimension((MASS,LENGTH,LENGTH),(TIME,TIME,TIME)):watt,#Power
    CompoundDimension((CURRENT,TIME),()):coulomb,#Charge
    CompoundDimension((MASS,LENGTH,LENGTH),(TIME,TIME,TIME,CURRENT)):volt,#Electric Potential
    CompoundDimension((MASS,LENGTH),(TIME,TIME,TIME,CURRENT)):voltPerMeter,#Electric Field
    CompoundDimension((MASS,),(MOL,)):amu,#Chemical
    CompoundDimension((LENGTH,LENGTH),(TIME,)):sqmPs,#Mass Diffusivity
}