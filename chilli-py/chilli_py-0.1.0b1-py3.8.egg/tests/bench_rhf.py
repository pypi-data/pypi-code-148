import numpy as np
from pprint import pprint 
from chilli_py.atoms import atoms_from_xyz
from chilli_py.RHF import RHF    
from chilli_py.utils import myprint, timeit 
from chilli_py import basis 
from chilli_py import __path__ as pkg_path
from chilli_py.bench import small_rbench, Entry, Benchmark, Settings, get_ref, sys2latex, print_latex_table, bench_chilli

""" Small benchmark for RHF """

def run_chilli_py(setup):
    """
        run
        Run chilli_py calculation. 
    """
    print('RHF, chilli_py')
    atoms = atoms_from_xyz(setup.f_xyz)
    rhf = RHF(atoms,
             basis_name=setup.basis_name,
             use_avg=setup.use_avg,
             maxiter=setup.maxiter,
             Etol=setup.Etol)
    rhf.kernel() 
    return rhf.Etot

def run_pyscf(setup):
    """
        run_pyscf 
        Run PySCF reference calculation (if needed). 
        We use this function to generate 
        the reference values (ref dict). 

        Note 
            - you need to install pyscf 
    """
    # Indirect imports, b/c CI 
    from pyscf import gto, scf
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
    # For Debugging 
    # Get overlap matrix 
    # S = mf.get_ovlp()
    # print('Overlap matrix \n S: \n {}'.format(S))
    # Get Hcore 
    # Hcore = Hcore = mf.get_hcore()
    # print('Hcore = T + V : \n {}'.format(Hcore))
    # Get Enuc 
    # print(f'Enuc = {mol.energy_nuc()}')
    # print(mf.mo_energy)
    # print("\n")
    return mf.e_tot 

def run_chilli_cpp(setup):
    """
        run_chilli_cpp 
        Run Chilli.cpp 

        Note
            - you need to install chilli_cpp 
    """
    # Indirect imports, b/c CI
    from chilli_cpp.chilli_cpp import Parameters, Calculation 
    mf = Calculation("RHF")
    p = Parameters()
    p.spin = setup.spin 
    p.charge = setup.charge  
    p.use_avg = setup.use_avg 
    p.maxiter = setup.maxiter 
    p.Etol = setup.Etol 
    p.f_xyz = setup.f_xyz
    p.basis_name = pkg_path[0]+"/basis/"+setup.basis_name 
    Etot = mf.kernel(p) 
    return Etot 

def run_chilli_jl(setup): 
    from chilli_py.tests.chilli_jl import interface_chilli_jl
    jl = interface_chilli_jl("RHF",
                             setup.f_xyz,
                             spin=setup.spin,
                             charge=setup.charge,
                             use_avg=str(setup.use_avg).lower(),
                             maxiter=setup.maxiter,
                             Etol=setup.Etol)
    Etot = jl.kernel()
    return Etot 

# SS. 13.07.2022, minimal parameters 
ref= {'CH4': {'ref': -39.72680917153617, 'val': -39.72680917658582},
 'H2': {'ref': -1.1166843870853405, 'val': -1.116684390016466},
 'H2O': {'ref': -74.96302313846277, 'val': -74.96302314036498},
 'He': {'ref': -2.807783957539974, 'val': -2.8077839575380965},
 'Ne': {'ref': -126.60452499680486, 'val': -126.60452499672792}
}


@timeit 
def test_rhf(use_ref=True,run_chilli_cpp=False,run_chilli_jl=False):
    """
        test_rhf
        Test RHF routine.
    """
    setup = Settings()
    #setup.basis_name = "3-21g"
    #setup.use_avg = False
    bench_dct = small_rbench
    bench_chilli(setup,
                 bench_dct,
                 method="RHF",
                 run_chilli_py=run_chilli_py,
                 run_chilli_cpp=run_chilli_cpp,
                 run_chilli_jl=run_chilli_jl,
                 run_pyscf=run_pyscf,
                 ref=ref,
                 use_ref=use_ref)

if __name__ == '__main__':
    # simple test using python3
    test_rhf(use_ref=True,run_chilli_cpp=False,run_chilli_jl=False)
    # full test using python-jl 
    # test_rhf(use_ref=True,run_chilli_cpp=run_chilli_cpp,run_chilli_jl=run_chilli_jl)

