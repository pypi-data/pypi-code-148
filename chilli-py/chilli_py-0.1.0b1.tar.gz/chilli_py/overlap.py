import numpy as np 
from chilli_py.alias import dist2, factorial2, binomial, div
from chilli_py.utils import myprint

""" One-electron integrals/ overlap matrix elements """

def overlap_pgbf(a,b):
    """
        overlap_pgbf
        Calculate overlap between two primitive 
        Gaussians.

        Input 
            - a,b: PGBF() 
    """
    s = overlap(a,b)
    return a.NORM*b.NORM*s

def overlap(a,b): 
    """
        overlap
        Calculate overlap between Gaussians a and b. 

        Input
            - a,b: PGBF()
    """
    ax, ay, az = a.center 
    bx, by, bz = b.center 

    aI,aJ,aK = a.power
    bI,bJ,bK = b.power

    gamma = a.expn + b.expn
    px,py,pz = gaussian_product_center(a,b)

    rab2 = dist2(a.center-b.center)
    pre = (np.pi/gamma)**1.5*np.exp(-a.expn*b.expn*rab2/gamma)
    
    wx = overlap1d(aI,bI,px-ax,px-bx,gamma)
    wy = overlap1d(aJ,bJ,py-ay,py-by,gamma)
    wz = overlap1d(aK,bK,pz-az,pz-bz,gamma)
    
    O = pre*wx*wy*wz
    return O 

def gaussian_product_center(a,b): 
    """ 
        gaussian_product_center
        Calculate Gaussian product center for 
        two Gaussian (a,b). 

        Input 
            - a,b: PGBF()
    """
    return (a.expn*a.center+b.expn*b.center)/(a.expn+b.expn)

def overlap1d(la,lb,ax,bx,gamma):
    """
        overlap1d
    """
    total = 0
    for i in range(div(la+lb,2)+1):
        tmp = binomial_prefactor(2*i,la,lb,ax,bx)*factorial2(2*i-1)/(2*gamma)**i
        total += tmp 
    return total

def binomial_prefactor(s,ia,ib,xpa,xpb):
    """
        binomial_prefactor
    """
    total = 0
    for t in range(s+1):
        if (s-ia) <= t <= ib:
            tmp = binomial(ia,s-t)*binomial(ib,t)*xpa**(ia-s+t)*xpb**(ib-t)
            total += tmp 
    return total
