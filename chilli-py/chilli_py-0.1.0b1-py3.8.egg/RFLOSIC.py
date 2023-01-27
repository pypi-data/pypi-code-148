import numpy as np 
from scipy.linalg import eigh
from scipy.optimize import minimize 
from chilli_py.RKS import RKS 
from chilli_py.RFLO import RFLO 
from chilli_py.integrals import pairs, iiterator, one, two, get_J, get_K, get_2JK, get_E, dmat, dip_moment

from chilli_py.bench import Ne, CH4, H2O, COH2
from chilli_py.utils import myprint 
from chilli_py.scf import DIIS,Results
from chilli_py.utils import timeit, history, tictoc

""" Restricted Fermi-Loewdin-orbital self-interaction correction (FLO-SIC) """

class SCF_FLOSIC1: 
    """
        SCF_FLOSIC1 class 
        Perform orignal coupled SCF 
            - outer loop: FOD optimization 
            - inner loop: density matrix optimization

        Input 
            - flo: RFLO(), RFLO() object instance 
            - fods: np.array(), Fermi-orbital descriptors (FODs) 
            - U0: np.array(), e.g., Fermi-Loewdin orbital (FLO) coeffcients  
            - opt_method: str(), FOD optimizer, e.g., CG or BFGS 
            - gtol: float(), gradient tolerance for the optimizer 
            - maxiter: int(), maximal number of iterations 
            - opt_verbose: bool(), switching on verbosity for optimization 

        Note: This class is "callable", thus it can 
        be used similar as SCF_FLOSIC2. 
    """
    def __init__(self,flo,fods,U0,opt_method="CG",gtol=5e-4,maxiter=300,opt_verbose=False): 
        """
            __init__
            Initialze an instance of the class. 
        """
        self.flo = flo 
        self.fods = fods 
        self.U0 = U0 
        self.fodopt = FODOPT(fods=self.fods,
                             U=self.U0,
                             f_energy=self._get_energy,
                             f_force=self._get_force,
                             opt_method=opt_method, 
                             gtol=gtol,
                             maxiter=maxiter,
                             opt_verbose=opt_verbose)
        # Build DIIS globally 
        # So we can rememeber the previous steps 
        self.avg = DIIS() 

    def _kernel(self,flo,fods,U,use_avg=True,maxiter=300,verbose=False,Etol=1e-6): 
        """
            _kernel
            Inner SCF cycle to optimze U for a given set of FODs. 
                - optimize: U 
                - fixed: fods 
        """
        # Initial values 
        S = flo.mf.S.copy()
        Eold, F, force = flo.kernel(fods=fods,U=U)
        IS_CONVERGED = False
        dEtot = 1.0
        if use_avg:
            avg = self.avg
        print(f"Starting: inner loop // density optimization")
        for iiter in range(maxiter):
            Eigs,U = eigh(F,S)
            print(f"Eigs: {Eigs}") 
            D = dmat(U,flo.Nclosed)
            if verbose:
                myprint(D=D)
            # Update: Kohn-Sham energy and Fockian
            Etot, F, force = flo.kernel(fods=fods,U=U,verbose=3)
            # Update: Fockian
            if use_avg:
                F,DIIS_e, dRMS, = avg.kernel(iiter,S,F,D)
            dEtot = abs(Etot - Eold)
            iiter_str = f">>> iter {iiter: 4d} E = {Etot: 18.10f} Eh DeltaE = {dEtot: 10.5e} Eh"
            if use_avg:
                iiter_str += f" dRMS: {dRMS: 10.5e}"
            print(iiter_str)
            if np.isclose(Etot,Eold,0,Etol):
                IS_CONVERGED = True
                Eigs,U = eigh(F,S)
                print("Final: Eigenvalues")
                print(f"Eigs = {Eigs}")
                D = dmat(U,flo.Nclosed)
                # Dipole moment
                #mu, mu_abs = dip_moment(atoms,Mx,My,Mz,D)
                break
            Eold  = Etot
        
        if not IS_CONVERGED:
            print(f"WARNING: Inner loop is not converged")
        print(f"Ending: inner loop // density optimization")
        
        # Output: final values 
        #myprint(Etot=Etot,force=force,fmax=self.fodopt._get_fmax(force))
        
        # Results
        res  = Results()
        res.Etot = Etot
        res.U = U 
        res.fods = fods
        res.force = force 
        res.fmax = self.fodopt._get_fmax(force) 
        return res

    def _get_energy(self,fods,U):
        """
            _get_energy
            Get the energy for a given set {fods,U}. 
            Executes self._kernel() to optimize U 
            for the given set of FODs. 
        """
        self.res = self._kernel(self.flo,fods,U) 
        self.fodopt.U = self.res.U 
        EPZ = self.flo._get_energy(fods=fods,U=self.res.U)
        return EPZ 

    def _get_force(self,fods,U):
        """
            _get_force
            Get force for given set {fods,U}. 
            Assumes that self._get_energy() was called already. 
            Thus, U correspondes is optimized for the given set of FODs. 
        """
        force = self.flo._get_force(fods=fods,U=U)
        fmax = self.fodopt._get_fmax(force)
        return force 

    def kernel(self):
        """
            kernel
            Kernel function to start the 
            coupled SCF cycles.
                - outer loop: FOD optimization 
                - inner loop: density matrix optimization 
                    + see self._kernel() 
        """
        # Start: Outer loop
        print(f"Starting: outer loop // FOD optimization")
        self.fodopt._optimize()
        print(f"Ending: outer loop // FOD optimization")
        # End: Outer loop 
        return self.res 

    def __call__(self): 
        """
            __call__
            Make a instance of the class "callable". 
        """
        # We make it look like a function call 
        return self.kernel() 

class FODOPT: 
    """
        FODOPT class 
        FOD optimization class. 

    """
    def __init__(self,fods,U,f_energy,f_force,**kwargs): 
        """
            __init__
            Initialize an instance of the class. 
        """
        self.fods = fods 
        self.U = U 
        self._f_energy = f_energy 
        self._f_force = f_force 
        self._set_kwargs(kwargs)
        self.x0 = self.pos2x(self.fods)

    def _set_kwargs(self,kwargs): 
        """
            set_kwargs
            Set (additional) keyword arguments. 
        """
        self.opt_method = kwargs.get("opt_method","CG") 
        self.gtol = kwargs.get("gtol",5e-4) 
        self.maxiter = kwargs.get("maxiter",300)
        self.opt_verbose = kwargs.get("opt_verbose",False) 

    def pos2x(self,fods):
        """
            pos2x 
            positions (fods.pos) to objective vector (x)
            linearisation of the FOD positions.
        """
        x = np.array(fods.pos).flatten()
        return x 

    def x2pos(self,x):
        """
            x2pos
            objective vector (x) to positions (fods.pos)
        """
        pos = np.reshape(x,(int(len(x)/3.),3))
        return pos

    def _get_energy(self,x):
        """
            _get_energy
            Transform x to pos and calculate energy.
        """
        pos = self.x2pos(x)
        self.fods.pos = pos.copy()
        EPZ = self._f_energy(fods=self.fods,U=self.U)
        return EPZ 

    def _get_force(self,x):
        """
            _get_force
            Transform x to pos and calculate force.
        """
        pos = self.x2pos(x)
        self.fods.pos = pos.copy()
        force = self._f_force(fods=self.fods,U=self.U)
        force1d = force.flatten()
        fmax = self._get_fmax(force)
        #myprint(force=force,fmax=fmax) 
        return -1*force1d 

    def _get_fmax(self,force):
        """
            _getfmax
            Get maximal force component (fmax)

            Input
                -force : np.array(), FOD forces (force)
        """
        fmax = np.sqrt((force**2).sum(axis=1).max())
        return fmax

    def _optimize(self,verbose=False): 
        """
            _optimize
            Optimize FODs. 
        """
        # Notes: 
        #  - "L-BFGS-B" sometimes is not converging 
        #  - one needs to disable the check for the objective function aka energy 
        #  - with ftol = 0 only the gradients are checked 
        options={'disp': self.opt_verbose, 
                 'gtol': self.gtol, 
                 'eps': 1e-08,
                 'maxiter': self.maxiter,
                 'ftol' : 0
                 }
        result = minimize(self._get_energy,
                          x0=self.x0,
                          jac=self._get_force,
                          method=self.opt_method,
                          options=options,
                          tol=self.gtol) 
        self.xopt = result.x.copy()
        if verbose: 
            self.finalize(xopt) 
        return self.fods 

    def _finalize(self,x): 
        """
            _finalize
            Callback/print/output if 
            one needs to debug the this class. 
        """
        Eopt = self._get_energy(x)
        forceopt1d = self._get_force(x)
        forceopt = self.x2pos(forceopt1d)
        fmax = self._get_fmax(forceopt)
        myprint(Eopt=Eopt,forceopt=forceopt,fmax=fmax) 
        return Eopt, forceopt, fmax  
         
def SCF_FLOSIC2(flo,fods,U0,use_avg=True,maxiter=300,verbose=False,Etol=1e-6,opt_method="CG",gtol=5e-4,opt_verbose=False):
    """
        SCF_FLOSIC2
        FLO-SIC2 SCF cycle
            - outer-loop: density/density matrix optimization 
            - inner-loop: FOD optimization 
    """
    U = U0.copy() 
    # Names 
    method_short ="FLO-SIC-2"
    method_long = "FLO-SIC-2"
    # Initial values 
    S = flo.mf.S.copy() 
    Eold, F, force = flo.kernel(fods=fods,U=U)
    print(f"Einit(PZ): {Eold} fforce: {force} \nU: {U}")
    IS_CONVERGED = False
    dEtot = 1.0
    if use_avg:
        avg = DIIS()
    print(f"Starting {method_short} calculation:")
    for iiter in range(maxiter):
        Eigs,U = eigh(F,S)
        print(f"Eigs: {Eigs}")
        D = dmat(U,flo.Nclosed)
        if verbose:
            myprint(D=D)
        # Update: Kohn-Sham energy and Fockian
        # Start: Inner Loop 
        fodopt = FODOPT(fods=fods,
                        U=U,
                        f_energy=flo._get_energy,
                        f_force=flo._get_force,
                        opt_method=opt_method,
                        gtol=gtol,
                        maxiter=maxiter,
                        opt_verbose=opt_verbose)
        fods = fodopt._optimize()
        # End: Inner loop 
        Etot, F, force = flo.kernel(fods=fods,U=U,verbose=3)
        # Update: Fockian
        if use_avg:
            F,DIIS_e, dRMS, = avg.kernel(iiter,S,F,D)
        dEtot = abs(Etot - Eold)
        iiter_str = f">>> iter {iiter: 4d} E = {Etot: 18.10f} Eh DeltaE = {dEtot: 10.5e} Eh"
        if use_avg:
            iiter_str += f" dRMS: {dRMS: 10.5e}"
        print(iiter_str)
        if np.isclose(Etot,Eold,0,Etol):
            IS_CONVERGED = True
            Eigs,U = eigh(F,S)
            print("Final: Eigenvalues")
            print(f"Eigs = {Eigs}")
            D = dmat(U,flo.Nclosed)
            # Dipole moment
            #mu, mu_abs = dip_moment(atoms,Mx,My,Mz,D)
            break
        Eold  = Etot

    if not IS_CONVERGED:
        print(f"WARNING: {method_short} is not converged")

    # Output: final values 
    # myprint(Etot=Etot,force=force,fmax=fodopt._get_fmax(force))

    # Results
    res  = Results()
    res.Etot = Etot
    res.U = U
    res.fods = fods
    res.force = force 
    res.fmax = fodopt._get_fmax(force)
    return res

class FLOSIC: 
    """
        FLOSIC class 
        Perform FLO-SIC calculations. 
    """
    def __init__(self,atoms,fods,**kwargs): 
        """
            __init__
            Initialize instance of the class. 
        """
        self.atoms = atoms 
        self.fods = fods 
        self._set_kwargs(kwargs)
        self._init_mf(self.mf_init)
        self._init_flo() 

    def _set_kwargs(self,kwargs): 
        """
            _set_kwargs
            Check keyword arguments 
            and defaults. 
        """
        self.xc_name = kwargs.get("xc_name","LDA,VWN") 
        self.basis_name = kwargs.get("basis_name","sto-3g")
        self.mf_init = kwargs.get("mf_init",None)   
        self.scf_type = kwargs.get("scf_type","FLOSIC2")
        self.opt_method = kwargs.get("opt_method","CG") #"L-BFGS-B" 
        self.gtol = kwargs.get("gtol",5e-4)
        self.maxiter = kwargs.get("maxiter",int(300))
        self.opt_verbose = kwargs.get("opt_verbose", False)

    def _init_mf(self,mf_init): 
        """
            _init_mf
            Initialize RKS object. 
        """
        if mf_init is None:
            self.mf = RKS(self.atoms,
                          xc_name=self.xc_name,
                          basis_name=self.basis_name)
            self.mf.kernel() 
            self.U0 = self.mf.U.copy() 
        if mf_init is not None: 
            self.mf = mf_init 
            self.U0 = self.mf.U.copy()

    def _init_flo(self):
        """
            _init_flo
            Initialize FLO object. 
        """
        self.flo = RFLO(self.atoms,
                       self.fods,
                       mf_init=self.mf)

    @tictoc 
    def kernel(self,verbose=False):
        """
            kernel 
            Optimize FODs and density matrix D 
            in coupled SCF cycles. 
        """
        if self.scf_type == "FLOSIC1": 
            res = SCF_FLOSIC1(flo=self.flo,
                              fods=self.fods,
                              U0=self.U0,
                              opt_method=self.opt_method,
                              gtol=self.gtol,
                              maxiter=self.maxiter,
                              opt_verbose=self.opt_verbose)() 
        if self.scf_type == "FLOSIC2": 
            res = SCF_FLOSIC2(flo=self.flo,
                              fods=self.fods,
                              U0=self.U0,
                              opt_method=self.opt_method,
                              gtol=self.gtol,
                              maxiter=self.maxiter,
                              opt_verbose=self.opt_verbose)
        print(f"Final values \n Etot: {res.Etot} \n fmax: {res.fmax} \n forces: {res.force} \n FODs: \n{res.fods}") 
        return res 

def main():
    """
        main 
        Main function to test this routine. 
    """
    def get_system(sys_name):
        """
            get_system 
            Returns atoms and fods for a given 
            sys_name. 
            The 1st FOD position is slighly 
            displaced. 
        """
        system = eval(sys_name)
        atoms, fods = system()
        fods.pos[0][0] += 0.1
        return atoms, fods 

    SYSTEM = ["Ne","CH4","H2O","COH2"] 
    # Note: L-BFGS-B currently cause errors. 
    OPT = ["CG","BFGS"] #,"L-BFGS-B"]
    TICTOC = np.zeros((len(SYSTEM),len(OPT),2))
    for i,sys_name in enumerate(SYSTEM): 
        for j,opt in enumerate(OPT):
            # Build: system 
            atoms, fods = get_system(sys_name)
            
            # SCF: FLOSIC1 
            mflo = FLOSIC(atoms,
                          fods,
                          xc_name="LDA,PW",
                          basis_name="pc-0",
                          scf_type="FLOSIC1",
                          opt_method=opt) 
            res1, dt1 = mflo.kernel()   
            print(f"time: {dt1}") 
            
            # Build: system
            atoms, fods = get_system(sys_name)

            # SCF: FLOSIC2 
            mflo = FLOSIC(atoms,
                          fods,
                          xc_name="LDA,PW",
                          basis_name="pc-0",
                          scf_type="FLOSIC2",
                          opt_method=opt)
            res2, dt2 = mflo.kernel() 

            # TIME and difference of the results 
            print(f"time: {dt2}")
            speedy = dt1/dt2
            TICTOC[i,j,0] = speedy 
            TICTOC[i,j,1] = abs(res2.Etot - res1.Etot)
            print(f"speed-up-factor: {dt1/dt2}") 

    # Output
    print("| System | Method | t1/t2 | abs(Etot2-Etot1) |") 
    for i,sys_name in enumerate(SYSTEM):
        for j,opt in enumerate(OPT):
            print(f"| {sys_name} |  {opt} | {TICTOC[i,j,0]: 10.2f} | {TICTOC[i,j,1]: 10.6f} |")

if __name__ == "__main__":
    main()


