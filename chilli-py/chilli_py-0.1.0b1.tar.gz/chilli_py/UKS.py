import numpy as np
from scipy.linalg import eigh
from chilli_py.atoms import Atoms, atoms_from_xyz
from chilli_py.BasisSet import BasisSet
from chilli_py.exc import XC
from chilli_py.integrals import pairs, iiterator, one, two, get_J, get_K, get_2JK, get_E, dmat
from chilli_py.nuclear import nuclear_repulsion
from chilli_py.utils import myprint 
# DFT 
from chilli_py.grids import Grids 
from chilli_py.scf import get_guess,DIIS,Results 
from chilli_py.spin import spin_square

""" Unrestricted Kohn-Sham (UKS) """

def UKS_SCF(atoms,basis,grids,xc,maxiter=20,verbose=True,Etol=1e-6,use_avg=True):
    """
        UKS_SCF 
        Unrestricted Kohn-Sham (UKS) self-consistent field (SCF) 

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
    method_short = 'UKS' 
    method_long = "Unrestricted Kohn-Sham (UKS)"
    print(method_long)
    
    Nelec= atoms.Nelec
    Nopen = atoms.spin
    Nclosed,Nerr = divmod( int(Nelec) - int(atoms.spin), 2 )
    Na = Nclosed + Nopen
    Nb = Nclosed
    print(f"Nel = {Nelec: d}, Na: {Na: d}, Nb: {Nb: d}\n")

    print("1e integrals ...")
    S,T,V,Mx,My,Mz = one(basis,atoms)
    if verbose: 
        myprint(S=S,T=T,V=V)
    print("2e integrals ...")
    ERI = two(basis)
    if verbose: 
        myprint(ERI=ERI)
    
    Hcore = T+V
    if verbose: 
        myprint(Hcore=Hcore)

    Fguess = get_guess(Hcore=Hcore,S=S,guess="Hcore") #"GWH")
    Eigs,U = eigh(Hcore,S)
    Ua, Ub = U, U 
    if verbose: 
        myprint(Eigs=Eigs)

    Enuc = nuclear_repulsion(atoms)
    if verbose:
        myprint(Enuc=Enuc)
    Eold = 0.0
    Energy = 0.0
    Fa = Fguess  
    Fb = Fguess
    IS_CONVERGED = False
    dEtot = 1.0

    if use_avg: 
        avg_a = DIIS()
        avg_b = DIIS() 

    print(f"Starting {method_short} calculation:")
    for iiter in range(maxiter):
        Eigs_a,Ua = eigh(Fa,S)
        Eigs_b,Ub = eigh(Fb,S)
        Da = dmat(Ua,Na)
        Db = dmat(Ub,Nb)
        Dab = Da + Db 
        if verbose: 
            myprint(Da=Da,Db=Db)
       
        Jab =get_J(Dab,ERI)
        EJ = 1/2*get_E(Jab,Dab)
        Eone = get_E(Hcore,Dab)
        Exc, Vxca, Vxcb = xc.kernel(Da=Da,Db=Db)
        Eel = EJ + Exc
        Fa = Hcore + Jab + Vxca
        Fb = Hcore + Jab + Vxcb
        Etmpa = get_E(Fa,Da)
        Etmpb = get_E(Fb,Db)
        
        if use_avg: 
            Fa,DIIS_e_a, dRMS_a, = avg_a.kernel(iiter,S,Fa,Da)
            Fb,DIIS_e_b, dRMS_b, = avg_b.kernel(iiter,S,Fb,Db)
            dRMS = 0.5*(dRMS_a + dRMS_b)

        Etot = Enuc + Eone + Eel

        if verbose:
            myprint(EJ=EJ,Eone=Eone,Exc=Exc,Eel=Eel)
        
        dEtot = abs(Etot - Eold)
        iiter_str = f">>> iter {iiter: 4d} E = {Etot: 18.10f} Eh DeltaE = {dEtot: 10.5e} Eh"
        if use_avg:
            iiter_str += f" dRMS: {dRMS: 10.5e}"
        print(iiter_str) 
        if verbose: 
            myprint(Enuc=Enuc,Eone=Eone)
        if np.isclose(Etot,Eold,0,Etol):
            IS_CONVERGED = True
            spin_square(S,Na,Nb,Ua,Ub)
            Eigs_a,Ua = eigh(Fa,S)
            Eigs_b,Ub = eigh(Fb,S)
            print("Final: Eigenvalues")
            print(f"Eigs_a = {Eigs_a}")
            print(f"Eigs_b = {Eigs_b}")
            break
        Eold  = Etot

    if not IS_CONVERGED:
        print(f"WARNING: {method_short} is not converged")

    # Results
    res  = Results()
    res.Etot = Etot
    res.mo_energy = Eigs
    res.mo_coeff = U
    res.Da = Da
    res.Db = Db 
    #res.mu = mu
    #res.mu_abs = mu_abs
    return res


class UKS: 
    """
        UKS class 
        Unrestricted Kohn-Sham (UKS). 
        Performs a UKS calculation. 

        Input 
            - atoms: Atoms() 
            - basis: str(), basis set name 
            - grids: tuple(), e.g., (100,110)
    """
    def __init__(self,atoms,basis="sto-3g",grids=(100,110),**kwargs):
        """
            __init__ 
            Initialize a instance of the class.
        """
        # primary input 
        self.atoms = atoms
        self._set_basis(basis)
        self._set_grid(grids)
        # secondary input 
        self._set_kwargs(kwargs)
        # primary input 
        self._set_xc() 

    def _set_basis(self,basis):
        """
            _set_basis
            Generate basis from str or use a given basis. 
        """
        # Generate basis from string str
        if type(basis) == str:
            self.basis = BasisSet.initialize(self.atoms,basis_name=basis)
        # Use given basis 
        if type(basis) == BasisSet:
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
        self.xc_name = kwargs.get('xc_name', 'LDA,VWN') 

    def _set_xc(self):
        """
            _set_xc 
            Construct a XC instance for 
            the given grid and xc_name. 
        """
        # Note: For XC the spin is either 0 or 1 
        # In this case the spin desides if one 
        # wants to use spin-polarized (spin=1) 
        # or spin-unpolarized (spin=0)
        # XC functionals 
        self.xc = XC(grids=self.grids,
                     spin=1,
                     xc_name=self.xc_name)

    def kernel(self):
        """
            kernel 
            Kernel function executing the self-consistent field
            calculation. 
        """
        results= UKS_SCF(
                    atoms = self.atoms, 
                    basis = self.basis, 
                    grids = self.grids,
                    maxiter=self.maxiter, 
                    verbose=self.verbose, 
                    Etol=self.Etol,
                    use_avg=self.use_avg,
                    xc=self.xc
                    )
        #self.Etot, self.mo_energy, self.mo_coeff = results 
        #return self.Etot 
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
    #   atoms = atoms_from_xyz(p_xyz+"/H.xyz",spin=1)
    #   atoms = atoms_from_xyz(p_xyz+"/He.xyz",spin=0)
    atoms = atoms_from_xyz(pkg_path[0]+"/structs"+"/LiH.xyz",spin=2)
    mf = UKS(atoms,"pc-1",xc_name="LDA,PW")
    mf.kernel() 
    
if __name__ == '__main__':
    main()

