import numpy as np
from chilli_py.bench import Benchmark, Entry, BenchmarkSet, run_chilli_py, run_pyscf  
from chilli.constants import ANG2BOHR, HA2KCALMOL

""" Benchmark set: 6 atomization energies (AE6) """

db_AE6 = {'C': {'charge': 0,
       'multiplicity': 3,
       'positions': [[0.0, 0.0, 0.0]],
       'symbols': ['C']},
       'C3H4_pro': {'charge': 0,
                    'multiplicity': 1,
                    'positions': [[0.0, 0.0, 0.21951],
                                  [0.0, 0.0, 1.42396],
                                  [0.0, 0.0, -1.24376],
                                  [0.0, 0.0, 2.48626],
                                  [0.0, 1.01901, -1.62815],
                                  [0.88249, -0.5095, -1.62815],
                                  [-0.88249, -0.5095, -1.62815]],
                    'symbols': ['C', 'C', 'C', 'H', 'H', 'H', 'H']},
       'C4H8_cyc': {'charge': 0,
                    'multiplicity': 1,
                    'positions': [[0.0, 1.07629, 0.14286],
                                  [0.0, -1.07629, 0.14286],
                                  [-1.07629, 0.0, -0.14286],
                                  [1.07629, 0.0, -0.14286],
                                  [0.0, 1.9792, -0.46516],
                                  [0.0, 1.35922, 1.19582],
                                  [0.0, -1.9792, -0.46516],
                                  [0.0, -1.35922, 1.19582],
                                  [-1.9792, 0.0, 0.46516],
                                  [-1.35922, 0.0, -1.19582],
                                  [1.9792, 0.0, 0.46516],
                                  [1.35922, 0.0, -1.19582]],
                    'symbols': ['C',
                                'C',
                                'C',
                                'C',
                                'H',
                                'H',
                                'H',
                                'H',
                                'H',
                                'H',
                                'H',
                                'H']},
       'H': {'charge': 0,
             'multiplicity': 2,
             'positions': [[0.0, 0.0, 0.0]],
             'symbols': ['H']},
       'HCOCOH': {'charge': 0,
                  'multiplicity': 1,
                  'positions': [[0.0, 0.0, 0.0],
                                [0.0, 0.0, 1.52071],
                                [1.02783, 0.0, -0.62647],
                                [-0.99667, 0.0, -0.46731],
                                [-1.02783, 0.0, 2.14718],
                                [0.99667, 0.0, 1.98802]],
                  'symbols': ['C', 'C', 'O', 'H', 'O', 'H']},
       'O': {'charge': 0,
             'multiplicity': 3,
             'positions': [[0.0, 0.0, 0.0]],
             'symbols': ['O']},
       'S': {'charge': 0,
             'multiplicity': 3,
             'positions': [[0.0, 0.0, 0.0]],
             'symbols': ['S']},
       'S2': {'charge': 0,
              'multiplicity': 3,
              'positions': [[0.0, 0.0, 0.0], [0.0, 0.0, 1.89259]],
              'symbols': ['S', 'S']},
       'Si': {'charge': 0,
              'multiplicity': 3,
              'positions': [[0.0, 0.0, 0.0]],
              'symbols': ['Si']},
       'SiH4': {'charge': 0,
                'multiplicity': 1,
                'positions': [[0.0, 0.0, 0.0],
                              [0.0, 0.0, 1.4767],
                              [1.39225, 0.0, -0.49223],
                              [-0.69612, -1.20572, -0.49223],
                              [-0.69612, 1.20572, -0.49223]],
                'symbols': ['Si', 'H', 'H', 'H', 'H']},
       'SiO': {'charge': 0,
               'multiplicity': 1,
               'positions': [[0.0, 0.0, 0.0], [0.0, 0.0, 1.51267]],
               'symbols': ['Si', 'O']}
}

def De_at_0K(name,dct_atoms,data):
    """
        De_at_0K
        Calculates the electronic atomization energy De 
    """
    Ee = data[name] # Etot for system 
    elements = dct_atoms[name].sym
    tmp_ee = 0
    for ee in elements:
        tmp_ee = tmp_ee + data[ee]
        De = tmp_ee - Ee
        De = De
    return De

def get_AE6(dct_atoms,data):
    """ 
        get_AE6 
        Calculate errors for AE6 benchmark set. 
    """
    sys_atoms = ['H','C','O','Si','S']
    sys_molecules = ['SiH4','S2','SiO','C3H4_pro','HCOCOH','C4H8_cyc']
    bench = Benchmark("AE6")
    for key in sys_molecules:
        De = De_at_0K(key,dct_atoms,data)*HA2KCALMOL
        e = Entry(f'{key}',De,ref_AE6(key),unit="kcal/mol")
        bench.add(e)
    bench.show()
    bench.analyze()
    return bench 

def ref_AE6(sys):
    """ 
        ref_AE6 
        AE6 reference values 
        
        Note
            - REF2 (B.E.) [kcal/mol]
    
        Reference 
            - https://comp.chem.umn.edu/db/dbs/mgae109.html
    """
    d = {'S2'           :       101.67,
         'SiH4'         :       322.40,
         'SiO'          :       192.08,
         'C3H4_pro'     :       704.79,
         'HCOCOH'       :       633.35,
         'C4H8_cyc'     :       1149.01}
    return d[sys]

def get_sys_bench_AE6():
    """
        get_sys_bench_AE6
        Get all systems needed to be calculated, i.e., sys_bench 
        for the AE6 benchmark set. 
    """
    sys_atoms = ['H','C','O','Si','S']
    sys_molecules = ['SiH4','S2','SiO','C3H4_pro','HCOCOH','C4H8_cyc']
    sys_bench = sys_atoms + sys_molecules
    return sys_bench 

class AE6(BenchmarkSet):
    """
        AE6 class. 
        Calculate (calc) and post-process (pp)
        the AE6 benchmark set. 

        Input 
            - name, str(), benchmark set name, i.e., "AE6" 
            - db, dct(), containing the system informations for AE6, ie., db_AE6 
            - sys_bench, [str(),...], list of systems needed to be calculated 
            - f_calc, python function, takes a atoms object and calculate target property 
            - f_pp, python function, use the benchmark information to calculate the benchmark target

        Note
            - derived class from BenchmarkSet
    """
    def __init__(self,
                 name = "AE6",
                 db=db_AE6,
                 sys_bench=get_sys_bench_AE6(),
                 f_calc=run_chilli,
                 f_pp=get_AE6,
                 **kwargs):
        """
            __init__
            Initialize an instance of the class. 
        """
        super().__init__(name=name,
                         db=db,
                         sys_bench=sys_bench,
                         f_calc=f_calc,
                         f_pp=f_pp,
                         **kwargs)


def main():
    """
        main 
        Main function to test this routine. 
    """
    #ae6 = AE6(f_run=run,mode="UHF",basis="sto-3g")
    #ae6 = AE6(f_run=run,mode="UKS",xc="LDA,PW",basis="pc-0",grid=(50,194)) #grid=(50,194))
    #ae6 = AE6(f_run=run_pyscf,mode="UHF",basis="sto-3g")
    #ae6 = AE6(f_run=run_pyscf,mode="UKS",xc="LDA,PW",basis="pc-0",grid=(50,194))
    #ae6.kernel() 
    
    # debug 
    #ae6 = AE6(f_run=run,mode="UKS",basis="pc-0",maxiter=300)
    ##ae6._calc_entry("C")
    #ae6.kernel()

    ae6 = AE6(f_calc=run_pyscf,mode="UKS",basis="pc-0",maxiter=300)
    ae6.kernel()
    prefix = ae6.prefix 

    ae6= AE6(f_calc=run_pyscf,mode="UKS",basis="pc-0",maxiter=300)
    ae6.read_dct(f"{prefix}.dct")


if __name__ == '__main__':
    main()
