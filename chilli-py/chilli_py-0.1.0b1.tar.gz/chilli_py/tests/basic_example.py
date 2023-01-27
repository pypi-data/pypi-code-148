from chilli_py.atoms import atoms_from_xyz
from chilli_py.RHF import RHF
from chilli_py import __path__ as pkg_path

def basic_example():
    """
        basic_example
        Run chilli_py calculation. 
    """
    print('RHF, chilli_py')
    f_xyz = pkg_path[0]+"/structs"+"/H2O.xyz" 
    atoms = atoms_from_xyz(f_xyz)
    rhf = RHF(atoms,
             basis_name="sto-3g",
             use_avg=True,
             maxiter=300,
             Etol=1e-6)
    rhf.kernel()
    return rhf.Etot

if __name__ == "__main__": 
    basic_example() 
