import numpy as np 

""" Spin functionality """

def spin_square(S,Na,Nb,Ua,Ub):
    """
        spin_square 
        Calculate spin contamination as implemented in PySCF.

        Input
            - S: np.array(), overlap matrix 
            - Na: int(), number of alpha electrons 
            - Nb: int(), number of beta electrons
            - Ua: np.array(), coefficients of the alpha channel 
            - Ub: np.array(), coefficients of the beta channel 

        Reference 
            - https://github.com/psi4/psi4numpy/blob/1233d1af2d168f91065e4f7dbb1a96e02b95b6e1/Self-Consistent-Field/UHF_libJK.py
            - https://github.com/pyscf/pyscf/blob/master/pyscf/scf/uhf.py#L335
    """
    spin_mat = (Ub[:, :Nb].T).dot(S).dot(Ua[:, :Na])
    #spin_contam = min(Na, Nb) - np.vdot(spin_mat, spin_mat)
    ssxy = (Na+Nb) * .5 - np.vdot(spin_mat, spin_mat)
    ssz = (Na-Nb)**2 * .25
    ss = (ssxy + ssz).real
    s = np.sqrt(ss+.25) - .5
    M = s*2+1
    print(f'M = 2S +1 : {M: .7f} <S^2> : {ss: .7f}')
    return ss, M

def spin_square2(S,Na,Nb,Ua,Ub):
    """
        spin_square2
        Calculate spin contamination as implemented in ERKALE.
        Should give identical results as spin_square,
        but is may easier to read. 

        Input
            - S: np.array(), overlap matrix 
            - Na: int(), number of alpha electrons 
            - Nb: int(), number of beta electrons
            - Ua: np.array(), coefficients of the alpha channel 
            - Ub: np.array(), coefficients of the beta channel

        Note 
            - https://github.com/susilehtola/erkale/blob/676f71d1246a065ba9750a1d64df6670f9a58747/src/properties.cpp#L845
            - Jamie S.Andrews et al., Spin contamination in single-determinant wavefunctions
    """
    Sz = (Na-Nb)/2. 
    Sab = (Ua.T).dot(S).dot(Ub)
    S2 = Sz*(Sz+1)+Nb  
    for i in range(Na):
        for j in range(Nb):
            S2 -= Sab[i,j]**2
    S = np.sqrt(S2+0.25) - 0.5 
    M = S*2 + 1 
    print(f'M = 2S +1 : {M: .7f} <S^2> : {S2: .7f}') 
    return S2, M 
