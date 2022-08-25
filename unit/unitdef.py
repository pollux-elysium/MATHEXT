from .DimAndUnit import BaseUnit,Dimension,Unit

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