import numpy as np 
from pprint import pprint 
from chilli_py.atoms import atoms_from_xyz
from chilli_py.RKS import RKS
from chilli_py.utils import myprint, timeit
from chilli_py import basis
from chilli_py import __path__ as pkg_path
from chilli_py.bench import small_rbench, Entry, Benchmark, Settings, get_ref, sys2latex, print_latex_table, bench_chilli

""" Small benchmark for RKS """

def run_chilli_py(setup):
    """
        run 
        Run chilli_py calculation. 
    """
    print("RKS, chilli_py")
    atoms = atoms_from_xyz(setup.f_xyz)
    rks = RKS(atoms,
            setup.basis_name,
            (setup.n_rad,setup.n_ang),
            Etol=setup.Etol,
            maxiter=setup.maxiter,
            verbose=False,
            use_avg=setup.use_avg,
            xc_name=setup.xc_name)
    rks.kernel() 
    return rks.Etot

def run_pyscf(setup):
    """
        run_pyscf 
        Run PySCF reference calculation (if needed).
        We use this to generate the reference values 
        (ref dict). 
    """
    # Indirect imports, b/c CI 
    from pyscf import gto, scf, dft
    print("RKS, PySCF")
    mol = gto.M(
                atom = setup.f_xyz,
                basis = setup.basis_name,
                symmetry = False,
                 )

    mf = scf.RKS(mol)
    mf.xc = setup.xc_name 
    mf.verbose = 4
    # PySCF hides one SCF step in the initialization 
    mf.max_cycle = setup.maxiter - 1 # maxiter -1 
    mf.conv_tol = setup.Etol 
    # With or without DIIS 
    #mf.diis = None
    # Use Hcore as inital guess for Fockian. 
    mf.init_guess = '1e'
    # We do not like pruning. 
    mf.grids.prune = None
    mf.grids.radi_method = dft.radi.gauss_chebyshev #dft.radi.becke
    mf.grids.radii_adjust = None 
    mf.grids.atom_grid = (setup.n_rad,setup.n_ang)
    mf.grids.build()
    if setup.use_avg == False:
        mf.diis = None
    
    mf.kernel()

    # Debugging 
    # Get overlap matrix 
    #S = mf.get_ovlp()
    #print('Overlap matrix \n S: \n {}'.format(S))
    #Hcore = mf.get_hcore()
    #print('Hcore = T + V : \n {}'.format(Hcore))
    #print(f'Enuc = {mol.energy_nuc()}')
    #print(mf.mo_energy)
    #print("\n")
    return mf.e_tot

def run_chilli_cpp(setup):
    """
        run_chilli.cpp 
        Run chilli.cpp 

        Note
            - you need to install chilli_py_cpp 
    """
    # Indirect imports, b/c CI
    from chilli_cpp.chilli_cpp import Parameters, Calculation
    mf = Calculation("RKS")
    p = Parameters()
    p.spin = setup.spin
    p.charge = setup.charge
    p.use_avg = setup.use_avg
    p.maxiter = setup.maxiter
    p.Etol = setup.Etol
    p.f_xyz = setup.f_xyz
    p.xc_name = setup.xc_name 
    p.n_rad = setup.n_rad 
    p.n_ang = setup.n_ang 
    p.basis_name = pkg_path[0]+"/basis/"+setup.basis_name
    Etot = mf.kernel(p)
    return Etot

def run_chilli_jl(setup):
    from chilli_py.tests.chilli_jl import interface_chilli_jl
    jl = interface_chilli_jl("RKS",
                             setup.f_xyz,
                             spin=setup.spin,
                             charge=setup.charge,
                             use_avg=str(setup.use_avg).lower(),
                             maxiter=setup.maxiter,
                             Etol=setup.Etol)
    Etot = jl.kernel()
    return Etot


# SS, 14.07.2022, minimal parameters 
ref={'CH4': {'ref': -39.61734073282798, 'val': -39.61734074295095},
 'H2': {'ref': -1.1211977345222683, 'val': -1.1211977349819646},
 'H2O': {'ref': -74.73205734781702, 'val': -74.73205736117771},
 'He': {'ref': -2.771886044438607, 'val': -2.771886044437081},
 'Ne': {'ref': -126.15195775319957, 'val': -126.15195775312718}
}

@timeit
def test_rks(use_ref=True,xc_name="LDA,VWN",run_chilli_cpp=False,run_chilli_jl=False):
    """
        test_rks
        Test RKS routine.
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
                 run_chilli_cpp=run_chilli_cpp,
                 run_chilli_jl=run_chilli_jl,
                 run_pyscf=run_pyscf,
                 ref=ref,
                 use_ref=use_ref)

if __name__ == '__main__': 
    test_rks(xc_name="LDA,VWN",use_ref=True,run_chilli_cpp=run_chilli_cpp,run_chilli_jl=run_chilli_jl)

