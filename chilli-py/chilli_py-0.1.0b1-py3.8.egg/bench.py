import numpy as np
from pprint import pprint 
from chilli_py import __path__ as pkg_path
from chilli_py import structs 
from chilli_py.utils import slice_dct, timeit 
from chilli_py.atoms import Atoms 
from chilli_py.constants import ANG2BOHR
from chilli_py.my_io import write_file, read_file

""" Benchmark sets and utils """

# Path to xyz structs 
rbench = {
            "H"    : {"f_xyz" : pkg_path[0]+"/structs"+"/H.xyz"   ,"spin" : 0 },
            "H2"   : {"f_xyz" : pkg_path[0]+"/structs"+"/H2.xyz"  ,"spin" : 0 },
            "He"   : {"f_xyz" : pkg_path[0]+"/structs"+"/He.xyz"  ,"spin" : 0 },
            "Li"   : {"f_xyz" : pkg_path[0]+"/structs"+"/Li.xyz"  ,"spin" : 0 },
            "LiH"  : {"f_xyz" : pkg_path[0]+"/structs"+"/LiH.xyz" ,"spin" : 0 },
            "H2O"  : {"f_xyz" : pkg_path[0]+"/structs"+"/H2O.xyz" ,"spin" : 0 },
            "CH4"  : {"f_xyz" : pkg_path[0]+"/structs"+"/CH4.xyz" ,"spin" : 0 },
            "Ne"   : {"f_xyz" : pkg_path[0]+"/structs"+"/Ne.xyz"  ,"spin" : 0 },
            "C2H6" : {"f_xyz" : pkg_path[0]+"/structs"+"/C2H6.xyz","spin" : 0 },
            "C6H6" : {"f_xyz" : pkg_path[0]+"/structs"+"/C6H6.xyz","spin" : 0 }, 
}
ubench = {
            "He"  : {"f_xyz" : pkg_path[0]+"/structs"+"/He.xyz" , "spin": 0},
            "H2"  : {"f_xyz" : pkg_path[0]+"/structs"+"/H2.xyz" , "spin": 0},
            "Ne"  : {"f_xyz" : pkg_path[0]+"/structs"+"/Ne.xyz" , "spin": 0},
            "H"   : {"f_xyz" : pkg_path[0]+"/structs"+"/H.xyz"  , "spin": 1},
            "LiH" : {"f_xyz" : pkg_path[0]+"/structs"+"/LiH.xyz", "spin": 2},
            "Li"  : {"f_xyz" : pkg_path[0]+"/structs"+"/Li.xyz" , "spin": 1},
            "O2"  : {"f_xyz" : pkg_path[0]+"/structs"+"/O2.xyz" , "spin": 2},
            "NO"  : {"f_xyz" : pkg_path[0]+"/structs"+"/NO.xyz" , "spin": 1},
            "NO2" : {"f_xyz" : pkg_path[0]+"/structs"+"/NO2.xyz", "spin": 1},
            "Si2" : {"f_xyz" : pkg_path[0]+"/structs"+"/Si2.xyz", "spin": 2},
            "NH"  : {"f_xyz" : pkg_path[0]+"/structs"+"/NH.xyz" , "spin": 2},
            "S2"  : {"f_xyz" : pkg_path[0]+"/structs"+"/S2.xyz" , "spin": 2},
}


sys2latex = {"H" : "H", 
             "H2" : "H$_{2}$",
             "He" : "He",
             "H2O" : "H$_{2}$O",
             "CH4" : "CH$_{4}$",
             "Ne" : "Ne",
             "Li" : "Li",
             "O2" : "O$_{2}$",
             "S2" : "S$_{2}$",
             "NH" : "NH",

}

def He():
    """
        He 
        The helium atom (He)
    """
    sym_nuc = ['He']
    sym_fod = ["X"]
    p0 = [+0.00000000, +0.00000000, +0.00000000]
    p1 = [+0.00000000, +0.00000000, +0.00000000]
    pos_nuc = np.array([p0])*ANG2BOHR
    pos_fod = np.array([p1])*ANG2BOHR
    charge = 0
    spin = 0
    atoms = Atoms(sym_nuc, pos_nuc, spin=spin, charge=charge)
    fods = Atoms(sym_fod, pos_fod)
    return atoms, fods

def H2():
    """
        H2
        Atoms + FODs
    """
    sym_nuc = 2 * ['H']
    sym_fod = ["X"]
    p0 = [+0.00000000, +0.00000000, +0.37070000]
    p1 = [+0.00000000, +0.00000000, -0.37070000]
    p2 = [+0.00000000, +0.00000000, +0.00000000]
    pos_nuc = np.array([p0,p1])*ANG2BOHR
    pos_fod = np.array([p2])*ANG2BOHR
    atoms = Atoms(sym_nuc,pos_nuc)
    fods = Atoms(sym_fod,pos_fod)
    return atoms, fods


def He2():
    """
        He2
        Atoms + FODs
    """
    sym_nuc = 2 * ['He']
    sym_fod = 2*  ["X"]
    p0 = [+0.00000000, +0.00000000, +0.37070000]
    p1 = [+0.00000000, +0.00000000, -0.37070000]
    pos_nuc = np.array([p0,p1])*ANG2BOHR
    pos_fod = np.array([p0,p1])*ANG2BOHR
    atoms = Atoms(sym_nuc,pos_nuc)
    fods = Atoms(sym_fod,pos_fod)
    return atoms, fods


def CH4():
    """
        CH4 
        The methane molecule (CH4)
        Atoms + FODs
    """
    sym_nuc = ["C"] + 4 * ["H"]
    sym_fod =  5 * ["X"]
    p0 = [+0.00000000, +0.00000000, +0.00000000]
    p1 = [+0.62912000, +0.62912000, +0.62912000]
    p2 = [-0.62912000, -0.62912000, +0.62912000]
    p3 = [+0.62912000, -0.62912000, -0.62912000]
    p4 = [-0.62912000, +0.62912000, -0.62912000]
    p5 = [+0.00000000, +0.00000000, +0.00000000]
    p6 = [+0.57606765, +0.57606765, +0.57606765]
    p7 = [-0.57606765, -0.57606765, +0.57606765]
    p8 = [+0.57606765, -0.57606765, -0.57606765]
    p9 = [-0.57606765, +0.57606765, -0.57606765]
    pos_nuc = np.array([p0, p1, p2, p3, p4])*ANG2BOHR
    pos_fod = np.array([p5, p6, p7, p8, p9])*ANG2BOHR
    charge = 0
    spin = 0
    atoms = Atoms(sym_nuc, pos_nuc, spin=spin, charge=charge)
    fods = Atoms(sym_fod, pos_fod)
    return atoms, fods

def Ne():
    """
        Ne
        The Ne atom, FODs of both spin channels at the same position (Ne)
        Atoms + FODs 
    """
    sym_nuc = ["Ne"]
    sym_fod = 5 * ["X"]
    p0 = [+0.000000001,  +0.0000000000, +0.0000000000]
    p1 = [+0.0000000000, +0.0000000000, +0.0000000000]
    p2 = [+0.3299621221, +0.3299621221, +0.3299621221]
    p3 = [-0.3299621221, -0.3299621221, +0.3299621221]
    p4 = [+0.3299621221, -0.3299621221, -0.3299621221]
    p5 = [-0.3299621221, +0.3299621221, -0.3299621221]
    pos_nuc = np.array([p0])*ANG2BOHR
    pos_fod = np.array([p1, p2, p3, p4, p5])*ANG2BOHR
    charge = 0
    spin = 0
    atoms = Atoms(sym_nuc, pos_nuc, spin=spin, charge=charge)
    fods = Atoms(sym_fod, pos_fod)
    return atoms, fods

def H2O():
    """
        H2O 
        The water molecule (H2O)
        Atoms + FODs 
    """
    sym_nuc = ["O"] + 2 * ["H"]
    sym_fod =  5 * ["X"]
    p0 = [+0.00000000, +0.00000000, +0.11730000]
    p1 = [+0.00000000, +0.75720000, -0.46920000]
    p2 = [+0.00000000, -0.75720000, -0.46920000]
    p3 = [+0.00000000, +0.00000000, +0.11730000]
    p4 = [+0.00000000, +0.64362000, -0.38122500]
    p5 = [+0.00000000, -0.64362000, -0.38122500]
    p6 = [+0.44297121, +0.00000000, +0.56027121]
    p7 = [-0.44297121, +0.00000000, +0.56027121]
    pos_nuc = np.array([p0, p1, p2])*ANG2BOHR
    pos_fod = np.array([p3, p4, p5, p6, p7])*ANG2BOHR
    charge = 0
    spin = 0
    atoms = Atoms(sym_nuc, pos_nuc, spin=spin, charge=charge)
    fods = Atoms(sym_fod, pos_fod)
    return atoms, fods

def COH2():
    """
       COH2 
       Atoms + FODs 
    """
    sym_nuc = ['O'] + ['C'] + 2 * ['H'] 
    sym_fod = 8 * ['X']
    p0 = [1.16250000, -0.00000000, 0.00000000]
    p1 = [-0.05750000, -0.00000000, 0.00000000]
    p2 = [-0.55250000, 0.85740000, 0.00000000]
    p3 = [-0.55250000, -0.85740000, 0.00000000]
    p4 = [1.16250000, 0.00000000, 0.00000000]
    p5 = [0.55250000, -0.00000000, -0.36600000]
    p6 = [0.55250000, 0.00000000, 0.36600000]
    p7 = [1.46750000, 0.36600000, -0.00000000]
    p8 = [1.46750000, -0.36600000, 0.00000000]
    p9 = [-0.05750000, 0.00000000, 0.00000000]
    p10 = [-0.47825000, 0.72879000, 0.00000000]
    p11 = [-0.47825000, -0.72879000, 0.00000000]
    pos_nuc = np.array([p0, p1, p2, p3])*ANG2BOHR
    pos_fod = np.array([p4, p5, p6, p7, p8, p9, p10, p11])*ANG2BOHR
    charge = 0
    spin = 0
    atoms = Atoms(sym_nuc, pos_nuc, spin=spin, charge=charge)
    fods = Atoms(sym_fod, pos_fod)
    return atoms, fods

small_bench_rflo = {
                    "He"  : He,
                    "H2"  : H2,
                    "He2" : He2,
                    "CH4" : CH4,
                    "Ne"  : Ne,
                    "H2O" : H2O
}

# Predefined benchmark sets 
rsubset_small = ["H2","He","H2O","CH4","Ne"]
small_rbench = slice_dct(rbench,rsubset_small)
usubset_small = ["H","O2","Li","NH","S2"]
small_ubench = slice_dct(ubench,usubset_small)

def name2path(key,bench=rbench):
    """
        name2path 
        Give a (available) system name, e.g., H2O, 
        which is then convert to the correct path 
        to the xyz file. 
    """
    return bench[key]

class Entry:
    """
        Entry class 
        Entry for Benchmark. 
    """
    def __init__(self,key,val,ref,unit="Eh"):
        """
            __init__
            Initialize class instance.
        """
        # Name of the property, key 
        self.key = key
        # Calculated value of the property, val 
        self.val = val
        # Reference value for the property, ref
        self.ref = ref
        # Unit of the property, unit 
        self.unit = unit 

    def show(self):
        """
            show
            Show the representation
            of the entry instance.
        """
        print(self.__repr__())

    def __repr__(self):
        """
            __repr__
            Representation of 
            the entry instance. 
        """
        return f'{self.key} : val: {self.val} ref: {self.ref}'

    def get_dict(self):
        """
            get_dict 
            Get entry as a dict. 
        """
        return {self.key: {'val' : self.val, 'ref': self.ref}}

class Benchmark:
    """
        Benchmark class. 
    """
    def __init__(self,name=None):
        """
            __init__
            Initialize class instance. 
        """
        self.name = name
        self.data = []

    def add(self,entry):
        """
            add 
            Add a new entry to the current benchmark. 
        """
        self.data.append(entry)
    
    def _get_errors(self):
        """
            _get_errors
            Get mean error (ME) and 
            mean absolute error (MAE) 
            for the given benchmark. 
        """
        ME = 0 
        MAE = 0
        RMSD = 0
        Nsys = len(self.data)
        for entry in self.data:
            me = entry.val - entry.ref 
            mae = abs(me) 
            rmsd = me**2 
            ME += me 
            MAE += mae 
            RMSD += rmsd 
        ME /= Nsys
        MAE /= Nsys
        RMSD = np.sqrt(RMSD/Nsys)
        return ME, MAE, RMSD, entry.unit  

    def analyze(self,verbose=False):
        """
            analyze 
            Analyze the given benchmark, 
            e.g., calculate errors. 
        """
        ME, MAE, RMSD, unit = self._get_errors() 
        if verbose > 0: 
            print(f"ME: {ME} {unit}")
            print(f"MAE: {MAE} {unit}")
            print(f"RMSD: {RMSD} {unit}")
        return ME, MAE, RMSD  

    def show(self):
        """
            show 
            Show the representation 
            of the benchmark. 
        """
        print(f"Benchmark: {self.name}")
        for entry in self.data:
            entry.show()

    def get_dict(self):
        """
            get_dict 
            Get benchmark as dict. 
        """
        d = {}    
        for entry in self.data:
            d.update(entry.get_dict())
        return d 

def entry2atoms(name,db):
    """
        entry2atoms
        Convert database entry to chilli_py Atoms object. 
    """
    data = db[name]
    atoms = Atoms(sym=data["symbols"],
                  pos=np.array(data["positions"])*ANG2BOHR,
                  charge=data["charge"],
                  spin=data['multiplicity']-1)
    return atoms

class BenchmarkSet:
    """
        BenchmarkSet class. 
        Calculate (calc) and post-process (pp)
        a benchmark set.

        Can be used to set up other classes, i.e., 
            - AE6 
            - SIE4X4 

        Input
            - name, str(), benchmark set name
            - db, dct(), containing the system informations for the benchmark set 
            - sys_bench, [str(),...], list of systems needed to be calculated
            - f_calc, python function, takes a atoms object and calculate target property
            - f_pp, python function, use the benchmark information to calculate the benchmark target

    """
    def __init__(self,name,db,sys_bench,f_calc,f_pp,**kwargs):
        """
            __init__
            Initialize an instance of the class. 
        """
        self.name = name 
        self.db = db
        self.dct_atoms = {}
        self.data = {}
        self.sys_bench = sys_bench
        self.f_calc = f_calc
        self.f_pp = f_pp
        self._init_kwargs(kwargs)
        self._get_prefix() 

    def _get_prefix(self):
        """
            _get_prefix
            Get prefix for output file.
        """
        if self.mode == "UHF":
            self.prefix = f"{self.name}_{self.mode}_{self.basis}_{self.grid[0]}_{self.grid[1]}"
        if self.mode != "UHF":
            self.prefix = f"{self.name}_{self.mode}_{self.basis}_{self.grid[0]}_{self.grid[1]}_{self.xc}"

    def _init_kwargs(self,kwargs):
        """
            _init_kwargs
            Define standards for secondary arguments. 
        """
        self.mode = kwargs.get("mode","UHF")
        self.basis = kwargs.get("basis","sto-3g")
        self.grid = kwargs.get("grid",(50,194))
        self.xc = kwargs.get("xc","LDA,VWN")
        self.maxiter = kwargs.get("maxiter",300)
        

    def _run(self,atoms):
        """
            _run 
            Run a calculation for a atoms object. 
        """
        return self.f_calc(atoms=atoms,
                           mode=self.mode,
                           basis = self.basis,
                           grid = self.grid,
                           xc = self.xc,
                           maxiter = self.maxiter)

    def _calc_entry(self,key):
        """
            _calc_entry
            Calculate one entry in the benchmark set. 
        """
        print(f"{key}")
        atoms = entry2atoms(key,self.db)
        self.dct_atoms[key] = atoms
        self.data[key] = self._run(atoms)

    def _calc_bench(self):
        """
            _calc_bench
            Calculate all entries in the benchmark set. 
        """
        for key in self.sys_bench:
            self._calc_entry(key)

    def _pp(self):
        """
            _pp
            Post-process, i.e., evaluate the benchmark set objective. 
        """
        return self.f_pp(self.dct_atoms,self.data)

    def _save(self):
        """
            _save 
            Save data to file. 
        """
        write_file(self.data,self.prefix+".dct")

    def _restart(self,f_name):
        """
            _restart
            Restart calculation from file.
        """
        self.data = read_file(f_name)
        for key in self.sys_bench:
            atoms = entry2atoms(key,self.db)
            self.dct_atoms[key] = atoms

    @timeit
    def kernel(self,calc=True):
        """
            kernel 
            Main function of the class. 
            Calculate the benchmark. 
        """
        if calc == True:
            # Calculate benchmark set 
            self._calc_bench()
        # Postprocessing (pp) 
        self._pp()
        print(f"data: {self.data}")
        # Save (data) 
        self._save()

    def read_dct(self,f_name):
        """
            read_dct 
            Calculate benchmark objective using dct file.
            Generate an instance of the BenchmarkSet class 
            and then use this function to evaluate 
            the benchmark target using the information 
            in f_name. 
        """
        self._restart(f_name)
        self._pp() 


def get_ref(key,typ,ref):
    """
        get_ref 
        Get reference value from dict ref. 
    """
    return ref[key][typ]


def print_latex_table(F,bench_py,bench_cpp,bench_jl,method):
    """
        print_latex_table
        Print results of chilli_py benchmarks as LaTeX table.
    """
    ME_py, MAE_py, RMSD_py = bench_py.analyze()
    ME_cpp, MAE_cpp, RMSD_cpp = bench_cpp.analyze()
    ME_jl, MAE_jl, RMSD_jl = bench_jl.analyze()

    unit = "$E_{\\text{h}}$"
    chillipy = "\\CHILLIPY{}"
    chillicpp = "\\CHILLICPP{}"
    chillijl = "\\CHILLIJL{}"
    pyscf = "\\PySCF{}"
    print("\\begin{table*}")
    print("\\caption{"+method+"\label{tab:"+method+"}}")
    print("\\begin{tabular}{c|rrrr}")
    print(f"System & {chillipy} & {chillicpp} & {chillijl} & {pyscf} \\ \\\\ \hline")
    for i,(key, f_xyz) in enumerate(F.items()):
        print(f"{sys2latex[key]} & {bench_py.data[i].val:10.7f} & {bench_cpp.data[i].val:10.7f} & {bench_jl.data[i].val:10.7f} & {bench_py.data[i].ref:10.7f} \\ \\\\")
    print(f"\hline ME [{unit}] & {ME_py:2.1e} & {ME_cpp:2.1e} & {ME_jl:2.1e} & \\ \\\\")
    print(f"MAE [{unit}] & {MAE_py:2.1e} & {MAE_cpp:2.1e} & {MAE_jl:2.1e} & \\ \\\\")
    print(f"RMSD [{unit}] & {RMSD_py:2.1e} & {RMSD_cpp:2.1e} & {RMSD_jl:2.1e} & \\ \\\\")
    print("\\end{tabular}")
    print("\\end{table*}")

class Settings:
    """
        Settings class 
        Numerical parameters to benchmark chilli_py implementations
    """
    defaults = {"f_xyz"       : None,
                "spin"        : 0, 
                "charge"      : 0, 
                "basis_name"  : "sto-3g",
                "Etol"        : 1e-6, 
                "maxiter"     : 300, 
                "use_avg"     : True,
                "xc_name"     : "LDA,VWN",
                "n_rad"        : 100,
                "n_ang"        : 110
               }

    def __init__(self): 
        """
            __init__
            Initialize an instance of the class 
        """
        # Set default parameters 
        for key,val in Settings.defaults.items(): 
            setattr(self,key,val) 


def bench_chilli(setup,
                 bench_dct,
                 method,
                 run_chilli_py,
                 run_chilli_cpp=False,
                 run_chilli_jl=False, 
                 run_pyscf=False,
                 ref=None,
                 use_ref=True,
                 Etol=1e-5):
    """
        bench_chilli
        Benchmark chilli implementations (py,cpp) against PySCF. 
    """
    bench_py = Benchmark(f"Chilli.py: {method}")
    if run_chilli_cpp is not False:
        bench_cpp = Benchmark(f"Chilli.cpp: {method}")
    if run_chilli_jl is not False:
        bench_jl = Benchmark(f"Chilli.jl: {method}")
    for key, data in bench_dct.items():

        setup.f_xyz = data["f_xyz"]
        setup.spin = data["spin"]
        print(f"system: {key} path: {setup.f_xyz}")

        E_chilli_py = run_chilli_py(setup)
        if run_chilli_cpp is not False:
            E_chilli_cpp, t_chilli_cpp = run_chilli_cpp(setup)
        if run_chilli_jl is not False:
            E_chilli_jl = run_chilli_jl(setup)
        if use_ref:
            E_pyscf = get_ref(key,typ="ref",ref=ref)
        else:
            E_pyscf = run_pyscf(setup)

        e_py = Entry(f'{key}',E_chilli_py,E_pyscf)
        if run_chilli_cpp is not False:
            e_cpp = Entry(f'{key}',E_chilli_cpp,E_pyscf)
        if run_chilli_jl is not False:
            e_jl = Entry(f'{key}',E_chilli_jl,E_pyscf)

        bench_py.add(e_py)
        if run_chilli_cpp is not False:
            bench_cpp.add(e_cpp)
        if run_chilli_jl is not False:
            bench_jl.add(e_jl)

    # values and errors
    bench_py.show()
    ME_py, MAE_py, RMSD_py = bench_py.analyze(verbose=True)
    if run_chilli_cpp is not False:
        bench_cpp.show()
        ME_cpp, MAE_cpp, RMSD_cpp = bench_cpp.analyze(verbose=True)
    if run_chilli_jl is not False:
        bench_jl.show()
        ME_jl, MAE_jl, RMSD_jl = bench_jl.analyze(verbose=True)

    # latex
    if run_chilli_cpp is not False and run_chilli_jl is not False:
        print_latex_table(bench_dct,bench_py,bench_cpp,bench_jl,method)


    if not use_ref:
        print("Chilli.py")
        print("ref=")
        pprint(bench_py.get_dict())
        if run_chilli_cpp is not False:
            print("Chilli.cpp")
            print("ref=")
            pprint(bench_cpp.get_dict())
        if run_chilli_jl is not False:
            print("Chilli.jl")
            print("ref=")
            pprint(bench_jl.get_dict())

    assert MAE_py < Etol  
    print(f"tests@{method}: sucessfully done!")


def run_chilli_py(atoms,basis="6-31G",grid=(50,194),mode="UHF",xc="LDA,VWN",maxiter=300):
    """
        run
        Run chilli_py calculation.
    """
    from chilli_py.UKS import UKS
    from chilli_py.UHF import UHF
    if mode == "UKS":
       mf = UKS(atoms,
                basis,
                grid,
                Etol=1e-8,
                maxiter=maxiter,
                verbose=False,
                use_avg=True)

    if mode == "UHF":
        mf = UHF(atoms,
                basis,
                Etol=1e-8,
                maxiter=maxiter,
                verbose=False,
                use_avg=True)
    mf.xc_name = xc
    mf.kernel()
    return mf.Etot


def run_pyscf(atoms,basis="6-31G",grid=(50,194),mode="UHF",xc="LDA,PW",maxiter=300):
    """
        run_pyscf
        Run PySCF reference calculation (if needed).
        We use this to generate the reference values
        (ref dict).
    """
    # Indirect imports, b/c CI
    from pyscf import gto, scf, dft
    print("UKS, PySCF")
    # SS: built mol from atoms
    # SS: atoms has Bohr
    s = ''
    for sym,pos in zip(atoms.sym,atoms.pos):
        s += f'{sym} {pos[0]} {pos[1]} {pos[2]};'
    mol = gto.M(
                atom = s,
                basis = basis, #sto-3g",#cc-pvqz',#"sto3g",
                symmetry = False,
                charge=atoms.charge,
                spin=atoms.spin,
                cart=False,
                unit = 'Bohr'
                 )
    if mode == "UHF":
        mf = scf.UHF(mol)
        mf.verbose = 4
        mf.max_cycle = maxiter-1  #999
        mf.conv_tol = 1e-8
        #mf.diis = None
        mf.init_guess = '1e'
        etot = mf.kernel()
    if mode == "UKS":
        mf = scf.UKS(mol)
        mf.max_cycle = maxiter-1
        mf.xc = xc
        mf.verbose = 4

        ## PySCF hides one SCF step in the initialization
        #mf.max_cycle = 99 # maxiter -1
        #mf.conv_tol = 1e-12
        ## With or without DIIS
        ##mf.diis = None
        ## Use Hcore as inital guess for Fockian.
        mf.init_guess = '1e'
        ## We do not like pruning.
        mf.grids.prune = None
        mf.grids.radi_method = dft.radi.gauss_chebyshev #dft.radi.becke
        #mf.grids.radii_adjust = None
        mf.grids.atom_grid = grid #(100,110) #(50,194)
        mf.grids.build()
        etot = mf.kernel()
    return etot

xc_name2libxc = {"LDA,PW" : "LDA_X,LDA_C_PW",
                 "LDA,VWN" : "LDA_X,LDA_C_VWN",
                 "LDA,CHACHIYO" : "LDA_X,LDA_C_CHACHIYO", 
                 "PBE,PBE" : "GGA_X_PBE,GGA_C_PBE",
}

