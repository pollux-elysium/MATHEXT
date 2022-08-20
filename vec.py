from cmath import rect as rec,phase,pi
from math import radians as rad,sin,cos,degrees as deg,hypot,atan2,acos
from typing import Union,Literal
from numpy import cross,dot

def drec(x: float, y: float):
    return rec(x, rad(y))


def dpol(x: Union[complex, float], y: float = 0):
    """x,y or just a complex"""
    if y:
        c = complex(x, y)
        return abs(c), deg(phase(c))
    else:
        return abs(x), deg(phase(x))

def rec3d(m: float, a: float, e: float):
    z = m*sin(e)
    x = m*cos(e)*cos(a)
    y = m*cos(e)*sin(a)
    return [x, y, z]


def drec3d(m: float, a: float, e: float):
    z = m*sin(rad(e))
    x = m*cos(rad(e))*cos(rad(a))
    y = m*cos(rad(e))*sin(rad(a))
    return [x, y, z]


def pol3d(x: float, y: float, z: float):
    m = hypot(x, y, z)
    a = atan2(y, x)
    e = atan2(z, hypot(x, y))
    return [m, a, e]


def dpol3d(x: float, y: float, z: float):
    m = hypot(x, y, z)
    a = atan2(y, x)
    e = atan2(z, hypot(x, y))
    return [m, deg(a), deg(e)]

class v3d:
    x: float
    y: float
    z: float

    def __repr__(self):
        return f'v3d([{self.x},{self.y},{self.z}])'

    def __init__(self, x: float | list[float], y: float = 0, z: float = 0):
        if type(x) == list:
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    def __add__(self, new: Union['v3d', list[float]]) -> list[float]:
        if type(self) is type(new):
            return [self.x+new.x, self.y+new.y, self.z+new.z]
        else:
            return [self.x+float(new[0]), self.y+float(new[1]), self.z+float(new[2])]

    def __sub__(self, new: Union['v3d', list[float]]) -> list[float]:
        if type(self) is type(new):
            return [self.x-new.x, self.y-new.y, self.z-new.z]
        else:
            return [self.x-float(new[0]), self.y-float(new[1]), self.z-float(new[2])]

    def __mul__(self, new: Union['v3d', list[float]]) -> list[float]:
        if type(self) is type(new):
            return ((self.x*new.x)+(self.y*new.y)+(self.z*new.z))
        else:
            return [
                self.x*float(new),
                self.y*float(new),
                self.z*float(new)]

    def __matmul__(self, new: 'v3d') -> list[float]:
        return list(cross([self.x, self.y, self.z], [new.x, new.y, new.z]))

    def __iadd__(self, new: Union['v3d', list[float]]):
        if type(self) is type(new):
            self.x += new.x
            self.y += new.y
            self.z += new.z
            return self
        else:
            self.x += float(new[0])
            self.y += float(new[1])
            self.z += float(new[2])
            return self

    def __isub__(self, new: Union['v3d', list[float]]):
        if type(self) is type(new):
            self.x -= new.x
            self.y -= new.y
            self.z -= new.z
            return self
        else:
            self.x -= float(new[0])
            self.y -= float(new[1])
            self.z -= float(new[2])
            return self

    def __imul__(self, new: Union['v3d', list[float]]):
        self.x *= float(new)
        self.y *= float(new)
        self.z *= float(new)

    def __abs__(self):
        return self.m

    def __str__(self):
        return f'[{self.x},{self.y},{self.z}]'

    def __neg__(self):
        return v3d(-self.x,-self.y,-self.z)

    def flip(self, i:Literal["x","y","z"]):
        """Flip axis x/y/z in string\nflip('xy') -> flip x and y"""
        if "x" in i:
            self.x = -self.x
        if "y" in i:
            self.y = -self.y
        if "z" in i:
            self.z = -self.z
        return self

    def __iter__(self):
        return iter([self.x,self.y,self.z])

    @property
    def m(self):
        """Magnitute"""
        return hypot(self.x, self.y, self.z)

    @property
    def angle(self):
        """Angle on plane XY from x+"""
        return atan2(self.y, self.x)

    @property
    def asc(self):
        """Ascention from plane XY"""
        return atan2(self.z, hypot(self.x, self.y))

    @property
    def az(self):
        """Angle between Z axis"""
        return abs((pi/2-self.asc))

    @property
    def ax(self):
        """Angle between X axis"""
        return abs(atan2(hypot(self.y, self.z), self.x))

    @property
    def ay(self):
        """Angle between Y axis"""
        return abs(atan2(hypot(self.x, self.z), self.y))

    @staticmethod
    def dmae(m: float, a: float, e: float):
        """v3d from m,a,e in degrees"""
        z = m*sin(rad(e))
        x = m*cos(rad(e))*cos(rad(a))
        y = m*cos(rad(e))*sin(rad(a))
        return v3d(x, y, z)

    @staticmethod
    def mae(m:float, a:float, e:float):
        """v3d from m,a,e in radian"""
        z = m*sin(e)
        x = m*cos(e)*cos(a)
        y = m*cos(e)*sin(a)
        return v3d(x, y, z)

    @staticmethod
    def dcyl(m:float, a:float, z:float):
        """v3d from m,a,z (Cylindrical Coordinate) in degrees"""
        z = z
        x = m*cos(rad(a))
        y = m*sin(rad(a))
        return v3d(x, y, z)

    @staticmethod
    def cyl(m: float, a: float, z: float):
        """v3d from m,a,z (Cylindrical Coordinate) in radians"""
        z = z
        x = m*cos(a)
        y = m*sin(a)
        return v3d(x, y, z)

    def rec3d(self):
        return [self.x, self.y, self.z]

    def pol3d(self):
        return [self.m, self.angle, self.asc]

    def dpol3d(self):
        return [self.m, deg(self.angle), deg(self.asc)]

    def unit(self):
        """Return unit vector"""
        return self.mae(1, self.angle, self.asc)

    def toList(self):
        return [self.x, self.y, self.z]

    def a2v(self, v: 'v3d'):
        """Angle between 2 vector"""
        if type(v) != v3d:
            v = v3d(*v)
        return acos(dot(self, v)/self.m/v.m)

    def da2v(self, v: 'v3d'):
        """Angle between 2 vector in degrees"""
        if type(v) != v3d:
            v = v3d(*v)
        return deg(acos(dot(self, v)/self.m/v.m))