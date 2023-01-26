from matplotlib.pyplot import fill
import numpy as np
import scipy.linalg as sp
from gqcms.matrices import Determinant
from typing import List


class Hubbard:
    def __init__(
        self,
        sites: int,
        t: float,
        U: float,
        circular: bool,
        nalpha: int = None,
        nbeta: int = None,
        basis: List[Determinant] = None
    ) -> None:
        """
        Initializes Hubbard object. For even number of sites, the number of
        alpha and beta electrons are, by default, both equal to half of the number of sites.
        If an odd number of sites is specified, then alpha has one more electron
        than beta electrons by default.

        input:
        :param sites: the amount of sites
        :param t: the hopping parameter
        :param U: the on site repulsion
        :param circular: True if molecule is cyclic
        :param nalpha: the amount of alpha electrons (default is None)
        :param nbeta: the amount of beta electrons (default is None)
        """

        self.sites = sites
        self.nalpha = sites // 2 + sites % 2 if nalpha is None else nalpha
        self.nbeta = sites // 2 if nalpha is None else nbeta
        # cannot have more electrons than twice the amount of sites
        assert self.nalpha + self.nbeta <= self.sites * 2, "to many electrons in system"
        self.U = U
        self.t = t
        self.circular = circular

        # initialize adjacency matrix
        adj_list = np.zeros(sites)

        if sites != 1:
            # assume every site has only two neighbours to start -> Append method to make branched chains
            adj_list[1] = 1
            adj_list[-1] = 1

            adj_mat = sp.circulant(adj_list)

        else:
            adj_mat = np.zeros(1)
        
        if not self.circular and self.sites > 2:
            adj_mat[0, -1] = 0
            adj_mat[-1, 0] = 0

        self.adj_mat = adj_mat
        self.basis = basis if basis is not None else Determinant(nalpha=self.nalpha, nbeta=self.nbeta, sites=self.sites).all_excitations(
            self.sites
        )
        self.basis_dict = {onv: i for i, onv in enumerate(self.basis)}

        # Compute hopping and onSiteRepulsion matrices
        self.hoppingMatrix = self.HoppingMatrix()
        self.onSiteRepulsionMatrix = self.OnSiteRepulsion()

        # potentials can be added using the ApplyPotential method
        self.potential = {}

    def AddPotential(self, pot_dict: dict) -> None:
        """
        Applies a potential to _specific sites

        :param pot_dict: dictionary containing the potential for each site {site, int: potential, float}
            negative potentials are favourable

        IMPORTANT: site numbers are zero indexed
        """
        self.potential.update(pot_dict)

    def ResetPotential(self) -> None:
        """
        Resets the potential
        """
        self.potential = {}

    def HoppingMatrix(self) -> np.ndarray:
        """
        Will generate the hopping part of the Hubbard Hamiltonian.
        """
        # We will gradually fill up this matrix with the hopping parameter t
        dimension = len(self.basis)
        fillmatrix = np.zeros((dimension, dimension))

        for det1 in self.basis:
            # There is only overlap between determinants that differ in only 1 orbital, i.e. single excitations
            hopped_dets = det1.single_excitations(self.sites)

            for det2 in hopped_dets:
                
                if det2 not in self.basis_dict.keys():
                    continue
                
                unique1, unique2, sign = det1.get_different_orbitals(det2)

                i = self.basis_dict[det1]
                j = self.basis_dict[det2]
                
                # we are only looking at singlet excitations excitations happened either in alpha of beta, never in both
                # the sites will always both contain an even or an odd number where even numbers are alphas and odd numbers are betas
                # so unique[0] // 2 will always represent the site number
                fillmatrix[i, j] = (
                    -self.t * sign * self.adj_mat[unique1[0] // 2, unique2[0] // 2]
                )

        return fillmatrix

    def OnSiteRepulsion(self) -> np.ndarray:
        """
        Will calculate the operator for the on site repulsion
        """
        # initialize repulsionlist, which will store all repulsion terms
        repulsionlist = []

        # loop over all determinants
        for det in self.basis:
            # collect bitstrings that show orbital occupation
            alpha = det._alpha_onv
            beta = det._beta_onv

            # Get doubly occupied orbitals using bitwise and, where alpha and beta are both true, we need a one
            double_occ = alpha & beta

            repulsion = 0
            while double_occ:
                # will keep score of the amount of times we encounter a doubly occupied orbital
                if double_occ & 1 == 1:
                    # add one U for every pair found
                    repulsion += self.U
                double_occ >>= 1
            repulsionlist.append(repulsion)

        # the on site repulsion part of the hamiltonian is diagonal.
        return np.diag(repulsionlist)

    def ApplyPotential(self, basis=None) -> np.ndarray:
        """
        Will apply potential for the ionic Hubbard model
        """
        if basis is None:
            basis = self.basis
        
        # since only the diagonal will be affected, we will again work with a list and np.diag
        potentialsList = [0] * len(basis)
        # First check every potential that needs to be applied
        for site in self.potential:
            assert site < self.sites, "applying potential to non-existent site"
            for index, det in enumerate(basis):
                # Get bitstring representation of current determinant
                alpha, beta = det._alpha_onv, det._beta_onv

                # if there is an alpha electron there, add potential
                if alpha & (1 << site):
                    potentialsList[index] += self.potential[site]

                # same for beta
                if beta & (1 << site):
                    potentialsList[index] += self.potential[site]

        return np.diag(potentialsList)

    def ConstrainHamiltonian(self, m, operator) -> None:
        return self.Hamiltonian() - m * operator

    def NewAdjacency(self, substituent, linking_sites: dict):
        """
        Creates a new adjacency matrix based on the added substituent

        :param substituent: another Hubbard molecule
        :param linking_site: tells you what sites of the old chain need to be linked to what sites of the new chain.
        => maps the old -> new

        NOTICE: sites are zero indexed
        """
        # Extend the adjacency matrix
        adj_1, adj_2 = self.adj_mat, substituent.adj_mat
        sites_1, sites_2 = self.sites, substituent.sites

        interaction_matrix = np.zeros((sites_1, sites_2))

        for old_site, new_site in linking_sites.items():
            interaction_matrix[old_site, new_site] = 1
        
        new_adj_mat = np.block(
            [[adj_1, interaction_matrix], [interaction_matrix.T, adj_2]]
        )

        self.adj_mat = new_adj_mat

    def NewBasis(self, substituent):
        """
        Will create a new basis by including the substituents sites

        :param substituent: another Hubbard molecule
        """
        sites_1, sites_2 = self.sites, substituent.sites
        alpha_1, beta_1 = self.nalpha, self.nbeta
        alpha_2, beta_2 = substituent.nalpha, substituent.nbeta
        test_det = Determinant(
            nalpha=alpha_1 + alpha_2, nbeta=beta_1 + beta_2, sites=sites_1 + sites_2
        )
        new_basis = test_det.all_excitations(nmo=test_det.sites)

        self.basis = new_basis

    def Append(self, substituent, linking_sites: dict) -> None:
        """
        Will add a new part to the molecule

        :param substituent: another Hubbard molecule
        :param linking_sites: tells you what sites of the old chain need to be linked to what sites of the new chain.
        => maps the old -> new

        NOTICE: sites are zero indexed
        """
        # extend the adjacency matrix
        self.NewAdjacency(substituent, linking_sites)

        # merge two bases
        self.NewBasis(substituent)

        # set a correct potential pattern
        new_potentials = {
            site + self.sites: potential
            for site, potential in substituent.potential.items()
        }
        self.AddPotential(new_potentials)

        # update class fields
        self.sites += substituent.sites
        self.nalpha += substituent.nalpha
        self.nbeta += substituent.nbeta
        self.basis_dict = {onv: i for i, onv in enumerate(self.basis)}

        # create new hopping matrix and on-site repulsion matrix
        self.hoppingMatrix = self.HoppingMatrix()
        self.onSiteRepulsionMatrix = self.OnSiteRepulsion()

    def Hamiltonian(self) -> np.ndarray:
        """
        Returns the Hubbard Hamiltonian
        """
        return self.onSiteRepulsionMatrix + self.hoppingMatrix + self.ApplyPotential()

    def ApplyTiltedPotential(self, increment: float) -> None:
        """
        Applies a tilted potential to the sites

        :param increment: the increment by which the potential increases
        """
        # resetting potential for pure tilted model, modifications to the tilted pattern need to be made afterwards via AddPotential
        self.ResetPotential()
        self.potential = {i: i * increment for i in range(self.sites)}
