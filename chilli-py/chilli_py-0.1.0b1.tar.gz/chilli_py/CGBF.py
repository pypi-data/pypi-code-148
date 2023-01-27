import numpy as np 
from chilli_py.overlap import overlap, overlap_pgbf 
from chilli_py.PGBF import PGBF

class CGBF: 
    """
        Contracted Gaussian Basis functions (CGBF)
        CGBF consist of primitive Gaussian Basis functions (PGBF).
    """
    def __init__(self,center,power):
        """
            __init__ 
            Initialize instance of the class. 
        """
        self.center = center 
        self.power = power 
        self.pgbfs = [] 
        self.coefs = [] 
        self.NORM = 1 
        self.Ncontr = len(self.pgbfs)

    def overlap(self,a,b):
        """
            overlap 
            Calculate overlap between a and b. 
            Is used by normalize. 
        """
        return contract(overlap_pgbf,a,b)

    def normalize(self):
        """
            normalize 
            (Self) normalize
            Calculate norm. 
        """
        NORM = 1/np.sqrt(self.overlap(self,self))
        self.NORM *= NORM
        return NORM 

    def eval(self,coord):
        """
            eval 
            Evaluate Gaussian at coord = (x,y,z). 
        """
        s = 0
        for c,pg in zip(self.coefs,self.pgbfs):
            s += c*pg.eval(coord)
        return self.NORM*s

    def grad(self,coord):
        """
           grad
        """
        val = np.zeros(3)
        for c,pg in zip(self.coefs,self.pgbfs):
            val += c*pg.grad(coord)
        return self.NORM*val 

    def __repr__(self): 
        """
            __repr__ 
            Representation of the class.
            Used by 
                - show
        """
        s = ""
        s += f"Ncontr : {self.Ncontr: d}\n"
        s += f"NORM : {self.NORM}\n"
        for i in range(self.Ncontr):
            s += f"Coef : {self.coefs[i]: 18.10f}\n"
            s += self.pgbfs[i].__repr__()
        return s 

    def show(self): 
        """
            show 
            Show the representation. 
        """
        print(self.__repr__)
       
    def add(self,coef,expn):
        """
            add 
            Add a primitive Gaussian to 
            the contracted Gaussian and 
            update norm. 
        """
        pg = PGBF(self.center,self.power,expn)
        self.pgbfs.append(pg)
        self.coefs.append(coef) 
        self.normalize()
        self.Ncontr = len(self.pgbfs)

def contract(f,a,b):
    """
        contract 
        Contract two Gaussians (a,b). 
    """
    s = 0.0
    for (ca,abf) in zip(a.coefs,a.pgbfs):
        for (cb,bbf) in zip(b.coefs,b.pgbfs):
            s += ca*cb*f(abf,bbf)
    return a.NORM*b.NORM*s

def contract_4c(f,a,b,c,d):
    """
        contract_4c 
        Contract four Gaussians (a,b,c,d). 
    """
    s = 0
    for (ca,abf) in zip(a.coefs,a.pgbfs):
        for (cb,bbf) in zip(b.coefs,b.pgbfs):
            for (cc,cbf) in zip(c.coefs,c.pgbfs):
                for (cd,dbf) in zip(d.coefs,d.pgbfs):
                    s += ca*cb*cc*cd*f(abf,bbf,cbf,dbf)
    return a.NORM*b.NORM*c.NORM*d.NORM*s

def overlap_cgbf(a,b):
    """ 
        overlap_cgbf
        Calculate overlap between Gaussians (a,b). 
    """
    return contract(overlap_pgbf,a,b)
