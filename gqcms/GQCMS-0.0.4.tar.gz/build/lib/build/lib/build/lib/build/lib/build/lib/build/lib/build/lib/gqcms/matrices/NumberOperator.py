from typing import List
import numpy as np

from . import Determinant


def NumberOperator(sites: list, basis: List[Determinant], balpha: bool =True, bbeta: bool =True, number_of_sites: int = None, N: np.ndarray = None) -> np.ndarray:
    """
    Creates the matrix representation of the number operator in ONV or site basis of
    the given sites.

    :param sites: sites of the number operator can be list or int
    :param basis: list of determinants or string 'site' to create the NumberOperator in site basis
    :param balpha: take alpha electrons into account or not (default is True)
    :param bbeta: take beta electrons into account or not (default is True)
    :param number_of_sites: the number of sites the hubbard system conains, used when basis = 'site' (default is None)
    :param N:

    :returns: diagonnal numpy array of the number operator
    """

    # If basis is 'site', create the Number operator in site basis
    if basis == "site":
        # Raise error if 'number_of_sites' is not specified
        if number_of_sites is None:
            raise ValueError("Please specifiy the number of sites of the Hubbard molecule this operator will act on.")

        matrix = np.zeros((number_of_sites, number_of_sites))

        # Set each diagonal index in 'sites' to one
        for site in sites:
            matrix[site, site] = 1

        # Return operator in site basis
        return matrix

    elif N is not None:
        
        # Create the number operator in the given ONV basis
        matrix = np.zeros((len(basis), len(basis)))

        # Change sites to list if an int is given
        if isinstance(sites, int):
            sites = [sites]

        # Loop for every site
        for site in sites:
            for i, det in enumerate(basis):

                # If a one is present on the position of the given site add a one
                # at this position of the matrix. Check for alpha and beta, so 
                # that spin resolved number operators can be created.
                if det.alpha_onv & (1 << site) and balpha:
                    matrix[i, i] += N[site, site]

                if det.beta_onv & (1 << site) and bbeta:
                    matrix[i, i] += N[site, site]

        return matrix
        
    
    else:
        # Create the number operator in the given ONV basis
        matrix = np.zeros((len(basis), len(basis)))

        # Change sites to list if an int is given
        if isinstance(sites, int):
            sites = [sites]

        # Loop for every site
        for site in sites:
            for i, det in enumerate(basis):

                # If a one is present on the position of the given site add a one
                # at this position of the matrix. Check for alpha and beta, so 
                # that spin resolved number operators can be created.
                if det.alpha_onv & (1 << site) and balpha:
                    matrix[i, i] += 1

                if det.beta_onv & (1 << site) and bbeta:
                    matrix[i, i] += 1

        return matrix

    
def basisTransform(numberOperator, basis: List[Determinant]):
    """
    Transform operator from site basis to given basis
    """
    
    matrix = np.zeros((len(basis), len(basis)))
    
    for i, det_i in enumerate(basis):
        for j, det_j in enumerate(basis[i:], start=i):
            
            # Check if num different orbitals is 1
            if det_i.num_different_orbitals(det_j) == 1:
                
                # Get different orbitals
                diff_orb_i, diff_orb_j, sign = det_i.get_different_orbitals(det_j)
                
                matrix[i, j] += sign*numberOperator[diff_orb_i[0], diff_orb_j[0]]
                matrix[j, i] += matrix[i, j]
    
            # Diagonal elements
            if i == j:
                # Get all orbitals in the ONV
                orbital_list = det_i.get_spin_orbitals()

                for u in orbital_list:
                    matrix[i, i] += numberOperator[u, u]
            
    return matrix