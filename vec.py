from cmath import rect as rec,phase,pi
from math import radians as rad,sin,cos,degrees as deg,hypot,atan2,acos
from typing import Union,Literal, overload
from numpy import cross,dot
from .typedef import *

def drec(x: float, y: float) -> complex:
    """Returns a complex number from polar coordinates
    
    Args:
        x (float): magnitude
        y (float): angle in degrees
        
    Returns:
        complex: complex number
    """
    return rec(x, rad(y))


def dpol(x: Union[complex, float], y: float = 0) -> tuple[float, float]:
    """Returns the polar coordinates of a complex number

    Args:
        x (float | complex): real part of the complex number or the complex number itself
        y (float, optional): imaginary part of the complex number. Defaults to 0.

    Returns:
        tuple[float, float]: magnitude and angle in degrees
    """

    if not isinstance(x, complex):
        c: complex = complex(x, y)
        return abs(c), deg(phase(c))
    else:
        return abs(x), deg(phase(x))

def rec3d(m: float, a: float, e: float) -> list[float]:
    """Returns a 3D vector from spherical coordinates
    
    Args:
        m (float): magnitude
        a (float): azimuth in radians
        e (float): elevation in radians
        
    Returns:
        list[float]: 3D vector
    """
    z: float = m*sin(e)
    x: float = m*cos(e)*cos(a)
    y: float = m*cos(e)*sin(a)
    return [x, y, z]


def drec3d(m: float, a: float, e: float) -> list[float]:
    """Returns a 3D vector from spherical coordinates

    Args:
        m (float): magnitude
        a (float): azimuth in degrees
        e (float): elevation in degrees
        
    Returns:
        list[float]: 3D vector
    """
    z: float = m*sin(rad(e))
    x: float = m*cos(rad(e))*cos(rad(a))
    y: float = m*cos(rad(e))*sin(rad(a))
    return [x, y, z]


def pol3d(x: float, y: float, z: float) -> list[float]:
    """Returns the spherical coordinates of a 3D vector
    
    Args:
        x (float): x component of the vector
        y (float): y component of the vector
        z (float): z component of the vector
        
    Returns:
        list[float]: magnitude, azimuth and elevation in radians
    """

    m: float = hypot(x, y, z)
    a: float = atan2(y, x)
    e: float = atan2(z, hypot(x, y))
    return [m, a, e]


def dpol3d(x: float, y: float, z: float) -> list[float]:
    """Returns the spherical coordinates of a 3D vector

    Args:
        x (float): x component of the vector
        y (float): y component of the vector
        z (float): z component of the vector

    Returns:
        list[float]: magnitude, azimuth and elevation in degrees
    """
    m: float = hypot(x, y, z)
    a: float = atan2(y, x)
    e: float = atan2(z, hypot(x, y))
    return [m, deg(a), deg(e)]

class v3d:
    """Wrapper of list[float] for 3D vectors"""
    x: float
    y: float
    z: float

    def __repr__(self) -> str:
        return f'v3d([{self.x},{self.y},{self.z}])'

    def __init__(self, x: float | list[float], y: float = 0, z: float = 0):
        """Initialize a 3D vector
        
        Args:
            x (float | list[float]): x component of the vector or a list of the form [x,y,z]
            y (float, optional): y component of the vector. Defaults to 0.
            z (float, optional): z component of the vector. Defaults to 0.
            
        """
        if isinstance(x,list):
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    def __add__(self, new: Union['v3d', list[float]]) -> list[float]:
        """Add a vector to the current vector
        
        Args:
            new (v3d | list[float]): vector to add
            
        Returns:
            list[float]: sum of the vectors
        """
        if isinstance(new,v3d):
            return [self.x+new.x, self.y+new.y, self.z+new.z]
        else:
            return [self.x+float(new[0]), self.y+float(new[1]), self.z+float(new[2])]

    def __sub__(self, new: Union['v3d', list[float]]) -> list[float]:
        """Subtract a vector from the current vector

        Args:
            new (v3d | list[float]): vector to subtract

        Returns:
            list[float]: difference of the vectors
        """
        if isinstance(new,v3d):
            return [self.x-new.x, self.y-new.y, self.z-new.z]
        else:
            return [self.x-float(new[0]), self.y-float(new[1]), self.z-float(new[2])]
   
    @overload
    def __mul__(self,new:"v3d")->number:
        ...
    @overload
    def __mul__(self,new:number)->list[float]:
        ...
    def __mul__(self, new:Union["v3d",number]) -> float | list[float]:
        """Multiply the current vector by a scalar or another vector

        Args:
            new (v3d | number): vector or scalar to multiply

        Returns:
            list[float]: product of the vectors (if new is a scalar)
            number: dot product of the vectors (if new is a vector)
        """
        if isinstance(new,v3d):
            return ((self.x*new.x)+(self.y*new.y)+(self.z*new.z))
        else:
            return [
                self.x*float(new),
                self.y*float(new),
                self.z*float(new)]

    def __matmul__(self, new: 'v3d') -> list[float]:
        """Cross product of the current vector and another vector

        Args:
            new (v3d): vector to cross

        Returns:
            list[float]: cross product of the vectors
        """
        return list(cross([self.x, self.y, self.z], [new.x, new.y, new.z]))

    def __iadd__(self, new: Union['v3d', list[float]]):
        """Add a vector to the current vector"""
        if isinstance(new,v3d):
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
        """Subtract a vector from the current vector"""
        if isinstance(new,v3d):
            self.x -= new.x
            self.y -= new.y
            self.z -= new.z
            return self
        else:
            self.x -= float(new[0])
            self.y -= float(new[1])
            self.z -= float(new[2])
            return self

    def __imul__(self, new:number):
        """Multiply the current vector by a scalar"""
        self.x *= float(new)
        self.y *= float(new)
        self.z *= float(new)
        return self

    def __abs__(self):
        """Return the magnitude of the vector"""
        return self.m

    def __str__(self):
        return f'[{self.x},{self.y},{self.z}]'

    def __neg__(self):
        """Return the negative of the vector"""
        return v3d(-self.x,-self.y,-self.z)

    def flip(self, i:Literal["x","y","z"]):
        """Flip axis x/y/z 
        
        Args:
            i (Literal["x","y","z"]): axis to flip

        Returns:
            v3d: flipped vector (self)
        """
        if "x" in i:
            self.x = -self.x
        if "y" in i:
            self.y = -self.y
        if "z" in i:
            self.z = -self.z
        return self

    def __iter__(self):
        """Return the vector as an iterable.
        
        Enables unpacking of the vector."""
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
        """Create v3d from spherical coordinate in degrees
        
        Args:
            m (float): magnitude
            a (float): azimuth
            e (float): elevation
            
        Returns:
            v3d: vector"""
        z = m*sin(rad(e))
        x = m*cos(rad(e))*cos(rad(a))
        y = m*cos(rad(e))*sin(rad(a))
        return v3d(x, y, z)

    @staticmethod
    def mae(m:float, a:float, e:float):
        """Create v3d from spherical coordinate in radians

        Args:
            m (float): magnitude
            a (float): azimuth
            e (float): elevation

        Returns:
            v3d: vector
        """
        z = m*sin(e)
        x = m*cos(e)*cos(a)
        y = m*cos(e)*sin(a)
        return v3d(x, y, z)

    @staticmethod
    def dcyl(m:float, a:float, z:float):
        """Create v3d from cylindrical coordinate in degrees

        Args:
            m (float): magnitude
            a (float): azimuth
            z (float): height

        Returns:
            v3d: vector
        """
        z = z
        x = m*cos(rad(a))
        y = m*sin(rad(a))
        return v3d(x, y, z)

    @staticmethod
    def cyl(m: float, a: float, z: float):
        """Create v3d from cylindrical coordinate in radians
        
        Args:
            m (float): magnitude
            a (float): azimuth
            z (float): height
            
        Returns:
            v3d: vector"""
        z = z
        x = m*cos(a)
        y = m*sin(a)
        return v3d(x, y, z)

    def rec3d(self):
        """Return vector in rectangular coordinate"""
        return [self.x, self.y, self.z]

    def pol3d(self):
        """Return vector in spherical coordinate in radians"""
        return [self.m, self.angle, self.asc]

    def dpol3d(self):
        """Return vector in spherical coordinate in degrees"""
        return [self.m, deg(self.angle), deg(self.asc)]

    def unit(self):
        """Return unit vector"""
        return self.mae(1, self.angle, self.asc)

    def toList(self):
        """Return vector as list"""
        return [self.x, self.y, self.z]

    def a2v(self, v: 'v3d'):
        """Angle between 2 vector
        
        Args:
            v (v3d): vector to compare to
            
        Returns:
            float: angle in radians"""
        if type(v) != v3d:
            v = v3d(*v)
        return acos(dot(self.toList(), v.toList())/self.m/v.m)

    def da2v(self, v: 'v3d'):
        """Angle between 2 vector in degrees
        
        Args:
            v (v3d): vector to compare to
            
        Returns:
            float: angle in degrees"""
        if type(v) != v3d:
            v = v3d(*v)
        return deg(acos(dot(self.toList(), v.toList())/self.m/v.m))

    def project(self,v:'v3d'):
        """Project vector to another vector
        
        Args:
            v (v3d): vector to project to
            
        Returns:
            v3d: projected vector
        """
        if type(v) != v3d:
            v = v3d(*v)
        return v*(self*v/v.m)