import numpy as np
from itertools import product
from functools import reduce

def ao2mo_mp2(ERI,U,nocc):
    """
        ao2mo_mp2
        Transform atomic orbitals (ERI from RHF) into molecular orbitals needed by RMP2.

        Reference 
            - https://github.com/rpmuller/pyquante2/blob/master/pyquante2/ints/integrals.py#L105
    """
    return np.einsum('aI,bJ,cK,dL,abcd->IJKL',U[:,:nocc],U,U[:,:nocc],U,ERI)


def rmp2(ERI,U,Eigs,nocc,nvirt):
    """
        rmp2
        Calculate correlation energy
        using Møller–Plesset perturbation theory (MP)
        in the second order (MP2). 

        Reference 
            - https://github.com/rpmuller/pyquante2/blob/master/pyquante2/pt/mp2.py
    """
    moints = ao2mo_mp2(ERI,U,nocc)
    Emp2 = 0
    for a,b in product(range(nocc),repeat=2):
        Eab = 0
        for r,s in product(range(nocc,nocc+nvirt),repeat=2):
            arbs,asbr = moints[a,r,b,s],moints[a,s,b,r]
            Eab += arbs*(2*arbs-asbr)/ (Eigs[a]+Eigs[b]-Eigs[r]-Eigs[s])
        # For debugging: 
        # print(f"MP2 pair energy for {a}, {b}: {Eab}")
        Emp2 += Eab
    # For debugging 
    # print(f"MP2: correlation energy: {Emp2}")
    return Emp2

class RMP2:
    """
        RMP2 class 
        Møller–Plesset perturbation theory (MP)
        in the second order (MP2). 

        Input 
            - atoms: Atoms(), chilli_pys atoms object  
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

    def kernel(self): 
        """
            kernel 
            Kernel function to calculate MP2 correlation energy. 
        """
        # MP2 correlation energy Ecorr 
        Ecorr = rmp2(self.mf_init.ERI,
                     self.mf_init.U,
                     self.mf_init.Eigs,
                     self.nocc,
                     self.nvirt)
        # Total Energy = E_HF + Ecorr 
        Etot = self.mf_init.Etot + Ecorr
        print(f"Etot(MP2): {Etot}")
        return Etot 

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
    # 1st: do a RHF calculation 
    mf = RHF(atoms,basis_name="sto-3g",use_avg=True)
    mf.verbose = False
    mf.kernel()
    # 2nd: do a RMP2 calculation 
    mf_mp2 = RMP2(atoms,mf)
    mf_mp2.kernel() 

if __name__ == '__main__':
    main()



