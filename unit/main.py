from ..typedef import *
from .DimAndUnit import CompoundUnit

class Value:
    unit: CompoundUnit
    Value:number

    def __init__(self,value:number,unit:CompoundUnit):
        self.Value=value
        self.unit=unit