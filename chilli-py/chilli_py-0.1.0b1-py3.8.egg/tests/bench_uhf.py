import numpy as np
from pprint import pprint 
from chilli_py.atoms import atoms_from_xyz
from chilli_py.UHF import UHF    
from chilli_py.utils import myprint, timeit
from chilli_py import basis  
from chilli_py import __path__ as pkg_path
from chilli_py.bench import small_ubench, Entry, Benchmark, Settings, get_ref, sys2latex, print_latex_table, bench_chilli

""" Small benchmark for UHF """

def run_chilli_py(setup):
    """
        run
        Run chilli_py calculation. 
    """
    print('UHF, chilli_py')
    atoms = atoms_from_xyz(setup.f_xyz,spin=setup.spin)
    mf = UHF(atoms,
             basis_name=setup.basis_name,
             use_avg=setup.use_avg,
             maxiter=setup.maxiter,
             Etol=setup.Etol 
    )
    mf.kernel() 
    return mf.Etot

def run_pyscf(setup):
    """
        run_pyscf 
        Run PySCF reference calculation (if needed). 
        We use this function to generate 
        the reference values (ref dict). 
    """
    # Indirect imports, b/c CI 
    from pyscf import gto, scf
    print('UHF, PySCF')
    mol = gto.M(
                atom = setup.f_xyz,
                basis = setup.basis_name,
                symmetry = False,
                spin=setup.spin
                 )

    mf = scf.UHF(mol)
    #mf.init_guess_breaksym = False
    mf.max_cycle = setup.maxiter -1 
    mf.conv_tol = setup.Etol 
    mf.init_guess = '1e'
    mf.verbose = 4
    if setup.use_avg == False: 
        mf.diis = None
    mf.kernel()

    # Debugging 
    ## Get overlap matrix 
    #S = mf.get_ovlp()
    #print('Overlap matrix \n S: \n {}'.format(S))
    #Hcore = Hcore = mf.get_hcore()
    #print('Hcore = T + V : \n {}'.format(Hcore))
    #print(f'Enuc = {mol.energy_nuc()}')
    #mf.kernel()
    #print(mf.mo_energy)
    #print("\n")
    return mf.e_tot

def run_chilli_cpp(setup):
    """
        run_chilli_cpp 
        Run Chilli.cpp 

        Note
            - you need to install chilli_cpp 
    """
    from chilli_cpp.chilli_cpp import Parameters, Calculation
    mf = Calculation("UHF")
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
    jl = interface_chilli_jl("UHF",
                             setup.f_xyz,
                             spin=setup.spin,
                             charge=setup.charge,
                             use_avg=str(setup.use_avg).lower(),
                             maxiter=setup.maxiter,
                             Etol=setup.Etol)
    Etot = jl.kernel()
    return Etot


# SS, 14.07.2022, minimal parameters 
ref={'H': {'ref': -0.46658184955727533, 'val': -0.46658184955686643},
 'Li': {'ref': -7.315525981281088, 'val': -7.315525981276171},
 'NH': {'ref': -54.261895676459545, 'val': -54.26189375451049},
 'O2': {'ref': -147.3785591407101, 'val': -147.37855845963608},
 'S2': {'ref': -786.1557515667291, 'val': -786.1557514367977}
}

@timeit
def test_uhf(use_ref=True,run_chilli_cpp=False,run_chilli_jl=False):
    """
        test_uhf
        Test UHF routine.
    """
    setup = Settings()
    #setup.basis_name = "3-21g"
    bench_dct = small_ubench
    bench_chilli(setup,
                 bench_dct,
                 method="UHF",
                 run_chilli_py=run_chilli_py,
                 run_chilli_cpp=run_chilli_cpp,
                 run_chilli_jl=run_chilli_jl,
                 run_pyscf=run_pyscf,
                 ref=ref,
                 use_ref=use_ref)


if __name__ == '__main__': 
    test_uhf(use_ref=True,run_chilli_cpp=run_chilli_cpp,run_chilli_jl=run_chilli_jl)

