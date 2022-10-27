import math
import numpy
from .typedef import *

def solvePoly(*coeffs):
    poly = numpy.polynomial.Polynomial(coeffs[::-1])
    return poly.roots()