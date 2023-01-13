from typing import Callable, Generic,TypeVar
from .typedef import *
import cmath
I1=TypeVar("I1")
I2=TypeVar("I2")
O=TypeVar("O")

class Infix(Generic[I1,I2,O]):
    def __init__(self, function: Callable[[I1,I2 ], O]):
        self.function = function
    def __ror__(self, other:I1):
        return InfixReturn(self.returnFunc(other))
    
    def __rlshift__(self, other:I1):
        return InfixReturn(self.returnFunc(other))
     
    def __call__(self, value1:I1, value2:I2):
        return self.function(value1, value2)

    def returnFunc(self,other:I1):
        def func(value:I2):
            return self.function(other,value)
        return func
        
class InfixReturn(Generic[I2,O]):
    def __init__(self, function: Callable[[I2],O]):
        self.function = function
    def __rshift__(self, other:I2):
        return self.function(other)
    def __or__(self, other:I2):
        return self.function(other) 

def Parallel2Resistor(R1:number,R2:number):
    return (R1*R2)/(R1+R2)

def Arg(mag:number,a:number):
    return cmath.rect(mag,a)

p = Infix(Parallel2Resistor)
A=Infix(Arg)