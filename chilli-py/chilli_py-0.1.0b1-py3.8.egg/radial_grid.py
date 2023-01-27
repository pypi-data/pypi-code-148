import numpy as np 
from chilli_py.constants import ANG2BOHR 

# Default value for unkown values.
unknown = 1.999999
# Reference
#   - JCP 41, 3199 (1964); DOI:10.1063/1.1725697.
bragg = np.array((unknown,  # Ghost atom
        0.35,                                     1.40,             # 1s
        1.45, 1.05, 0.85, 0.70, 0.65, 0.60, 0.50, 1.50,             # 2s2p
        1.80, 1.50, 1.25, 1.10, 1.00, 1.00, 1.00, 1.80,             # 3s3p
        2.20, 1.80,                                                 # 4s
        1.60, 1.40, 1.35, 1.40, 1.40, 1.40, 1.35, 1.35, 1.35, 1.35, # 3d
                    1.30, 1.25, 1.15, 1.15, 1.15, 1.90,             # 4p
        2.35, 2.00,                                                 # 5s
        1.80, 1.55, 1.45, 1.45, 1.35, 1.30, 1.35, 1.40, 1.60, 1.55, # 4d
                    1.55, 1.45, 1.45, 1.40, 1.40, 2.10,             # 5p
        2.60, 2.15,                                                 # 6s
        1.95, 1.85, 1.85, 1.85, 1.85, 1.85, 1.85,                   # La, Ce-Eu
        1.80, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75,             # Gd, Tb-Lu
              1.55, 1.45, 1.35, 1.35, 1.30, 1.35, 1.35, 1.35, 1.50, # 5d
                    1.90, 1.80, 1.60, 1.90, 1.45, 2.10,             # 6p
        1.80, 2.15,                                                 # 7s
        1.95, 1.80, 1.80, 1.75, 1.75, 1.75, 1.75,
        1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75,
        1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75,
                    1.75, 1.75, 1.75, 1.75, 1.75, 1.75,
        1.75, 1.75,
        1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75, 1.75))
bragg_radii = ANG2BOHR*bragg

def rad_grid_becke(Npoints, **kwargs):
    """
        
        rad_grid_becke 
        Gauss-Chebyshev of the first kind, and the transformed interval [0,infty).

        Input
            - Npoints: int(), Number of sample points
            - Z: int(), atomic number 
        
        Reference
            - https://github.com/pyscf/pyscf/blob/master/pyscf/dft/radi.py
            - [Becke88](Becke, JCP 88, 2547 (1988); DOI:10.1063/1.454033)
    """
    Z = kwargs.get("Z",1) 
    if Z == 1:
        rm = bragg_radii[Z]
    else:
        rm = bragg_radii[Z] * .5
    # PySCF uses: 
    #   points, weights = np.polynomial.chebyshev.chebgauss(Npoints)
    # PyQuante uses: 
    # SS: this gives similar results as gauss_chebyshev
    points, weights = np.polynomial.legendre.leggauss(Npoints)
    r = (1+points)/(1-points) * rm
    weights *= 2/(1-points)**2 * rm
    return r, weights

def gauss_chebyshev(Npoints,**kwargs):
    """
        gauss_chebyshev

        Input 
            - Npoints: int() 

        Notes
            - Gauss-Chebyshev of the second kind,  and the transformed interval [0,\infty)

        Reference 
             - https://github.com/pyscf/pyscf/blob/master/pyscf/dft/radi.py
             - Gauss-Chebyshev [JCP 108, 3226 (1998); DOI:10.1063/1.475719) radial grids
             - Matthias Krack and Andreas M. Koster,  J. Chem. Phys. 108 (1998), 3226
             - https://en.wikipedia.org/wiki/Chebyshev%E2%80%93Gauss_quadrature
    """
    ln2 = 1 / np.log(2)
    fac = 16./3 / (Npoints+1)
    x1 = np.arange(1,Npoints+1) * np.pi / (Npoints+1)
    xi = ((Npoints-1-np.arange(Npoints)*2) / (Npoints+1.) + (1+2./3*np.sin(x1)**2) * np.sin(2*x1) / np.pi)
    xi = (xi - xi[::-1])/2
    r = 1 - np.log(1+xi) * ln2
    dr = fac * np.sin(x1)**4 * ln2/(1+xi)
    return r, dr
