from ..typedef import *
from .DimAndUnit import CompoundUnit

class Value:
    unit: CompoundUnit
    value:number

    def __init__(self,value:number,unit:CompoundUnit):
        self.value=value
        self.unit=unit