from .DimAndUnit import BaseUnit, CompoundDimension, CompoundUnit,Dimension,Unit, prefix

#Sync with DimeAndUnit.py

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
squareKilometer = CompoundUnit([meter,meter],[],"square kilometer","m.km",1e6)
squareMiles = CompoundUnit([miles,miles],[],"square miles","mi.mi",2.58999e6)
squareYard = CompoundUnit([yard,yard],[],"square yard","yd.yd",0.836127)
squareFoot = CompoundUnit([foot,foot],[],"square foot","ft.ft",0.09290304)
squareInch = CompoundUnit([inch,inch],[],"square inch","in.in",0.00064516)
acre = CompoundUnit([meter,meter],[],"acre","acre",4046.8564224)
hectre = CompoundUnit([meter,meter],[],"hectre","hectre",1e4)
วา = CompoundUnit([meter,meter],[],"วา","วา",4)
ไร่ = CompoundUnit([meter,meter],[],"ไร่","ไร่",1600)
งาน = CompoundUnit([meter,meter],[],"งาน","งาน",400)
darcy = CompoundUnit([meter,meter],[],"darcy","darcy",9.869233e-13)

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
cc = CompoundUnit([inch,inch,inch],[],"CC","CC",0.001)

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

DefaultCompoundUnit = {
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
}