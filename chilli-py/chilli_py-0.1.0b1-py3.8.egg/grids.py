import numpy as np 
from chilli_py.atoms import Atoms
from chilli_py.radial_grid import rad_grid_becke, bragg_radii, gauss_chebyshev
from chilli_py.angular_grid import Lebedev
from chilli_py.constants import BOHR2ANG 
from chilli_py.utils import myprint 

""" Generate DFT grid """

def prange(start,end,step):
    """
        prange 
        Make block indices. 

        Input 
            - start: int()  
            - end: int() 
            - step: int()  
    """
    for i in range(start, end, step):
        yield i, min(i+step, end)

def gen_atomgrid(n_rad,n_ang,symb,Z,func_rad=gauss_chebyshev,func_ang=Lebedev):
    """
        gen_atomgrid
        Generate atomic grid for one atom. 

            atomic grid = radial grid * angular grid 
    """
    # Radial grid 
    chg = Z
    rad, dr = func_rad(n_rad, Z=Z) 
    rad_weight = 4*np.pi * rad**2 * dr

    angs = [n_ang] * n_rad
    angs = np.array(angs)
    coords = []
    vol = []
    for n in sorted(set(angs)):
        # Angular grid 
        grid = func_ang(n_ang)
        idx = np.where(angs==n)[0]
        for i0, i1 in prange(0, len(idx), 12):  # 12 radi-grids as a group
            coords.append(np.einsum('i,jk->jik',rad[idx[i0:i1]], grid[:,:3]).reshape(-1,3))
            vol.append(np.einsum('i,j->ji', rad_weight[idx[i0:i1]], grid[:,3]).ravel())
    return np.vstack(coords), np.hstack(vol)

def original_becke(mu,k=3):
    """
        original_becke
        
        Notes: 
            - PySCF, This function has been optimized in the C code VXCgen_grid

        Reference
            - [Becke88](Becke, JCP 88, 2547 (1988); DOI:10.1063/1.454033)
    """

    def p(mu): 
        """
            p 
            p(mu): [Becke88] Eq. 19
        """
        return (3/2.*mu - 1/2.*mu**3) 

    def f(mu,k):
        """
            f 
            fk(mu) : [Becke88] Eq. 20
        """
        for i in range(k):
            mu = p(mu)
        return mu 

    return f(mu,k)

def inter_distance(coords):
    """
        inter_distance
        Calculate inter-particle distance array. 

        Input 
            - coords: np.array(), coordinates 
    """
    rr = np.linalg.norm(coords.reshape(-1,1,3) - coords, axis=2)
    rr[np.diag_indices_from(rr)] = 0
    return rr

def gen_grid_partition(atoms,coords,becke_scheme=original_becke):
    """
        gen_grid_partition
        Paritioning using Becke scheme becke_scheme. 
    """
    ngrids = coords.shape[0]
    atm_dist = inter_distance(atoms.pos)
    grid_dist = np.empty((atoms.Natoms,ngrids))
    for ia in range(atoms.Natoms):
        dc = coords - atoms.pos[ia]
        grid_dist[ia] = np.sqrt(np.einsum('ij,ij->i',dc,dc))
    # P of [Becke88] Eq. 13
    P = np.ones((atoms.Natoms,ngrids))
    for i in range(atoms.Natoms):
        for j in range(i):
            mu = 1/atm_dist[i,j] * (grid_dist[i]-grid_dist[j])
            # Becke scheme 
            f = becke_scheme(mu)
            # [Becke88] Eq. 21 
            s = [0.5 * (1-f),0.5 * (1+f)]
            # [Becke88] Eq. 13
            P[i] *= s[0]
            P[j] *= s[1]
    return P 

def gen_grid(atoms,n_rad,n_ang,func_rad=gauss_chebyshev,func_ang=Lebedev):
    """
        gen_grid 
        Generate DFT grid from atomic grids 
        using Becke partioning.

        Reference
            - [Becke88](Becke, JCP 88, 2547 (1988); DOI:10.1063/1.454033)

    """
    coords_all = []
    weights_all = []
    # Loop over all atomic grids 
    for ia,(symb,coord,Z) in enumerate(zip(atoms.sym,atoms.pos,atoms.Z)):
        Z = int(Z)
        coords, weights = gen_atomgrid(n_rad,n_ang, symb, Z, func_rad=func_rad,func_ang=func_ang)
        # Shift grid points to atomic coordinate 
        coords = coords + coord
        # Partition 
        # [Becke88] Eq. 13 
        P = gen_grid_partition(atoms,coords)
        # [Becke88] Eq. 22 
        wn = P[ia] * (1./P.sum(axis=0))
        weights = weights * wn
        coords_all.append(coords)
        weights_all.append(weights)
    coords_all = np.vstack(coords_all)
    weights_all = np.hstack(weights_all)
    return coords_all, weights_all


class Grids:
    """
        Grids class 
        Produce a real-space grid 
        (optimal) for Gaussian integrals. 

        Input 
            - atoms: Atoms() 
            - n_rad: int() 
            - n_ang: int() 
    """
    def __init__(self,atoms,n_rad,n_ang,**kwargs):
        """
            __init__ 
            Initialize instance of the class.
        """
        # primary input 
        self.atoms = atoms
        self.n_rad = n_rad
        self.n_ang = n_ang
        # secondary input 
        self._set_kwargs(kwargs)

    def _set_kwargs(self,kwargs):
        """
            _set_kwargs
            Set secondary input. 
        """
        self.func_rad = kwargs.get("func_rad",gauss_chebyshev)
        self.func_ang = kwargs.get("func_ang",Lebedev)

    def _plot(self,C,W):
        """
            _plot 
            Plot the grid. 
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        p = ax.scatter(C[:,0], C[:,1] , C[:,2] , c=W, marker='o')
        plt.colorbar(p)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    def get_grid(self):
        """
            get_grid 
            For all atoms in the system a atomic grid is produced 
            and combined to a system grid (real-space grid). 
        """
        self.coords, self.weights = gen_grid(self.atoms, self.n_rad,self.n_ang,func_rad=self.func_rad,func_ang=self.func_ang)
        return self.coords, self.weights

    def eval(self,basis):
        """
            eval 
            Evaluate basis on grid. 
        """
        bfs = basis.basis
        npts = len(self.coords)
        nbf = len(bfs)
        self.basis_ongrid = np.zeros((npts,nbf))
        for j,bf in enumerate(bfs):
            for i,(coord) in enumerate(self.coords):
                self.basis_ongrid[i,j] = bf.eval(coord)

    def grad(self,basis):
        """
           grad
        """
        bfs = basis.basis
        npts = len(self.coords)
        nbf = len(bfs)
        self.basisgrad_ongrid = np.zeros((npts,nbf,3))
        for j,bf in enumerate(bfs):
            for i,(coord) in enumerate(self.coords):
                self.basisgrad_ongrid[i,j,:] = bf.grad(coord)

    def get_rho(self,D):
        """
            get_rho 
            Get rho(r) from density matrix D
            using the basis evaluated on the grid basis_ongrid. 
        """
        return 2*np.einsum('pI,pJ,IJ->p',self.basis_ongrid,self.basis_ongrid,D)

    def get_grad(self,D):
        """
           get_grad
        """
        
        def bdg(b,d,g):
            """Basis x Density x Gradient matrix multiply."""
            n,m = b.shape
            _bdg = np.zeros((n,3),'d')
            db = np.dot(b,d)
            for j in range(3):
                _bdg[:,j] = abdot(db,g[:,:,j])
            return _bdg

        def abdot(A,B):
            """
            Multiply two n x m matrices together so that the result is a n-length vector
            (i.e. the part over m is accumulated).
            """
            return (A*B).sum(1)
    

        #grho = 2*bdg(self.basis_ongrid,D,self.basisgrad_ongrid) 
        #gamma = None

        #Dx = 2*np.dot(self.basis_ongrid,np.dot(D,self.basisgrad_ongrid[0])) #+ 2*np.dot(self.basisgrad_ongrid[0],np.dot(D,self.basis_ongrid)).T
        #Dy = 2*np.dot(self.basis_ongrid,np.dot(D,self.basisgrad_ongrid[1])) #+ 2*np.dot(self.basisgrad_ongrid[1],np.dot(D,self.basis_ongrid)).T
        #Dz = 2*np.dot(self.basis_ongrid,np.dot(D,self.basisgrad_ongrid[3])) #+ 2*np.dot(self.basisgrad_ongrid[2],np.dot(D,self.basis_ongrid)).T
        #grho = np.array([Dx,Dy,Dz]) 
        #gamma = None  
        nbf = self.basis_ongrid.shape[1]
        npts = len(self.coords)
        grho = np.zeros((npts,3))
        gamma = np.zeros((npts))
        gx = gy = gz = 0
        Dx = np.zeros((npts))
        Dy = np.zeros((npts))
        Dz = np.zeros((npts))
        for i,(coord) in enumerate(self.coords):
            gx = gy = gz = ga = 0
            for j in range(nbf):
                iamp = self.basis_ongrid[i,j] # bfs[i].eval(coord)
                igx,igy,igz = self.basisgrad_ongrid[i,j] #bfs[i].grad(coord)
                for k in range(nbf):
                    jamp = self.basis_ongrid[i,k] #bfs[j].eval(coord)
                    jgx,jgy,jgz = self.basisgrad_ongrid[i,k] #bfs[j].grad(coord)
                    gx += 2*D[j,k]*(iamp*jgx+jamp*igx) # 2 
                    gy += 2*D[j,k]*(iamp*jgy+jamp*igy) # 2 
                    gz += 2*D[j,k]*(iamp*jgz+jamp*igz) # 2 
                    #gx += 1/2*(D[j,k]*jgx+D[k,j]*igx)
                    #gy += 1/2*(D[j,k]*jgy+D[k,j]*igy)
                    #gz += 1/2*(D[j,k]*jgz+D[k,j]*igz)
                    #ga += gx**2 + gy**2 + gz**2
            Dx[i] = gx
            Dy[i] = gy
            Dz[i] = gz
            grho[i,:] = np.array([gx,gy,gz]) 
            #gamma[i] = ga
        gamma = Dx**2 + Dy**2 + Dz**2
        #print(grho)
        #grho2 = np.array([dx,dy,dz]) 
        #assert np.allclose(grho,grho2)
        #print(grho,gamma)
        return grho, gamma 


    def get_sigma(self,grad):
        """
           get_sigma
        """
        return np.linalg.norm(grad,axis=1)**2

