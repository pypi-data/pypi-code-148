import numpy as np
import scipy.linalg as sp

class heisenberg():
    def __init__(self, sites, S=0.5):
        """
        Will initialize the Heisenberg object
        sites: the amount of sites
        S: the total spin per site
        """

        self.sites = sites
        self.S = S
        self.degeneracy = int(2*S + 1)
        
        self.spinops = np.array([[0, 0.5], [0.5, 0]]), np.array([[0, -0.5j], [0.5j, 0]]), np.array([[0.5, 0], [0, -0.5]])
        self.raising = self.spinops[0] + 1j*self.spinops[1]
        self.lowering = self.spinops[0] - 1j*self.spinops[1]

    def calculateHamiltonian(self, J, periodic=True):
        """
        Will calculate the Heisenberg Hamiltonian with a given coupling constant
        J: the coupling constant
        """

        total_ham = np.zeros((2**self.sites, 2**self.sites))
          
        for site in range(self.sites - 1 + periodic):
                # reset button for when the site is adapted
                reset = site
                S_z_site = np.kron(np.eye(2**(site)), np.kron(self.spinops[2], np.eye(2**(self.sites - site - 1))))
                if site + 1 == self.sites:
                    site = -1
                S_z_nextdoor = np.kron(np.eye(2**(site + 1)), np.kron(self.spinops[2], np.eye(2**(self.sites - site - 2))))

                site = reset
                S_minus_site = np.kron(np.eye(2**(site)), np.kron(self.lowering, np.eye(2**(self.sites - site - 1))))
                if site + 1 == self.sites:
                    site = -1
                S_minus_nextdoor = np.kron(np.eye(2**(site + 1)), np.kron(self.lowering, np.eye(2**(self.sites - site -2))))

                site = reset
                S_plus_site = np.kron(np.eye(2**(site)), np.kron(self.raising, np.eye(2**(self.sites - site - 1))))
                if site + 1 == self.sites:
                    site = -1
                S_plus_nextdoor = np.kron(np.eye(2**(site + 1)), np.kron(self.raising, np.eye(2**(self.sites - site - 2))))  
                              
                total_ham = total_ham + S_z_site@S_z_nextdoor + 0.5*S_plus_site@S_minus_nextdoor + 0.5*S_minus_site@S_plus_nextdoor
        
        return total_ham*J

