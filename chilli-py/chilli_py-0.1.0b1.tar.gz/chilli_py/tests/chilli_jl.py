#from julia.api import Julia
#jl = Julia(compiled_modules=False)
#from julia import Pkg
#Pkg.add(path="/home/theonov13/Programms/chilli_jl/",subdir="chilli_jl")

from julia import Main 
from julia import chilli_jl 

# chilli.jl in Python (24.01.2023) 
# 
# Reference 
# - https://blog.esciencecenter.nl/how-to-call-julia-code-from-python-8589a56a98f2
# 
# Needed to be adjust on the Julia side 
# ```
# julia> using Pkg 
# julia> Pkg.add("PyCall")
# ```
# 
# Needed to be adjust on the Python side 
# ```
# pip3 install julia 
# ipython> python-jl -m IPython 
# ipython> from julia import Pkg  
# ipython> Pkg.add(path="/home/theonov13/Programms/chilli_jl/",subdir="chilli_jl")
# ```
# 
# Afterwards you can simply import chilli_jl 
# ```
# from julia import chilli_jl 
# ``` 
# Notes 
#  - Julia variables in Python are under the Main.[variable] name space 
#  - to run it; the simplest way is python-jl [script_name].py 

class interface_chilli_jl:
    """
        interface_chilli_jl class 
        Runs chilli_jl from Python. 
    """
    def __init__(self,
                 method,
                 f_xyz,
                 spin=0,
                 charge=0,
                 basis_name="sto-3g",
                 use_avg="true",
                 maxiter=300,
                 Etol=1e-6):
        """
            __init__
            Initialize an instance of the class. 
        """
        # Variables 
        self.pkg_path = Main.eval("chilli_jl.pkg_path")
        self.method = method 
        self.f_xyz = f_xyz 
        self.spin = spin 
        self.charge = charge 
        self.basis_name = self.pkg_path+"/src/basis/"+basis_name
        self.use_avg = use_avg 
        self.maxiter = maxiter 
        self.Etol = Etol 

        # Atoms 
        Main.atoms = chilli_jl.atoms_from_xyz(self.f_xyz,
                                              spin=self.spin,
                                              charge=self.charge)
        self.atoms = Main.atoms 

        # Paramaters 
        Main.parms = chilli_jl.parameters(self.atoms,self.basis_name)
        Main.eval(f"Main.parms.use_avg = {self.use_avg}")
        Main.eval(f"Main.parms.maxiter = {self.maxiter}")
        Main.eval(f"Main.parms.Etol = {self.Etol}")
        self.parms = Main.parms

    def kernel(self):
        """
            kernel 
            Main function of the class. 
            Execute the respective Julian kernel function 
            of the selected method.
        """
        # RHF 
        if self.method == "RHF":
            Main.ret = chilli_jl.RHF_SCF(self.parms)
        # RKS 
        if self.method == "RKS": 
            Main.ret = chilli_jl.RKS_SCF(self.parms)
        # UHF
        if self.method == "UHF":
            Main.ret = chilli_jl.UHF_SCF(self.parms)
        # UKS
        if self.method == "UKS":
            Main.ret = chilli_jl.UKS_SCF(self.parms)
        self.ret = Main.ret 
        Etot = Main.ret.Etot 
        return Etot 

def test_chilli_jl():
    """
        test_chilli_jl
        Test chilli_jl interface. 
    """
    method = "UHF"
    f_xyz = chilli_jl.pkg_path+"/src/structs/H2O.xyz"
    Methods = ["RHF","RKS","UHF","UKS"]
    d = {}
    for method in Methods: 
        jl = interface_chilli_jl(method,f_xyz)
        Etot = jl.kernel() 
        d.update({method: Etot})
        print(f"Etot = {Etot}")
    for key,val in d.items(): 
        print(f"{key}: {val}") 

if __name__ == "__main__": 
    test_chilli_jl()
