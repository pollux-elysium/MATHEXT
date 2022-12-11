import math
import numpy
from .typedef import *

def solvePoly(*coeffs)-> list[complex]:
    """Solve a polynomial equation of the form ax^n + bx^(n-1) + ... + c = 0
    
    Args:
        coeffs (list): The coefficients of the polynomial equation in the form [a,b,c,...]
        
    Returns:
        list: The roots of the polynomial equation
    """
    poly = numpy.polynomial.Polynomial(coeffs[::-1])
    return poly.roots()