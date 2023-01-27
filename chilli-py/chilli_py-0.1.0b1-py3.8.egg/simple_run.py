from chilli_py.atoms import atoms_from_xyz
from chilli_py.RHF import RHF
from chilli_py.RKS import RKS
from chilli_py.bench import name2path 

def run(sys_name,mode="RKS"):
    """
        run 
        Simple run function, e.g., run a calculation, 
        for one of the predefined systems sys_name. 

        Input
            - sys_name, str(), e.g., "H2" or "H2O"
            - mode, str(), e.g., "RHF" or "RKS"
    """
    modes = ["RHF","RKS"]
    data = name2path(sys_name)
    f_xyz = data["f_xyz"]
    atoms = atoms_from_xyz(f_xyz)
    if mode == "RHF": 
        mf = RHF(atoms,
                "pc-0",
                Etol=1e-12,
                maxiter=300,
                verbose=False,
                use_avg=False)
    if mode == "RKS": 
        mf = RKS(atoms,
                "pc-0",
                (200,110),
                Etol=1e-12,
                maxiter=300,
                verbose=False,
                use_avg=True)
    if mode not in modes:
        print(f"mode {mode} not available")
    if mode in modes:        
        mf.kernel()
        return mf.Etot, mf.Eigs

def main():
    """
        main 
        Main function to this routine. 
    """
    run("H2O","RHF")
    run("H2O","RKS")

if __name__ == '__main__':
    main()


