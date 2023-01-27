import numpy as np 
from pprint import pprint 
from chilli_py.atoms import atoms_from_xyz
from chilli_py.RHF import RHF    
from chilli_py.RTDHF import RTDHF 
from chilli_py.utils import myprint, timeit 
from chilli_py import basis  
from chilli_py.bench import small_bench, Entry, Benchmark
# for mmd 
from chilli_py.constants import BOHR2ANG

""" Small benchmark for RTDHF """

def run(f_xyz):
    """
        run
        Run chilli_py calculation. 
    """
    print('RTDHF, chilli_py')
    atoms = atoms_from_xyz(f_xyz)
    mf_hf = RHF(atoms,"sto-3g")
    mf_hf.kernel()
    mf_tdhf = RTDHF(atoms,mf_hf) 
    e = mf_tdhf._rtdhf(method="full") 
    return e

def run_pyscf(f_xyz):
    """
        run_pyscf 
        Run PySCF reference calculation (if needed). 
        We use this function to generate 
        the reference values (ref dict). 
    """
    # Indirect imports, b/c CI 
    from pyscf import gto, scf
    from pyscf.tdscf import TDHF
    print('RTDHF, PySCF')
    mol = gto.M(
                atom = f_xyz,
                basis = 'sto-3g',
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
    td = TDHF(mf)
    td.singlet = True
    e = td.kernel(nstates=20)[0]
    return e

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
    from mmd.postscf import PostSCF
    atoms = atoms_from_xyz(f_xyz)
    geometry = atoms2mmdgeometry(atoms)
    mol = Molecule(geometry=geometry,basis='sto-3g')
    mol.RHF(conver=1e-12)
    PostSCF(mol).TDHF(alg="full") 
    return mol.tdhf_omega/27.211399 


# SS,06.12.2021, RHF, STO3G 
ref = {'CH4': {'ref': -39.78326353939042, 'val': -39.783263535258435},
       'H2': {'ref': -1.1298721951303525, 'val': -1.1298721967775218},
       'H2O': {'ref': -74.99400795113664, 'val': -74.99400794065048},
       'He': {'ref': -2.807783957539976, 'val': -2.8077839575380965},
       'Ne': {'ref': -126.60452499680474, 'val': -126.60452499672792}
}


def get_ref(key,typ="ref",ref=ref):
    """
        get_ref 
        Get reference value from dict ref. 
    """
    return ref[key][typ]

@timeit 
def test_rtdhf(use_ref=True):
    """
        test_rhf
        Test RTDHF routine.
    """
    F = small_bench
    bench = Benchmark("RTDHF") 
    for key, f_xyz in F.items(): 
        print(f"system: {key} path: {f_xyz}")
        E = run(f_xyz)  
        if use_ref: 
            E_pyscf = get_ref(key)
        else: 
            #E_pyscf = run_pyscf(f_xyz)
            E_mmd = run_mmd(f_xyz)
            E_ref = E_mmd #E_pyscf 
        if len(E) > 1 and len(E_ref) > 1:
            e = Entry(f'{key}',E[0],E_ref[0])
            bench.add(e) 
    bench.show()
    ME, MAE, RMSD = bench.analyze()
    if not use_ref:
        pprint(bench.get_dict())
    assert MAE < 1e-7 
    print("tests@RTDHF: sucessfully done!")

if __name__ == '__main__': 
    test_rtdhf(use_ref=False)

