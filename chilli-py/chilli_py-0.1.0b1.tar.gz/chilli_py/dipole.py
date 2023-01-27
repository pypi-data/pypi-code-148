import numpy as np
from chilli_py.overlap import gaussian_product_center

def E(i,j,t,Qx,a,b):
    """
        E 
        Recursive definition of Hermite Gaussian coefficients.

        Input 
            - a: orbital exponent on Gaussian 
            - b: orbital exponent on Gaussian 
            - i,j: orbital angular momentum number on Gaussian
            - t: number nodes in Hermite 
                 It depends on type of integral, e.g., always zero for overlap integrals.
            - Qx: distance between origins of Gaussian (a,b) 
            
        Output 
            - float 

        Needs
            - E (Recursion) 
    """
    p = a + b
    q = a*b/p
    if (t < 0) or (t > (i + j)):
        # out of bounds for t
        return 0.0
    elif i == j == t == 0:
        # base case
        return np.exp(-q*Qx*Qx)
    elif j == 0:
        # decrement index i
        return (1/(2*p))*E(i-1,j,t-1,Qx,a,b) - (q*Qx/a)*E(i-1,j,t,Qx,a,b) + \
               (t+1)*E(i-1,j,t+1,Qx,a,b)
    else:
        # decrement index j
        return (1/(2*p))*E(i,j-1,t-1,Qx,a,b) + (q*Qx/b)*E(i,j-1,t,Qx,a,b) + \
               (t+1)*E(i,j-1,t+1,Qx,a,b)

def dipole_cgbf(a,b,direction,center=np.zeros((3))):
    """
        dipole_cgbf 
        Multipole matrix, i.e., Dipole, elements for Gaussian a and b.
        Element is here the component the respective direction. 

        Needs
            - dipole
            - shell == power 
    """
    mu = 0.0
    for ia,(ca,abf) in enumerate(zip(a.coefs,a.pgbfs)):
        for ib,(cb,bbf) in enumerate(zip(b.coefs,b.pgbfs)):
            mui = abf.NORM*bbf.NORM*ca*cb*dipole(abf,bbf,direction=direction,center=center)
            mu += mui
    return mu

def dipole(a,b,direction="x",center=np.zeros((3))):
    """
        dipole 
        Get dipole matrix element for primitive Gaussians a and b. 

        Needs
            - E 

        Reference
            -  McMurchie-Davidson:
                + https://github.com/jjgoings/McMurchie-Davidson/blob/dcff9d232f7950f2e6b0b879387c76bb83ebf812/mmd/backup/reference-integrals.py
                + https://github.com/jjgoings/McMurchie-Davidson/blob/dcff9d232f7950f2e6b0b879387c76bb83ebf812/mmd/integrals/reference.py

        Notes 
            + It is similar to the overlap
            + However it uses the recursion (E) instead of overlap1d 
            - McMurchie-Davidson: 
                + lmn: power 
                + a,b: expn 
                + A,B,C:  center of Gaussians 
    """
    ax, ay, az = a.center
    bx, by, bz = b.center
    cx, cy, cz = center 

    aI,aJ,aK = a.power
    bI,bJ,bK = b.power

    gamma = a.expn + b.expn

    P = gaussian_product_center(a,b)
    px, py, pz = P 
    pre = np.power(np.pi/(gamma),1.5)

    if direction == 'x':
        pcx = px - cx
        dx  = E(aI,bI,1,ax-bx,a.expn,b.expn) + pcx*E(aI,bI,0,ax-bx,a.expn,b.expn)
        wy = E(aJ,bJ,0,ay-by,a.expn,b.expn)
        wz = E(aK,bK,0,az-bz,a.expn,b.expn)
        mu = pre*dx*wy*wz
    elif direction == 'y':
        pcy = py - cy
        wx = E(aI,bI,0,ax-bx,a.expn,b.expn)
        dy = E(aJ,bJ,1,ay-by,a.expn,b.expn) + pcy*E(aJ,bJ,0,ay-by,a.expn,b.expn)
        wz = E(aK,bK,0,az-bz,a.expn,b.expn)
        mu = pre*wx*dy*wz
    elif direction == 'z':
        pcz = pz - cz
        wx = E(aI,bI,0,ax-bx,a.expn,b.expn)
        wy = E(aJ,bJ,0,ay-by,a.expn,b.expn)
        dz = E(aK,bK,1,az-bz,a.expn,b.expn) + pcz*E(aK,bK,0,az-bz,a.expn,b.expn)
        mu = pre*wx*wy*dz
    return mu 

def dip_nuc(atoms,center):
    """
        dip_nuc
        Calculate nuclear contribution mu_nuc to the dipole moment mu.

        Input 
            - atoms: Atoms(), chilli_py atoms object 
            - center: np.array(), 3d coordinate 
    """
    # Compare explict python vs np.einsum
    #   mu_nuc = np.sum(Z * (pos - center) for (Z,pos) in zip(atoms.Z,atoms.pos))
    mu_nuc = np.einsum('i,ix->x', atoms.Z, atoms.pos - center)
    return mu_nuc

