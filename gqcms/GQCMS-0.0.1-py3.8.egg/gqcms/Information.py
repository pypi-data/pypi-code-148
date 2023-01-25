import numpy as np
import pandas as pd

import gqcms


def CoefficientMatrix(
    hubbard: gqcms.Hubbard, state: np.ndarray, system_sites: list
) -> np.ndarray:
    """
    Create the coefficient matrix that expresses the wave function in the two subsystems

    :param hubbard: a hubbard class object
    :param state: wave function coefficient vector
    :param system_sites: sites where the entropy is computed for can be list or int
    """

    # Change system_sites to list if int is given
    if isinstance(system_sites, int):
        system_sites = [system_sites]

    # Create a zero coefficient matrix of dimentions 4**A x 4**B
    # where A are the system_sites and B all other sites. A power of four is
    # taken, because one site has four possible configurations i.e empty, alpha, beta, alpha and bet.
    C = np.zeros((4 ** len(system_sites), 4 ** (hubbard.sites - len(system_sites))))

    for i, onv_i in enumerate(hubbard.basis):

        bitstring_alpha = bin(onv_i.alpha_onv)[2:].rjust(hubbard.sites, "0")[::-1]
        bitstring_beta = bin(onv_i.beta_onv)[2:].rjust(hubbard.sites, "0")[::-1]

        indices = tuple(
            "".join(index) for index in zip(bitstring_alpha, bitstring_beta)
        )

        sys_index = int("".join([indices[sys_site] for sys_site in system_sites]), 2)
        env_index = int(
            "".join(
                indices[site]
                for site in range(hubbard.sites)
                if site not in system_sites
            ),
            2,
        )

        C[sys_index, env_index] = onv_i.get_sign(system_sites, system_sites) * state[i]

    return C


def Entropy(state: np.ndarray, hubbard: gqcms.Hubbard, system_sites: list) -> float:
    """
    Computes Von Neumann entropy of the given state at the given site(s)

    :param state: the state used for the entropy computation
    :param hubbard: a hubbard class object
    :param system_sites: sites where the entropy needs to be computed from
    """

    C = CoefficientMatrix(hubbard, state, system_sites)
    # Compute the reduced density matrix
    rdm_sys = np.einsum("ij,kj->ik", C, C, optimize=True)

    # Compute the eigenvalues of the reduced density matrix
    eigvals = np.linalg.eigvalsh(rdm_sys)
    # Compute the natural log of the eigenvalues and remove the NAN values
    ln_eigvals = np.log(eigvals)
    valid_values = np.where(~np.isnan(ln_eigvals) & np.isfinite(ln_eigvals))
    # Finally compute the Von Neumann entropy
    S = -np.sum((eigvals * ln_eigvals)[valid_values])

    return S


def EntropyFromDataFrame(df: pd.DataFrame, hubbard: gqcms.Hubbard, system_sites: list) -> None:
    """
    Compute the Von Neumann entropy at the given site(s) for all rows in the given dataframe.
    The dataframe must contain a column named 'C'.

    :param df: pandas dataframe with a column named 'C'
    :param hubbard: a hubbard class object
    :param system_sites: sites where the entropy needs to be computed from
    """

    if isinstance(system_sites, int):
        system_sites = [system_sites]

    sites_str = "".join(str(site) for site in system_sites)

    df[f"S{sites_str}"] = df['C'].apply(
        Entropy, hubbard=hubbard, system_sites=system_sites
    )


def MutualInformation(
    state: np.ndarray, hubbard: gqcms.Hubbard, site_p: int, site_q: int
) -> float:
    """
    Computes the mutual information of site p and q from a Hubbard computation

    :param state: the state used for the entropy computation
    :param hubbard: a hubbard class object
    :param site_p: site index
    :param site_q: site index
    """

    # If sites p and q are equal, the mutual information is zero
    if site_p == site_q:
        return 0

    return 0.5 * (
        Entropy(state, hubbard, site_p)
        + Entropy(state, hubbard, site_q)
        - Entropy(state, hubbard, [site_p, site_q])
    )


def MutualInformationFromDataFrame(df, hubbard, site_p, site_q):

    df[f"I{site_p}{site_q}"] = df['C'].apply(
        MutualInformation, hubbard=hubbard, site_p=site_p, site_q=site_q
    )