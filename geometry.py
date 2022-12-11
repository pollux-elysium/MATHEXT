from math import hypot
from typing import Literal, overload

import numpy as np
from numpy import dot
from numpy.linalg import det
from numpy.linalg import solve as asolve

from .floatCalc import nearZero
from .vec import v3d


class line:
    """Line Class"""
    a: v3d #Anchor
    d: v3d #Direction

    def __repr__(self):
        return f'p:{self.a} d:{self.d}'

    def __init__(self, a: v3d| list[float] = v3d(0, 0, 0), d: v3d| list[float] = v3d(0, 0, 0)):
        """Line Class
        
        Args:
            a (v3d | list[float], optional): Anchor. Defaults to v3d(0, 0, 0).
            d (v3d | list[float], optional): Direction. Defaults to v3d(0, 0, 0).
            
        Examples:
            >>> line(v3d(0,0,0),v3d(1,0,0))
            p:(0,0,0) d:(1,0,0)
            >>> line([0,0,0],[1,0,0])
            p:(0,0,0) d:(1,0,0)
            
        """
        if isinstance(a,v3d):
            self.a = a
        else:
            self.a = v3d(*a)
        if isinstance(d,v3d):
            self.d = d.unit()
        else:
            self.d = v3d(*d).unit()

    def dbyd(self, a1: Literal["x","y","z"], a2: Literal["x","y","z"]):
        """Slope of line by axis

        Args:
            a1 (Literal["x","y","z"]): Axis 1
            a2 (Literal["x","y","z"]): Axis 2

        Returns:
            float: Slope of line by axis (axis1/axis2)

        Examples:
            >>> line(v3d(0,0,0),v3d(1,0,0)).dbyd("x","y")
            inf
            >>> line(v3d(0,0,0),v3d(1,1,0)).dbyd("x","y")
            1.0

        """
        d1: float
        d2: float
        d1 = getattr(self.d, a1)
        d2 = getattr(self.d, a2)
        if d2 == 0 and d1 != 0:
            return float('inf')
        elif d2 == 0 and d1 == 0:
            return None
        else:
            return d1/d2

    @staticmethod
    def f2p(a: v3d | list[float], b: v3d | list[float]) -> 'line':
        """Line from 2 points

        Args:
            a (v3d | list[float]): Point 1
            b (v3d | list[float]): Point 2

        Returns:
            line: Line from 2 points

        Examples:
            >>> line.f2p(v3d(0,0,0),v3d(1,0,0))
            p:(0,0,0) d:(1,0,0)
            >>> line.f2p([0,2,0],[2,0,0])
            p:(0,2,0) d:(0.7071067811865475,-0.7071067811865475,0.0)

        """
        if isinstance(a,v3d):
            a = a
        else:
            a = v3d(*a)
        if isinstance(b,v3d):
            b = b
        else:
            b = v3d(*b)
        return line(a, b-a)
        

    def pol(self, a: Literal["x","y","z"], n: float) -> v3d:
        """Point on line by axis and value

        Args:
            a (Literal["x","y","z"]): Axis
            n (float): Value

        Returns:
            v3d: Point on line by axis and value

        Examples:
            >>> line(v3d(3,0,0),v3d(1,1,0)).pol("x",1)
            v3d([1.0,-2.0,0.0])
            >>> line(v3d(3,0,0),v3d(1,1,0)).pol("y",1)
            v3d([4.0,1.0,0.0])
        """
        anc: float
        d: float
        anc = getattr(self.a, a)
        d = getattr(self.d, a)
        if d == 0:
            raise ValueError
        dt = (n-anc)/d
        return v3d(self.a+self.d*dt)

    def pat(self, t: float) -> v3d:
        """Point at t(var)"""
        return v3d(self.a+self.d*t)


    @overload
    def dist(self, b: v3d| list[float])->float: ...
    @overload
    def dist(self, b: v3d|list[float],mag:Literal[True]) -> float: ...
    @overload
    def dist(self, b: v3d|list[float],mag:Literal[False]) -> v3d: ...
    def dist(self, b: v3d| list[float],mag:bool|None=True):
        """Distance from point to line

        Args:
            b (v3d| list[float]): Point
            mag (bool, optional): Magnitude. Defaults to True.

        Returns:
            float: Distance from point to line (magnitude) (mag = True) 
            v3d: Distance from point to line (vector) (mag = False)
        """
        if mag:return v3d((v3d(self.a-b))@self.d).m
        elif not mag:
            if not isinstance(b,v3d):
                b=v3d(b)
            return v3d(b-v3d(self.a+(self.d*dot(b-self.a,self.d.toList()))))

    def comp(self, a: 'line',debug:bool=False):
        """Compare 2 lines

        Args:
            a (line): Line to compare

        Returns:
            v3d: Point of intersection
        print Parallel, Same Line, or Skewed
        """

        if np.allclose(self.d.rec3d(), a.d.rec3d())or np.allclose(self.d.__neg__().rec3d(),a.d.rec3d()):#Check direction for parallel or same line
            if not(nearZero(self.d.x)or nearZero(a.d.x)):
                if np.allclose(self.pol('x',0).rec3d(),a.pol('x',0).rec3d()):#Check position when x=0
                    print("Same Line")
                else:print('Parallel')
            elif not(nearZero(self.d.y)or nearZero(a.d.y)):
                if np.allclose(self.pol('y',0).rec3d(),a.pol('y',0).rec3d()):#Check position when y=0
                    print("Same Line")
                else:print('Parallel')
            elif not(nearZero(self.d.z)or nearZero(a.d.z)):
                if np.allclose(self.pol('z',0).rec3d(),a.pol('z',0).rec3d()):#Check position when z=0
                    print("Same Line")
                else:print('Parallel')
            return

        t: float
        s: float
        m,n,o,p,q,r=self.d.x,self.d.y,self.d.z,a.d.x,a.d.y,a.d.z
        #Finding intersection of line
        if not(nearZero(det([[m,p],[n,q]]))):# type: ignore #Test for matrix solvability 
            t, s = asolve([
                [round(m, 9), -round(p, 9)],
                [round(n, 9), -round(q, 9)]
            ], [  # type: ignore
                round(a.a.x-self.a.x, 9), round(a.a.y-self.a.y, 9)   # type: ignore # type: ignore
            ])
        elif not(nearZero(det([[o,r],[n,q]]))):# type: ignore #Test for matrix solvability
            t, s = asolve([
                [round(o, 9), -round(r, 9)],
                [round(n, 9), -round(q, 9)]
            ], [  # type: ignore
                round(a.a.z-self.a.z, 9), round(a.a.y-self.a.y, 9)  # type: ignore
            ])
        elif not(nearZero(det([[o,r],[m,n]]))):# type: ignore # type: ignore #Test for matrix solvability
            t, s = asolve([
                [round(o, 9), -round(r, 9)],
                [round(m, 9), -round(n, 9)]
            ], [  # type: ignore
                round(a.a.z-self.a.z, 9), round(a.a.x-self.a.x, 9)  # type: ignore
            ])
        else:
            print("Some Error")
        if debug:print(t,s,self.pat(t),a.pat(s)) #type:ignore
        if np.allclose(self.pat(t).rec3d(), a.pat(s).rec3d()):#type:ignore #If third axis is the same 
            return self.pat(t)#type:ignore

        else:
            print("Skewed or Some Error Check code")
            return


class plane:
    """Plane Class"""
    a: v3d #Anchor
    n: v3d #Normal

    def __repr__(self):
        return f'p:{self.a} n:{self.n}'

    def __init__(self, a: v3d| list[float] = v3d(0, 0, 0), n: v3d| list[float] = v3d(0, 0, 0)):
        """Plane Class

        Args:
            a (v3d| list[float], optional): Anchor. Defaults to v3d(0, 0, 0).
            n (v3d| list[float], optional): Normal. Defaults to v3d(0, 0, 0).
        """
        if isinstance(a,v3d):
            self.a = a
        else:
            self.a = v3d(*a)
        if isinstance(n,v3d):
            self.n = n.unit()
        else:
            self.n = v3d(*n).unit()

    def equa(self):
        """Equation of plane

        Returns:
            str: Equation of plane
        """
        a = self.a
        n = self.n
        return f'{n.x}x{n.y:+}y{n.z:+}z={n.x*a.x+n.y*a.y+n.z*a.z}'

    @property
    def eqx(self):
        return self.n.x

    @property
    def eqy(self):
        return self.n.y

    @property
    def eqz(self):
        return self.n.z

    @property
    def eqd(self):
        a = self.a
        n = self.n
        return -(n.x*a.x+n.y*a.y+n.z*a.z)

    @staticmethod
    def feq(l: float| list[float], b: float, c: float, d: float):
        """From equation

        Args:
            l (float| list[float]): a or [a,b,c,d]
            b (float): b
            c (float): c
            d (float): d

        Returns:
            plane: Plane
        """
        a: float
        if isinstance(l,list):
            a = l[0]
            b = l[1]
            c = l[2]
            d = l[3]
        else:
            a = l
        if a != 0:
            return plane([-d/a, 0, 0], [a, b, c])
        elif b != 0:
            return plane([0, -d/b, 0], [a, b, c])
        elif c != 0:
            return plane([0, 0, -d/c], [a, b, c])

    @staticmethod
    def f3p(a: v3d, b: v3d, c: v3d):
        """From 3 points

        Args:
            a (v3d): Point 1
            b (v3d): Point 2
            c (v3d): Point 3

        Returns:
            plane: Plane
        """
        return plane(a, v3d(b-a)@v3d(c-a))

    def dist(self, b: v3d):
        """Distance from point to plane
        
        Args:
            b (v3d): Point
            
        Returns:
            float: Distance
        """
        return v3d(dot((self.a-b), self.n.rec3d())).m

    def d2p(self, b: 'plane'):
        """Distance between 2 plane
        
        Args:
            b (plane): Plane
            
        Returns:
            float: Distance
            
        Print "Not Parallel" if not parallel
        """
        if np.allclose(self.n.rec3d(), b.n.rec3d()):
            return (self.eqd-b.eqd)/hypot(b.n.x, b.n.y, b.n.z)
        else:
            print("Not Parallel")
            return

    def intersec(self, b: 'plane'):
        """Intersection of 2 planes

        Args:
            b (plane): Plane

        Returns:
            line: Intersection line

        Print "Parallel" if parallel
        """

        if np.allclose(self.n.rec3d(), b.n.rec3d()):
            print("Parallel")
            return

        if not(nearZero(det([[self.eqx,self.eqy],[b.eqx,b.eqy]]))):# type: ignore #test for unsolvable
            x,y=asolve([#Find remaining 2 axis when 1 is fixed
                [self.eqx,self.eqy],
                [b.eqx,b.eqy]
            ],[  # type: ignore
                -self.eqd,
                -b.eqd
            ])
            return line([x,y,0],self.n@b.n)

        elif not(nearZero(det([[self.eqx,self.eqz],[b.eqx,b.eqz]]))):  # type: ignore
            x,z=asolve([
                [self.eqx,self.eqz],
                [b.eqx,b.eqz]
            ],[  # type: ignore
                -self.eqd,
                -b.eqd
            ])
            return line([x,0,z],self.n@b.n)

        elif not(nearZero(det([[self.eqy,self.eqz],[b.eqy,b.eqz]]))):   # type: ignore # type: ignore
            y,z=asolve([
                [self.eqy,self.eqz],
                [b.eqy,b.eqz]
            ],[  # type: ignore
                -self.eqd,
                -b.eqd
            ])
            return line([0,y,z],self.n@b.n)

        else:print("error")
