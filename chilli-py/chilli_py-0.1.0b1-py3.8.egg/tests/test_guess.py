#from chilli_py.bench import small_rbench, Entry, Benchmark
from chilli_py.bench import small_rbench, Entry, Benchmark, Settings, get_ref, sys2latex, print_latex_table, bench_chilli
from chilli_py.atoms import Atoms, atoms_from_xyz 
from chilli_py.RHF import RHF 
from chilli_py.UHF import UHF 
from chilli_py.UKS import UKS 
from chilli_py import basis 
import scipy 

atoms_config = {
                "H" : {"spin": 1},
                "He": {"spin": 0},
                "C" : {"spin": 2},
                "O" : {"spin": 2},
                "Ne": {"spin": 0},
}

def run_chilli_py(setup):
    # try to implement a simple superposition of atomic orbitals guess 
    atoms = atoms_from_xyz(setup.f_xyz)
    atoms_D = []
    for sym,pos in zip(atoms.sym,atoms.pos):
        atoms = Atoms([sym],[pos],spin=atoms_config[sym]["spin"])
        mf = UHF(atoms,
                 setup.basis_name,
                 Etol=setup.Etol,
                 maxiter=setup.maxiter,
                 verbose=False,
                 use_avg=setup.use_avg
        ) 
        mf.kernel()
        atoms_D.append(mf.Da+mf.Db)
    D = scipy.linalg.block_diag(*atoms_D)
    return D 

ref = {}

def run_pyscf(setup): 

    # https://github.com/pyscf/pyscf/blob/master/pyscf/scf/hf.py
    # init_guess_by_atom
    # SAD
    # https://github.com/pyscf/pyscf/blob/master/pyscf/scf/hf.py#L465
    # Indirect imports, b/c CI 
    from pyscf import gto, scf, dft
    print("RKS, PySCF")
    mol = gto.M(
                atom = setup.f_xyz,
                basis = setup.basis_name,
                symmetry = False,
                )

    mf = scf.UHF(mol)
    #mf.xc = xc
    mf.verbose = 8
    # PySCF hides one SCF step in the initialization 
    mf.max_cycle = setup.maxiter - 1 # maxiter -1 
    mf.conv_tol = setup.Etol
    # With or without DIIS 
    #mf.diis = None
    # Use Hcore as inital guess for Fockian. 
    #mf.init_guess = '1e'
    # We do not like pruning. 
    #mf.grids.prune = None
    #mf.grids.radi_method = dft.radi.gauss_chebyshev #dft.radi.becke
    #mf.grids.radii_adjust = None
    #mf.grids.atom_grid = (setup.n_rad,setup.n_ang)
    #mf.grids.build()
    if setup.use_avg == False:
        mf.diis = None

    mf.kernel()

    DM = scf.hf.init_guess_by_atom(mol)
    return DM

def test_guess(use_ref=True,xc_name="LDA,VWN"):
    """
        test_guess
        Test guess routine. 
    """
    setup = Settings()
    #setup.basis_name = "3-21g"
    #setup.use_avg = False
    setup.xc_name = xc_name
    bench_dct = small_rbench
    bench_chilli(setup,
                 bench_dct,
                 method="RKS",
                 run_chilli_py=run_chilli_py,
                 run_chilli_cpp=False,
                 run_pyscf=run_pyscf,
                 ref=ref,
                 use_ref=use_ref)

if __name__ == '__main__':
    test_guess(use_ref=False)

