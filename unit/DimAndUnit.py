import sys
from typing import Literal, Union, overload
from ..typedef import *
from ..stats import freq

BaseDim=Literal["T","L","M","N","I","J","H"]
DimensionResolvables = Union["Dimension","BaseUnit","Unit",str]
CompoundDimensionResolvables = Union["CompoundDimension","CompoundUnit","CompoundBaseUnit",DimensionResolvables,str]
CompoundUnitResolvables = Union["CompoundUnit","Unit","BaseUnit"]
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
    if isinstance(i,str):
        num,den = i.split("/")
        return CompoundDimension(
            [resolveDim(j) for j in num if j in baseDim],
            [resolveDim(j) for j in den if j in baseDim]
        )
    elif isinstance(i,CompoundBaseUnit):
        return CompoundDimension(i.numerator,i.denominator)  # type: ignore
    elif isinstance(i,BaseUnit):
        return CompoundDimension([resolveDim(i)],[])
    elif isinstance(i,Dimension):
        return CompoundDimension([i],[])
    if isinstance(i,CompoundDimension):
        return i
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

def parseSymbol(s:str) ->str:
    n,d = s.split("/")
    fn,fd = freq(n.split(".")),freq(d.split("."))
    return f"{'*'.join([f'{i}^{fn[i]}'if fn[i]>1 else i for i in fn  ])} / {'*'.join([f'{i}^{fd[i]}'if fd[i]>1 else i for i in fd  ])}"

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
        self.onEdit(True)

    def __repr__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.numerator,key=lambda x: x.dim))+tuple(sorted(self.denominator,key=lambda x: x.dim)))

    def __eq__(self, o:CompoundDimensionResolvables) -> bool:
        o=resolveCompoundDim(o)
        return sorted(self.numerator,key=lambda x: x.dim)==sorted(o.numerator,key=lambda x: x.dim) and sorted(self.denominator,key=lambda x: x.dim)==sorted(o.denominator,key=lambda x: x.dim)

    @staticmethod
    def resolve(i:CompoundDimensionResolvables)->"CompoundDimension":
        return resolveCompoundDim(i)

    def onEdit(self,callback=False):
        for i in self.numerator:
            for j in self.denominator:
                if i==j:
                    self.numerator.remove(i)
                    self.denominator.remove(j)
                    break
        for i in self.denominator:
            for j in self.numerator:
                if i==j:
                    self.numerator.remove(i)
                    self.denominator.remove(j)
                    break

        if callback:
            self.onEdit()
        return self

    def __mul__(self, o:CompoundDimensionResolvables) -> "CompoundDimension":
        o=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+o.numerator,self.denominator+o.denominator)  # type: ignore

    def __rmul__(self, o:CompoundDimensionResolvables) -> "CompoundDimension":
        o=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+o.numerator,self.denominator+o.denominator)  # type: ignore

    def __truediv__(self, o:CompoundDimensionResolvables) -> "CompoundDimension":
        o=resolveCompoundDim(o)
        return CompoundDimension(self.numerator+o.denominator,self.denominator+o.numerator)  # type: ignore

    def __rtruediv__(self, o:CompoundDimensionResolvables|Literal[1]) -> "CompoundDimension":
        if o ==1:
            return CompoundDimension(self.denominator,self.numerator) # type: ignore
        else:
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
        dim=resolveDim(o)
        o = resolveUnit(o)
        ret = resolveDim(self.dim)*dim
        offset = (self.offset*self.mul + o.offset*o.mul)/(self.mul*o.mul)
        return CompoundUnit(ret.numerator,ret.denominator,self.name + "*" + o.name,self.symbol+"."+o.symbol,self.mul*o.mul,offset)  # type: ignore

    def __truediv__(self, o: UnitResolvables) -> "CompoundUnit":
        dim=resolveDim(o)
        o = resolveUnit(o)
        ret = resolveDim(self.dim)/dim
        offset = (self.offset*self.mul - o.offset*o.mul)/(self.mul*o.mul)
        return CompoundUnit(ret.numerator,ret.denominator,self.name + "/" + o.name,self.symbol+"/"+o.symbol,self.mul/o.mul,offset)  # type: ignore

    def __rmul__(self, o:number) -> "Value":
        return Value(o,self)
    
    def __rtruediv__(self, o:number) -> "Value":
        dim = resolveDim(self.dim)
        return Value(o,CompoundUnit([],[dim],"/"+self.name,"/"+self.symbol,1/self.mul,-self.offset/self.mul)) 
    
    def __pow__(self,o:int) -> "CompoundUnit":
        return CompoundUnit([self]*o,[],self.name+f"^{o}",self.symbol+f"^{o}",self.mul**o,self.offset*o)

class Unit(BaseUnit):
    mul:number


class CompoundBaseUnit(BaseUnit,CompoundDimension):

    def __init__(self,num:list[DimensionResolvables],den:list[DimensionResolvables],name:str,symbol:str,mul:number=1.,offset:number=0.):
        self.numerator=list(map(resolveDim,num))
        self.denominator=list(map(resolveDim,den))
        self.name=name
        self.mul=mul
        self.symbol=symbol
        self.offset=offset
        self.baseSymbol = f'{".".join(DefaultUnit[i].symbol for i in self.numerator)}/{".".join(DefaultUnit[i].symbol for i in self.denominator)}'
        self.onEdit()

    def __repr__(self) -> str:
        return f"{[i.dim for i in self.numerator]}/{[i.dim for i in self.denominator]} : {self.name} = {self.mul} {parseSymbol(self.baseSymbol)} {self.offset:+.4}"

    def __mul__(self, o: CompoundUnitResolvables) -> "CompoundUnit":
        o=resolveCompoundUnit(o)
        return CompoundUnit(self.numerator+o.numerator,self.denominator+o.denominator,self.name + "*" + o.name,self.symbol+"."+o.symbol,self.mul*o.mul,self.offset+o.offset)  # type: ignore

    def __truediv__(self, o: CompoundUnitResolvables) -> "CompoundUnit":
        o=resolveCompoundUnit(o)
        return CompoundUnit(self.numerator+o.denominator,self.denominator+o.numerator,self.name + "/" + o.name,self.symbol+"/"+o.symbol,self.mul/o.mul,self.offset-o.offset)  # type: ignore

    def __pow__(self, o: int) -> "CompoundUnit":
        return CompoundUnit(self.numerator*o,self.denominator*o,self.name+f"^{o}",self.symbol+f"^{o}",self.mul**o,self.offset*o) # type: ignore

    def sameDim(self,o:"CompoundBaseUnit")->bool:
        return sorted(self.numerator,key = lambda x:x.dim)==sorted(o.numerator,key = lambda x:x.dim) and sorted(self.denominator,key = lambda x:x.dim)==sorted(o.denominator,key = lambda x:x.dim)

    def ratio(self,o:"CompoundBaseUnit")->number:
        """Ratio of 1 self to n other"""
        if self.sameDim(o):
            return self.mul/o.mul
        else:
            raise Exception("Cannot find ratio of units with different dimensions")

    def base(self)->"CompoundBaseUnit":
        dim=resolveCompoundDim(self)
        if dim in DefaultCompoundUnit:
            return DefaultCompoundUnit[dim]
        else:
            raise NotImplementedError("Not implemented dynamic base unit")

    def __eq__(self, o: "CompoundBaseUnit"):
        return sorted(self.numerator,key = lambda x:x.dim)==sorted(o.numerator,key = lambda x:x.dim) and sorted(self.denominator,key = lambda x:x.dim)==sorted(o.denominator,key = lambda x:x.dim) and self.mul==o.mul and self.offset==o.offset

    @overload
    def __rmul__(self, o: number) -> "Value":
        ...
    @overload
    def __rmul__(self, o: CompoundUnitResolvables) -> "CompoundUnit":
        ...
    def __rmul__(self, o: CompoundUnitResolvables|number) -> Union["CompoundUnit" , "Value"]:
        if isinstance(o,number):
            return Value(o,self)
        else:
            o=resolveCompoundUnit(o)
            return CompoundUnit(self.numerator+o.numerator,self.denominator+o.denominator,self.name + "*" + o.name,self.symbol+"."+o.symbol,self.mul,self.offset) # type: ignore

class CompoundUnit(CompoundBaseUnit):
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
        return CompoundUnit(o.numerator,o.denominator,self.name + o.name,self.symbol+o.symbol,(10**self.mul)*o.mul,o.offset/10**o.mul)  # type: ignore

    def __rmul__(self, o: number) -> number:
            return o*10**self.mul

class Value:
    unit: CompoundUnit
    value:number

    def __init__(self,value:number,unit:CompoundUnitResolvables):
        self.value=value
        self.unit=resolveCompoundUnit(unit)

    def __repr__(self) -> str:
        return f"{self.value} {self.unit.symbol}"

    def __mul__(self, o: "Value" | CompoundUnitResolvables|number) -> "Value":
        if isinstance(o,Value):
            return Value(self.value*o.value,self.unit*o.unit)
        elif isinstance(o,number):
            return Value(self.value*o,self.unit)
        else:
            return Value(self.value,resolveCompoundUnit(o)*self.unit)

    def __rmul__(self, o: "Value" | CompoundUnitResolvables|number) -> "Value":
        if isinstance(o,Value):
            return Value(self.value*o.value,self.unit*o.unit)
        elif isinstance(o,number):
            return Value(self.value*o,self.unit)
        else:
            return Value(self.value,resolveCompoundUnit(o)*self.unit)

    def __truediv__(self, o: "Value" | CompoundUnitResolvables|number) -> "Value":
        if isinstance(o,Value):
            return Value(self.value/o.value,self.unit/o.unit)
        elif isinstance(o,number):
            return Value(self.value/o,self.unit)
        else:
            return Value(self.value,self.unit/resolveCompoundUnit(o))
        
    def __rtruediv__(self, o: "Value" | CompoundUnitResolvables|number) -> "Value":
        if isinstance(o,Value):
            return Value(o.value/self.value,o.unit/self.unit)
        elif isinstance(o,number):
            return o*meter/meter/self
        else:
            return Value(self.value,resolveCompoundUnit(o)/self.unit)

    def __add__(self, o: "Value") -> "Value":
        if self.unit == o.unit:
            return Value(self.value+o.value,self.unit)
        elif self.unit.sameDim(o.unit):
            return Value(self.value + ((o.value-o.unit.offset)*o.unit.mul/self.unit.mul +self.unit.offset),self.unit)
        else:
            raise Exception("Unit mismatch")

    def __sub__(self, o: "Value") -> "Value":
        if self.unit == o.unit:
            return Value(self.value-o.value,self.unit)
        elif self.unit.sameDim(o.unit):
            return Value(self.value - ((o.value-o.unit.offset)*o.unit.mul/self.unit.mul +self.unit.offset),self.unit)
        else:
            raise Exception("Unit mismatch")

    def __neg__(self) -> "Value":
        return Value(-self.value,self.unit)
    
    def __pow__(self, o: int) -> "Value":
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

sec = BaseUnit("T","Second","s")
meter=BaseUnit("L","Meter","m")
kilogram = BaseUnit("M","gram","kg")
mol=BaseUnit("N","Mole","mol")
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
#LENGTH
foot = Unit("L","foot","ft",0.3048)
inch = Unit("L","inch","in",0.0254)
miles = Unit("L","miles","mi",1609.344)
yard = Unit("L","yard","yd",0.9144)
angstrom = Unit("L","angstrom","A",1e-10)


#MASS
pound = Unit("M","pound","lbm",.45359237)
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

#Dimensionless

DimLes = CompoundUnit([],[],"","",1)

#Speed
meterPerSecond = CompoundUnit([meter],[sec],"meter/sec","m/s",1)
kilometerPerHour = CompoundUnit([meter],[hour],"kilometer/hour","km/h",1/3.6)
milesPerHour = CompoundUnit([miles],[hour],"miles/hour","mph",1/2.237)

#Acceleration
meterPerSecondSquared = CompoundUnit([meter],[sec,sec],"meter/sec^2","m/s.s",1)
kilometerPerHourSquared = CompoundUnit([meter],[hour,hour],"kilometer/hour^2","km/hr.hr",1/1.944**2)

#Area
squareMeter = CompoundUnit([meter,meter],[],"square meter","m.m",1)
squareKilometer = CompoundUnit([meter,meter],[],"square kilometer","km.km",1e6)
squareMiles = CompoundUnit([miles,miles],[],"square miles","mi.mi",2.58999e6)
squareYard = CompoundUnit([yard,yard],[],"square yard","yd.yd",0.836127)
squareFoot = CompoundUnit([foot,foot],[],"square foot","ft.ft",0.09290304)
squareInch = CompoundUnit([inch,inch],[],"square inch","in.in",0.00064516)
acre = CompoundUnit([meter,meter],[],"acre","acre",4046.8564224)
hectre = CompoundUnit([meter,meter],[],"hectre","hectre",1e4)
วา = CompoundUnit([meter,meter],[],"วา","วา",4)
ไร่ = CompoundUnit([meter,meter],[],"ไร่","ไร่",1600)
งาน = CompoundUnit([meter,meter],[],"งาน","งาน",400)

#Volume
liter = CompoundUnit([meter,meter,meter],[],"liter","l",1e-3)
cubicMeter = CompoundUnit([meter,meter,meter],[],"cubic meter","m.m.m",1)
gallon = CompoundUnit([meter,meter,meter],[],"gallon","gal",0.0037854118)
cubicFoot = CompoundUnit([foot,foot,foot],[],"cubic foot","ft.ft.ft",0.028316846592)
cubicInch = CompoundUnit([inch,inch,inch],[],"cubic inch","in.in.in",0.000016387064)
fluidOunce = CompoundUnit([inch,inch,inch],[],"fluid ounce","fl.oz",0.0000295735295625)
cup = CompoundUnit([inch,inch,inch],[],"cup","cup",0.0002365882365)
pint = CompoundUnit([inch,inch,inch],[],"pint","pt",0.000473176473)
quart = CompoundUnit([inch,inch,inch],[],"quart","qt",0.000946352946)
cc = CompoundUnit([meter,meter,meter],[],"CC","CC",0.000001)

#Density
kilogramPerCubicMeter = CompoundUnit([kilogram],[meter,meter,meter],"kilogram/cubic meter","kg/m.m.m",1)
gramPerCubicMeter = CompoundUnit([gram],[meter,meter,meter],"gram/cubic meter","g/m.m.m",1e-3)
poundPerCubicFoot = CompoundUnit([pound],[foot,foot,foot],"pound/cubic foot","lbm/ft.ft.ft",16.01846337)
poundPerCubicInch = CompoundUnit([pound],[inch,inch,inch],"pound/cubic inch","lbm/in.in.in",27679.9047)
gramPerCc = CompoundUnit([gram],[inch,inch,inch],"gram/cc","g/cc",1000)
kilogramPerLiter = CompoundUnit([kilogram],[meter,meter,meter],"kilogram/liter","kg/l",1e3)
gramPerLiter = CompoundUnit([gram],[meter,meter,meter],"gram/liter","g/l",1)

#Force
newton = CompoundUnit([kilogram,meter],[sec,sec],"newton","N",1)
dyne = CompoundUnit([kilogram,meter],[sec,sec],"dyne","dyn",1e-5)
poundForce = CompoundUnit([pound,foot],[sec,sec],"pound force","lbf",4.4482216152605)

#Pressure
pascal = CompoundUnit([kilogram],[meter,sec,sec],"pascal","Pa",1)
bar = CompoundUnit([kilogram],[meter,sec,sec],"bar","bar",1e5)
atm = CompoundUnit([kilogram],[meter,sec,sec],"atmosphere","atm",101325)
psi = CompoundUnit([kilogram],[meter,sec,sec],"pound/square inch","psi",6894.757293168)
mmHg = CompoundUnit([kilogram],[meter,sec,sec],"millimeter of mercury","mmHg",133.322)
torr = CompoundUnit([kilogram],[meter,sec,sec],"torr","torr",133.322)

#Energy
joule = CompoundUnit([kilogram,meter,meter],[sec,sec],"joule","J",1)
eV = CompoundUnit([kilogram,meter,meter],[sec,sec],"electron volt","eV",1.602176634e-19)
kWh = CompoundUnit([kilogram,meter,meter],[sec,sec],"kilowatt hour","kWh",3600000)
calorie = CompoundUnit([kilogram,meter,meter],[sec,sec],"calorie","cal",4.1868)
btu = CompoundUnit([kilogram,meter,meter],[sec,sec],"British thermal unit","btu",1055.05585262)

#Power
watt = CompoundUnit([kilogram,meter,meter],[sec,sec,sec],"watt","W",1)
horsepower = CompoundUnit([kilogram,meter,meter],[sec,sec,sec],"horsepower","hp",745.699871582270)

#Charge
coulomb = CompoundUnit([amp,sec],[],"coulomb","C",1)
faraday = CompoundUnit([amp,sec],[],"faraday","F",96485.3399)
electron = CompoundUnit([amp,sec],[],"electron charge","e",1.602176634e-19)

#Electric Potential
volt = CompoundUnit([kilogram,meter,meter],[sec,sec,sec,amp],"volt","V",1)

#Electric Field
voltPerMeter = CompoundUnit([kilogram,meter],[sec,sec,sec,amp],"volt/meter","V/m",1)

#Chemical.14
amu = CompoundUnit([kilogram],[],"atomic mass unit","amu",1.66053906660e-27)
gpm = CompoundUnit([kilogram],[mol],"gram per mole","gpm",1e-3)

#Viscosity
poise = CompoundUnit([kilogram],[meter,sec],"poise","P",0.1)
pascalSecond = CompoundUnit([kilogram],[meter,sec],"pascal second","Pa.s",1)
centipoise = CompoundUnit([kilogram],[meter,sec],"centipoise","cP",1e-3)
micropoise = CompoundUnit([kilogram],[meter,sec],"micropoise","uP",1e-7)
millipoise = CompoundUnit([kilogram],[meter,sec],"millipoise","mP",1e-4)

#Mass Diffusivity
sqfPs = CompoundUnit([meter,meter],[sec],"square foot per second","ft.ft/s",0.09290304)
sqmPs = CompoundUnit([meter,meter],[sec],"square meter per second","m.m/s",1)
sqcmPs = CompoundUnit([meter,meter],[sec],"square centimeter per second","cm.cm/s",1e-4)

DefaultCompoundUnit = {
    Dimension("T"):sec,
    Dimension("L"):meter,
    Dimension("M"):kilogram,
    Dimension("N"):mol,
    Dimension("H"):kelvin,
    Dimension("I"):amp,
    Dimension("J"):cd,
    CompoundDimension([],[]):DimLes,
    CompoundDimension(["L"],["T"]):meterPerSecond, #Speed
    CompoundDimension(["L"],["T","T"]):meterPerSecondSquared,#Acceleration
    CompoundDimension(["L","L"],[]):squareMeter,#Area
    CompoundDimension(["L","L","L"],[]):cubicMeter,#Volume
    CompoundDimension(["M"],["L","L","L"]):gramPerCubicMeter,#Density
    CompoundDimension(["L","M"],["T","T"]):newton,#Force
    CompoundDimension(["M"],["L","T","T"]):pascal,#Pressure
    CompoundDimension(["M","L","L"],["T","T"]):joule,#Energy
    CompoundDimension(["M","L","L"],["T","T","T"]):watt,#Power
    CompoundDimension(["I","T"],[]):coulomb,#Charge
    CompoundDimension(["M","L","L"],["T","T","T","I"]):volt,#Electric Potential
    CompoundDimension(["M","L"],["T","T","T","I"]):voltPerMeter,#Electric Field
    CompoundDimension(["M"],["N"]):amu,#Chemical
    CompoundDimension(["L","L"],["T"]):sqmPs,#Mass Diffusivity
}