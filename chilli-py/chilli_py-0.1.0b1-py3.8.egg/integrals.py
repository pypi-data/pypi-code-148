import numpy as np 
from itertools import combinations_with_replacement
from chilli_py.alias import norm
from chilli_py.constants import AU2DEBYE
from chilli_py.CGBF import overlap, overlap_cgbf
from chilli_py.kinetic import kinetic_cgbf as kinetic
from chilli_py.coulomb import coulomb_cgbf as coulomb
from chilli_py.nuclear import nuclear_attraction_cgbf_atoms
from chilli_py.dipole import dipole_cgbf, dip_nuc 
from chilli_py.utils import myprint 

""" 1e (one) and 2e (two) electron integrals and utility functions"""

def pairs(it):
    """
        pairs
        Indicies pairs of a NxN matrix. 
    """
    return combinations_with_replacement(range(it),2)

def iiterator(nbf):
    """
        iiterator
        Iterator over n**4 integral indices.
    """
    for i,j in pairs(nbf):
        ij = i*(i+1)/2+j
        for k,l in pairs(nbf):
            kl = k*(k+1)/2+l
            if ij <= kl:
                yield i,j,k,l
    return

def one(basis, atoms):
    """
        one
        All one electron (1e) integrals.

        Input 
            - basis: basis set 
            - atoms: Atoms() 

        Output
        
            - S  : overlap matrix 
            - T  : kinetic energy matrix 
            - V  : nuclear attraction matrix 
            - Mx : moments matrix for x direction
            - My : moments matrix for y direction
            - Mz : moments matrix for z direction

    """
    n = len(basis)
    # one electron matrices for energy 
    S = np.zeros((n,n),dtype=float)
    T = np.zeros((n,n),dtype=float)
    V = np.zeros((n,n),dtype=float)
    # one electron matrices for dipole 
    Mx = np.zeros((n,n),dtype=float)
    My = np.zeros((n,n),dtype=float)
    Mz = np.zeros((n,n),dtype=float)
    # Note: pairs replace the douple loop
    for (i,j) in pairs(n):
    # The loops would look like  
    # for i in range(n):
    #     for j in range(i,n):
    # for i in (range(n)):
    #     for j in range(i+1):
        a,b = basis.basis[i], basis.basis[j]
        S[i,j] = S[j,i] = overlap_cgbf(a,b)
        T[i,j] = T[j,i] = kinetic(a,b)
        V[i,j] = V[j,i] = nuclear_attraction_cgbf_atoms(a,b,atoms)
        Mx[i,j] = Mx[j,i] = dipole_cgbf(a,b,direction="x",center=atoms.center)
        My[i,j] = My[j,i] = dipole_cgbf(a,b,direction="y",center=atoms.center)
        Mz[i,j] = Mz[j,i] = dipole_cgbf(a,b,direction="z",center=atoms.center)
    return S,T,V,Mx,My,Mz

def two(basis,ERI=coulomb):
    """
        two 
        All two electron (2e) integrals.

        Input 
            - basis: basis set 
            - ERI, i.e., coulomb, electron-repulsion integral (ERI) 
    """
    nbf = len(basis)
    bfs = basis.basis
    ints = np.empty((nbf,nbf,nbf,nbf))
    # Note: iiterator replace the four loop 
    for i,j,k,l in iiterator(nbf):
        ints[i,j,k,l] = ints[j,i,k,l] = ints[i,j,l,k] = ints[j,i,l,k] = \
                        ints[k,l,i,j] = ints[l,k,i,j] = ints[k,l,j,i] = \
                        ints[l,k,j,i] = ERI(bfs[i],bfs[j],bfs[k],bfs[l])
    return ints

def get_J(D,Ints):
    """
        get_J 
        Get Coulomb matrix J. 

        Input 
            - D: np.array(), density matrix (D) sometimes called DM 
            - Ints: np.array(), 2e integrals, e.g., from two() 
    """
    return np.einsum('kl,ijkl->ij',D,Ints)

def get_K(D,Ints):
    """
        get_K 
        Get Exchange matrix K.

        Input
            - D: np.array(), density matrix (D) sometimes called DM
            - Ints: np.array(), 2e integrals, e.g., from two() 
    """
    return np.einsum('ij,ikjl->kl',D,Ints)

def get_2JK(D,Ints):
    """
        get_2JK
        Get restricted Fockian 2*J+K

        Input
            - D: np.array(), density matrix (D) sometimes called DM
            - Ints: np.array(), 2e integrals, e.g., from two()
    """
    return 2*get_J(D,Ints)-get_K(D,Ints)


def get_JK(D,Ints):
    """
        get_JK
        Get unrestricted Fockian J and K

        Input
            - D: np.array(), density matrix (D) sometimes called DM
            - Ints: np.array(), 2e integrals, e.g., from two() 
    """
    return get_J(D,Ints),get_K(D,Ints)


def dmat(U,nocc):
    """
        dmat
        Determine density matrix D.

        Input 
            - U: np.array(), molecular orbital coefficients, i.e., in PySCF mo_coeff 
            - nocc: int(), number of occupied orbitals 
    """
    return np.dot(U[:,:nocc],U[:,:nocc].T)

def get_E(H,D):
    """
        get_E
        Get the energy E from a Fockian like matrix H, i.e.,
        Hcore to get Eone or F to get Etwo.

        Input 
            - H: Hamiltonian/Fockian, e.g., Hcore 
            - D: np.array(), density matrix

        Notes
            - pyquante/2 used trace2 to do so
    """
    E = np.einsum('pq,qp',H,D)
    return E

def dip_moment(atoms,Mx,My,Mz,D):
    """
        dip_moment
        Calculate dipole moment mu

            mu = mu_el + mu_nuc

        and the absolute value of mu

            mu_abs = norm(mu)

        in Debye units.
        The converstion from a.u.
        can be found in the constants module.

        Input
            - atoms: Atoms() object
            - Mx,My,Mz: moments matricies calcualted by one()
            - D: np.array(), density matrix 
    """
    mu_nuc = dip_nuc(atoms,center=atoms.center)
    # Compute dipole moment components
    mux_el = -2*get_E(Mx,D)
    muy_el = -2*get_E(My,D)
    muz_el = -2*get_E(Mz,D)
    mu_el = np.array([mux_el,muy_el,muz_el])
    mu = mu_el + mu_nuc
    print(f"mu_el : {mu_el} mu_nuc: {mu_nuc}") 
    # Convert from a.u. to Debye
    mu *= AU2DEBYE
    unit = "Debye"
    # Compute the dipole moment
    mu_abs = norm(mu)
    print(f"Dipole moment: \n mu = [{mu[0]: 10.5f},{mu[1]: 10.5f},{mu[2]: 10.5f}], |mu| = {mu_abs: 10.5f} {unit}")
    return mu, mu_abs

