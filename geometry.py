from .vec import v3d
from typing import Literal
from numpy import dot
from numpy.linalg import det,solve as asolve
import numpy as np
from .floatCalc import nearZero
from math import hypot

class line:
    a: v3d
    d: v3d

    def __repr__(self):
        return f'p:{self.a} d:{self.d}'

    def __init__(self, a: v3d| list[float] = v3d(0, 0, 0), d: v3d| list[float] = v3d(0, 0, 0)):
        """Anchor : a \nDirection : d  v3d or list of 3"""
        if type(a) == v3d:
            self.a = a
        else:
            self.a = v3d(*a)
        if type(d) == v3d:
            self.d = d.unit()
        else:
            self.d = v3d(*d).unit()

    def dbyd(self, a1: Literal["x","y","z"], a2: Literal["x","y","z"]):
        """d x|y|z / d x|y|z"""
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
    def f2p(a: v3d, b: v3d):
        """Line from 2 point"""
        return line(a, a-b)

    def pol(self, a: str, n: float) -> v3d:
        """Point on Line (axis,coord)"""
        anc: float
        d: float
        anc = getattr(self.a, a)
        d = getattr(self.d, a)
        if d == 0:
            print(f"Error: d{a}=0")
            return None
        dt = (n-anc)/d
        return v3d(self.a+self.d*dt)

    def pat(self, t: float):
        """Point at t(var)"""
        return v3d(self.a+self.d*t)

    def dist(self, b: v3d| list[float],mag:bool=True):
        """Distance between point to line
        \nVector between point to line"""
        if mag:return v3d((v3d(self.a-b))@self.d).m
        elif not mag:
            if type(b)!=v3d:
                b=v3d(b)
            return v3d(b-v3d(self.a+(self.d*dot(b-self.a,self.d.toList()))))

    def comp(self, a: 'line',debug:bool=False):
        """Compare 2 line"""

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
                if np.allclose(self.pol('z',0).rec3d(),a.pol('z',0).rec3d()):#Check position when x=0
                    print("Same Line")
                else:print('Parallel')
            return

        t: float
        s: float
        m,n,o,p,q,r=self.d.x,self.d.y,self.d.z,a.d.x,a.d.y,a.d.z
        #Finding intersection of line
        if not(nearZero(det([[m,p],[n,q]]))):#Test for matrix solvability
            t, s = asolve([
                [round(m, 9), -round(p, 9)],
                [round(n, 9), -round(q, 9)]
            ], [
                round(a.a.x-self.a.x, 9), round(a.a.y-self.a.y, 9)
            ])
        elif not(nearZero(det([[o,r],[n,q]]))):#Test for matrix solvability
            t, s = asolve([
                [round(o, 9), -round(r, 9)],
                [round(n, 9), -round(q, 9)]
            ], [
                round(a.a.z-self.a.z, 9), round(a.a.y-self.a.y, 9)
            ])
        elif not(nearZero(det([[o,r],[m,n]]))):#Test for matrix solvability
            t, s = asolve([
                [round(o, 9), -round(r, 9)],
                [round(m, 9), -round(n, 9)]
            ], [
                round(a.a.z-self.a.z, 9), round(a.a.x-self.a.x, 9)
            ])
        else:
            print("Some Error")
        if debug:print(t,s,self.pat(t),a.pat(s))
        if np.allclose(self.pat(t).rec3d(), a.pat(s).rec3d()):#If third axis is the same 
            return self.pat(t)

        else:
            print("Skewed or Some Error Check code")
            return


class plane:
    a: v3d
    n: v3d

    def __repr__(self):
        return f'p:{self.a} n:{self.n}'

    def __init__(self, a: v3d| list[float] = v3d(0, 0, 0), n: v3d| list[float] = v3d(0, 0, 0)):
        """a:Anchor \n n:Parallel Normal Vector"""
        if type(a) == v3d:
            self.a = a
        else:
            self.a = v3d(*a)
        if type(n) == v3d:
            self.n = n.unit()
        else:
            self.n = v3d(*n).unit()

    def equa(self):
        """Return equation"""
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
        """From equation"""
        a: float
        if type(l) == list:
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
        """From 3 point"""
        return plane(a, v3d(b-a)@v3d(c-a))

    def dist(self, b: v3d):
        """Distance from point to plane"""
        return v3d(dot((self.a-b), self.n.rec3d())).m

    def d2p(self, b: 'plane'):
        """Distance between 2 plane"""
        if np.allclose(self.n.rec3d(), b.n.rec3d()):
            return (self.eqd-b.eqd)/hypot(b.n.x, b.n.y, b.n.z)
        else:
            print("Not Parallel")
            return

    def intersec(self, b: 'plane'):
        """Intersectiong line"""

        if np.allclose(self.n.rec3d(), b.n.rec3d()):
            print("Parallel")
            return

        if not(nearZero(det([[self.eqx,self.eqy],[b.eqx,b.eqy]]))):#test for unsolvable
            x,y=asolve([#Find remaining 2 axis when 1 is fixed
                [self.eqx,self.eqy],
                [b.eqx,b.eqy]
            ],[
                -self.eqd,
                -b.eqd
            ])
            return line([x,y,0],self.n@b.n)

        elif not(nearZero(det([[self.eqx,self.eqz],[b.eqx,b.eqz]]))):
            x,z=asolve([
                [self.eqx,self.eqz],
                [b.eqx,b.eqz]
            ],[
                -self.eqd,
                -b.eqd
            ])
            return line([x,0,z],self.n@b.n)

        elif not(nearZero(det([[self.eqy,self.eqz],[b.eqy,b.eqz]]))):
            y,z=asolve([
                [self.eqy,self.eqz],
                [b.eqy,b.eqz]
            ],[
                -self.eqd,
                -b.eqd
            ])
            return line([0,y,z],self.n@b.n)

        else:print("error")
