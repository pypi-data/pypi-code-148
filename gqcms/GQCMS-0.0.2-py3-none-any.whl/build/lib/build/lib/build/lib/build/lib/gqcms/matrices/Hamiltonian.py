import numpy as np
from typing import List

from gqcms import Hubbard
from gqcms.matrices import Determinant


def createHamiltonian(H_core: np.ndarray, I: np.ndarray, determinants: list) -> np.ndarray:
    """
    Create the hamiltonian matrix from a list of determinants

    :param H_core: core Hamiltonian i.e one electron integrals
    :param I: two electron integrals
    :param determinants: list of Determinants objects
    """

    H = np.zeros((len(determinants), len(determinants)))

    # Make use of the fact that H is hermitian and calculate only the 
    # upper traingle
    for i, det_i in enumerate(determinants):
        for j, det_j in enumerate(determinants[i:], start=i):
    
            # Compute how many orbitals are different
            num_diff_orbitals = det_i.num_different_orbitals(det_j)
    
            output = 0
    
            if num_diff_orbitals == 0:
                # Get all orbitals in the ONV
                orbital_list = det_i.get_spin_orbitals()
                
                # One electron integrals
                for u in orbital_list:
                    output += H_core[u, u]
            
                # Two electron integrals
                for k, p in enumerate(orbital_list):
                    for q in orbital_list[k+1:]:
                        output += I[p, q, p, q]
            
            elif num_diff_orbitals == 1:
                # Get different orbitals and sign
                diff_spin_orb_i, diff_spin_orb_j, sign = det_i.get_different_orbitals(det_j)
                # print(f"i: {i}\t{diff_spin_orb_i}\t j: {j}\t{diff_spin_orb_j}")
                
                # One electron term
                output += H_core[diff_spin_orb_i[0],
                                       diff_spin_orb_j[0]]
                # Two electron terms
                for p in det_i.get_spin_orbitals():
                    if p != diff_spin_orb_i[0]:
                        output += I[p, diff_spin_orb_i[0],
                                          p, diff_spin_orb_j[0]]
                output *= sign
            
            elif num_diff_orbitals == 2:
                # Get different orbitals and sign
                diff_spin_orb_i, diff_spin_orb_j, sign = det_i.get_different_orbitals(det_j)
            
                output += sign * \
                        I[diff_spin_orb_i[0], diff_spin_orb_i[1],
                            diff_spin_orb_j[0], diff_spin_orb_j[1]]
            
            # H is hermitian
            H[i, j] = output
            H[j, i] = H[i, j]

    return H


def createHamiltonianSCI(molecule: Hubbard, result_HF, excitations: List[int] = None, basis=None, return_extra=False) -> np.ndarray:
    """
    Create the selected configration interaction (SCI) Hamiltonian
    
    :param molecule: information of the Hubbard system
    :param excitations: list of the selected excitations
    :param result_HF: result of an HF calculation
    :param return_extra: return the spin block coefficient matrix and CI basis or not (default is False)
    """

    # Create one electron intergral matrix
    H_core_ao = -molecule.t*molecule.adj_mat + np.diag([molecule.potential.get(site, 0) for site in range(molecule.sites)])

#     # Transform H_core to HF-MO basis
#     H_core_mo_a = np.einsum('uj,vi,uv', result_HF.C_a, result_HF.C_a, H_core_ao)
#     H_core_mo_b = np.einsum('uj,vi,uv', result_HF.C_b, result_HF.C_b, H_core_ao)

#     # Spin block H_core_mo
#     H_core_mo = np.zeros((2*molecule.sites, 2*molecule.sites))
#     H_core_mo[::2, ::2] = H_core_mo_a
#     H_core_mo[1::2, 1::2] = H_core_mo_b
    
    # Create spin block coefficient matrix and sort
    C = np.block([
        [result_HF.C_a, np.zeros_like(result_HF.C_b)],
        [np.zeros_like(result_HF.C_a), result_HF.C_b]
    ])

    # Spin block H_core in AO basis
    H_core_ao_spin_block = np.block([
        [H_core_ao, np.zeros_like(H_core_ao)],
        [np.zeros_like(H_core_ao), H_core_ao]
    ])
    
    # Transform H_core from AO to HF-MO basis
    H_core_mo = C.T @ H_core_ao_spin_block @ C
    
    # Sort C and H_core_mo to align with the electron repulsion tenor indices
    sort_indices = np.asarray([p for pair in zip(range(0, molecule.sites), range(molecule.sites, 2*molecule.sites)) for p in pair])
    C = C[:, sort_indices]
    
    H_core_mo = H_core_mo[:, sort_indices]
    H_core_mo = H_core_mo[sort_indices, :]
    
    # Create electron repulsion integrals (eri) tensor
    eri_ao = np.zeros((molecule.sites, molecule.sites, molecule.sites, molecule.sites))
    for site in range(molecule.sites):
        eri_ao[site, site, site, site] = molecule.U

    # Spin block eri
    I = np.eye(2)
    eri_spin_block_ao = np.kron(I, eri_ao)
    eri_spin_block_ao = np.kron(I, eri_spin_block_ao.T)

    # Convert to physicist's notation and antisymmetrize
    eri_spin_block_ao_phys = eri_spin_block_ao.transpose(0, 2, 1, 3)
    gao = eri_spin_block_ao_phys - eri_spin_block_ao_phys.transpose(0, 1, 3, 2)

    # Transform gao from AO to MO basis
    temp = np.einsum('pi,pqrs->iqrs', C, gao)
    temp = np.einsum('qj,iqrs->ijrs', C, temp)
    temp = np.einsum('ijrs,rk->ijks', temp, C)
    eri_mo = np.einsum('ijks,sl->ijkl', temp, C)
    
    if excitations is not None:
        # Generate requested excitations
        det_ref = Determinant(nalpha=molecule.nalpha, nbeta=molecule.nbeta, sites=molecule.sites)
        basis = [det_ref]

        for excitation in excitations:
            basis.extend(det_ref.n_tuply_excitations(excitation, molecule.sites))
    
    # Check if a basis is given, else return error
    elif basis is None:
        raise ValueError("A list of excitations or a list of determinants should be given.")

    # Create Hamiltonian in ONV basis
    H_onv = createHamiltonian(H_core_mo, eri_mo, basis)
    
    # Return basis if asked
    if return_extra:
        return H_onv, basis
    else:
        return H_onv
