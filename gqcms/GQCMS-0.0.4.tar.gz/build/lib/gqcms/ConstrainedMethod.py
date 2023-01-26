import numpy as np
import pandas as pd
from scipy import linalg
from typing import List

from gqcms import Hubbard
from gqcms import FCI
from gqcms import HartreeFock
from gqcms import Determinant
from gqcms import createHamiltonianSCI
from gqcms import NumberOperator
from gqcms import DensityOperator
from gqcms import basisTransform


def ConstrainedFCI(molecule: Hubbard, operator: np.ndarray, m: float) -> pd.DataFrame:
    """
    Computes the FCI energy and expectation value of a contrained Hubbard Hamiltonian.

    :param molecule: hubbard class object
    :param m: Lagrange multiplier
    :param operator: matrix representation of the feature operator

    :returns: pandas DataFrame with the the columns
        ['E', 'C', '1PDM', 'mu', 'expectation_value']
    """

    # Create a constrained Hubbard Hamiltonian for a Lagrange multiplier
    contrained_hamiltonian = molecule.ConstrainHamiltonian(m, operator)

    # Compute the energy, wave function and 1PDM
    result = FCI(contrained_hamiltonian)

    # Compute the expectation value of the operator using the 1PDM
    expectation_value = np.einsum("ij,ij", result["1PDM"][0], operator)
    
    D = DensityOperator(result['C'][0], molecule.basis, molecule.sites)

    # Add the Lagrange multiplier and expectation value to the result DataFrame
    result["mu"] = m
    result["expectation_value"] = expectation_value
    result["E"] = result["E"][0] + m * expectation_value
    result["D"] = [D]

    return result


class ConstrainedHartreeFock(HartreeFock):
    """
    Hartree Fock solver for the Hubbard model with a constraint
    on the Hamiltonian matrices using the feature operator
    """

    def __init__(
        self,
        system: Hubbard,
        operator: np.ndarray,
        m: float,
        bdiis: bool = False,
        bdamping: bool = True,
        bseries: bool = False,
        max_size: int = None,
        diis_convergence: float = 1e-2,
        E_convergence: float = 1e-4,
        D_convergence: float = 1e-8,
        maxiter: int = 200,
    ):
        """
        Initialize a constrained Hubbard Hartree-Fock solver

        :param system: the Hubbard system used in the SCF algoritm
        :param operator: feature operator used to constrain the Hamiltonians
        :param m: Lagrange multiplier
        :param bdiis: use DIIS or not (default is False)
        :param bdamping: use density damping or not (default is True)
        :param bseries: return a pandas series instead of HubbardEnvironment (default is False)
        :param max_size: maximum size of the DIIS queue, if None queue is infinite (default is None)
        :param diss_convergence: min threshold of DIIS needed to stop the algorithm succesfull
        :param E_convergence: min threshold of energy difference to stop the algorithm succesfull
        :param maxiter: maximum number of iterations allowed if threshold is not reached
        """

        super().__init__(
            system, bdiis, bdamping, bseries, max_size, diis_convergence, E_convergence, D_convergence, maxiter
        )

        # Add Lagrange multiplier and feature operator to environment
        self._env.m = m
        self._env.mod = operator

        # Insert the constrain functions
        self._steps.insert(1, self.constrainHamiltonians)
        self._steps.append(self.expectationValue)

    def constrainHamiltonians(self):
        """
        Constrain the Hamiltonians using the mod matrix
        """

        self._env.H_a -= self._env.m * self._env.mod
        self._env.H_b -= self._env.m * self._env.mod

    def expectationValue(self):
        """
        Compute the expectation value of the feature operator
        """

        self._env.expectationValue = np.einsum(
            "ij,ij", self._env.D_a + self._env.D_b, self._env.mod
        )

    def solve(self):
        """
        Overwrite default solve method to return a pandas Series
        """

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
                "mu": self._env.m,
                "expectation_value": self._env.expectationValue,
            }
        )


def ConstrainedSCI(
    molecule: Hubbard,
    operator: np.ndarray,
    m: float,
    excitations: list = None,
    basis: list = None,
    result_HF = None,
    bdiis: bool = False,
    bdamping: bool = True,
    bseries: bool = False,
    max_size: int = None,
    diis_convergence: float = 1e-2,
    E_convergence: float = 1e-6,
    D_convergence: float = 1e-8,
    maxiter: int = 200,
) -> pd.Series:
    """
    Performs a constrained selected CI calculation with the given excitation degrees of the Hartree-Fock determinant

    :param molecule: Hubbard molecule
    :param operator: feature operator used in the constraint
    :param m: Lagrange multiplier
    :param excitations: list of excitation degrees that are taken into account
    :param basis: list of Determinants
    :param result_HF: result of a Hartree-Fock computation
    :param bdiis: use DIIS or not (default is False)
    :param bdamping: use density damping or not (default is True)
    :param bseries: return a pandas series object or not (default is False)
    :param max_size: max queue size of DIIS (default is None)
    :param diss_convergence: min threshold of DIIS needed to stop the algorithm succesfull (default is 1e-2)
    :param E_convergence: min threshold of energy difference to stop the algorithm succesfull (default is 1e-6)
    :param D_convergence: min threshold of in density matrices (default is 1e-8)
    :param maxiter: maximum number of iterations allowed if threshold is not reached (default is 200)

    :return: pandas DataFrame with the the columns ['E', 'C', '1PDM']
    """

    # Perform a Hartree-Fock computation if result_HF is None
    if result_HF is None:
        HF_solver = HartreeFock(molecule, bdiis, bdamping, bseries, max_size, diis_convergence, E_convergence, D_convergence, maxiter)
        result_HF = HF_solver.solve()
        
    # Create SCI Hamiltonian and coefficient matrix
    if basis is not None:
        H, det_list = createHamiltonianSCI(molecule, result_HF, basis=basis, return_extra=True)
    elif excitations is not None:
        
        # Convert excitations to list if int is given
        if isinstance(excitations, int):
            excitations = [excitations]
            
        H, det_list = createHamiltonianSCI(molecule, result_HF, excitations=excitations, return_extra=True)
    else:
        raise ValueError("A list of excitations or determinants should be given.")
    
    operator_mo_a = np.einsum("uj,vi,uv", result_HF.C_a, result_HF.C_a, operator)
    operator_mo_b = np.einsum("uj,vi,uv", result_HF.C_b, result_HF.C_b, operator)
    
    # Spin block operator
    operator_mo = np.zeros((2*molecule.sites, 2*molecule.sites))
    operator_mo[::2, ::2] = operator_mo_a
    operator_mo[1::2, 1::2] = operator_mo_b
    
    # Transform operator to CI basis
    nr_op_onv_mo = basisTransform(operator_mo, det_list)

    # Compute energie
    energies, C_sci = linalg.eigh(H - m*nr_op_onv_mo)
    
    # Compute density matrix in ONV basis
    D_onv = np.outer(C_sci[:, 0], C_sci[:, 0])

    # Compute density matrix in HF-MO basis
    D_mo = DensityOperator(C_sci[:, 0], det_list, molecule.sites)

    # Compute density matrix in site basis
    D_site =result_HF.C_a @ D_mo @ result_HF.C_a.T
    # D_site = C @ D_mo @ C.T
    
    # Compute population in site basis
    # expectation_value = np.einsum("ij,ij", D_site, np.diag(np.repeat(np.diagonal(operator), 2)))
    expectation_value = np.einsum("ij,ij", D_site, operator)

    return pd.Series(
        {
            "E": energies[0] + m*expectation_value,
            "C": C_sci[:, 0],
            "D_site": D_site,
            "D_mo": D_mo,
            "mu": m,
            "expectation_value": expectation_value,
        }
    )
