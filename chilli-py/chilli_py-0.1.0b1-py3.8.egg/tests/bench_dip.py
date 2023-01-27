import numpy as np 
from pprint import pprint 
from chilli_py.alias import norm 
from chilli_py.atoms import atoms_from_xyz
from chilli_py.RHF import RHF    
from chilli_py.utils import myprint 
from chilli_py import basis  
from chilli_py.bench import small_rbench, Entry, Benchmark
# for mmd 
from chilli_py.constants import BOHR2ANG

""" Small benchmark for RHF """

def run(f_xyz):
    """
        run
        Run chilli_py calculation. 
    """
    print('RHF, chilli_py')
    atoms = atoms_from_xyz(f_xyz)
    mf = RHF(atoms,"sto-3g")
    mf.kernel() 
    return mf.mu_abs, mf.mu

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
    print("\n")
    mu = mf.dip_moment() 
    mu_abs = norm(mu)
    return mu_abs, mu

def atoms2mmdgeometry(atoms):
    """
        atoms2mmdgeometry
        Convert chilli_pys atom obect to mmd geometry string.
    """
    geometry = """\n"""
    geometry += f"{atoms.charge} {atoms.spin+1}\n"
    for sym,pos in zip(atoms.sym,atoms.pos):
        pos *= BOHR2ANG
        geometry += f"{sym} {pos[0]: 10.12f} {pos[1]: 10.12f} {pos[2]: 10.12f}\n"
    return geometry

def run_mmd(f_xyz):
    """
        run_mmd
        Run mmd reference calculation (if needed).
        We use this function to generate
        the reference values (ref dict).
    """
    from mmd.molecule import Molecule
    atoms = atoms_from_xyz(f_xyz)
    geometry = atoms2mmdgeometry(atoms)
    mol = Molecule(geometry=geometry,basis='sto-3g')
    mol.RHF(conver=1e-12)
    mu = mol.mu
    mu_abs = norm(mu) 
    return mu_abs, mu 

# SS,19.11.2021, RHF, STO3G, PySCF 
ref_pyscf = {'CH4': {'ref': 2.318568799567918e-05, 'val': 2.3183057048409987e-05},
             'H2' : {'ref': 1.6931432361110742e-15, 'val': 8.465715561900567e-16},
             'H2O': {'ref': 1.7342190515562697, 'val': 1.734219159359075},
             'He' : {'ref': 0.0, 'val': 0.0},
             'Ne' : {'ref': 0.0, 'val': 0.0}
}
# SS,19.11.2021, RHF, STO3G, mmd
ref_mmd = {'CH4': {'ref': 2.3183646422270222e-05, 'val': 2.318568799567918e-05},
           'H2' : {'ref': 4.232889039279541e-16, 'val': 1.6931432361110742e-15},
           'H2O': {'ref': 1.734231736511634, 'val': 1.7342190515562697},
           'He' : {'ref': 0.0, 'val': 0.0},
           'Ne' : {'ref': 0.0, 'val': 0.0}
}

def get_ref(key,typ="ref",ref=ref_pyscf):
    """
        get_ref 
        Get reference value from dict ref. 
    """
    return ref[key][typ]

def test_dip(use_ref=True):
    """
        test_dip
        Test dipole moment routine.
    """
    F = small_rbench
    bench = Benchmark("DIPOLE") 
    for key, values in F.items(): 
        f_xyz = values["f_xyz"]
        print(f"system: {key} path: {f_xyz}")
        mu_abs, mu = run(f_xyz)  
        if use_ref is True: 
            mu_abs_ref = get_ref(key)
        if use_ref == "pyscf": 
            mu_abs_ref, mu_ref = run_pyscf(f_xyz)
        if use_ref == "mmd": 
            mu_abs_ref, mu_ref = run_mmd(f_xyz)
        e = Entry(f'{key}',mu_abs,mu_abs_ref,unit="Debye")
        bench.add(e) 
    bench.show()
    ME, MAE, RMSD = bench.analyze()
    if use_ref is not True:
        pprint(bench.get_dict())
    assert MAE < 1e-5 
    print("tests@DIPOLE: sucessfully done!")

if __name__ == '__main__': 
    test_dip(use_ref="pyscf")

