import numpy as np 
from chilli_py.alias import factorial, dist2, div
from chilli_py.overlap import binomial_prefactor,gaussian_product_center, overlap
from chilli_py.nuclear import Fgamma
from chilli_py.PGBF import PGBF
from chilli_py.CGBF import CGBF, contract_4c
from chilli_py.utils import myprint 

""" Two electron integrals """

def coulomb(a,b,c,d):
    """
        coulomb 
        Calculate Coulomb between four Gaussians (a,b,c,d). 

        This is the slow method of computing integrals from Huzinaga et al.

        Input
            - a,b,c,d: PGBF()

        Needs
            - dist2 
            - gaussian_product_center
            - Fgamma
            - Barray

        Reference 
            - [THO1966](H. Taketa, S. Huzinaga, and K. O-ohata. H. Phys. Soc. Japan, 21, 2313, 1966.)
              + https://journals.jps.jp/doi/abs/10.1143/JPSJ.21.2313  
    """

    ax, ay, az = a.center[0], a.center[1], a.center[2]
    bx, by, bz = b.center[0], b.center[1], b.center[2]
    cx, cy, cz = c.center[0], c.center[1], c.center[2]
    dx, dy, dz = d.center[0], d.center[1], d.center[2]              

    aI, aJ, aK = a.power[0], a.power[1], a.power[2]
    bI, bJ, bK = b.power[0], b.power[1], b.power[2]
    cI, cJ, cK = c.power[0], c.power[1], c.power[2]
    dI, dJ, dK = d.power[0], d.power[1], d.power[2]

    rab2 = dist2(a.center - b.center)
    rcd2 = dist2(c.center - d.center)

    p = gaussian_product_center(a,b)
    px,py,pz = p
    q = gaussian_product_center(c,d)
    qx,qy,qz = q 
    rpq2 = dist2(p-q)

    g1 = a.expn + b.expn
    g2 = c.expn + d.expn
    delta = 0.25*(1/g1+1/g2)

    Bx = Barray(aI,bI,cI,dI,px,ax,bx,qx,cx,dx,g1,g2,delta)
    By = Barray(aJ,bJ,cJ,dJ,py,ay,by,qy,cy,dy,g1,g2,delta)
    Bz = Barray(aK,bK,cK,dK,pz,az,bz,qz,cz,dz,g1,g2,delta)

    s = 0
    for I in range(aI+bI+cI+dI+1):
        for J in range(aJ+bJ+cJ+dJ+1):
            for K in range(aK+bK+cK+dK+1):
                s += Bx[I]*By[J]*Bz[K]*Fgamma(I+J+K,0.25*rpq2/delta)
    return 2*np.pi**(2.5)/(g1*g2*np.sqrt(g1+g2))*np.exp(-a.expn*b.expn*rab2/g1)*np.exp(-c.expn*d.expn*rcd2/g2)*s

def coulomb_pgbf(a,b,c,d):
    """
        coulomb_pgbf
        Calculate Coulomb for four PGBFs (a,b,c,d).

        Input 
            - a, b, c, d: PGBF() 
    """
    return a.NORM*b.NORM*c.NORM*d.NORM*coulomb(a,b,c,d)

def fB(i, l1, l2, p, a, b, r, g):
    """
        fB

        Needs
            - binomial_prefactor
            - B0
    """
    return binomial_prefactor(i,l1,l2,p-a,p-b)*B0(i,r,g)

def B0(i,r,g):
    """
        B0

        Needs 
            - fact_ratio2
    """
    return fact_ratio2(i,r)*(4*g)**(r-i)

def fact_ratio2(a, b):
    """
        fact_ratio2

        Needs 
            - factorial
    """
    return factorial(a)/factorial(a-2*b)/factorial(b)

def Bterm(i1,i2,r1,r2,u,l1,l2,l3,l4,Px,Ax,Bx,Qx,Cx,Dx,gamma1,gamma2,delta):
    """
        Bterm

        Reference 
            - [THO1966] Eq. 2.22
    """
    val = (-1)**(i2+u)*fB(i1,l1,l2,Px,Ax,Bx,r1,gamma1)*fB(i2,l3,l4,Qx,Cx,Dx,r2,gamma2)*(
          fact_ratio2(i1+i2-2*(r1+r2),u)*(Qx-Px)**(i1+i2-2*(r1+r2)-2*u)/delta**(i1+i2-2*(r1+r2)-u))
    return val

def Barray(l1,l2,l3,l4,p,a,b,q,c,d,g1,g2,delta):
    """
        Barray

        Needs 
            - Bterm 
    """
    Imax = l1+l2+l3+l4+1
    B = np.zeros(Imax)
    for i1 in range(l1+l2+1):
        for i2 in range(l3+l4+1):
            for r1 in range(div(i1,2)+1):
              for r2 in range(div(i2,2)+1):
                  for u in range(div(i1+i2,2)-r1-r2+1):
                      I = i1+i2-2*(r1+r2)-u
                      B[I] += Bterm(i1,i2,r1,r2,u,l1,l2,l3,l4,p,a,b,q,c,d,g1,g2,delta)
    return B

def coulomb_cgbf(a,b,c,d):
    """
        coulomb_cgbf
        Calculate Coulomb for four Gaussians (a,b,c,d).         

        Input 
            - a,b,c,d, CGPF()
    """
    return contract_4c(coulomb_pgbf,a,b,c,d)

def main():
    """
        main 
        Main function to test this routine. 
    """
    print("Calling test_two_terms\n")
    
    assert fB(0,0,0,0.0,0.0,0.0,0,2.0) == 1
    assert fB(0,0,0,1.0,1.0,1.0,0,2.0) == 1
    assert fB(0,0,0,0.0,0.0,0.0,0,2.0 ) == 1
    assert fB(1,0,1,0.0,0.0,0.0,0,2.0 ) == 0.125
    assert B0(0,0,2.0) == 1
    assert fact_ratio2(0,0) == 1
    assert Bterm(0,0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,2.0,0.25)==1
    assert Bterm(0,1,0,0,0,0,0,0,1,0.0,0.0,0.0,0.0,0.0,0.0,2.0,2.0,0.25)==0
    
    print("Pass test_two_terms\n")
    
    
    print("Calling test_coul1\n")
    center = [0,0.0,0.0]
    s = PGBF(center,[0,0,0],1)
    px = PGBF(center,[1,0,0],1)
    coul = coulomb(s,s,s,px)
    print(coul)
    assert coul==0 # 0
    coul = coulomb_pgbf(s,s,px,px)
    print(coul)
    assert np.isclose(coul,0.9403159725793305)
    print("Pass test_coul1\n")

if __name__ == '__main__':
    main()

