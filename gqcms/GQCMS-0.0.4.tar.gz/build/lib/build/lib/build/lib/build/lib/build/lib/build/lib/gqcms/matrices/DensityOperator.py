import numpy as np


def DensityOperator(C: np.ndarray, basis: list, nmo: int) -> np.ndarray:
    """
    Create the density matrix in ONV basis
    
    :param C: coefficient vector
    :param basis: list of gqcms.Determinants representing the ONV basis
    :param nmo: number of molecular orbitals
    """
    
    # Initialize zero matrix
    D = np.zeros(shape=(nmo, nmo))
    
    # Loop through the basis
    for i, det_i in enumerate(basis):
        for j, det_j in enumerate(basis):
            
            number_different_orbitals = det_i.num_different_orbitals(det_j)
            
            # Check if the number of different orbitals is zero or one
            if number_different_orbitals == 0:
                
                # If no different orbitals, only diagonal elements
                for u in det_i.get_spin_orbitals():
                    D[u//2, u//2] += C[i]*C[i]
                    
            elif number_different_orbitals == 1:
                
                # If one different orbital, indices are the different orbitals
                diff_1, diff_2, sign = det_i.get_different_orbitals(det_j)

                for u in diff_1:
                    for v in diff_2:                        
                        D[u//2, v//2] += sign*C[i]*C[j]
        
    return D