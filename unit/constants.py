from .DimAndUnit import Value,CompoundUnit
from .unitdef import *
from math import pi


R = Value(8.31446261815324,joule/mol/kelvin)
g = Value(9.80665,meter/sec/sec)
mu0 = Value(4*pi*1e-7,meter*meter/sec*sec)
eps0 = Value(8.854187817e-12,coulomb/volt/meter)
R_atm = Value(0.08206,liter*atm/mol/kelvin)
Na = 6.02214129e23
h = Value(6.626070040e-34,joule*sec)
G = Value(6.67408e-11,meter*meter*meter/kilogram/sec/sec)