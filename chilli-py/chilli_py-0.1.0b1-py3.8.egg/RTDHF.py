import numpy as np 
from scipy.linalg import eigh,sqrtm, lu
from itertools import product

# Notes
#   - mmd code notation 
#       + mmd vs chilli_py 
#       + self.mol.TwoE -> ERI 
#       + self.mol.C -> U 
#       + MO -> Eigs 
#       + single_bar -> moints (MP2) 
#       + Core -> T + V = Hcore 
#       + PySCF: A, B for HF and DFT 
#           * https://github.com/pyscf/pyscf/blob/master/pyscf/tdscf/rhf.py#L110
#           * PySCF reports the transition energies for Nstates
#           * SS: I currently do not understand how PySCF counts these states 

def ao2mo(Hcore,ERI,U,nocc,Eigs):
    """ 
        ao2mo
        Convert atomic orbitals (ao) to 
        molecular orbitals (mo). 
        
        Output 
            - single_bar, needed by RMP2, RTDHF 
            - double_bar, needed by RTDHF 
            - Hp, needed by RTDHF
            - fs, needed by RTDHF
    """
    # single_bar -> molint
    single_bar = np.einsum('mp,mnlz->pnlz',U,ERI)
    temp = np.einsum('nq,pnlz->pqlz',U,single_bar)
    single_bar = np.einsum('lr,pqlz->pqrz',U,temp)
    temp = np.einsum('zs,pqrz->pqrs',U,single_bar)
    single_bar = temp

    # double_bar  
    double_bar = np.zeros([2*idx for idx in single_bar.shape])
    for p in range(double_bar.shape[0]):
        for q in range(double_bar.shape[1]):
            for r in range(double_bar.shape[2]):
                for s in range(double_bar.shape[3]):
                    value1 = single_bar[p//2,r//2,q//2,s//2].real * (p%2==r%2) * (q%2==s%2)
                    value2 = single_bar[p//2,s//2,q//2,r//2].real * (p%2==s%2) * (q%2==r%2)
                    double_bar[p,q,r,s] = value1 - value2

    # create Hp, the spin basis one electron operator
    spin = np.eye(2)
    Hp = np.kron(np.einsum('uj,vi,uv',U,U, Hcore).real,spin)

    # create fs, the spin basis fock matrix eigenvalues
    fs = np.kron(np.diag(Eigs),spin)
    return single_bar, double_bar, Hp, fs 

def rmp2(Hcore,ERI,U,Eigs,nocc,nvirt):
    """
        rmp2 
        Alternative formulation from the mmd code. 
        This here to debug/understand other post-SCF 
        routines from the mmd code. 
    """
    # MO -> Eigs 
    # Use spatial orbitals from RHF reference
    single_bar, double_bar, Hp, fs = ao2mo(Hcore,ERI,U,nocc,Eigs)
    EMP2 = 0.0
    occupied = range(nocc)
    virtual  = range(nocc,nocc+nvirt)
    for i,j,a,b in product(occupied,occupied,virtual,virtual):
        denom = Eigs[i] + Eigs[j] - Eigs[a] - Eigs[b]
        numer = single_bar[i,a,j,b]*(2.0*single_bar[i,a,j,b] - single_bar[i,b,j,a])
        EMP2 += numer/denom
    return EMP2  

def rtdhf(Hcore,ERI,U,Eigs,nocc,nvirt,method):
    """
        rtdhf
        Restricted time-dependent Hartree-Fock (RTDHF) 

        Workflow 
            - build A, M matricies 
            - build Hamiltonian H = H(A,B) 
            - diagonalize H

        Reference 
            - https://github.com/jjgoings/McMurchie-Davidson/blob/master/mmd/postscf.py#L311
    """
    def method_hermitian(A,B): 
        """
            method_hermitian
            method hermitian does the Hermitian reduced variant, e.g., sqrt(A-B).(A+B).sqrt(A-B)
        """
        # SS: the sqrtm term is numerical dangerous 
        sqrt_term = sqrtm(A-B)
        H = np.dot(sqrt_term,np.dot(A+B,sqrt_term))
        transition_energies,transition_densities = eigh(H)
        transition_energies = np.sqrt(transition_energies)
        return transition_energies

    def method_reduced(A,B): 
        """
            method_reduced
            method reduced does the non-Hermitian reduced variant, e.g.,  (A-B).(A+B)
        """
        H = np.dot(A-B,A+B)
        transition_energies,transition_densities = np.linalg.eig(H)
        transition_energies = np.sqrt(transition_energies)
        idx = transition_energies.argsort()
        transition_energies = transition_energies[idx].real
        return transition_energies

    def method_full(A,B,nov): 
        """
            method_full
            method full  does the non-Hermitian, e.g., [[A,B],[-B.T,-A.T]]' 
        """
        H = np.block([[A,B],[-B.T,-A.T]])
        transition_energies,transition_densities = np.linalg.eig(H)
        idx = transition_energies.argsort()
        transition_energies = transition_energies[idx].real
        # take positive eigenvalues
        transition_energies = transition_energies[nov:]
        return transition_energies 

    def print_results(A,transition_energies):
        """
            print_results
            Print the transition energies. 
        """
        tdhf_omega = transition_energies * 27.211399 # to eV

        print("\nTime-dependent Hartree-Fock (TDHF)")
        print("------------------------------")
        print(f"Algorithm:        {method}")
        for state in range(min(len(A),10)):
            print(f"TDHF state {state} (eV): {tdhf_omega[state]: 12.4f}")

    # transform: ao2mo 
    single_bar, double_bar, Hp, fs = ao2mo(Hcore,ERI,U,nocc,Eigs)
    # spin? 
    nocc  *= 2 
    nvirt *= 2 
    nov = nocc * nvirt
    occ = slice(nocc) 
    vir = slice(nocc,nocc+nvirt)
    
    # form full A and B matrices 
    # depends on: fs, double_bar 
    # A matrix 
    A  = np.einsum('ab,ij->iajb',np.diag(np.diag(fs)[vir]),np.diag(np.ones(nocc))) # + e_a
    A -= np.einsum('ij,ab->iajb',np.diag(np.diag(fs)[occ]),np.diag(np.ones(nvirt))) # - e_i
    A += np.einsum('ajib->iajb',double_bar[vir,occ,occ,vir]) # + <aj||ib>

    # B matrix 
    B  = np.einsum('abij->iajb',double_bar[vir,vir,occ,occ]) # + <ab||ij>

    A = A.reshape(nov,nov)
    B = B.reshape(nov,nov)

    if method == "hermitian": 
        transition_energies = method_hermitian(A,B)
    if method == "reduced":
        transition_energies = method_reduced(A,B)
    if method == "full":
        transition_energies = method_full(A,B,nov)
    # Output 
    print_results(A,transition_energies)
    return transition_energies 

class RTDHF:
    """
        RTDHF class 
        Restricted time-dependent Hartree-Fock (RTDHF). 

        Includes 
            - Møller–Plesset perturbation theory (MP)
              in the second order (MP2). 
              For debugging reasons. 

        Input 
            - atoms: Atoms(), chilli_py Atoms object 
            - mf_init: a chilli_py RHF() object for the respective atoms 
    """
    def __init__(self,atoms,mf_init):
        """
            __init__
            Initialize an instance of the class. 
        """
        self.atoms = atoms
        self.mf_init = mf_init
        self._init_orbs()

    def _init_orbs(self):
        """
            _init_orbs
            Get number of occupied and virtual orbitals. 
        """
        # number of occupied orbitals 
        self.nocc = int(self.atoms.Nelec/2)
        # number of molecular orbitals 
        self.nmo = len(self.mf_init.basis)
        # number of virtual orbitals 
        self.nvirt = self.nmo - self.nocc
        print(f"nocc: {self.nocc} nvirt: {self.nvirt} nmo: {self.nmo}")

    def _mp2(self):
        """
            kernel 
            Kernel function to calculate MP2 correlation energy. 
        """
        # MP2 correlation energy Ecorr 
        Ecorr = rmp2(self.mf_init.Hcore,
                     self.mf_init.ERI,
                     self.mf_init.U,
                     self.mf_init.Eigs,
                     self.nocc,
                     self.nvirt)
        # Total Energy = E_HF + Ecorr 
        Etot = self.mf_init.Etot + Ecorr
        print(f"Etot(MP2): {Etot}")
        return Etot

    def _rtdhf(self,method="full"): 
        transition_energies = rtdhf(self.mf_init.Hcore,
                                    self.mf_init.ERI,
                                    self.mf_init.U,
                                    self.mf_init.Eigs,
                                    self.nocc,
                                    self.nvirt,
                                    method)
        return transition_energies

def main():
    """
        main
        Main function to test this routine.
    """
    from chilli_py.atoms import Atoms, atoms_from_xyz
    from chilli_py.BasisSet import BasisSet
    from chilli_py.RHF import RHF
    from chilli_py import __path__ as pkg_path

    # using Atoms object
    #   atoms = Atoms(['H','H'],[[0,0,0],[1.4,0,0]])
    # using xyz files
    f_xyz = pkg_path[0]+"/structs"+"/CH4.xyz"
    atoms = atoms_from_xyz(f_xyz)
    basis = BasisSet.initialize(atoms,basis_name="sto-3g")
    # 1st: do a RHF calculation
    mf = RHF(atoms,basis_name="sto-3g",use_avg=True)
    mf.verbose = False
    mf.kernel()
    # 2nd: do a RMP2 calculation
    mf_rtdhf = RTDHF(atoms,mf)
    mf_rtdhf._mp2()
    #mf_rtdhf._rtdhf(method="hermitian")
    #mf_rtdhf._rtdhf(method="reduced")
    #mf_rtdhf._rtdhf(method="full")

if __name__ == '__main__':
    main()

