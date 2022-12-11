import numpy as np
from numpy.linalg import solve as asolve,inv
from .floatCalc import *
from .load import lda, ldae, ldf, ldfe
number = float|int

class Mat:
    """Matrix class wrapper for numpy.ndarray"""
    a:np.ndarray #array
    log:list[str] #log of operations

    def __init__(self,a:np.ndarray):
        """Initializes matrix
        
        Args:
            a (np.ndarray): Matrix to be wrapped
            
        Returns:
            Mat: Matrix object
        """
        self.a=a
        self.log=["Created"]

    def __repr__(self):
        string=""
        for i,j in enumerate(self.a):
            string+=f'{str(list(map(lambda x: round(x,5),list(j))))}\n'
        return string

    def __add__(self, new: "Mat"):
        """Adds two matrices together or a number elementwise"""
        if type(self) is type(new):
            return Mat(self.a+new.a)
        else:
            return Mat(self.a+new)

    def __sub__(self, new: "Mat"):
        """Subtracts two matrices or a number elementwise"""
        if type(self) is type(new):
            return Mat(self.a-new.a)  # type: ignore
        else:
            return Mat(self.a-new)

    def __mul__(self, new: "Mat"):
        """Multiplies two matrices or a number elementwise"""
        if type(self) is type(new):
            return Mat(self.a*new.a)
        else:
            return Mat(self.a*new)

    def __matmul__(self, new: 'Mat') :
        """Matrix multiplication"""
        return Mat(self.a@new.a)

    def __pow__(self, power: int):
        """Matrix power"""
        if power==0:
            return Mat(np.identity(self.a.shape[0]))
        if power==1:
            return self
        return self*self**(power-1)

    def __neg__(self):
        """Negates matrix"""
        return Mat(-self.a)

    def trans(self):
        """Transpose"""
        return Mat(self.a.transpose())

    def tr(self) -> float:
        "Trace"
        return self.a.trace()

    def inv(self):
        """Inverse"""
        return Mat(inv(self.a))

    @staticmethod
    def matlab(ipt:str):
        """Converts matlab matrix to Mat object

        Args:
            ipt (str): Matlab matrix

        Returns:
            Mat: Mat object
        """
        ipt=ipt.strip("[]")
        l=np.array([[float(j) for j in i.split()] for i in ipt.split(";")])
        return Mat(l)

    @staticmethod
    def log2short(i:str):
        """Converts log to shorthand form

        Args:
            i (str): Log

        Returns:
            str: Shorthand form
        """
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
        """Converts log to elementary matrix form

        Args:
            i (str): Log

        Returns:
            Mat: Mat object
        """
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
        """Returns log in shorthand form"""
        ret = [self.log2short(i) for i in self.log[1:]]
        return "\n".join([i for i in ret if i])

    def elog(self):
        """Returns log in elementary matrix form"""
        arr = [self.log2emat(i) for i in self.log[1:]][::-1]
        fil=[i for i in arr if isinstance(i,Mat)]
        return [i for i in fil if not((i.a.shape[0] == i.a.shape[1]) and np.allclose(i.a, np.eye(i.a.shape[0])))]

    @staticmethod
    def make(x:int,y:int,eval:bool=False):
        """Macro for creating matrix based on lda or ldae
        
        Args:
            x (int): Number of rows
            y (int): Number of columns
            eval (bool, optional): Whether to use load.ldae or load.lda. Defaults to False.
            
        Returns:
            Mat: Mat object
        """
        if eval:
            a=ldae(x,y)
            return Mat(a)
        else:
            a=lda(x,y)
            return Mat(a)

    def mov(self,r1:int,r2:int):
        """Row Operation: Swap row
        
        Args:
            r1 (int): Row 1
            r2 (int): Row 2

            Array starts from 0
            
        Returns:
            Mat: Mat object (self)
        """
        a=self.a.copy()
        a[r1]=self.a[r2]
        a[r2]=self.a[r1]
        self.a=a
        self.log.append(f'Moved {r1} and {r2}')
        return self

    def mul(self,r:int,m:number):
        """Row Operation: Multiply row

        Args:
            r (int): Row
            m (number): Multiplier

            Array starts from 0

        Returns:
            Mat: Mat object (self)
        """
        self.a[r]*=m
        self.log.append(f'Mul {r} by {m}')
        return self

    def addr(self,r1:int,r2:int,m:number):
        """Row Operation: Add row

        Args:
            r1 (int): Add to this row
            r2 (int): Add from this row
            m (number): Multiplier

            Array starts from 0

        Returns:
            Mat: Mat object (self)
        """
        self.a[r1]+=self.a[r2]*m
        self.log.append(f'Added row {r2} {m} times to {r1}')
        return self

    def undo(self):
        """Undo last operation"""
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
        """Converts to reduced echelon form

        Returns:
            Mat: Mat object (self)
        """
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
        """Converts to reduced row echelon form

        Returns:
            Mat: Mat object (self)
        """

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
        """Returns dot product of elementary matrices

        Returns:
            Mat: Mat object
        """
        return np.linalg.multi_dot(list(map(lambda a: a.a,self.elog())))

    def det(self) -> number:
        """Returns determinant of matrix

        Returns:
            number: Determinant
        """
        return np.linalg.det(self.a)

    def minor(self,r:int,c:int):
        """Returns minor of matrix at row r and column c

        Args:
            r (int): Row
            c (int): Column

            Array starts from 0

        Returns:
            Mat: Mat object
        """
        return Mat(np.delete(np.delete(self.a,r,0),c,1))

    def cofactor(self,r:int,c:int) -> number:
        """Returns cofactor of matrix at row r and column c

        Args:
            r (int): Row
            c (int): Column

            Array starts from 0

        Returns:
            number: Cofactor
        """
        return (-1)**(r+c)*self.minor(r,c).det()

    def adj(self):
        """Returns adjoint of matrix

        Returns:
            Mat: Mat object
        """
        return Mat(np.array([[self.cofactor(j,i) for i in range(self.a.shape[1])] for j in range(self.a.shape[0])]).T)

    def cofactorMatrix(self):
        """Returns cofactor matrix of matrix

        Returns:
            Mat: Mat object
        """
        return Mat(np.array([[self.cofactor(j,i) for i in range(self.a.shape[1])] for j in range(self.a.shape[0])]))

    def eigenVector(self):
        """Returns eigen vectors of matrix
        
        Returns:
            tuple: numpy.linalg.eig tuple
        """
        return np.linalg.eig(self.a)

    def eigenValue(self):
        """Returns eigen values of matrix

        Returns:
            tuple: Tuple of eigen values
        """
        return np.linalg.eigvals(self.a)

class AugMat(Mat):
    a:np.ndarray
    b:list[number]
    log:list[str]=[]

    def __init__(self,a:np.ndarray,b:list[number]):
        """Initializes AugMat object

        Args:
            a (np.ndarray): Matrix
            b (list[number]): List of constants
        """
        super().__init__(a)
        self.b=b

    def __repr__(self):
        string=""
        for i,j in enumerate(self.a):
            string+=f'{str(list(j))} : {self.b[i]}\n'
        return string

    @staticmethod
    def matlab(ipt: str):
        """NOT IMPLEMENTED
        
        Converts matlab matrix to AugMat object

        Args:
            ipt (str): Matlab matrix

        Returns:
            AugMat: AugMat object
        """
        raise NotImplementedError

    @staticmethod
    def make(x:int,y:int,eval:bool=False,env:dict|None=None):
        """Creates AugMat object with lda or ldae then ldf or ldfe

        Args:
            x (int): Number of rows
            y (int): Number of columns
            eval (bool, optional): Whether to evaluate. Defaults to False.
            env (dict|None, optional): Environment. Defaults to None. globals() can be used

        Returns:
            AugMat: AugMat object
        """
            
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
        """Solves augmented matrix
        
        Returns:
            list[number]: List of solutions
        """
        return asolve(self.a,self.b)

    def detArr(self):
        """Returns determinant of cramers rule

        Returns:
            list[number]: List of determinants
        """
        o:list[number]=[]
        for i,j in enumerate(self.b):
            a=self.a.copy()
            a[:,i]=np.array(self.b)
            o.append(np.linalg.det(a))
        return o