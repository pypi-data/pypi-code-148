import numpy as np
import pandas as pd
import scipy.linalg as sp


def generateUnitVectors(amount: int, dim: int) -> np.ndarray:
    """
    Generate the specified amount of unit vectors.
    :param amount: amount of unit vectors needed
    :param dim: the dimension of the hamiltonian

    returns the selected unit vectors
    """
    total_space = np.eye(dim)
    subspace = total_space[:, :amount]
    return subspace


def orthogonalizer(basis_vectors: np.ndarray, voi: np.ndarray) -> np.ndarray:
    """
    Orthogonalizes one vector with respect to a set of other vectors

    :param basis_vectors: the basis
    :param voi: the vector that needs to be orthogonalized
    """
    for vector in range(basis_vectors.shape[1]):
        prefactor = basis_vectors[:, vector].T @ voi
        for number, element in enumerate(voi):
            voi[number] -= prefactor * basis_vectors[number, vector]
    return voi


def normalizer(vector: np.ndarray) -> np.ndarray:
    """
    Normalizes a vector

    :param vector: the vector to normalize
    """
    norm = np.sqrt(vector.T @ vector)
    return vector / norm


def expandBasis(
    basis_vectors: np.ndarray, correction_vector: np.ndarray, criterion: float = 1e-3
) -> np.ndarray:
    """
    Checks if the subspace needs to be expanded by a single given vector

    :param basis_vectors: the first set of basis vectros
    :param correction_vector: the vector to add to the basis
    :param criterion: the treshold for adding a vector to the set
    """
    # first normalize
    vector = normalizer(correction_vector)

    # then orthogonalize
    orthogonal = orthogonalizer(basis_vectors, correction_vector)

    # then check if the norm is large enough
    # If the norm is large, the vector contains a lot of information
    # not yet in the basis, so include it.
    if np.linalg.norm(orthogonal) > criterion:
        orthogonal = normalizer(orthogonal)
        basis_vectors = np.c_[basis_vectors, orthogonal]

    return basis_vectors


def Davidson(
    operator: np.ndarray,
    subspace_size: int,
    requested_roots: int = 1,
    treshhold: float = 1e-3,
    maxiter: int = 100,
) -> np.ndarray:
    """
    The Davidson Liu diagonalization algorithm

    :param operator: the operator that needs to be diagonalized
    :param subspace size: the amount of initial guess vectors
    :param requested_roots: the amount of solutions needed, default = 1
    :param treshhold: the threshold for inclusion, default 1e-3
    """

    # step 1-- generate subspace
    V = generateUnitVectors(subspace_size, operator.shape[0])
    diagonals = np.diagonal(operator)
    keepgoing = True
    itercount = 0
    # start iterations
    while keepgoing and (itercount <= maxiter):
        # step 2 -- construct the subspace matrix
        S = V.T @ operator @ V
        # step 3 -- diagonalize the subspace matrix
        E, Z = sp.eigh(S)
        # sort E
        order = E.argsort()
        E_sorted = E[order]
        C_sorted = Z[:, order]
        # step 4 -- construct the current estimates
        X = V @ C_sorted

        old_size = V.shape[1]
        for vector in range(subspace_size):
            # step 5 -- calculate the residuals
            r = (operator - E[vector] * np.eye(operator.shape[0])) @ X[:, vector]
            denoms = E_sorted[vector] - diagonals
            delta = r / denoms
            # step 6 -- expand subspace
            V = expandBasis(V, delta, treshhold)
        new_size = V.shape[1]

        if new_size == old_size:
            keepgoing = False
        itercount += 1

    if (itercount >= maxiter) and keepgoing:
        print(f"maximum iteration reached without converging")

    df_list = []

    for state in range(requested_roots):
        D = np.outer(X[:, state], X[:, state].T)
        df = pd.DataFrame(
            [(E_sorted[state], X[:, state], D)], columns=["E", "C", "1PDM"]
        )
        df_list.append(df)

    final_frame = pd.concat(df_list, axis=0, ignore_index=True, join="outer")
    return final_frame
