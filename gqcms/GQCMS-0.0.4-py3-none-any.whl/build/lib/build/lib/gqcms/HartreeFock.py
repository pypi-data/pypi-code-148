from dataclasses import dataclass, field
from scipy import linalg
import numpy as np
import pandas as pd
from collections import deque

from gqcms import Hubbard
from .General import IterativeAlgorithm, DIIS


@dataclass
class HubbardEnvironment:
    """
    Class that stores variables used during Hubbard Hartree-Fock algorithm
    """

    # Constants
    DIIS_CONVERGENCE: float = 1e-4
    E_CONVERGENCE: float = 1e-6
    D_CONVERGENCE: float = 1e-4
    MAXITER: int = 100

    # Algorithm status values
    bconverged: bool = field(init=False, default=False)
    iteration: int = field(init=False, default=0)

    # Energy
    E_old: float = field(init=False, default=np.inf)
    E: float = field(init=False, default_factory=float)
    
    # Density damping
    damping = 0.5
    D_a_queue: deque = field(init=False, default=None)
    D_b_queue: deque = field(init=False, default=None)

    # Matrices
    H_a: np.ndarray = field(init=False, default=None)
    H_b: np.ndarray = field(init=False, default=None)
    D_a: np.ndarray = field(init=False, default=None)
    prev_D_a: np.ndarray = field(init=False, default=None)
    D_b: np.ndarray = field(init=False, default=None)
    prev_D_b: np.ndarray = field(init=False, default=None)
    prev_D_spin_block: np.ndarray = field(init=False, default=None)
    C_a: np.ndarray = field(init=False, default=None)
    C_b: np.ndarray = field(init=False, default=None)
    site_potentials: np.ndarray = field(init=False, default=None)

    
class HubbardDiis(DIIS):
    """
    Implementation of the abstract classes of the general DIIS class for 
    the Hubbard model
    """

    def check_convergence(self):
        # self._env.errVec[:self._env.system.sites**2] = np.reshape(self._env.H_a @ self._env.D_a - self._env.D_a @ self._env.H_a, self._env.system.sites**2)
        # self._env.errVec[self._env.system.sites**2:] = np.reshape(self._env.H_b @ self._env.D_b - self._env.D_b @ self._env.H_b, self._env.system.sites**2)
        # self._env.err = np.linalg.norm(self._env.errVec)
        
        self._env.delta_D_a = np.sqrt(np.einsum('ij->', np.square(self._env.D_a - self._env.prev_D_a)))
        self._env.delta_D_b = np.sqrt(np.einsum('ij->', np.square(self._env.D_b - self._env.prev_D_b)))
        
        # self._env.delta_D_spin_block = np.sqrt(np.einsum('ij->', np.square(self._env.D_spin_block - self._env.prev_D_spin_block)))
        
        self._env.bconverged = np.abs(self._env.E - self._env.E_old) <= self._env.E_CONVERGENCE \
                and self._env.delta_D_a <= self._env.D_CONVERGENCE \
                and self._env.delta_D_b <= self._env.D_CONVERGENCE \
                and np.abs(self._env.rmsd_H_a < self._env.DIIS_CONVERGENCE) \
                and np.abs(self._env.rmsd_H_b < self._env.DIIS_CONVERGENCE) \
                # and self._env.err <= self._env.E_CONVERGENCE


    def compute_residual(self):
        
        if 'alpha' in self._P_string:
            return self._env.H_a @ self._env.D_a - self._env.D_a @ self._env.H_a
        else:
            return self._env.H_b @ self._env.D_b - self._env.D_b @ self._env.H_b 
    

class HartreeFock(IterativeAlgorithm):
    """
    Hartree-Fock solver for the Hubbard model.
    Use the .solve() function to run the algorithm
    """

    def __init__(
        self,
        system: Hubbard,
        bdiis: bool = False,
        bdamping: bool = True,
        bseries: bool = False, 
        max_size: int = None,
        diis_convergence: float = 1e-2,
        E_convergence: float = 1e-6,
        D_convergence: float = 1e-4,
        maxiter: int = 500
    ):
        """
        Initialize a Hubbard Hartree-Fock solver

        :param system: the Hubbard system used in the HF algoritm
        :param bdiis: use DIIS or not (default is False)
        :param bdamping: use density damping or not (default is True)
        :param bseries: return a pandas series object or not (default is False)
        :param max_size: queue size of DIIS (default is None, i.e. infinite)
        :param E_convergence: convergence threshold of energy (default is 1e-6)
        :param D_convergence: convergence threshold of density (default is 1e-4)
        :param maxiter: maximum number of iterations allowed (default is 500)
        """

        # Initialize environment
        self._env = HubbardEnvironment(diis_convergence, E_convergence, D_convergence, maxiter)
        self._env.system = system
        self.bseries = bseries
        
        # init density queue
        self._env.D_a_queue = deque(maxlen=2)
        self._env.D_b_queue = deque(maxlen=2)

        # Create the hopping_matrix
        self._env.hopping_matrix = -self._env.system.t * self._env.system.adj_mat
        
        # Create site potentials matrix
        self._env.site_potentials = np.zeros((system.sites, system.sites))
        
        # # error of commutator [F, D] to check convergence
        # self._env.errVec = np.zeros(2*system.sites**2)
    
        for site, potential in system.potential.items():
            self._env.site_potentials[site, site] = potential

        init_steps = [self.guess, self.updateDensity]

        if bdiis:
            # Init DIIS
            self.diis_a = HubbardDiis(self._env, "H_a", max_size)
            self.diis_b = HubbardDiis(self._env, "H_b", max_size)

            if bdamping:
                steps = [
                    self.updateHamiltonians,
                    self.diis_a.diis_step,
                    self.diis_b.diis_step,
                    self.updateCoefficients,
                    self.updateDensity,
                    self.densityDamping,
                    self.updateEnergy,
                ]
            else:
                steps = [
                    self.updateHamiltonians,
                    self.diis_a.diis_step,
                    self.diis_b.diis_step,
                    self.updateCoefficients,
                    self.updateDensity,
                    self.updateEnergy,
                ]

        else:
            if bdamping:
                steps = [
                    self.updateHamiltonians,
                    self.updateCoefficients,
                    self.updateDensity,
                    self.densityDamping,
                    self.updateEnergy,
                    self.checkConvergence,
                ]
            else:
                steps = [
                    self.updateHamiltonians,
                    self.updateCoefficients,
                    self.updateDensity,
                    self.updateEnergy,
                    self.checkConvergence,
                ]                

        super().__init__(self._env, init_steps, steps)
        
    
        
    @property
    def env(self):
        return self._env
    
    @env.setter
    def env(self, name_value):
        name, value = name_value
        
        setattr(self._env, name, value)

    def guess(self):
        """
        Create density matrices from a first guess
        """

        # Create a guess coefficient matrix where the even sum of indices is one
        # for C_a and the odd sum of indices is one for C_b
        self._env.C_a = np.zeros((self._env.system.sites, self._env.system.sites))
        self._env.C_b = np.zeros((self._env.system.sites, self._env.system.sites))

        for i in range(self._env.system.sites):
            for j in range(self._env.system.sites):
                if (i + j) % 2 == 0:
                    self._env.C_a[i, j] = 1
                else:
                    self._env.C_b[i, j] = 1

    def updateHamiltonians(self):
        """
        Create alpha and beta Hamiltonian
        """

        self._env.H_a = np.copy(self._env.hopping_matrix)
        self._env.H_b = np.copy(self._env.hopping_matrix)
        
        for i in range(self._env.system.sites):
            # self._env.H_a[i, i] += self._env.system.U * self._env.D_b[i, i] * (1 - self._env.D_a[i, i])
            # self._env.H_b[i, i] += self._env.system.U * self._env.D_a[i, i] * (1 - self._env.D_b[i, i])
            self._env.H_a[i, i] += self._env.system.U * self._env.D_b[i, i]
            self._env.H_b[i, i] += self._env.system.U * self._env.D_a[i, i]

    def updateCoefficients(self):
        """
        Diagonalize the Hamiltonians to get energies and coefficient matrix
        """
        
        self._env.eps_a, self._env.C_a = np.linalg.eigh(self._env.H_a + self._env.site_potentials)
        self._env.eps_b, self._env.C_b = np.linalg.eigh(self._env.H_b + self._env.site_potentials)
        
        # Sort eigenvalues
        sort_indices = np.argsort(self._env.eps_a.real)
        self.env.C_a = self.env.C_a[:, sort_indices]
        
        sort_indices = np.argsort(self._env.eps_b.real)
        self._env.C_b = self._env.C_b[:, sort_indices]
        

    def updateDensity(self):
        """
        Compute alpha and beta density matrices
        """
        
        # Store previous density matrix to check convergence criteria
        if self._env.D_a is None:
            self._env.prev_D_a = np.zeros((self._env.system.sites, self._env.system.sites))
            self._env.prev_D_b = np.zeros((self._env.system.sites, self._env.system.sites))
            # self._env.prev_D_spin_block = np.zeros((2*self._env.system.sites, 2*self._env.system.sites))
        else:
            self._env.prev_D_a = np.copy(self._env.D_a)
            self._env.prev_D_b = np.copy(self._env.D_b)
            # self._env.D_prev_spin_block = np.copy(self._env.D_spin_block)
        
        self._env.D_a = (
            self._env.C_a[:, : self._env.system.nalpha]
            @ self._env.C_a[:, : self._env.system.nalpha].T
        )
        self._env.D_b = (
            self._env.C_b[:, : self._env.system.nbeta]
            @ self._env.C_b[:, : self._env.system.nbeta].T
        )
        
        # Spin block density matrices 
        # self._env.D_spin_block = np.block([
        #     [self._env.D_a, np.zeros_like(self._env.D_b)],
        #     [np.zeros_like(self._env.D_a), self._env.D_b]
        # ])
        
        # self._env.D_spin_block = np.block([
        #     [self._env.prev_D_a, np.zeros_like(self._env.prev_D_b)],
        #     [np.zeros_like(self._env.prev_D_a), self._env.prev_D_b]
        # ])
        
    def densityDamping(self):
        """
        Use density damping to control convergence
        """

        # Store density matrices in queue
        self._env.D_a_queue.append(self._env.D_a)
        self._env.D_b_queue.append(self._env.D_b)

        # Perform damping if queue is filled
        if len(self._env.D_a_queue) == 2:
            self._env.D_a = self._env.damping*self._env.D_a_queue[0] + (1 - self._env.damping)*self._env.D_a_queue[1]
            self._env.D_b = self._env.damping*self._env.D_b_queue[0] + (1 - self._env.damping)*self._env.D_b_queue[1]

    def updateEnergy(self):
        """
        Compute SCF energy
        """
        
        self._env.E_old = self._env.E

        self._env.E = np.trace(
            self._env.hopping_matrix @ (self._env.D_a + self._env.D_b)
        ) + self._env.system.U * (np.diag(self._env.D_a) @ np.diag(self._env.D_b))

    def checkConvergence(self):
        """
        Check convergence criteria
        """
        
        # Check convergence via the commutator [F, D]
        # self._env.errVec[:self._env.system.sites**2] = np.reshape(self._env.H_a @ self._env.D_a - self._env.D_a @ self._env.H_a, self._env.system.sites**2)
        # self._env.errVec[self._env.system.sites**2:] = np.reshape(self._env.H_b @ self._env.D_b - self._env.D_b @ self._env.H_b, self._env.system.sites**2)
        # self._env.err = np.linalg.norm(self._env.errVec)
        
        # Density convergence
        self._env.delta_D_a = np.sqrt(np.einsum('ij->', np.square(self._env.D_a - self._env.prev_D_a)))
        self._env.delta_D_b = np.sqrt(np.einsum('ij->', np.square(self._env.D_b - self._env.prev_D_b)))
        # self._env.delta_D_spin_block = np.sqrt(np.einsum('ij->', np.square(self._env.D_spin_block - self._env.prev_D_spin_block)))
        
        self._env.bconverged = (
            np.abs(self._env.E_old - self._env.E) < self._env.E_CONVERGENCE \
                and self._env.delta_D_a <= self._env.D_CONVERGENCE \
                and self._env.delta_D_b <= self._env.D_CONVERGENCE \
                # and self._env.err <= self._env.E_CONVERGENCE
                # and self._env.delta_D_spin_block <= self._env.D_CONVERGENCE
        )

        
    def solve(self):
        """
        Overwrite default solve method to return a pandas Series
        """
        
        if self.bseries:
            super().solve()
                
            return pd.Series(
                {
                    "iterations": self._env.iteration,
                    "E": self._env.E,
                    "C_a": self._env.C_a,
                    "C_b": self._env.C_b,
                    "eps_a": self._env.eps_a,
                    "eps_b": self._env.eps_b,
                    "D_a": self._env.D_a,
                    "D_b": self._env.D_b,
                }
            )
        else:
            return super().solve()