import numpy as np
from copy import copy, deepcopy 
from scipy.linalg import eigh
from chilli_py.atoms import Atoms, atoms_from_xyz
from chilli_py.BasisSet import BasisSet
from chilli_py.exc import XC
from chilli_py.integrals import pairs, iiterator, one, two, get_J, get_K, get_2JK, get_E, dmat, dip_moment
from chilli_py.nuclear import nuclear_repulsion
from chilli_py.utils import myprint 
# DFT 
from chilli_py.grids import Grids 
from chilli_py.scf import DIIS,Results 
from chilli_py.linalg import get_Sinvh, diag 
""" Restricted Kohn-Sham (RKS) """

def eval_RKS(ERI,Hcore,xc,Enuc,D,verbose=False):
    """
        eval_KS
        Evaluate Kohn-Sham for 
        total density matrix D.

        Input 
            - ERI: np.array(), e.g., from two() 
            - Hcore: np.array(), core Hamiltonian  
            - xc: XC(), instance of XC  
            - Enuc: float(), e.g., from nuclear_repulsion()
            - D: np.array(), density matrix  
            - verbose: bool(), controls verbosity  
    """
    J = get_J(D,ERI)
    EJ = 2*get_E(J,D)
    Eone = 2*get_E(Hcore,D)
    Exc, Vxc = xc.kernel(D=D)
    Eel = EJ + Exc
    FKS = Hcore + 2*J + Vxc
    EKS = Enuc + Eone + Eel
    if verbose:
        myprint(EJ=EJ,Eone=Eone,Exc=Exc,Eel=Eel)
    return EKS, FKS

def RKS_SCF(atoms,basis,grids,xc,maxiter=20,verbose=True,Etol=1e-6,use_avg=True):
    """
        RKS_SCF 
        Restricted Kohn-Sham (RKS) self-consistent field (SCF) 

        Input
            - atoms: Atoms(), contains sym and pos 
            - basis: BasisSet(), basis set information 
            - grids: Grids(), real-space grid for integration 
            - xc: XC(), exchange-correlation functional information  
            - maxiter: int(), maximal number of iterations
            - verbose: True or False, more output or not 
            - Etol: float(), convergence threshold 
            - use_avg: bool(), using DIIS or not 
    """
    method_short = 'RKS' 
    method_long = "Restricted Kohn-Sham (RKS)"
    print(method_long)
    
    Nelec= atoms.Nelec
    Nclosed,Nopen = divmod( int(Nelec), 2 )
    print(f"Nel = {Nelec: d}, Nclosed: {Nclosed: d}, Nopen: {Nopen: d}\n")

    print("1e integrals ...")
    S,T,V,Mx,My,Mz = one(basis,atoms)
    Sinvh = (get_Sinvh(S,1e-6)).T 
    if verbose: 
        myprint(S=S,T=T,V=V)
    print("2e integrals ...")
    ERI = two(basis)
    if verbose: 
        myprint(ERI=ERI)
    
    Hcore = T+V
    if verbose: 
        myprint(Hcore=Hcore)
    
    Eigs,U = eigh(Hcore,S)
    #Eigs, U = diag(Hcore,Sinvh) 

    if verbose: 
        myprint(Eigs=Eigs)

    Enuc = nuclear_repulsion(atoms)
    if verbose:
        myprint(Enuc=Enuc)
    Eold = 0.0
    Energy = 0.0
    F = deepcopy(Hcore)
    IS_CONVERGED = False
    dEtot = 1.0

    if use_avg: 
        avg = DIIS()

    print(f"Starting {method_short} calculation:")
    for iiter in range(maxiter):
        print(f"S: {S} \n F : {F}") 
        Eigs,U = eigh(F,S)
        #Eigs, U = diag(F,Sinvh) 
        print(f"Eigs: {Eigs}") 
        D = dmat(U,Nclosed)
        if verbose: 
            myprint(D=D)
        myprint(U=U)
        myprint(D=D)
        # Update: Kohn-Sham energy and Fockian  
        Etot, F = eval_RKS(ERI,Hcore,xc,Enuc,D)
        
        # Update: Fockian 
        if use_avg:
            print(f"Fin: {F}") 
            F,DIIS_e, dRMS, = avg.kernel(iiter,S,F,D)
            print(f"Fout: {F} \n Fockian: {avg.Fockians}") 
        dEtot = abs(Etot - Eold)
        iiter_str = f">>> iter {iiter: 4d} E = {Etot: 18.10f} Eh DeltaE = {dEtot: 10.5e} Eh"
        if use_avg:
            iiter_str += f" dRMS: {dRMS: 10.5e}"
        print(iiter_str) 
        if np.isclose(Etot,Eold,0,Etol):
            IS_CONVERGED = True
            Eigs,U = eigh(F,S)
            print("Final: Eigenvalues")
            print(f"Eigs = {Eigs}")
            D = dmat(U,Nclosed)
            # Dipole moment
            mu, mu_abs = dip_moment(atoms,Mx,My,Mz,D)
            break
        Eold  = Etot

    if not IS_CONVERGED:
        print(f"WARNING: {method_short} is not converged")

    # Results
    res  = Results()
    res.S = S
    res.T = T 
    res.V = V
    res.Hcore = Hcore 
    #res.J = J
    #res.Vxc = Vxc 
    res.ERI = ERI
    res.Enuc = Enuc 
    res.Etot = Etot
    res.Eigs = Eigs
    res.U = U
    res.D = D
    res.mu = mu
    res.mu_abs = mu_abs
    return res


class RKS: 
    """
        RKS class 
        Restricted Kohn-Sham (RKS). 
        Performs a RKS calculation. 

        Input 
            - atoms: Atoms()
            - basis_name: str(), basis set name 
            - grids: tuple(), e.g., (100,110)
    """
    def __init__(self,atoms,basis_name="sto-3g",grids=(100,110),**kwargs):
        """
            __init__ 
            Initialize a instance of the class.
        """
        # primary input 
        self.atoms = atoms
        self._set_basis(basis_name)
        self._set_grid(grids)
        # secondary input 
        self._set_kwargs(kwargs)
        # primary input 
        self._set_xc()

    def _set_basis(self,basis_name):
        """
            _set_basis
            Generate basis from str or use a given basis. 
        """
        # Generate basis from string str
        if type(basis_name) == str:
            self.basis = BasisSet.initialize(self.atoms,basis_name=basis_name)
        # Use given basis 
        if type(basis_name) == BasisSet:
            self.basis = basis 

    def _set_grid(self,grids):
        """
            _set_grids
            Generate grids from tuple (n_rad,n_ang) or 
            use given grid. 
        """
        if type(grids) == tuple:
            n_rad,n_ang = grids 
            self.grids = Grids(self.atoms,n_rad,n_ang)
        if type(grids) == Grids:
            self.grids = grids 
        coords, weights = self.grids.get_grid()
        self.grids.eval(self.basis)

    def _set_kwargs(self,kwargs): 
        """
            _set_kwargs
            Check if parameters are given. 
            If given use this parameter. 
            If not given use default values.
        """
        self.maxiter = kwargs.get('maxiter',300)
        self.verbose = kwargs.get('verbose',False)
        self.Etol = kwargs.get('Etol',1e-6)
        self.use_avg = kwargs.get('use_avg',True)
        self.xc_name = kwargs.get("xc_name","LDA,VWN")

    def _set_xc(self): 
        """
            _set_xc 
            Construct a XC instance for 
            the given grid and xc_name.
            This call assumes that _set_kwargs() 
            was called before. 
        """
        # Note: For XC the spin is either 0 or 1 
        # In this case the spin desides if one 
        # wants to use spin-polarized (spin=1) 
        # or spin-unpolarized (spin=0)
        # XC functionals 
        self.xc = XC(grids=self.grids,
                     spin=0,
                     xc_name=self.xc_name)
        print(self.xc)

    def kernel(self):
        """
            kernel 
            Kernel function executing the self-consistent field
            calculation. 
        """
        results= RKS_SCF(
                    atoms = self.atoms, 
                    basis = self.basis, 
                    grids = self.grids,
                    maxiter=self.maxiter, 
                    verbose=self.verbose, 
                    Etol=self.Etol,
                    use_avg=self.use_avg,
                    xc=self.xc
                    )
        results.update(self)
        return self.Etot


def main():
    """
        main 
        Main function to test this routine. 
    """
    from chilli_py.atoms import Atoms, atoms_from_xyz
    from chilli_py import __path__ as pkg_path 
    # Using Atoms object 
    #   atoms = Atoms(['H','H'],[[0,0,0],[1.4,0,0]])
    # Using xyz file 
    atoms = atoms_from_xyz(pkg_path[0]+"/structs/"+"CH4.xyz")
    mf = RKS(atoms,"pc-0",xc_name="LDA,PW")
    mf.verbose = False
    mf.use_avg = True
    mf.kernel() 
    
if __name__ == '__main__':
    main()

