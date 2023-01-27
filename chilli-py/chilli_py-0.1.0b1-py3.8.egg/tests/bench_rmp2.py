import numpy as np 
from pprint import pprint 
from chilli_py.atoms import atoms_from_xyz
from chilli_py.RHF import RHF    
from chilli_py.RMP2 import RMP2 
from chilli_py.utils import myprint, timeit 
from chilli_py import basis  
#from chilli_py.bench import small_rbench, Entry, Benchmark
from chilli_py.bench import small_rbench, Entry, Benchmark, Settings, get_ref, sys2latex, print_latex_table, bench_chilli

""" Small benchmark for RMP2 """

def run_chilli_py(setup):
    """
        run
        Run run_chilli_py calculation. 
    """
    print('RMP2, chilli_py')
    atoms = atoms_from_xyz(setup.f_xyz)
    rhf = RHF(atoms,
              basis_name=setup.basis_name,
              use_avg=setup.use_avg,
              maxiter=setup.maxiter,
              Etol=setup.Etol
    )
    rhf.kernel()
    mp2 = RMP2(atoms,rhf) 
    Etot = mp2.kernel() 
    return Etot 

def run_pyscf(setup):
    """
        run_pyscf 
        Run PySCF reference calculation (if needed). 
        We use this function to generate 
        the reference values (ref dict). 
    """
    from pyscf import gto, scf
    from pyscf.mp.mp2 import MP2
    print('RHF, PySCF')
    mol = gto.M(
                atom = setup.f_xyz,
                basis = setup.basis_name,
                symmetry = False,
    )

    mf = scf.HF(mol)
    # Hcore guess 
    mf.init_guess = '1e'
    mf.verbose = 4
    mf.max_cycle = setup.maxiter  - 1
    mf.conv_tol = setup.Etol
    if setup.use_avg == False:
        mf.diis = None
    mf.kernel()
    print('RMP2, PySCF')
    mf_mp2 = MP2(mf)
    mf_mp2.kernel()
    e_corr = mf_mp2.e_corr 
    return mf.e_tot + e_corr 

# SS: 08.02.2022, RMP2, STO-3G
ref = {'CH4': {'ref': -39.78306565312914, 'val': -39.78306564333435},
       'H2': {'ref': -1.1298551535553094, 'val': -1.1298551552512728},
       'H2O': {'ref': -74.9985687902156, 'val': -74.99856878634886},
       'He': {'ref': -2.807783957539974, 'val': -2.8077839575380965},
       'Ne': {'ref': -126.60452499680486, 'val': -126.60452499672792}
}

@timeit
def test_rmp2(use_ref=True,run_chilli_cpp=False):
    """
        test_rmp2
        Test RMP2 routine.
    """
    setup = Settings()
    bench_dct = small_rbench
    bench_chilli(setup,
                 bench_dct,
                 method="RMP2",
                 run_chilli_py=run_chilli_py,
                 run_chilli_cpp=run_chilli_cpp,
                 run_pyscf=run_pyscf,
                 ref=ref,
                 use_ref=use_ref)

if __name__ == '__main__': 
    test_rmp2(use_ref=True)

