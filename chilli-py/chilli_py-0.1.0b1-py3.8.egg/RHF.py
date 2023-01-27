import numpy as np
from chilli_py.BasisSet import BasisSet
from scipy.linalg import eigh
from chilli_py.utils import myprint 
from chilli_py.integrals import pairs, iiterator, one, two, get_J, get_K, get_2JK, get_E, dmat, dip_moment
from chilli_py.coulomb import coulomb_cgbf as coulomb
from chilli_py.HGP import coulomb_hgp_cgbf
from chilli_py.nuclear import nuclear_repulsion
from chilli_py.scf import DIIS, Results
from chilli_py.utils import timeit

""" Restricted Hartree-Fock """

def RHF_SCF(atoms,basis,maxiter=20,verbose=True,Etol=1e-6,use_avg=False,coulomb=coulomb):
    """
        RHF_SCF 
        Restricted Hartree-Fock (RHF) self-consistent field (SCF) 

        Input
            - atoms, Atoms(), contains sym and pos 
            - basis, BasisSet(), basis set information 
            - maxiter, int(), maximal number of iterations
            - verbose, True or False, more output or not 
            - Etol, float(), convergence threshold
            - use_avg, bool(), using DIIS or not 
            - coulomb, Python function, i.e., coulomb_cgbf or coulomb_hgp_cgbf
    """
    print("Restricted Hartree-Fock (RHF)")
    
    Nelec= atoms.Nelec
    Nclosed,Nopen = divmod( int(Nelec), 2 )
    print(f"Nel = {Nelec: d}, Nclosed: {Nclosed: d}, Nopen: {Nopen: d}\n")

    print("1e integrals ...")
    S,T,V,Mx,My,Mz = one(basis,atoms)
    if verbose: 
        myprint(S=S,T=T,V=V)
    print("2e integrals ...")
    ERI = two(basis,ERI=coulomb)
    if verbose: 
        myprint(ERI=ERI)
    
    Hcore = T+V
    if verbose: 
        myprint(Hcore=Hcore)
    
    Eigs,U = eigh(Hcore,S)
    if verbose: 
        myprint(Eigs=Eigs)

    Enuc = nuclear_repulsion(atoms)
    if verbose:
        myprint(Enuc=Enuc)
    Eold = 0.0
    Energy = 0.0
  
    IS_CONVERGED = False
    dEtot = 1.0
    if use_avg:
        avg = DIIS()
    print("Starting RHF calculation:")
    for iiter in range(maxiter):
        D = dmat(U,Nclosed)
        if verbose: 
            myprint(D=D)
        G = get_2JK(D,ERI)
        F = Hcore + G
        if use_avg:
            #F = avg.get_F(F,D)
            F,DIIS_e, dRMS, = avg.kernel(iiter,S,F,D)
        Eigs,U = eigh(F,S)
        # Note PySCF notation: Eigs, U = mo_energy, mo_coeff 
        Eone = get_E(Hcore,D)
        Etwo = get_E(F,D)
        Etot = Enuc + Eone + Etwo
        dEtot = abs(Etot - Eold)
        iiter_str = f">>> iter {iiter: 4d} E = {Etot: 18.10f} Eh DeltaE = {dEtot: 10.5e} Eh"
        if use_avg: 
            iiter_str += f" dRMS: {dRMS: 10.5e}"
        print(iiter_str)
        if verbose: 
            # Dipole moment 
            mu, mu_abs = dip_moment(atoms,Mx,My,Mz,D)
            myprint(Enuc=Enuc,Eone=Eone,Etwo=Etwo)
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
        print("WARNING: RHF is not converged")

    # Results 
    res  = Results() 
    res.Etot = Etot
    res.Hcore = Hcore 
    res.ERI = ERI 
    res.Eigs = Eigs
    res.U = U 
    res.D = D 
    res.mu = mu 
    res.mu_abs = mu_abs
    return res 

class RHF: 
    """
        RHF class 
        Restricted Hartree-Fock (RHF) class. 

        Input
            - atoms 
            - basis 
    """
    def __init__(self,atoms,basis_name="sto-3g",**kwargs): 
        """
            __init__ 
            Initialize instance of the class. 
        """
        # primary input 
        self.atoms = atoms
        self._set_basis(basis_name)
        # secondary input 
        self._set_kwargs(kwargs)

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
            self.basis = basis_name 

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
        self.coulomb = kwargs.get('coulomb',coulomb)

    @timeit 
    def kernel(self):
        """
            kernel 
            Kernel function executing the self-consistent field
            calculation. 
        """
        results= RHF_SCF(
                    atoms = self.atoms, 
                    basis = self.basis, 
                    maxiter=self.maxiter, 
                    verbose=self.verbose, 
                    Etol=self.Etol,
                    use_avg=self.use_avg,
                    coulomb=self.coulomb
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

    # using Atoms object 
    #   atoms = Atoms(['H','H'],[[0,0,0],[1.4,0,0]])
    # using xyz files 
    atoms = atoms_from_xyz(pkg_path[0]+"/structs"+"/H2O.xyz")
    basis = BasisSet.initialize(atoms,basis_name="sto-3g")

    mf = RHF(atoms,basis_name="sto-3g",use_avg=False,coulomb=coulomb)
    # If you want more output, you can use: 
    # mf.verbose = True
    mf.kernel()
    
    mf = RHF(atoms,basis_name="pc-0",use_avg=True,coulomb=coulomb_hgp_cgbf)
    mf.verbose = False
    mf.kernel()

if __name__ == '__main__':
    main()

