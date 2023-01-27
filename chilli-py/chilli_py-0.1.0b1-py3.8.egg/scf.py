import numpy as np 
from chilli_py.alias import ortho 

""" Self-consistent field (SCF) functionality """ 

def get_guess(Hcore,S,guess="GWH"):
    """
        get_guess
        type: inital guess for SCF
        Get an initial Hamiltonian. 

        Input 
            - Hcore, np.array(), core Hamiltonian 
            - S, np.array(), overlap matrix 
            - guess, str(), "GWH" or "Hcore"

        Notes
            - Hcore = T + V 
    """
    if guess == "Hcore": 
        return Hcore 
    if guess == "GWH": 
        return get_GWH(Hcore,S) 

def get_GWH(Hcore,S,K=1.75): 
    """
        get_GWH
        type: inital guess for SCF
        Get an initial Hamiltonian.
        Generalized Wolfsberg–Helmholz (GWH) approximation.

        Input
            - Hcore, core Hamiltonian 
            - S. overlap matrix 
            - K, float(), 1.75 open-shell 

        Reference 
            - Assessment of Initial Guesses for Self-Consistent Field Calculations. Superposition of Atomic Potentials: Simple yet Efficient
    """ 
    Hguess = np.zeros_like(Hcore) 
    for i in range(Hcore.shape[0]):
        for j in range(Hcore.shape[1]):
            Hguess[i,j] = 1/2.*K*(Hcore[i,i]+Hcore[j,j])*S[i,j]
    return Hguess 

class DIIS:
    """
        DIIS class 
        Pulay's direct inversion of the iterative subspace (DIIS)
        also known as Pulay mixing. 

        Reference 
            - [PyQuante](https://github.com/gabrielelanaro/pyquante/blob/master/PyQuante/Convergence.py#L73)
    """
    def __init__(self,S):
        """
            __init__
            Initialize instance of class.

            Input 
                - S, overlap matrix 
        """
        self.F_history = []
        self.error_history = []
        self.Fold = None
        self.S = S
        # Begin DIIS from iteration 0 in all cases
        self.started = 0
        self.tol = 0.1
        self.verbose = True

    def _simple_avg(self,F):
        """
            _simple_avg
            Simple averaging of current and the old Fockian. 

            Input 
                - F, Fockian 
        """
        if self.Fold is not None:
            Favg = 0.5*F + 0.5*self.Fold
        else:
            Favg = F
        self.Fold = F
        return Favg


    def get_F(self,F,D):
        """
            get_F 
            Get new F from DIIS update.

            Input
                - F, Fockian 
                - D, Density matrix 
        """
        error = np.dot(F,np.dot(D,self.S)) - np.dot(self.S,np.dot(D,F))
        error = np.ravel(error)
        maxerror = max(abs(error))
        self.maxerror = maxerror

        if maxerror < self.tol and not self.started:
            if self.verbose:
                print(f"Starting DIIS: Max(Error) = {maxerror}")
            self.started = 1


        if not self.started:
            return self._simple_avg(F)

        # Fill the history 
        self.F_history.append(F)
        self.error_history.append(error)

        Nit = len(self.error_history)
        a = np.zeros((Nit+1,Nit+1))
        b = np.zeros(Nit+1) 
        for i in range(Nit):
            for j in range(Nit):
                a[i,j] = np.dot(self.error_history[i],self.error_history[j])
        for i in range(Nit):
            a[Nit,i] = a[i,Nit] = -1.0
            b[i] = 0
        a[Nit,Nit] = 0
        b[Nit] = -1.0

        try:
            c = np.linalg.solve(a,b)
        except:
            self.Fold = F
            return F

        Favg = np.zeros_like(F)
        for i in range(Nit):
            Favg += c[i]*self.F_history[i]
        return Favg


class DIIS_psi4numpy:
    """
	DIIS_psi4numpy class 
        Pulay's direct inversion of the iterative subspace (DIIS)
        also known as Pulay mixing. 

	Reference
	    - https://github.com/psi4/psi4numpy/blob/master/Self-Consistent-Field/RHF_DIIS.py
    """
    def __init__(self,DIIS_max=6):
        """
            __init__
            Initialize an instance of the class. 
        """
        self.DIIS_max = DIIS_max # max length of DIIS history
        self.Fockians = []
        self.DIIS_errors = []
        self.DIIS_start = 2 

    def _get_DIIS_error(self,S,F,D):
        """
            _get_DIIS_error
            DIIS error build

            Reference 
                - DIIS error build w/ HF analytic gradient ([Pulay:1969:197])
        """
        diis_e = np.einsum('ij,jk,kl->il', F, D, S) - np.einsum('ij,jk,kl->il', S, D, F)
        A = ortho(S)
        diis_e = A.dot(diis_e).dot(A)
        dRMS = np.mean(diis_e**2)**0.5
        return diis_e, dRMS

    def _update(self,F,diis_e):
        """
            _update
            Update the DIIS history, i.e., 
            Fockians and DIIS_errors.
        """
        self.Fockians.append(F)
        self.DIIS_errors.append(diis_e)
        # Limit size of DIIS vector
        self.DIIS_count = len(self.Fockians)
        if self.DIIS_count > self.DIIS_max: 
            # Remove the oldest entry 
            del self.Fockians[0]
            del self.DIIS_errors[0]
            self.DIIS_count -= 1 

    def _build_Bmatrix(self):
        """
            _build_Bmatrix
            Build error matrix B. 

            Reference 
                - [Pulay:1980:393], Eqn. 6, LHS
        """
        B = np.empty((self.DIIS_count + 1, self.DIIS_count + 1))
        B[-1, :] = -1
        B[:, -1] = -1
        B[-1, -1] = 0
        for i, e1 in enumerate(self.DIIS_errors):
            for j, e2 in enumerate(self.DIIS_errors):
                if j > i:
                    continue
                val = np.einsum('ij,ij->', e1, e2)
                B[i,j] = val
                B[j,i] = val
        # normalize
        B[abs(B) < 1.e-14] = 1.e-14
        B[:-1, :-1] /= np.abs(B[:-1, :-1]).max()
        return B  

    def _get_F(self,SCF_ITER):
        """
            _get_F
            Get new Fockian, Fnew. 

            References
                - Build residual vector, [Pulay:1980:393], Eqn. 6, RHS
                - Solve Pulay equations, [Pulay:1980:393], Eqn. 6
        """
        if SCF_ITER >= self.DIIS_start:
            B = self._build_Bmatrix()

            # Build residual vector, [Pulay:1980:393], Eqn. 6, RHS
            resid = np.zeros(self.DIIS_count + 1)
            resid[-1] = -1

            # Solve Pulay equations, [Pulay:1980:393], Eqn. 6
            # SS: The problem can get sigular, e.g., H atom 
            # SS: try to catch this error with the try/ except 
            try:
                ci = np.linalg.solve(B, resid)
            except: 
                print("failed solve Pulay") 
                return self.Fockians[-1]
            
            # Calculate new fock matrix as linear
            # combination of previous fock matrices
            Fnew = np.zeros_like(self.Fockians[-1])
            for i, c in enumerate(ci[:-1]):
                Fnew += c * self.Fockians[i]
        if SCF_ITER < self.DIIS_start:
            # Debugging
            # print(f"direct {SCF_ITER} < {self.DIIS_start}") 
            Fnew = self.Fockians[-1]
        return Fnew 

    def kernel(self,SCF_ITER,S,F,D):
        """
            kernel
            Main function of this class. 
        """
        diis_e,dRMS = self._get_DIIS_error(S,F,D)
        self._update(F,diis_e)
        Fnew = self._get_F(SCF_ITER)
        return Fnew, diis_e, dRMS  

# Set the standard export 
DIIS = DIIS_psi4numpy

class Results:
    """
        Results class 
        Collect results in object.

        Used by 
            - SCF to copy the results to another class 
    """
    def __init__(self,name=None):
        """
            __init__
            Initialize instance of the class.
        """
        self.name = name 

    def update(self,other):
        """
           update
           Add the results to another object, e.g., 
           the results of SCF function to the SCF class.
        """
        keys = vars(self) 
        for key in keys:
            if key != "name":
                val = getattr(self,key)
                setattr(other,key,val)


