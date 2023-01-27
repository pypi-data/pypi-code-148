import numpy as np 
from chilli_py.atoms import atoms_from_xyz
from chilli_py.RHF import RHF    
from chilli_py.HGP import coulomb_hgp_cgbf
from chilli_py.utils import myprint, timeit 
from chilli_py import basis  
from chilli_py.bench import small_bench, Entry, Benchmark

""" Small benchmark for RHF """

def run(f_xyz):
    """
        run
        Run chilli_py calculation. 
    """
    print('RHF, chilli_py')
    atoms = atoms_from_xyz(f_xyz)
    mf = RHF(atoms,"sto-3g",coulomb=coulomb_hgp_cgbf)
    mf.kernel() 
    return mf.Etot, mf.mo_energy 

def run_pyscf(f_xyz):
    """
        run_pyscf 
        Run PySCF reference calculation (if needed). 
        We use this function to generate 
        the reference values (ref dict). 
    """
    # Indirect imports, b/c CI 
    from pyscf import gto, scf
    print('RHF, PySCF')
    mol = gto.M(
                atom = f_xyz,
                basis = 'sto3g',
                symmetry = False,
                 )

    mf = scf.HF(mol)
    mf.init_guess = '1e'
    mf.verbose = 8#4
    # Get overlap matrix 
    S = mf.get_ovlp()
    print('Overlap matrix \n S: \n {}'.format(S))
    Hcore = Hcore = mf.get_hcore()
    print('Hcore = T + V : \n {}'.format(Hcore))
    print(f'Enuc = {mol.energy_nuc()}')
    mf.kernel()
    print(mf.mo_energy)
    print("\n")
    return mf.e_tot, mf.mo_energy 

# SS,17.11.2021, RHF, STO3G 
ref = {"H2"  : {"val": -1.1167143279698633 ,"ref": -1.1167143250893625}, 
       "He"  : {"val": -2.8077839575380965 ,"ref": -2.807783957539976}, 
       "H2O" : {"val": -74.95985767659002  ,"ref": -74.9598577912773}, 
       "CH4" : {"val": -39.726700000693256 ,"ref": -39.72670000318733}, 
       "Ne"  : {"val": -126.60452499672792 ,"ref": -126.60452499680474}
}

def get_ref(key,typ="ref",ref=ref):
    """
        get_ref 
        Get reference value from dict ref. 
    """
    return ref[key][typ]

@timeit 
def test_rhf(use_ref=True):
    """
        test_rhf
        Test RHF routine.
    """
    F = small_bench
    bench = Benchmark("RHF") 
    for key, f_xyz in F.items(): 
        print(f"system: {key} path: {f_xyz}")
        E, Eigs = run(f_xyz)  
        if use_ref: 
            E_pyscf = get_ref(key)
        else: 
            E_pyscf, Eigs_pyscf = run_pyscf(f_xyz)
        e = Entry(f'Etot: {key}',E,E_pyscf)
        bench.add(e) 
    bench.show()
    ME, MAE, RMSD = bench.analyze()
    if not use_ref:
        print(bench.__dict__)
    assert MAE < 1e-7 
    print("tests@RHF: sucessfully done!")

if __name__ == '__main__': 
    test_rhf(use_ref=True)

