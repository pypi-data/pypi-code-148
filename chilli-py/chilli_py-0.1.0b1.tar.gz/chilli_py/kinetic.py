import numpy as np 
from chilli_py.overlap import overlap, overlap_pgbf
from chilli_py.PGBF import PGBF
from chilli_py.CGBF import CGBF, contract
from chilli_py.utils import myprint
from copy import deepcopy 

"""  Kinetic matrix elements """

def kinetic_pgbf(a, b):
    """
        kinetic_pgbf
        Kinetic matrix elements for PGBFs a and b,

        Input 
            - a,b: PGBF()
    """
    K = kinetic(a,b)
    return a.NORM*b.NORM*K

def kinetic(a0,b0):
    """
        kinetic
        Kinetic matrix elements for Gaussians a and b.

        Input 
            - a0, b0: PGBF() 
    """
    # SS: deepcopy needed b/c of the middle block assigments 
    a = deepcopy(a0)
    b = deepcopy(b0)
    ax, ay, az = a.center[0],a.center[1],a.center[2]
    bx, by, bz = b.center[0],b.center[1],b.center[2]
              
    aI,aJ,aK = a.power[0],a.power[1],a.power[2]
    bI,bJ,bK = b.power[0],b.power[1],b.power[2]

    bpower0 = b.power 
    overlap0  = overlap(a,b)
    b.power = [bI+2,bJ,bK]
    overlapx1 = overlap(a,b)
    b.power = [bI,bJ+2,bK]
    overlapy1 = overlap(a,b)
    b.power = [bI,bJ,bK+2]
    overlapz1 = overlap(a,b)
    b.power = [bI-2,bJ,bK]
    overlapx2 = overlap(a,b)
    b.power = [bI,bJ-2,bK]
    overlapy2 = overlap(a,b)
    b.power = [bI,bJ,bK-2]
    overlapz2 = overlap(a,b)
    b.power = bpower0 
    term0 = b.expn*( 2 * (bI + bJ + bK) + 3)*overlap0
    term1 = -2*(b.expn**2)*(overlapx1 + overlapy1 + overlapz1)
    term2 = -0.5*(bI*(bI-1)*overlapx2+bJ*(bJ-1)*overlapy2 + bK*(bK-1)*overlapz2)
    return term0 + term1 + term2

def kinetic_cgbf(a, b):
    """
        kinetic_cgbf
        Kinetic matrix elements for CGBFs a and b. 

        Input 
            - a,b: CGBF() 
    """
    return contract(kinetic_pgbf,a,b)

def main():
    """
        main 
        Main function to test this routine. 
    """
    center = [0.0,0.0,0.0]
    power = [0,0,0]
    expn = 1
    coef = 1
    s = PGBF(center,power,expn)
    print(s)

    c = CGBF(center,power)
    c.add(coef,expn)
 
    k = kinetic(s,s) 
    print(k)
    assert np.isclose(k,2.9530518648229536)
    k = kinetic_pgbf(s,s)
    print(k)
    assert np.isclose(k,1.5)
    print("test_kinetic is passed\n")

if __name__ == '__main__':
    main() 
