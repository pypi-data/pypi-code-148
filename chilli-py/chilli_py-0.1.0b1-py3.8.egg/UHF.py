import numpy as np
from chilli_py.BasisSet import BasisSet
from scipy.linalg import eigh
from chilli_py.utils import myprint 
from chilli_py.integrals import pairs, iiterator, one, two, get_J, get_K, get_JK, get_E, dmat 
from chilli_py.nuclear import nuclear_repulsion
from chilli_py.scf import DIIS, Results
from chilli_py.spin import spin_square, spin_square2

""" Unrestricted Hartree-Fock """

def UHF_SCF( atoms, basis, maxiter=20, verbose=True, Etol=1e-6,use_avg=False):
    """
        UHF_SCF 
        Unrestricted Hartree-Fock (UHF) self-consistent field (SCF) 

        Input
            - atoms: Atoms(), contains sym and pos 
            - basis: BasisSet(), basis set information 
            - maxiter: int(), maximal number of iterations
            - verbose: True or False, more output or not 
            - Etol: float(), convergence threshold 
            - use_avg: bool(), using DIIS or not 
    """
    print("Unrestricted Hartree-Fock (UHF)")
    
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
    
    Eigs,U = eigh(Hcore,S)
    Ua, Ub = U, U 
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
        avg_a = DIIS()
        avg_a.DIIS_start =1
        avg_b = DIIS()
        avg_b.DIIS_start =1


    print("Starting UHF calculation:")
    for iiter in range(maxiter):
        Da = dmat(Ua,Na)
        Db = dmat(Ub,Nb)
        if verbose: 
            myprint(Da=Da,Db=Db)
        Ja, Ka = get_JK(Da,ERI)
        Jb, Kb = get_JK(Db,ERI)
        Fa = Hcore + Ja + Jb - Ka
        Fb = Hcore + Ja + Jb - Kb
        Eone = get_E(Hcore,Da+Db)/2.
        Etwoa = get_E(Fa,Da)/2.
        Etwob = get_E(Fb,Db)/2.
        Etwo = Etwoa + Etwob

        if use_avg:
            Fa,DIIS_e_a, dRMS_a, = avg_a.kernel(iiter,S,Fa,Da)
            Fb,DIIS_e_b, dRMS_b, = avg_b.kernel(iiter,S,Fb,Db)
            dRMS = 0.5*(dRMS_a + dRMS_b)

        Eigs_a,Ua = eigh(Fa,S)
        Eigs_b,Ub = eigh(Fb,S)
        # Note PySCF notation: 
        #   Eigs, U = mo_energy, mo_coeff 
        Etot = Enuc + Eone + Etwo
        dEtot = abs(Etot - Eold)
        # Iteration: Output 
        iiter_str = f">>> iter {iiter: 4d} E = {Etot: 18.10f} Eh DeltaE = {dEtot: 10.5e} Eh"
        if use_avg:
            iiter_str += f" dRMS: {dRMS: 10.5e}"
        print(iiter_str) 
        if verbose: 
            myprint(Enuc=Enuc,Eone=Eone,Etwo=Etwo)
        if np.isclose(Etot,Eold,0,Etol):
            spin_square(S,Na,Nb,Ua,Ub)
            # check if it is equal to spin_square 
            # spin_square2(S,Na,Nb,Ua,Ub)
            IS_CONVERGED = True
            Eigs_a,Ua = eigh(Fa,S)
            Eigs_b,Ub = eigh(Fb,S)
            Da = dmat(Ua,Na)
            Db = dmat(Ub,Nb)
            print("Final: Eigenvalues")
            print(f"Eigs_a = {Eigs_a}")
            print(f"Eigs_b = {Eigs_b}")
            break
        Eold  = Etot

    if not IS_CONVERGED:
        print("WARNING: UHF is not converged")

    # Results 
    res  = Results()
    res.Etot = Etot
    res.Eigs_a= Eigs_a
    res.Eigs_b= Eigs_b
    res.Ua = Ua
    res.Ub = Ub 
    res.Da = Da
    res.Db = Db
    #res.mu = mu
    #res.mu_abs = mu_abs
    return res

class UHF: 
    """
        UHF class 
        Unrestricted Hartree-Fock (UHF) class. 

        Input
            - atoms: Atoms()
            - basis_name: str(), basis set name  
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


    def kernel(self):
        """
            kernel 
            Kernel function executing the self-consistent field
            calculation. 
        """
        results= UHF_SCF(
                    atoms = self.atoms, 
                    basis = self.basis, 
                    maxiter=self.maxiter, 
                    verbose=self.verbose, 
                    Etol=self.Etol,
                    use_avg=self.use_avg
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
    atoms = atoms_from_xyz(pkg_path[0]+"/structs"+"/H2O.xyz",spin=2)
    mf = UHF(atoms,basis_name="pc-0",use_avg=True)
    mf.kernel() 
    
if __name__ == '__main__':
    main()

