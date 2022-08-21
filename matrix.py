import numpy as np
from numpy.linalg import solve as asolve,inv
from .floatCalc import *
from .load import lda, ldae, ldf, ldfe
number = float|int

class Mat:
    a:np.ndarray
    log:list[str]

    def __init__(self,a:np.ndarray):
        self.a=a
        self.log=["Created"]

    def __repr__(self):
        string=""
        for i,j in enumerate(self.a):
            string+=f'{str(list(j))}\n'
        return string

    def __add__(self, new: "Mat"):
        if type(self) is type(new):
            return Mat(self.a+new.a)
        else:
            return Mat(self.a+new)

    def __sub__(self, new: "Mat"):
        if type(self) is type(new):
            return Mat(self.a-new.a)  # type: ignore
        else:
            return Mat(self.a-new)

    def __mul__(self, new: "Mat"):
        if type(self) is type(new):
            return Mat(self.a*new.a)
        else:
            return Mat(self.a*new)

    def __matmul__(self, new: 'Mat') :
        return Mat(self.a@new.a)

    def __neg__(self):
        return Mat(-self.a)

    def trans(self):
        return Mat(self.a.transpose())

    def tr(self) -> float:
        "trace"
        return self.a.trace()

    def inv(self):
        return Mat(inv(self.a))

    @staticmethod
    def matlab(ipt:str):
        ipt=ipt.strip("[]")
        l=np.array([[float(j) for j in i.split()] for i in ipt.split(";")])
        return Mat(l)

    @staticmethod
    def log2short(i:str):
        s=i.split()
        if s[0]=="Mul":
            if not nearZero(float(s[3])): return f'R{int(s[1])} * {float(s[3]):.4}'
        if s[0]=="Moved":
            if s[1]!=s[3]: return f'R{int(s[1])} ↔ R{int(s[3])}'
        if s[0]=="Added":
            if not nearZero(float(s[3])): return f'R{int(s[6])} {float(s[3]):+.4}*R{int(s[2])}'
        if s[0]=="Created":
            return ""
        return ""

    def log2emat(self,i:str):
        s=i.split()
        if s[0]=="Mul":
            arr = np.identity(self.a.shape[0])
            arr[int(s[1]),int(s[1])]=float(s[3])
            return Mat(arr)
        if s[0]=="Moved":
            arr = Mat(np.identity(self.a.shape[0]))
            arr.mov(int(s[1]),int(s[3]))
            return arr
        if s[0]=="Added":
            arr = np.identity(self.a.shape[0])
            arr[int(s[6]),int(s[2])]=float(s[3])
            return Mat(arr)
        if s[0]=="Created":
            return ""

    def slog(self):
        ret = [self.log2short(i) for i in self.log[1:]]
        return "\n".join([i for i in ret if i])

    def elog(self):
        arr = [self.log2emat(i) for i in self.log[1:]][::-1]
        fil=[i for i in arr if isinstance(i,Mat)]
        return [i for i in fil if not((i.a.shape[0] == i.a.shape[1]) and np.allclose(i.a, np.eye(i.a.shape[0])))]
    @staticmethod
    def make(x:int,y:int,eval:bool=False):
        if eval:
            a=ldae(x,y)
            return Mat(a)
        else:
            a=lda(x,y)
            return Mat(a)

    def mov(self,r1:int,r2:int):
        a=self.a.copy()
        a[r1]=self.a[r2]
        a[r2]=self.a[r1]
        self.a=a
        return self

    def mul(self,r:int,m:number):
        self.a[r]*=m
        self.log.append(f'Mul {r} by {m}')
        return self

    def addr(self,r1:int,r2:int,m:number):
        self.a[r1]+=self.a[r2]*m
        self.log.append(f'Added row {r2} {m} times to {r1}')
        return self

    def undo(self):
        if self.log.__len__()<2:
            return self
        s=self.log.pop().split()
        if s[0]=="Mul":
            self.mul(int(s[1]),1/float(s[3]))
        if s[0]=="Moved":
            self.mov(int(s[1]),int(s[3]))
        if s[0]=="Added":
            self.addr(int(s[6]),int(s[2]),-float(s[3]))
        self.log.pop()
        return self

    
    def ref(self):
        o=0
        for i in range(self.a.shape[0]):
            arr = list(self.a[i:,i+o])
            while not any(arr):
                o+=1
                if i+o > self.a.shape[1]-1 : return self
                arr = list(self.a[i:,i+o])
            try:
                n1 = arr.index(1)
                self.mov(n1+i,i)
            except ValueError as err:
                n1=arr.index(min([j for j in arr if j],key=abs))
                self.mov(n1+i,i)
                self.mul(i,1/min([j for j in arr if j],key=abs))
            finally:
                arr = list(self.a[i:,i])
                for j,k in enumerate(arr):
                    if j:
                        self.addr(j+i,i,-k)
        return self

    def rref(self):
        self.ref()
        o=0
        for i in range(self.a.shape[0]):
            arr = list(self.a[...,i+o])
            while not any(arr[i:]):
                o+=1
                if i+o > self.a.shape[1]-1 : return self
                arr = list(self.a[...,i+o])
            for j,k in enumerate(arr):
                if j!=i:
                    self.addr(j,i,-k)
        return self

    def dotE(self):
        return np.linalg.multi_dot(list(map(lambda a: a.a,self.elog())))

    def det(self):
        return np.linalg.det(self.dotE())

    def minor(self,r:int,c:int):
        return Mat(np.delete(np.delete(self.a,r,0),c,1))

    def cofactor(self,r:int,c:int):
        return (-1)**(r+c)*self.minor(r,c).det()

    def adj(self):
        return Mat(np.array([[self.cofactor(i,j) for i in range(self.a.shape[0])] for j in range(self.a.shape[1])]).T)

class AugMat(Mat):
    a:np.ndarray
    b:list[number]
    log:list[str]=[]

    def __init__(self,a:np.ndarray,b:list[number]):
        super().__init__(a)
        self.b=b

    def __repr__(self):
        string=""
        for i,j in enumerate(self.a):
            string+=f'{str(list(j))} : {self.b[i]}\n'
        return string

    @staticmethod
    def matlab(ipt: str):
        raise NotImplementedError

    @staticmethod
    def make(x:int,y:int,eval:bool=False,env:dict|None=None):
        if eval:
            a=ldae(x,y)
            b=[]
            ldfe(b,y,env)
            return AugMat(a,b)
        else:
            a=lda(x,y)
            b=[]
            ldf(b,y)
            return AugMat(a,b)

    def mov(self,r1:int,r2:int):
        super().mov(r1,r2)
        b1,b2=self.b[r1],self.b[r2]
        self.b[r2]=b1
        self.b[r1]=b2
        return self

    def mul(self,r:int,m:number):
        super().mul(r,m)
        self.b[r]*=m
        return self

    def addr(self,r1:int,r2:int,m:number):
        super().addr(r1,r2,m)
        self.b[r1]+=self.b[r2]*m
        return self

    def asolve(self):
        return asolve(self.a,self.b)