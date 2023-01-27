import numpy as np
from copy import deepcopy 
from chilli_py.PGBF import PGBF
from chilli_py.CGBF import CGBF, contract_4c
from chilli_py.alias import dist2 
from chilli_py.nuclear import Fgamma 

""" ERI/coulomb according to M. Head-Gordon and J. Pople (HGP) """

def extract_values(g): 
    """
        extract_values
        Extract values from PGBF. 

        Input 
            - g: PGBF() 
    """
    gx,gy,gz = g.center 
    gI,gJ,gK = g.power 
    gexpn = g.expn 
    return gexpn, gx,gy,gz, gI,gJ,gK

def coulomb_hgp_pgbf(a,b,c,d):
    """
        coulomb_hgp_pgbf
        Coulomb for four PGBFs (a, b, c, d).

        Input 
            - a,b,c,d: PGBF() 

        Reference
            - M. Head-Gordon and J. Pople
              A method for two‐electron Gaussian integral and integral derivative evaluation using recurrence relations.
              J. Chen. Phys. 89, 5777 (1988). http://dx.doi.org/10.1063/1.455553
            - https://github.com/rpmuller/pyquante2/blob/master/pyquante2/ints/hgp.py
            - https://github.com/f-fathurrahman/ffr-ElectronicStructure.jl/blob/master/LO_Gaussian/orig/pyquante_orig_new.jl

        Note
            - hrr: performs the horizontal recursion relationships
            - vrr: vrr performs the vertical recursion relationship
            - SS: I know this is ugly written/handeled. 
            - SS: I tried to reformulate it. 
            - SS: However resursion if object instances is hard to debug. 

    """
    # Extract values from instances 
    aexpn,ax,ay,az,aI,aJ,aK = extract_values(a) 
    bexpn,bx,by,bz,bI,bJ,bK = extract_values(b) 
    cexpn,cx,cy,cz,cI,cJ,cK = extract_values(c) 
    dexpn,dx,dy,dz,dI,dJ,dK = extract_values(d) 
    NORM = a.NORM*b.NORM*c.NORM*d.NORM
    hrr_val = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                  bexpn,bx,by,bz,bI,bJ,bK,
                  cexpn,cx,cy,cz,cI,cJ,cK,
                  dexpn,dx,dy,dz,dI,dJ,dK) 
    return NORM*hrr_val 

def coulomb_hgp_cgbf(a,b,c,d): 
    """
        coulomb_hgp_cgbf
        Coulomb for four CGBFs (a, b, c, d). 

        Input 
            - a,b,c,d: CGBF()
    """
    return contract_4c(coulomb_hgp_pgbf,a,b,c,d)

def gaussian_product_center(aexpn,ax,ay,az,bexpn,bx,by,bz):
    """ 
        gaussian_product_center
        Calculate Gaussian product center for 
        two Gaussian (a,b). 
    """
    acenter = np.array([ax,ay,az]) 
    bcenter = np.array([bx,by,bz])
    return (aexpn*acenter+bexpn*bcenter)/(aexpn+bexpn)

def hrr(aexpn,ax,ay,az,aI,aJ,aK,
        bexpn,bx,by,bz,bI,bJ,bK,
        cexpn,cx,cy,cz,cI,cJ,cK,
        dexpn,dx,dy,dz,dI,dJ,dK,
        ):
    """
        hrr 
        The HGP horizontal recursion relations (HRR). 

        Notes
            - SS: enforce block structure to increase readability 

        Needs
            - hrr 
            - vrr 
    """
    if bI > 0:
        hrr_a = hrr(aexpn,ax,ay,az,aI+1,aJ,aK,
                    bexpn,bx,by,bz,bI-1,bJ,bK, 
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI,dJ,dK) 
        hrr_b = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,bI-1,bJ,bK,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI,dJ,dK)
        hrr_c = hrr_a + (ax-bx)*hrr_b
        return hrr_c 
    elif bJ > 0:
        hrr_a = hrr(aexpn,ax,ay,az,aI,aJ+1,aK,
                    bexpn,bx,by,bz,bI,bJ-1,bK,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI,dJ,dK) 
        hrr_b = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,bI,bJ-1,bK,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI,dJ,dK)
        hrr_c = hrr_a + (ay-by)*hrr_b
        return hrr_c
    elif bK > 0:
        hrr_a = hrr(aexpn,ax,ay,az,aI,aJ,aK+1,
                    bexpn,bx,by,bz,bI,bJ,bK-1,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI,dJ,dK) 
        hrr_b = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,bI,bJ,bK-1,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI,dJ,dK)
        hrr_c = hrr_a + (az-bz)*hrr_b
        return hrr_c
    elif dI > 0:
        hrr_a = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,bI,bJ,bK,
                    cexpn,cx,cy,cz,cI+1,cJ,cK,
                    dexpn,dx,dy,dz,dI-1,dJ,dK) 
        hrr_b = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,bI,bJ,bK,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI-1,dJ,dK)
        hrr_c = hrr_a + (cx-dx)*hrr_b
        return hrr_c 
    elif dJ > 0:
        hrr_a = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                     bexpn,bx,by,bz,bI,bJ,bK,
                     cexpn,cx,cy,cz,cI,cJ+1,cK,
                     dexpn,dx,dy,dz,dI,dJ-1,dK) 
        hrr_b = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,bI,bJ,bK,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI,dJ-1,dK)
        hrr_c = hrr_a + (cy-dy)*hrr_b
        return hrr_c 
    elif dK > 0:
        hrr_a = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,bI,bJ,bK,
                    cexpn,cx,cy,cz,cI,cJ,cK+1,
                    dexpn,dx,dy,dz,dI,dJ,dK-1) 
        hrr_b = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,bI,bJ,bK,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,dI,dJ,dK-1)
        hrr_c = hrr_a + (cz-dz)*hrr_b
        return hrr_c 
    return vrr(aexpn,ax,ay,az,aI,aJ,aK,
               bexpn,bx,by,bz,
               cexpn,cx,cy,cz,cI,cJ,cK,
               dexpn,dx,dy,dz,
               0)

def vrr(aexpn,ax,ay,az,aI,aJ,aK,
        bexpn,bx,by,bz,
        cexpn,cx,cy,cz,cI,cJ,cK,
        dexpn,dx,dy,dz,
        m):
    """
        vrr 
        The HGP vertical recursion relations (VRR). 

        Needs   
            - gaussian_product_center
            - hrr 
            - vrr
            - dist2 
    """

    P = gaussian_product_center(aexpn,ax,ay,az,bexpn,bx,by,bz)
    px,py,pz = P 
    Q = gaussian_product_center(cexpn,cx,cy,cz,dexpn,dx,dy,dz)
    qx,qy,qz = Q 
    zeta,eta = aexpn+bexpn,cexpn+dexpn
    W = gaussian_product_center(zeta,px,py,pz,eta,qx,qy,qz)
    wx,wy,wz = W
    vrr_c = 0
    if cK>0:
        vrr_a = vrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,
                    cexpn,cx,cy,cz,cI,cJ,cK-1,
                    dexpn,dx,dy,dz,m) 
        vrr_b = vrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,
                    cexpn,cx,cy,cz,cI,cJ,cK-1,
                    dexpn,dx,dy,dz,m+1)
        vrr_c = (qz-cz)*vrr_a + (wz-qz)*vrr_b
        #print(f"val1 vrr= {vrr_c}") 
        if cK>1:
            vrr_a = vrr(aexpn,ax,ay,az,aI,aJ,aK,
                        bexpn,bx,by,bz,
                        cexpn,cx,cy,cz,cI,cJ,cK-2,
                        dexpn,dx,dy,dz,m) 
            vrr_b = vrr(aexpn,ax,ay,az,aI,aJ,aK,
                        bexpn,bx,by,bz,
                        cexpn,cx,cy,cz,cI,cJ,cK-2,
                        dexpn,dx,dy,dz,m+1)
            vrr_c += 0.5*(cK-1)/eta*(vrr_a - zeta/(zeta+eta)*vrr_b)
            #print(f"val2 vrr= {vrr_c}")
        if aK>0:
            vrr_a = vrr(aexpn,ax,ay,az,aI,aJ,aK-1,
                      bexpn,bx,by,bz,
                      cexpn,cx,cy,cz,cI,cJ,cK-1,
                      dexpn,dx,dy,dz,m+1)
            vrr_c += 0.5*aK/(zeta+eta)*vrr_a
            #print(f"val3 vrr= {vrr_c}")
        return vrr_c 
    elif cJ>0: 
        vrr_a = vrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,
                    cexpn,cx,cy,cz,cI,cJ-1,cK,
                    dexpn,dx,dy,dz,m) 
        vrr_b = vrr(aexpn,ax,ay,az,aI,aJ,aK,
                    bexpn,bx,by,bz,
                    cexpn,cx,cy,cz,cI,cJ-1,cK-1,
                    dexpn,dx,dy,dz,m+1)
        vrr_c = (qy-cy)*vrr_a + (wy-qy)*vrr_b
        #print(f"val4 vrr= {vrr_c}")
        if cJ>1:
            vrr_c += 0.5*(cJ-1)/eta*(
            vrr(aexpn,ax,ay,az,aI,aJ,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ-2,
                cK,dexpn,dx,dy,dz,m) -
            zeta/(zeta+eta)*
            vrr(aexpn,ax,ay,az,aI,aJ,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ-2,cK,
                dexpn,dx,dy,dz,m+1)
            )
            #print(f"val5 vrr= {vrr_c}")
        if aJ>0:    
            vrr_c += 0.5*aJ/(zeta+eta)*\
            vrr(aexpn,ax,ay,az,aI,aJ-1,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ-1,cK,
                dexpn,dx,dy,dz,m+1)
        #print(f"val6 vrr= {vrr_c}")
        return vrr_c 
    elif cI>0: 
        vrr_c = (qx-cx)*vrr(aexpn,ax,ay,az,aI,aJ,aK,
                          bexpn,bx,by,bz,
                          cexpn,cx,cy,cz,cI-1,cJ,cK,
                          dexpn,dx,dy,dz,m) +\
              (wx-qx)*vrr(aexpn,ax,ay,az,aI,aJ,aK,
                          bexpn,bx,by,bz,
                          cexpn,cx,cy,cz,cI-1,cJ,cK-1,
                          dexpn,dx,dy,dz,m+1)
        #print(f"val7 vrr= {vrr_c}")
        if cI>1:
            vrr_c += 0.5*(cI-1)/eta*(
            vrr(aexpn,ax,ay,az,aI,aJ,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI-2,cJ,cK,
                dexpn,dx,dy,dz,m) -\
            zeta/(zeta+eta)*
            vrr(aexpn,ax,ay,az,aI,aJ,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI-2,cJ,cK,
                dexpn,dx,dy,dz,m+1))
            #print(f"val8 vrr= {vrr_c}")
        if aI>0:
            vrr_c += 0.5*aI/(zeta+eta)*\
            vrr(aexpn,ax,ay,az,aI-1,aJ,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI-1,cJ,cK,
                dexpn,dx,dy,dz,m+1)
        #print(f"val9 vrr= {vrr_c}")
        return vrr_c
    # SS: here we varry a 
    elif aK>0:
        vrr_c = (pz-az)*vrr(aexpn,ax,ay,az,aI,aJ,aK-1,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ,cK,
                dexpn,dx,dy,dz,m) +\
        (wz-pz)*vrr(aexpn,ax,ay,az,aI,aJ,aK-1,
                    bexpn,bx,by,bz,
                    cexpn,cx,cy,cz,cI,cJ,cK,
                    dexpn,dx,dy,dz,m+1)
        #print(f"val10 vrr= {vrr_c}")
        if aK>1:
            vrr_c += 0.5*(aK-1)/zeta*(
            vrr(aexpn,ax,ay,az,aI,aJ,aK-2,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI-1,cJ,cK,
                dexpn,dx,dy,dz,m) -\
            eta/(zeta+eta)*
            vrr(aexpn,ax,ay,az,aI,aJ,aK-2,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI-1,cJ,cK,
                dexpn,dx,dy,dz,m+1)
            )
        #print(f"val11 vrr= {vrr_c}")
        return vrr_c 
    elif aJ>0:
        vrr_c = (py-ay)*vrr(aexpn,ax,ay,az,aI,aJ-1,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ,cK,
                dexpn,dx,dy,dz,m)+\
        (wy-py)*vrr(aexpn,ax,ay,az,aI,aJ-1,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ,cK,
                dexpn,dx,dy,dz,m+1)
        #print(f"val12 vrr= {vrr_c}")
        if aJ>1:
            vrr_c += 0.5*(aJ-1)/zeta*(
            vrr(aexpn,ax,ay,az,aI,aJ-2,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ,cK,
                dexpn,dx,dy,dz,m) -\
            eta/(zeta+eta)*
            vrr(aexpn,ax,ay,az,aI,aJ-2,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ,cK,
                dexpn,dx,dy,dz,m+1)
            )
        #print(f"val13 vrr= {vrr_c}")
        return vrr_c
    elif aI>0:
        vrr_c = (px-ax)*vrr(aexpn,ax,ay,az,aI-1,aJ,aK,
                          bexpn,bx,by,bz,
                          cexpn,cx,cy,cz,cI,cJ,cK,
                          dexpn,dx,dy,dz,m) +\
              (wx-px)*vrr(aexpn,ax,ay,az,aI-1,aJ,aK,
                          bexpn,bx,by,bz,
                          cexpn,cx,cy,cz,cI,cJ,cK,
                          dexpn,dx,dy,dz,m+1)
        #print(f"val14 vrr= {vrr_c}")
        if aI>1:
            vrr_c += 0.5*(aI-1)/zeta*(
            vrr(aexpn,ax,ay,az,aI-2,aJ,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ,cK,
                dexpn,dx,dy,dz,m) -\
            eta/(zeta+eta)*
            vrr(aexpn,ax,ay,az,aI-2,aJ,aK,
                bexpn,bx,by,bz,
                cexpn,cx,cy,cz,cI,cJ,cK,
                dexpn,dx,dy,dz,m+1)
            )
        #print(f"val15 vrr= {vrr_c}")
        return vrr_c 

    #print("Bottom")
    acenter = np.array([ax,ay,az])
    bcenter = np.array([bx,by,bz])
    ccenter = np.array([cx,cy,cz])
    dcenter = np.array([dx,dy,dz])
    pcenter = P 
    qcenter = Q 
    rab2 = dist2(acenter-bcenter)
    rcd2 = dist2(ccenter-dcenter)
    rpq2 = dist2(pcenter-qcenter)
    T = zeta*eta/(zeta+eta)*rpq2
    Kab = np.sqrt(2)*np.pi**1.25/zeta*np.exp(-aexpn*bexpn*rab2/zeta)
    Kcd = np.sqrt(2)*np.pi**1.25/eta *np.exp(-cexpn*dexpn*rcd2/eta)
    #print(f"m={m} T={T}")
    return Kab*Kcd/np.sqrt(zeta+eta)*Fgamma(m,T)

def main():
    """
        main
        Main function to test this routine.
    """
    print("Calling test_coul1\n")
    center = [0,0.0,0.0]
    s = PGBF(center,[0,0,0],1)
    px = PGBF(center, [1,0,0], 1)
    coul = coulomb_hgp_pgbf(s,s,s,px)
    print(coul)
    assert coul==0 # 0
    coul = coulomb_hgp_pgbf(s,s,px,px)
    print(coul)
    assert np.isclose(coul, 0.9403159725793305 )
    print("Pass test_coul1\n")

def test_vrr(): 
    """
        test_vrr 
    """
    
    ax=ay=az=bx=by=bz=cx=cy=cz=dx=dy=dz=0.0
    aexpn=bexpn=cexpn=dexpn=1.0
    aI=aJ=aK=0
    cI=cJ=cK=0
    m=0
    data = [[0.,0.,0., 0,0,0, 0,0,0, 4.37335456733],  # <1 
            
            [0.,0.,0., 1,0,0, 1,0,0, 0.182223107579], # =1
            [0.,0.,0., 0,1,0, 0,1,0, 0.182223107579],
            [0.,0.,0., 0,0,1, 0,0,1, 0.182223107579], 

            [0.,0.,0., 2,0,0, 2,0,0, 0.223223306785], # > 1, = 2 
            [0.,0.,0., 0,2,0, 0,2,0, 0.223223306785],
            [0.,0.,0., 0,0,2, 0,0,2, 0.223223306785],

            [1.,2.,3., 1,0,0, 1,0,0, -5.63387712455e-06],
            [1.,2.,3., 0,1,0, 0,1,0, -0.000116463120359],
            [1.,2.,3., 0,0,1, 0,0,1, -0.000301178525749],

            [1.,2.,3., 2,0,0, 2,0,0, 0.00022503308545040895],
            [1.,2.,3., 0,2,0, 0,2,0, 0.0006102470883881907],
            [1.,2.,3., 0,0,2, 0,0,2, 0.0013427831014563411],

            [0.,0.,0., 1,1,0, 1,1,0, 0.0136667330685],
            [0.,0.,0., 0,1,1, 0,1,1, 0.0136667330685],
            [0.,0.,0., 1,0,1, 1,0,1, 0.0136667330685],

            [3.,2.,1., 1,1,0, 1,1,0, 5.976771621486971e-5],
            [3.,2.,1., 0,1,1, 0,1,1, 1.5742904443905067e-6],
            [3.,2.,1., 1,0,1, 1,0,1, 4.00292848649699e-6]
            ]
    for i,(ax,ay,az, aI,aJ,aK, cI,cJ,cK, result) in enumerate(data): 
        val1 = vrr(aexpn,ax,ay,az,aI,aJ,aK,
                   bexpn,bx,by,bz,
                   cexpn,cx,cy,cz,cI,cJ,cK,
                   dexpn,dx,dy,dz,
                   m)
        val2 = vrr(cexpn,cx,cy,cz,cI,cJ,cK,
                   dexpn,dx,dy,dz,
                   aexpn,ax,ay,az,aI,aJ,aK,
                   bexpn,bx,by,bz,
                   m)
        print(i,val1,val2,np.isclose(val1,val2))
        print(i,val1,result,np.isclose(val1,result))
        assert np.isclose(val1,val2)
    print("\n")

def test_hrr():
    ax=ay=az=bx=by=bz=cx=cy=cz=dx=dy=dz=0.0
    aexpn=bexpn=cexpn=dexpn=1.0
    aI=aJ=aK=0
    bI,bJ,bK = 1,0,1
    cI=cJ=cK=0
    dI,dJ,dK = 1,0,1

    data = [[0.,0.,0., 0,0,0, 0,0,0, 0.0136667330685],
            [0.,0.,0., 1,0,0, 1,0,0, 0.00821630976139],
            [0.,0.,0., 0,1,0, 0,1,0, 0.00122024402397],
            [0.,0.,0., 0,0,1, 0,0,1, 0.00821630976139],

            [0.,0.,0., 2,0,0, 2,0,0,   0.0039759617781],
            [0.,0.,0., 0,2,0, 0,2,0,   0.000599953311785],
            [0.,0.,0., 0,0,2, 0,0,2,  0.0039759617781],

            [1.,2.,3., 1,0,0, 1,0,0, -1.1851316496333975e-6],
            [1.,2.,3., 0,1,0, 0,1,0,  -4.669991667384835e-6],
            [1.,2.,3., 0,0,1, 0,0,1, -3.474373852654044e-5],

            [1.,2.,3., 2,0,0, 2,0,0, 2.81002247462e-6],
            [1.,2.,3., 0,2,0, 0,2,0, 7.09856891538e-6],
            [1.,2.,3., 0,0,2, 0,0,2, 3.62153023224e-5],

            [0.,0.,0., 1,1,0, 1,1,0, 0.000599953311785],
            [0.,0.,0., 0,1,1, 0,1,1, 0.000599953311785],
            [0.,0.,0., 1,0,1, 1,0,1, 0.0116431617287],

            [3.,2.,1., 1,1,0, 1,1,0, 7.37307761485e-6],
            [3.,2.,1., 0,1,1, 0,1,1, 2.5333243119843164e-7],
            [3.,2.,1., 1,0,1, 1,0,1, 2.452115184675799e-6]]
    for i, (ax,ay,az, aI,aJ,aK, cI,cJ,cK, result) in enumerate(data): 
        val1 = hrr(aexpn,ax,ay,az,aI,aJ,aK,
                   bexpn,bx,by,bz,bI,bJ,bK,
                   cexpn,cx,cy,cz,cI,cJ,cK,
                   dexpn,dx,dy,dz,dI,dJ,dK)
        val2 = hrr(cexpn,cx,cy,cz,cI,cJ,cK,
                   dexpn,dx,dy,dz,dI,dJ,dK,
                   aexpn,ax,ay,az,aI,aJ,aK,
                   bexpn,bx,by,bz,bI,bJ,bK)
        print(val1,val2,np.isclose(val1,val2))
        print(val1,result,np.isclose(val1,result))
    print("\n")

if __name__ == '__main__':
    main()
    test_vrr()
    test_hrr()
