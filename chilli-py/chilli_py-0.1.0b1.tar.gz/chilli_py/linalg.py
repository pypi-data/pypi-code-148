import numpy as np 

"""
    canonical_ortho
    Canonical orthogonalization 

    Reference 
        - https://github.com/susilehtola/erkale/blob/8297aefe5aac9dbbb291e04c07661f3cff94a99a/src/linalg.cpp#L75
"""
def canonical_ortho(Svec,Sval,cutoff):
    Nbf = Svec.shape[0]
    Nlin = 0
    for i in range(0,Nbf):
        if Sval[i] >= cutoff :
            Nlin += 1

    # Number of linearly dependent basis functions 
    Ndep = Nbf - Nlin 

    # Form returned matrix 
    Sinvh = np.zeros((Nbf,Nlin))
    for i in range(0,Nlin):
        Sinvh[:,i] = Svec[:,Ndep+i]/np.sqrt(Sval[Ndep+i])
    return Sinvh 

"""
    get_Sinvh 
    Calculate S^(-1/2) (S-inverse-half, e.g. Sinvh)

    Reference 
        - Erkale
        - https://github.com/susilehtola/erkale/blob/8297aefe5aac9dbbb291e04c07661f3cff94a99a/src/linalg.cpp#L94 
"""
def get_Sinvh(S,cutoff):
    Sval, Svec = np.linalg.eig(S)
    return canonical_ortho(Svec,Sval,cutoff)

"""
    diag 
    Diagonalize the Hamiltonian H 
    using the S^(-1/2) Sinvh, e.g., 
    
        Hortho = Sinvh*H*Sinvh' 
    Calculate eigenvalues und eigenvectors 
    for Hortho. 

    Note 
        - in Python we use scipy.eigh() 
    
    Reference 
        - Erkale 
        - https://github.com/susilehtola/erkale/blob/8297aefe5aac9dbbb291e04c07661f3cff94a99a/src/contrib/guessbench.cpp#L64    
"""
def diag(H,Sinvh):
    # filter zeros 
    #H[abs.(H).<1e-8] .= 0.0
    #
    Hortho = np.dot(Sinvh,np.dot(H,Sinvh.T))
    Eigs, U = np.linalg.eigh(Hortho)
    U = np.dot(Sinvh.T,U)
    return np.real(Eigs), np.real(U)

"""
    test_linalg
    test linalg functionality
"""
def test_linalg1(): 
    S = np.array([[1.               ,0.81471811604023], [0.81471811604023 , 1.              ]])
    Hcore = np.array([[-1.30365848262366,  -1.25605294504914], [-1.25605294504914 ,-1.30365848262366]])
    Sinvh = get_Sinvh(S,1e-6)
    print(Sinvh)
    Eigs, U = diag(Hcore,Sinvh.T)
    Eigs_ref = np.array([-1.4105283928383148, -0.2569357378989974])
    U_ref = np.array([[0.5249046436007102 ,-1.6427388312443174], [0.5249046436007102,1.6427388312443174]])
    print(Eigs,U)
    assert np.allclose(Eigs,Eigs_ref)
    assert np.allclose(U,U_ref)
    print("test_linalg is passed.")

def test_linalg2():
    S = np.array([[1.0       ,0.242782  ,0.0  ,0.0  ,0.0],  
                   [0.242782  ,1.0       ,0.0  ,0.0  ,0.0],
                   [0.0       ,0.0       ,1.0  ,0.0  ,0.0],
                   [0.0       ,0.0       ,0.0  ,1.0  ,0.0],
                   [0.0       ,0.0       ,0.0  ,0.0  ,1.0]])
    Hcore = np.array([[ -49.4245 , -11.8587 ,   0.0    ,   0.0   ,    0.0],
                      [-11.8587  , -13.159  ,   0.0    ,   0.0   ,    0.0],
                      [ 0.0      ,  0.0     ,  -10.2241,   0.0   ,    0.0],
                      [ 0.0      ,  0.0     ,   0.0    , -10.2241,    0.0],
                      [ 0.0      ,  0.0     ,   0.0    ,   0.0   ,  -10.2241]])
    Sinvh = get_Sinvh(S,1e-6)
    Eigs, U = diag(Hcore,Sinvh.T)
    print(Eigs,U)

def main(): 
    test_linalg2()

if __name__ == "__main__": 
    main() 
