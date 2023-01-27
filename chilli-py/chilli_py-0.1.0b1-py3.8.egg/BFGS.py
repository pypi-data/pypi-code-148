import numpy as np
from chilli_py.bench import H2, CH4 #, H2O, 
from chilli_py.atoms import Atoms 
from chilli_py.constants import ANG2BOHR
from chilli_py.RKS import RKS 
from chilli_py.RFLO import RFLO
from chilli_py.lj import LJ 
from copy import copy, deepcopy  
from scipy.linalg import eigh
#from chilli_py.scipy_eigh import eigh

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

class State: 
    def __init__(self,atoms,typ,**kwargs): 
        self.atoms = atoms
        self.typ = typ 
        self.Etot = None 
        self.forces = None 
        self.consistent = False 
        self._init_kwargs(kwargs) 

    def _init_kwargs(self,kwargs): 
        for key,value in kwargs.items(): 
            setattr(self,key,value) 

    def update(self,Etot,forces): 
        self.Etot = Etot 
        self.forces = forces 
        self.consistent = True

    def get_coords(self): 
        if self.typ == "nuclei": 
            res =  self.atoms.pos 
        if self.typ == "FODs": 
            res = self.fods.pos 
        return res 

    def set_coords(self,r): 
        if self.typ == "nuclei": 
            self.atoms.pos = r 
        if self.typ == "FODs": 
            self.fods.pos = r 

    def show(self):
        notshown = ["atoms","fods","mf"]
        for attr in vars(self): 
            if attr not in notshown:
                val = getattr(self,attr) 
                print(f"{attr} : {val}") 

class GD: 
    def __init__(self,state,func,alpha=0.001,Nmax=100,maxstep=0.2,Etol=1e-5,fmax=0.05): 
        self.state = state
        self.func = func 
        self.alpha = alpha
        self.Nmax = Nmax
        self.maxstep = maxstep
        self.Etol = Etol
        self.fmax = fmax 
        self._init_params()

    def _init_params(self):
        """
            _init_params
            Set inital parameters
        """
        self.H0 = np.eye(3 * len(self.state.get_coords()))*self.alpha
        self.H = None
        # if H is None we do not update in the 1st iteration
        self.r0 = self.state.get_coords() # here not flatted 
        self.f0 = 0

    def step(self,r,f): 
        dr = self.alpha*f #np.dot(alpha,df)
        r -= dr
        print(f"new r: {r}") 
        self.state.set_coords(r)

    def get_fmax(self,f):
        """
            get_fmax
            Get maximal force component
        """
        fmax = np.sqrt((f**2).sum(axis=1).max())
        return fmax

    def kernel(self):
        r = self.r0 
        Eold = 0
        for iiter in range(0,self.Nmax):

            self.func(self.state) 
            Etot = self.state.Etot 
            f = -1.*self.state.forces 

            fmaxiter = self.get_fmax(f) 
            r = self.state.get_coords() 
            self.step(r,f) 

            print(f"iter: {iiter} Etot = {Etot:10.5f} fmax: {fmaxiter:10.5f} ")
            deltaf = abs(Etot - Eold)
            if abs(deltaf) <= self.Etol and fmaxiter < self.fmax: 
                print(f"Finished! \n iteration: {iiter} \n Etot : {Etot} \n fmax : {fmaxiter}")
                break
            Eold = Etot

class BFGS: 

    def __init__(self,state,func,alpha=70.,Nmax=100,maxstep=0.2,Etol=1e-5,fmax=0.05): 
        self.state = state
        self.fmax = fmax 
        self.func = func 
        self.alpha = alpha 
        self.Nmax = Nmax 
        self.maxstep = maxstep 
        self.Etol = Etol
        self._init_params() 

    def _init_params(self):
        """
            _init_params 
            Set inital parameters 
        """
        self.H0 = np.eye(3 * len(self.state.get_coords()))*self.alpha 
        self.H = None 
        # if H is None we do not update in the 1st iteration 
        self.r0 = None  
        self.f0 = None 
    
    def update(self,r,f): 
        """
            update 
            Update Hessian 
            Notes
                - updates H 
        """
        if self.H is None: 
            self.H = self.H0
            return 
        
        delta_r = r - self.r0  
        delta_f = f - self.f0 
       
        if max(abs(delta_r)) < 1e-7: 
            print("same config") 
            return 

        print(f"r: {r} \n r0: {self.r0}") 
        print(f"f: {f} \n f0: {self.f0}") 
        print(f"delta_r : {delta_r} \n delta_f : {delta_f}") 

        a = np.dot(delta_r,delta_f)
        print(f"a: {a}")
        dg = np.dot(self.H,delta_r) 
        #print(f"dg: {dg}") 
        b= np.dot(delta_r,dg)
        print(f"b: {b}")
        #print(f"b = {b}") 
        #print(f"H part1 : {np.outer(delta_f,delta_f) }")
        v1 = np.outer(delta_f,delta_f) / a 
        v2 =  np.outer(dg,dg) / b
        print(f"v1: {v1}") 
        print(f"v2: {v2}")

        #print(f"v1: {v1} \n v2: {v2}") 
        self.H -= np.outer(delta_f,delta_f) / a + np.outer(dg,dg) / b 
        print(f"H : {self.H}") 
    def check_dr(self,dr,steplengths): 
        """ 
            check_dr 
            Rescale dr if the actual max steplength is 
            bigger then the threshold maxstep. 
        """
        iter_maxstep = np.max(steplengths)
        #print(f"iter_maxstep: {iter_maxstep} \n steplengths : {steplengths}") 
        if iter_maxstep > self.maxstep: 
            scale = self.maxstep / iter_maxstep
            print(f"scale: {scale}") 
            dr *= scale 
        return dr 

    def step(self,r,f):
        """
            step 
            One iteration step 
        """
        print(f"r: {r} \n f: {f}") 
        self.update(r,f) 
        
        omega, V = eigh(self.H)
        print(f"opt.H \n {self.H}")
        print(f"omega[0]: {omega[0]}") 
        print(f"omega: {omega} size:  {omega.shape}")
        #print(f"V : {V} size: {V.shape}")
        #print(f"f: {f}")  
        #print(f" dot(f,V) : {np.dot(f, V) / np.fabs(omega)}")
        #print(f" dot(f,V) : {np.dot(V, np.dot(f, V) / np.fabs(omega))}") 
        print(f"dr: {np.dot(V, np.dot(f, V) / np.fabs(omega))} \n \n ")
        dr = np.dot(V, np.dot(f, V) / np.fabs(omega)).reshape((-1, 3))
        print(f"dr: {dr} {dr.shape}") 
        #print(f"r: {r.reshape(-1,3)}") 
        #print(f"dr (pre check)  : {dr}") 
        steplengths = (dr**2).sum(1)**0.5
        print(f"steplengths: {steplengths}")
        dr = self.check_dr(dr, steplengths)
        #print(f"dr (after check)  : {dr}")
        #print(f"r: {r.reshape(-1,3) + dr}") 
        #self.atoms.set_positions(r.reshape(-1,3) + dr)
        print(f"dr : {dr}")
        print(f"r + dr : {r.reshape(-1,3) + dr}")
        self.state.set_coords(r.reshape(-1,3) + dr) 

        # update reference 
        print(f"sliced r0: {r} \n\n")
        self.r0 = r.copy() 
        print(f"new f0: {f}") 
        self.f0 = f.copy()  


    def get_fmax(self,f): 
        """
            get_fmax 
            Get maximal force component 
        """
        fmax = np.sqrt((f**2).sum(axis=1).max())
        return fmax

    def kernel(self):
        """
            kernel 
            Main function 
        """
        Eold = 0 
        DeltaE = 0
        for iiter in range(0,self.Nmax): 
            #r = self.atoms.positions.flatten() 
            print(f"r top scf: {self.state.get_coords()} \n flatt: {self.state.get_coords().flatten()}")
            r  = self.state.get_coords().flatten() 
            self.func(self.state)
            Etot = self.state.Etot
            f = self.state.forces.flatten() # -1
            print(self.state.get_coords())
            #print(f" f in interation: {f}") 
            #Etot = self.atoms.get_potential_energy()
            #f = self.atoms._calc.results["forces"].flatten() 
            fmaxiter = self.get_fmax(f.reshape(-1,3)) 
            self.step(r,f)
            print(f"BFGS iter: {iiter} Etot = {Etot:10.8f} fmax: {fmaxiter:10.8f} ") 
            #print(f"forces: {f}")
            DeltaE = abs(Etot - Eold) 
            if DeltaE <= self.Etol and fmaxiter <= self.fmax: 
                print("Finished") 
                break 
            Eold = Etot 

def rflo(state): 
    flo = RFLO(state.atoms,state.fods,mf_init=state.mf)
    flo.kernel(verbose=4,U=state.U)
    if np.isfinite(flo.fforce).all() and np.isfinite(flo.Etot): 
        state.update(flo.Etot,flo.fforce) 
    else: 
        force = np.ones_like(flo.fforce) * 10000000.
        Etot = 10000000.
        state.update(Etot,fforce)

def lj(state):
    calc = LJ(state.atoms,state.sigma,state.epsilon)
    Etot, forces = calc.kernel()
    state.update(Etot,forces)

def main(): 
    
    #atoms, fods = H2()
    #atoms,fods  = H2O() 
    atoms,fods  = CH4()

    mf = RKS(atoms,basis_name="sto-3g",xc_name="LDA,VWN")
    mf.kernel()

    flo = RFLO(atoms,fods,mf_init=copy(mf))
    flo.kernel(verbose=4)

    # testing/debugging U 
    #U = np.diag([1]*mf.U.shape[0])*2.
    #U[4,5] = 1
    #U = copy(mf.U) 
    U = mf.U

    # Define the state 
    #state = State(atoms,"FODs",fods=fods,mf=copy(mf),U=copy(U))
    #rflo(state) 
    #state.show()
    #rflo(state) 
    #state.show() 

    ## GD 
    #print(atoms)
    #gd = GD(state,rflo,alpha=0.1,Nmax=3000,fmax=0.0001)
    #gd.kernel()
    #state.show()

   
    # Lennard-Jones 
    #state = State(atoms,"nuclei",sigma=2,epsilon=11)
    #bfgs = BFGS(state,lj,alpha=70.,Nmax=1000,maxstep=0.2,Etol=1e-5,fmax=0.05)
    #bfgs.kernel()
    ##gd = GD(state,lj,alpha=0.001,Nmax=1000,fmax=0.0001)
    ##gd.kernel()
    #state.show()

    # RFLO 
    state = State(atoms,"FODs",fods=fods,mf=copy(mf),U=copy(U))
    bfgs = BFGS(state,rflo,alpha=70.,Nmax=100,maxstep=0.2,Etol=1e-6,fmax=0.001) 
    bfgs.kernel() 
    state.show()


if __name__ == "__main__": 
    main() 
