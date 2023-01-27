from chilli_py.read_basis_g94 import read_basis_set_g94
from chilli_py.atoms import Atoms 
from chilli_py.CGBF import CGBF
from chilli_py import __path__ as pkg_path  
from copy import copy, deepcopy 

class BasisSet:
    """
        BasisSet class 
        Construct for atoms object the 
        CGBF basis. 
    """
    def __init__(self): 
        """
            __init__
            Initialize instance of the class. 
        """
        self.basis = []

    @staticmethod
    def _full_path(basis_name):
        """
            _full_path

            Private method. 
            Used to determine the package path 
            to the basis sets. 
        """
        return pkg_path[0]+"/basis/"+basis_name 

    @staticmethod
    def initialize(atoms,basis_name="sto-3g"):
        """
            initialize
            Initialize a BasisSet instance from a basis name. 

            Input 
                - atoms: Atoms(), chilli_pys Atoms object 
                - basis_name: str(), basis set name, e.g., "sto-3g" 
        """
        basis_name = BasisSet._full_path(basis_name) 
        basis = get_basis(atoms,basis_name)
        return basis 

    def add(self,bf):
        """
            add 
            Add new basis function (bf) to basis. 
            For Gaussians bf is a CGBF. 
        """
        self.basis.append(bf) 

    def __repr__(self):
        """
            __repr__
            Representation of the instance. 
        """
        s = ''
        for i,bf in enumerate(self.basis):
            s += f'\n\nCGBF: {i}\n\n'
            s += repr(bf) 
        return s 

    def show(self):
        """
            show 
            Show the representation of the instance. 
        """
        print(self.__repr__())


    def __len__(self):
        """
            __len__
            Length of the instance. 
            This is return if len() is 
            applied to a instance of the class. 
        """
        return len(self.basis)

def get_basis(atoms,basis_name):
    """
        get_basis 
        Construct CGBFs for atoms object. 

        Input
            - atoms, Atoms(), contains sym,pos etc.
            - basis_name, str(), basis set file, e.g., g94 format 

        Output 
            - basis, BasisSet(), basis set information 

    """
    # Read: Basis set 
    #   + returns dct with basis data per species 
    data_dict = read_basis_set_g94(basis_name)
    # Build: basis set instance 
    basis = BasisSet()
    
    Nbasis = 0
    # Loop over all atoms
    for ia,syma in enumerate(atoms.sym):
        x,y,z = atoms.pos[ia]
        # Basis set entry for element 
        data = data_dict[syma]
        Nsyms = data.Nsyms
        # Loop over basis functions 
        for isym in range(Nsyms):
            # get basis symbols: S, P, D, F
            bsym = data.syms[isym]
            # Loop over basis symbols 
            for (I,J,K) in sym2power[bsym]:
                # Build: CGBF
                cgbf = CGBF( (x,y,z), (I,J,K) )
                ncontr = data.Ncontr[isym]
                for i in range(ncontr):
                    expn = data.expns[isym][i]
                    coef = data.coeffs[isym][i]
                    # Add PGBF to CGBF 
                    cgbf.add(coef,expn)
                # Add: CGBF to basis 
                basis.add(cgbf)
                Nbasis = Nbasis + 1
    print("Nbasis = ", Nbasis)
    return basis

sym2power = {
        "S" : [(0,0,0)],
        "P" : [(1,0,0),(0,1,0),(0,0,1)],
        "D" : [(2,0,0),(0,2,0),(0,0,2),(1,1,0),(1,0,1),(0,1,1)],
        "F" : [(3,0,0),(0,3,0),(0,0,3),(2,1,0),(2,0,1),(1,2,0),(1,1,1),(1,0,2),(0,2,1),(0,1,2)]
        } 

def main():
    """
        main 
        Main function to test the routine.
    """
    atoms = Atoms(['H','H'],[[0,0,0],[1.4,0,0]])
    print(atoms.Z)
    basis = BasisSet.initialize(atoms) 
    print(basis)

if __name__ == '__main__': 
    main() 
