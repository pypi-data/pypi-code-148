import numpy as np 
from pprint import pprint 
from chilli_py.atoms import atoms_from_xyz, Atoms
from chilli_py.RKS import RKS
from chilli_py.RFLO import RFLO 
from chilli_py.utils import myprint 
from chilli_py import basis
from chilli_py.bench import small_bench_rflo, Entry, Benchmark
from chilli_py.constants import ANG2BOHR, BOHR2ANG

""" Small benchmark for RFLO """

def run(key,xc,bench=small_bench_rflo):
    """
        run 
        Run chilli_py calculation. 
    """
    atoms, fods = bench[key]()
    print("RKS, chilli_py")
    mf = RKS(atoms,
            "sto-3g",
            (100,110),
            Etol=1e-12,
            maxiter=100,
            verbose=False,
            use_avg=True,
            xc_name=xc)
    mf.kernel() 
    print("RFLO, chilli_py")
    flo = RFLO(atoms,
               fods,
               mf_init=mf)
    Etot, HSIC, FFORCE = flo.kernel() 
    return Etot

def atoms2atoms(atoms,fods):
    """
        atom2atoms 
        Convert chilli_py (atoms,fods) to PyFLOSIC atoms object. 
        Notes: The two Atoms objects use different units!
    """
    from pyflosic2.atoms.atoms import Atoms as PyFLOSIC_Atoms 
    sym_nuc = atoms.sym
    sym_fod = fods.sym
    pos_nuc = atoms.pos*BOHR2ANG
    pos_fod = fods.pos*BOHR2ANG
    sym = sym_nuc+sym_fod
    pos = [] 
    pos.extend(pos_nuc) 
    pos.extend(pos_fod) 
    spin = atoms.spin 
    charge = atoms.charge 
    atoms = PyFLOSIC_Atoms(sym,pos,spin=spin,charge=charge) 
    return atoms 
    

def run_pyflosic(key,xc,bench=small_bench_rflo):
    from pyscf import scf, dft
    from pyflosic2.sic.rflo import RFLO
    from pyflosic2.parameters.flosic_parameters import parameters
    from pyflosic2 import units
    """
        Test: rflo routine
    """
    xc_helper = { "LDA,VWN" : "LDA,VWN",
                  "LDA,PW"  : "LDA,PW",
                  "LDA,CHACHIYO" : "LDA_X,LDA_C_CHACHIYO"}
    xc = xc_helper[xc]
    
    atoms, fods = bench[key]()
    atoms = atoms2atoms(atoms,fods) 

    # standard parameters
    p = parameters(mode='restricted')
    p.verbose = 5
    # System information
    p.init_atoms(atoms)
    p.basis ='sto3g'
    p.xc = xc

    # generate mf object
    # Choosing RKS
    mf = scf.RKS(p.mol)  # unrestricted
    # Note:
    # We set the verbosity to zero
    # because PySCF use a different logger
    mf.verbose = 4
    mf.xc = p.xc
    # With or without DIIS
    #mf.diis = None
    # Use Hcore as inital guess for Fockian.
    mf.init_guess = '1e'
    # We do not like pruning.
    mf.grids.prune = None
    mf.grids.radi_method = dft.radi.gauss_chebyshev #dft.radi.gauss_chebyshev #dft.radi.becke
    mf.grids.radii_adjust = None
    mf.grids.atom_grid = (100,110)
    mf.grids.build()
    edft = mf.kernel()
    # s1e print(mf.get_ovlp())
    # U print(mf.mo_coeff)
    ao1 = dft.numint.eval_ao(mf.mol, p.fod1.positions *ANG2BOHR)
    psi_ai_1 = ao1.dot(mf.mo_coeff)
    myprint(ao1=ao1,psi_ai_1=psi_ai_1)
    # Set up the SIC Hamiltonian
    p.ham_sic = 'HOOOV'
    p.show()
    # test FLO-SIC functions
    flo = RFLO(mf=mf, p=p)
    etot = flo.kernel()
    return flo.e_tot 


# SS, 26.11.2021, STO3G, (100,110), Etol=1e-12, maxiter=100, use_avg=True, xc="LDA,VWN" 
# using: gauss_chebyshev b/c AE6 
ref_lda_vwn = {'CH4': {'ref': -40.21076632568385, 'val': -40.21076618643119},
               'H2': {'ref': -1.1665875883888643, 'val': -1.1665875915736916},
               'H2O': {'ref': -75.55602657170328, 'val': -75.55602656184152},
               'He': {'ref': -2.8672161694178215, 'val': -2.8672161694159426},
               'He2': {'ref': -5.210093702342384, 'val': -5.210093574546134},
               'Ne': {'ref': -127.2718540557619, 'val': -127.27185405564153}
}


# SS, 26.11.2021, STO3G, (100,110), Etol=1e-12, maxiter=100, use_avg=True, xc="LDA,PW" 
# using: gauss_chebyshev b/c AE6 
ref_lda_pw = {'CH4': {'ref': -40.208140451850724, 'val': -40.20814031186499},
              'H2': {'ref': -1.1663137623533961, 'val': -1.1663137655312918},
              'H2O': {'ref': -75.55253325204725, 'val': -75.55253324214247},
              'He': {'ref': -2.8666889909259634, 'val': -2.8666889909240845},
              'He2': {'ref': -5.208912321933452, 'val': -5.208912194123649},
              'Ne': {'ref': -127.26740632677696, 'val': -127.26740632665657}
}

ref = {'LDA,VWN' : ref_lda_vwn, 
       'LDA,PW'  : ref_lda_pw,
}

def get_ref(key,xc="VWN",typ="ref",ref=ref):
    """
        get_ref
        Get reference value from dict ref.
    """
    return ref[xc][key][typ]

def test_rflo(use_ref=True,xc="LDA,VWN"):
    """
        test_rflo
        Test RFLO routine. 
    """
    F = small_bench_rflo
    bench = Benchmark(f"RFLO: xc: {xc}") 
    for key in F.keys():
        print(f"system: {key}")
        E = run(key,xc)  
        if use_ref: 
            E_pyflosic = get_ref(key,xc=xc)
        else: 
            E_pyflosic = run_pyflosic(key,xc)
        e = Entry(f'{key}',E,E_pyflosic)
        bench.add(e) 
    bench.show()
    ME, MAE, RMSD = bench.analyze()
    if not use_ref:
        pprint(bench.get_dict())
    assert MAE < 1e-6
    print("tests@RFLO: sucessfully done!")
    
if __name__ == '__main__': 
    test_rflo(use_ref=False,xc="LDA,PW") 

