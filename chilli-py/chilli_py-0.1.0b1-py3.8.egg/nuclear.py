import numpy as np
from chilli_py.alias import factorial, dist2, div, norm, lgamma
from chilli_py.overlap import binomial_prefactor, gaussian_product_center
from chilli_py.PGBF import PGBF 
from chilli_py.CGBF import CGBF, contract 
from chilli_py.utils import myprint 
from chilli_py.atoms import Atoms 
from chilli_py.BasisSet import BasisSet
from copy import deepcopy 

""" Nuclear attraction term """

def Aterm(i,r,u,l1,l2,ax,bx,cx,gamma):
    """
       Aterm function

       Reference 
           - [THO1966] Eq. (2.18)
       
    """
    term1 = (-1)**(i+u)*binomial_prefactor(i,l1,l2,ax,bx)
    term2 = factorial(i)*cx**(i-2*r-2*u)
    term3 = (1/4/gamma)**(r+u)/factorial(r)/factorial(u)/factorial(i-2*r-2*u)
    return term1*term2*term3

def Aarray(l1,l2,a,b,c,g):
    """
        Aarray function

        Needs 
            - Aterm 
    """
    Imax = l1 + l2 + 1
    A = np.zeros(Imax,dtype=float)
    for i in range(Imax):
        for r in range(div(i,2)+1):
            for u in range(div(i-2*r,2)+1):
                I = i-2*r-u+1
                A[I-1] += Aterm(i,r,u,l1,l2,a,b,c,g)
    return A

def nuclear_attraction(a, b, ccenter):
    """
        nuclear_attraction
        Nuclear attraction between two Gaussians a and b 
        with center ccenter.

        Input 
            - a,b: PGBF()
            - ccenter: np.array(), 3D cartesian coordinate 

        Needs
            - gaussian_product_center 
            - Aarray 
            - dist2 
            - Fgamma

        Reference 
            - [THO1966](H. Taketa, S. Huzinaga, and K. O-ohata. H. Phys. Soc. Japan, 21, 2313, 1966.)
              + https://journals.jps.jp/doi/abs/10.1143/JPSJ.21.2313  
            - [THO1966] Eq. (2.17) 
    """
    ax, ay, az = a.center[0],a.center[1],a.center[2]
    bx, by, bz = b.center[0],b.center[1],b.center[2]

    aI,aJ,aK = a.power[0],a.power[1],a.power[2]
    bI,bJ,bK = b.power[0],b.power[1],b.power[2]

    cx, cy, cz = ccenter[0],ccenter[1],ccenter[2]

    p = gaussian_product_center(a,b)
    px, py, pz = p 
    
    gamma = a.expn + b.expn

    rab2 = dist2(a.center-b.center)
    rcp2 = dist2(ccenter - p)
    
    Ax = Aarray(aI,bI,px-ax,px-bx,px-cx,gamma)
    Ay = Aarray(aJ,bJ,py-ay,py-by,py-cy,gamma)
    Az = Aarray(aK,bK,pz-az,pz-bz,pz-cz,gamma)
    
    total = 0
    for I in range(aI+bI+1):
        for J in range(aJ+bJ+1):
            for K in range(aK+bK+1):
                total += Ax[I]*Ay[J]*Az[K]*Fgamma(I+J+K,rcp2*gamma)

    val = -2.0*np.pi*np.exp(-a.expn*b.expn*rab2/gamma)*total/gamma
    return val

def nuclear_attraction_pgbf_atom(a,b,ccenter,atno):
    """
        nuclear_attraction_pgbf_atom
        Nuclear attraction for PGBFs a and b
        and one atom (ccenter,atno).
    """
    Vab = nuclear_attraction(a,b, ccenter)
    return atno*a.NORM*b.NORM*Vab

def nuclear_attraction_pgbf_atoms(a,b,atoms): 
    """
        nuclear_attraction_pgbf_atom
        Nuclear attraction for PGBFs a and b
        and all atoms.
    """
    Vab = 0.0
    for ia,iZ in enumerate(atoms.Z):
        ccenter = atoms.pos[ia]
        Vab = Vab + nuclear_attraction_pgbf_atom(a,b,ccenter, iZ)
    return Vab

def Fgamma(m,x,SMALL=1e-12):
    """
        Fgamma 
        Incomplete gamma function
    """
    # Evidently needs underflow protection
    x = max(x,SMALL) 
    return 0.5*x**(-m-0.5)*gammainc(m+0.5,x)

def gammainc(a,x):
    """
        gammainc 
        
        This is the series version of gamma from pyquante. 
        Note: There seem to be issues around a~1. 

        Needs
            - gser
            - gcf

        Reference 
            - https://github.com/rpmuller/pyquante2/blob/6e34cb4480ae7dbd8c5e44d221d8b27584890c83/pyquante2/utils.py#L67
    """
    if abs(a-1) < 1e-3:
        print("Warning: gammainc_series is known to have problems for a ~ 1")
    if x < (a+1.0):
        #Use the series representation
        gam,gln = gser(a,x)
    else:
        #Use continued fractions
        gamc,gln = gcf(a,x)
        gam = 1-gamc
    return np.exp(gln)*gam

def gser(a, x, ITMAX=100, EPS=3e-9 ): 
    """
        gser
        Series representation of Gamma (gser). 

        Reference 
            - https://github.com/rpmuller/pyquante2/blob/6e34cb4480ae7dbd8c5e44d221d8b27584890c83/pyquante2/utils.py#L86
    """
    gln = lgamma(a)
    if x == 0:
        return 0,gln
    ap = a
    delt = s = 1/a
    for i in range(ITMAX):
        ap += 1
        delt *= (x/ap)
        s += delt
        if abs(delt) < abs(s)*EPS:
            break
    return s*np.exp(-x+a*np.log(x)-gln),gln

def gcf(a,x,ITMAX=200,EPS=3e-9,FPMIN=1e-30):
    """
        gcf 
        Continued fraction representation of Gamma (gcf). 

        Reference 
            - https://github.com/rpmuller/pyquante2/blob/6e34cb4480ae7dbd8c5e44d221d8b27584890c83/pyquante2/utils.py#L107
    """
    gln = lgamma(a)
    b = x + 1.0 - a
    c = 1.0/FPMIN
    d = 1.0/b
    h = d
    for i in range(1,ITMAX+1):
        an = -i*(i-a)
        b = b + 2.0
        d = an*d + b
        if abs(d) < FPMIN:
            d = FPMIN
        c = b + an/c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0/d
        delt = d*c
        h = h*delt
        if abs(delt-1.0) < EPS:
            break
    gammcf = np.exp(-x + a*np.log(x) - gln)*h
    return gammcf,gln

def nuclear_attraction_cgbf_atom(a,b,ccenter,atno): 
    """
        nuclear_attraction_cgbf_atom
        Nuclear attraction for two CGBFs and one atom. 
    """
    na = lambda a,b: nuclear_attraction_pgbf_atom(a,b,ccenter,atno)
    return contract(na,a,b)

def nuclear_attraction_cgbf_atoms(a,b,atoms): 
    """
        nuclear_attraction_cgbf_atom
        Nuclear attraction for two CGBFs and all atoms.
    """
    na = lambda a,b: nuclear_attraction_pgbf_atoms(a,b,atoms)
    val = contract(na,a,b)
    return val 

# SS 
#def nuclear_attraction_cgbf_atoms(a, b, atoms):
#    """
#       same as the previous function 
#       only written explictly 
#    """
#    Vab = 0.0
#    for ia,iZ in enumerate(atoms.Z):
#        ccenter = atoms.pos[ia]
#        myprint(Vab=Vab)
#        na = lambda a,b: nuclear_attraction_pgbf_atom( a, b, ccenter, iZ )
#        Vab_tmp = contract(na,a,b)
#        Vab += Vab_tmp
#        #Vab = Vab + nuclear_attraction_pgbf_atom(a,b,ccenter, iZ)
#    return Vab


def nuclear_repulsion_ij(ZA,posA,ZB,posB): 
    """
        nuclear_repulsion_ij
        Calculate nuclear repulsion
        for one pair of nuclei (ZA,posA) and (ZB,posB). 
    """
    dr = posA-posB
    return ZA*ZB/norm(dr)

def nuclear_repulsion(atoms):
    """
        nuclear_repulsion
        Nuclear repulsion for a atoms object.

        Needs
            - nuclear_repulsion_ij

        Input
            - atoms, Atoms(), contains sym and pos
    """
    nr = 0.0
    for ia,ipos in enumerate(atoms.pos):
        for ja,jpos in enumerate(atoms.pos):
            if ia > ja: 
                dr = ipos-jpos
                nr = nr + nuclear_repulsion_ij(atoms.Z[ia],ipos,atoms.Z[ja],jpos)
    return nr

def main():
    """
        main 
        Main function to test this routine. 
    """
    center = [1.4,0.0,0.0]
    power = [0,0,0]
    expn = 2
    coef = 2 
    s = PGBF(center,power,expn)

    c = CGBF(center,power)
    c.add(coef,expn)

    c2 = CGBF([0,0,0],power)
    c2.add(coef,expn)

    print(s)
    print(c)

    Vab = nuclear_attraction_pgbf_atom( s,s, (0.0,0.0,0.0), 1)
    print(f"Vab = {Vab: 18.10f}\n")

    Vab = nuclear_attraction_cgbf_atom( c,c, (0.0,0.0,0.0), 1)
    print(f"Vab = {Vab: 18.10f}\n")

    Vab = nuclear_attraction_cgbf_atom( c,c2, (0.0,0.0,0.0), 1)
    print(f"Vab = {Vab: 18.10f}\n")

    atoms = Atoms(['H','H'],[[0,0,0],[1.4,0,0]])
    basis = BasisSet.initialize(atoms,basis_name="sto-3g")

    Nbasis = len(basis)
    for i in range(Nbasis):
        print("--------")
        print(f"Basis # {i}")
        print("--------")
        print(basis.basis[i])

    H1s  = basis.basis[0]
    H2s  = basis.basis[1]
    myprint(H1s=H1s)

    Vab_1 = nuclear_attraction_cgbf_atom(H1s,H2s,(0,0.0,0.0),1)
    print(f"Vab_1 = {Vab_1}")
    Vab_2 = nuclear_attraction_cgbf_atom(H1s,H2s,(1.4,0.0,0.0),1)
    print(f"Vab_2 = {Vab_2}")
    Vab = Vab_1 + Vab_2
    print(f"Vab = {Vab}")
    ENN = nuclear_repulsion(atoms)
    print(f"ENN = {ENN}")

if __name__ == '__main__':
    main()
