import numpy as np 
import scipy.linalg 
from chilli_py.integrals import one 
from chilli_py.RHF import RHF
from chilli_py.RKS import RKS 
from chilli_py.atoms import Atoms, atoms_from_xyz
from chilli_py import __path__ as pkg_path
from chilli_py.dipole import dip_nuc 
from chilli_py.constants import BOHR2ANG 
from chilli_py.alias import ortho
from scipy.optimize import minimize

# Status 
# - 10.06.2022 
#   + seems to work for H2O, CH4 and Ne 

# Notes 
# - for sto-3g and fixed common origin [0,0,0] it works 
# - with common origin as charge center is does not work 
# - pc-0 gives slightly different dipole; thus everthing is different 

# References 
# - PySCF
#   + Boys 
#     * https://raw.githubusercontent.com/pyscf/pyscf/master/pyscf/lo/boys.py
# - ERKALE 
#   + Boys 
#     * https://github.com/susilehtola/erkale/blob/master/src/localization.cpp#L477
#   + needs basis.moment 
#     * https://github.com/susilehtola/erkale/blob/8297aefe5aac9dbbb291e04c07661f3cff94a99a/src/basis.cpp#L1175
# - MMD 
#   + https://github.com/jjgoings/McMurchie-Davidson/blob/dcff9d232f7950f2e6b0b879387c76bb83ebf812/mmd/backup/reference-integrals.py#L90

# Paths 
# - (base) theonov13@dragon:~/Calculations/localization$

def get_com(mf, U,f_name="COM.xyz"):
    """
        get_com
        mode: restricted 
        Calculate center of mass 
        from orbital densities.  
    """
    f = open(f_name,"w")
    l_com = []
    ao1 = mf.grids.basis_ongrid
    Nelec = mf.atoms.Nelec
    Nclosed,Nopen = divmod( int(Nelec), 2 )

    f.write(f"{len(mf.atoms.sym) + Nclosed}\n\n")
    print(mf.atoms.pos,mf.atoms)
    for s,p in zip(mf.atoms.sym,mf.atoms.pos):
        print(p)
        p *= BOHR2ANG
        print(p)
        f.write(f"{s} {p[0]} {p[1]} {p[2]}\n")
    for i in range(Nclosed):
        phi = ao1.dot(U[:, i])
        dens = np.conjugate(phi) * phi * mf.grids.weights
        print(f"shape(dens): {dens.shape}") 
        # COM
        x = np.sum(dens * mf.grids.coords[:, 0]) * BOHR2ANG
        y = np.sum(dens * mf.grids.coords[:, 1]) * BOHR2ANG
        z = np.sum(dens * mf.grids.coords[:, 2]) * BOHR2ANG
        f.write(f"X {x} {y} {z}\n")
        l_com.append([x, y, z])
    f.close()
    return l_com

def expmat(mat):
    """
        expmat
        Matrix exponential of matrix mat. 
    """
    return scipy.linalg.expm(mat)

def mat2vec(mat):
    """
        mat2vec
        Transform a matrix mat to a vector vec. 

        Notes
            - in PySCF pack_uniq_var
    """
    nmo = mat.shape[0]
    idx = np.tril_indices(nmo, -1)
    return mat[idx]

def vec2mat(vec):
    """
        vec2mat
        Transform a vector vec to a matrix mat. 

        Notes 
            - in PySCF unpack_uniq_var
    """
    nmo = int(np.sqrt(vec.size*2)) + 1
    idx = np.tril_indices(nmo, -1)
    mat = np.zeros((nmo,nmo))
    mat[idx] = vec
    return mat - mat.conj().T

def dipole_integral(Mx,My,Mz,U):
    """
        dipole_integral
        Get Boys cost_function and gradient. 
    """
    Nocc = U.shape[1]
    dip = np.zeros((3,Nocc,Nocc))

    dip[0,:,:] = np.dot(U.T,np.dot(Mx,U))
    dip[1,:,:] = np.dot(U.T,np.dot(My,U))
    dip[2,:,:] = np.dot(U.T,np.dot(Mz,U))
    
    # cost function 
    e = -np.einsum('xii,xii->', dip, dip) * 2

    # gradient 
    g0 = np.einsum('xii,xip->pi', dip, dip)
    g = -1*mat2vec(g0-g0.conj().T)  * 2  
    return e, g 

def ltrial(vec):
    """
       ltrial 
       Get the maximal step length

       Input 
            - mat
    """
    mat = vec2mat(vec)
    # Matrix is antihermitian, so eigenvalues are purely
    # imaginary. Multiply by -i to make matrix hermitian and
    # eigenvalues real.
    kval, kvec = np.linalg.eigh(-1j*mat)
    # Maximum step length is
    return np.pi / (2 * np.max(np.abs(kval)))

    
class Boys: 
    """
        Boys Class 
        Boys localization 

        Notes
            - it is designed to generate COMs 
              as inital FODs 
            - only for the COM purpose the 
              routine is checked 

    """
    def __init__(self,mf,U=None):
        """
            __init__ 
            Initialize an instance of the class. 
        """
        self.mf = mf 

        # get moment matrices 
        S,T,V,Mx,My,Mz = one(mf.basis,mf.atoms)
        self.Mx = Mx
        self.My = My
        self.Mz = Mz

        # Check: U 
        if U is None:
            self.U = mf.U
        if U is not None: 
            self.U = U 

        # Get: guess for x0 and W 
        self.init_guess() 
        
        # Parameters 
        self.maxiter = 1000
        self.Etol = 1e-6
        self.h = 1e-4 
        self.stab_thr = 1e-4 

    def init_guess(self): 
        """
            init_guess 
            Get initial guess for x0 and W0. 
        """
        Nelec= self.mf.atoms.Nelec
        self.Nclosed,Nopen = divmod( int(Nelec), 2 )
        self.x0 = np.ones(self.Nclosed*2)
        print(f"len(self.x0) : {len(self.x0)}")
        mat = vec2mat(self.x0)
        self.W0 = expmat(mat)
        print(f"W0: {self.W0}") 
        print(f"U : {self.U[:,:self.Nclosed]}") 
        self.U = np.dot(self.U[:,:self.Nclosed],self.W0)
        print(f"U_next : {self.U}") 
        self.dx = ltrial(self.x0)/5
        print(f"dx : {self.dx}") 
    def get_energy(self,x): 
        """
            get_energy
            get the E_Boys = sum_i <psi_i| r | psi_i>**2 
            and the respective derivative. 
        """
        mat = vec2mat(x)
        self.W = expmat(mat)
        self.U = np.dot(self.U,self.W) 
        e,g  = dipole_integral(self.Mx,self.My,self.Mz,self.U)
        self.g = g
        return e

    def get_grad(self,x):
        """
            get_grad 
            Get gradient grad. 
            Assumes that get_energy was called before. 
        """
        return self.g

    def hessian(self):
        """
            hessian 
            Calculate the Hessian and check 
            its eigenvalues. 
            If the lowest eigenvalue is close 
            to zero we may found good 
            localized orbitals. 
            Its preferable if the sign of 
            the lowest eigenvalue is positive. 
            However, small negative values 
            close to zero are okay as well as. 
        """
        # Form finite-difference Hessian
        occ = len(self.x0)
        hessian = np.zeros((occ, occ))
        for i in range(occ):
            x = np.zeros(occ)

            # left 
            x[i] = -self.h
            mat = vec2mat(x)
            W = expmat(mat)
            Uleft = np.dot(self.U,W)
            eleft, gleft = dipole_integral(self.Mx,self.My,self.Mz,Uleft)

            #right 
            x[i] = +self.h
            mat = vec2mat(x)
            W = expmat(mat)
            Uright = np.dot(self.U,W)
            eright, gright = dipole_integral(self.Mx,self.My,self.Mz,Uright)

            hessian[:,i] = (gright-gleft)/(2*self.h)
        
        # Symmetrize it
        hessian = 0.5*(hessian + hessian.T)

        # Eigenvectors and eigenvalues
        hval, hvec = np.linalg.eigh(hessian)
        
        # min(hval)
        if len(hval) > 1:
            hval_min = np.min(hval)
        if len(hval) <= 1:
            hval_min = hval
       
        # Check: the smallest eigenvalue 
        hval_min_sign = np.sign(hval_min) 

        print(f"hval_min: {hval_min}") 
        print(f"Aim: Values close to zero and preferable with positive sign.")

        return hval_min, hval, hvec 

    def _write_com(self): 
        """
            _write_com
            Write center of mass (COM) of densities 
            orbital densities to approximate 
            Fermi-orbital descriptors.

            Note 
                - the mf must have mf.grids
        """
        get_com(self.mf, self.U,"BOYS_COM.xyz")

    def kernel(self): 
        """
            kernel 
            Kernel/main function of this class. 

            Notes 
                - its written like a SCF procedure 
        """
        # inital values 
        E0 = self.get_energy(self.x0) 
        print(f"E0: {E0}") 
        x = self.x0
        sd = None
        oldsd = None
        Eold = E0
        
        # Start: SCF 
        for iiter in range(self.maxiter): 
            # Update: cost function and gradient 
            E = self.get_energy(x) 
            g = self.get_grad(x)
            if sd is not None:
                oldsd = sd.copy()
            sd = -g 
            # Update: search direction 
            if oldsd is not None:
                # Polak-Ribière conjugate gradients (CG)
                gamma = np.dot(sd,sd-oldsd)/np.dot(oldsd,oldsd)
                sd += gamma*oldsd
            # New: x
            x = np.multiply(self.dx,sd)
            # Check: convergence 
            DeltaE = abs(Eold - E)
            print(f"iiter:{iiter} E: {E} DeltaE: {DeltaE}") 
            if DeltaE <= self.Etol: 
                break 
            Eold = E 
            #oldsd = sd 
        self._write_com()
        return E 

    def stability_anlysis(self):
        run = True 
        iiter_outer = 0 
        while run: 
            hval_min, hval, hvec = self.hessian()
            if hval_min > self.stab_thr:
                print("Minima detected")
                run = False 
            if hval_min <= self.stab_thr:
                print("Instability detected, minimize along the direction")
                sd = hvec[:,0] 
                # Period of oscillation is
                dx = ltrial(sd)
                # Brute-force line search
                x_range = np.arange(0.1*dx, 1.1*dx, 0.1*dx)
                y = np.zeros_like(x_range)
                for i,xi in enumerate(x_range): 
                    y[i] = self.get_energy(xi*sd)
                idxmin = np.argmin(y)
                # New starting point 
                x0 = x_range[idxmin]*sd
                self.x0 = x0 
                mat = vec2mat(x0)
                W = expmat(mat)
                self.U = np.dot(self.U[:,:self.Nclosed],self.W)
                #self.dx = ltrial(x0)/5
                E = self.kernel()
                iiter_outer += 1 
                print(f"iiter_outer {iiter_outer}: {E}") 
                run = True 
def main():
    """
        main 
        Main function to check the functionality of this routine 
    """
    # RKS 
    #atoms = Atoms(['Ar'],[[0.,0.,0.]])
    atoms = atoms_from_xyz(pkg_path[0]+"/structs"+"/H2O.xyz")
    #atoms = atoms_from_xyz(pkg_path[0]+"/structs"+"/CH4.xyz")
    #atoms = atoms_from_xyz(pkg_path[0]+"/structs"+"/allyl.xyz")
    
    print(atoms)
    mf = RKS(atoms,basis_name="pc-0",use_avg=True,grids=(100,110))
    mf.verbose = False
    mf.kernel()
    
    # BOYS 
    boys = Boys(mf)
    e, g = dipole_integral(boys.Mx,boys.My,boys.Mz,boys.U) #mf.U) #np.eye(mf.U.shape[1]))
    print(e,g)
    boys.kernel() 
    #boys.hessian() 
    boys.stability_anlysis()
    #boys.kernel()
    print(f"rks U : {mf.U}")

if __name__ == "__main__": 
    main() 
