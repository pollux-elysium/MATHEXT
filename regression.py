from load import ldfe,ldf


number = float|int

class Reg:
    x:list[number]
    fx:list[number]

    def __init__(self,x:list[number],fx:list[number]):
        if len(x) == len(fx):
            self.x=x
            self.fx=fx
        else:
            raise ValueError

    @staticmethod
    def make(n:int=0,eval:bool=False):
        if eval:
            x=[]
            ldfe(x,n)
            fx=[]
            ldfe(fx,n)
            return Reg(x,fx)
        else:
            x=[]
            ldf(x,n)
            fx=[]
            ldf(fx,n)
            return Reg(x,fx)

    @staticmethod
    def lot(n:list[tuple[number,number]]):
        x,fx = [],[]
        for i in n:
            a,b=i
            x.append(a)
            fx.append(b)
        return Reg(x,fx)