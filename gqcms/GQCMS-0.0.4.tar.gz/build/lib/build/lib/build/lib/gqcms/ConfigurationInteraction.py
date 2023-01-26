import numpy as np
import pandas as pd
from scipy import linalg

from gqcms import HartreeFock
from gqcms import Hubbard
from gqcms import Determinant
from gqcms import createHamiltonianSCI
from gqcms import DensityOperator


def FCI(hamiltonian: np.ndarray, states: tuple = 0) -> pd.DataFrame:
    """
    Computes the energy of a Hamiltonian via exact diagonalization.

    :param hamiltonian: a np.ndarray of a Hamiltonian
    :param state: indicates from which states the output is returned (default is 0 i.e. groundstate)

    :return: pandas DataFrame with the the columns ['E', 'C', '1PDM']
    """

    energies, C = linalg.eigh(hamiltonian)

    if isinstance(states, int):
        states = (states,)

    df_list = []
    # get individual states
    for state in states:
        D = np.outer(C[:, state], C[:, state].T)
        df = pd.DataFrame([(energies[state], C[:, state], D)], columns=["E", "C", "1PDM"])
        # df = pd.Series({"E": energies[state], "C": C[:, state], "1PDM": D})
        df_list.append(df)

    if len(df_list) > 1:
        final_frame = pd.concat(df_list, ignore_index=True, axis=1).T
    else:
        final_frame = df_list[0]
        
    return final_frame


def SCI(
    molecule: Hubbard, 
    excitations: list, 
    result_HF=None,
    maxiter: int = 100, 
    max_size: int = 5,
    bdiis: bool = False,
    bdamping: bool = True,
    bseries: bool = False,
    diis_convergence: float = 1e-2,
    E_convergence: float = 1e-6,
    D_convergence: float = 1e-8,
) -> pd.Series:
    """
    Performs a selected CI calculation with the given excitation degrees of the Hartree-Fock determinant
    
    :param molecule: Hubbard molecule
    :param excitations: list of excitation degrees that are taken into account
    :param result_HF: result of a Hartree-Fock computation
    :param maxiter: max number of iterations the Hartree-Fock algorithm is allowed to take
    :param bdiis: use DIIS or not (default is False)
    :param bdamping: use density damping or not (default is True)
    :param bseries: return a pandas series object or not (default is False)
    :param diss_convergence: min threshold of DIIS needed to stop the algorithm succesfull (default is 1e-2)
    :param E_convergence: min threshold of energy difference to stop the algorithm succesfull (default is 1e-6)
    :param D_convergence: min threshold of in density matrices (default is 1e-8)
    
    :return: pandas DataFrame with the the columns ['E', 'C', '1PDM']
    """
    
    # Convert excitations to list if int is given
    if isinstance(excitations, int):
        excitations = [excitations]
    
    # Perform a Hartree-Fock computation if result_HF is None
    if result_HF is None:
        HF_solver = HartreeFock(molecule, bdiis, bdamping, bseries, max_size, diis_convergence, E_convergence, D_convergence, maxiter)
        result_HF = HF_solver.solve()
            
    # Create Hamiltonian
    H, basis = createHamiltonianSCI(molecule, result_HF, excitations=excitations, return_extra=True)
    
    # Compute energie
    energies, coefficients = linalg.eigh(H)
    
    # Create density matrix in MO basis
    D_mo = DensityOperator(coefficients[:, 0], basis, molecule.sites)
    
    # Compute density matrix in site basis
    D_site = result_HF.C_a @ D_mo @ result_HF.C_a.T
   
    return pd.Series({'E': energies[0], 'C': coefficients[:, 0], '1PDM': np.outer(coefficients[:, 0], coefficients[:, 0].T), 'D_site': D_site})
