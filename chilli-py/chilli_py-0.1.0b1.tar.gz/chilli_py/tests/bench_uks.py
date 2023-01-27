import numpy as np 
from pprint import pprint
from chilli_py.atoms import atoms_from_xyz
from chilli_py.UKS import UKS
from chilli_py.utils import myprint, timeit
from chilli_py import basis
from chilli_py import __path__ as pkg_path
from chilli_py.bench import small_ubench, Entry, Benchmark, Settings, get_ref, sys2latex, print_latex_table, bench_chilli, xc_name2libxc

""" Small benchmark for UKS """

def run_chilli_py(setup):
    """
        run 
        Run chilli_py calculation. 
    """
    print("UKS, chilli_py")
    atoms = atoms_from_xyz(setup.f_xyz,spin=setup.spin)
    mf = UKS(atoms,
            setup.basis_name,
            (setup.n_rad,setup.n_ang),
            Etol=setup.Etol,
            maxiter=setup.maxiter,
            verbose=False,
            use_avg=setup.use_avg,
            xc_name=setup.xc_name)
    mf.kernel() 
    return mf.Etot

def run_pyscf(setup):
    """
        run_pyscf 
        Run PySCF reference calculation (if needed).
        We use this to generate the reference values 
        (ref dict). 
    """
    # Indirect imports, b/c CI 
    from pyscf import gto, scf, dft
    print("UKS, PySCF")
    mol = gto.M(
                atom = setup.f_xyz,
                basis = setup.basis_name,
                symmetry = False,
                spin=setup.spin
    )

    mf = scf.UKS(mol)
    mf.xc = xc_name2libxc[setup.xc_name]
    mf.verbose = 4
    # PySCF hides one SCF step in the initialization 
    mf.max_cycle = setup.maxiter -1 # maxiter -1 
    mf.conv_tol = setup.Etol 
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
        run_chilli_cpp 
        Run Chilli.cpp 

        Note
            - you need to install chilli_cpp 
    """
    # Indirect imports, b/c CI
    from chilli_cpp.chilli_cpp import Parameters, Calculation
    mf = Calculation("UKS")
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
    jl = interface_chilli_jl("UKS",
                             setup.f_xyz,
                             spin=setup.spin,
                             charge=setup.charge,
                             use_avg=str(setup.use_avg).lower(),
                             maxiter=setup.maxiter,
                             Etol=setup.Etol)
    Etot = jl.kernel()
    return Etot

# SS, 14.07.2022, minimal parameters
ref= {'H': {'ref': -0.4356702329795719, 'val': -0.435670232979293},
 'Li': {'ref': -7.221301649774393, 'val': -7.221301649770039},
 'NH': {'ref': -54.001295811516485, 'val': -54.00129563361183},
 'O2': {'ref': -147.19399357766653, 'val': -147.1939935450742},
 'S2': {'ref': -784.7274122078315, 'val': -784.7274121604823}
}


@timeit
def test_uks(use_ref=True,xc_name="LDA,VWN",run_chilli_cpp=False,run_chilli_jl=False):
    """
        test_uks
        Test UKS routine.
    """
    setup = Settings()
    #setup.basis_name = "3-21g"
    #setup.use_avg = False
    setup.xc_name = xc_name
    bench_dct = small_ubench
    bench_chilli(setup,
                 bench_dct,
                 method="UKS",
                 run_chilli_py=run_chilli_py,
                 run_chilli_cpp=run_chilli_cpp,
                 run_chilli_jl=run_chilli_jl,
                 run_pyscf=run_pyscf,
                 ref=ref,
                 use_ref=use_ref)

if __name__ == '__main__': 
    test_uks(xc_name="LDA,VWN",use_ref=True,run_chilli_cpp=run_chilli_cpp,run_chilli_jl=run_chilli_jl)

