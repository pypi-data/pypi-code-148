import numpy as np

import gqcms


def test_fci():
    
    mol1 = gqcms.Hubbard(6, t=1, U=2, circular=False)
    mol2 = gqcms.Hubbard(4, t=1, U=1, circular=False)
    mol3 = gqcms.Hubbard(4, t=0.01, U=2, nalpha=1, nbeta=1, circular=False)

    for i, molecule in enumerate([mol1, mol2, mol3]):
        
        # Compute exact energy via exact diagonalization
        E_ed = gqcms.FCI(molecule.Hamiltonian()).E
        # Compute FCI energy via Hartree-Fock reference
        E_fci_hf = gqcms.SCI(molecule, range(1, molecule.nalpha+molecule.nbeta+1)).E
        
        assert np.isclose(E_ed, E_fci_hf), f"Mistake for molecule {i}. Expected {E_ed} but got {E_sci}"

        
def test_constrained_fci():
    
    sys = gqcms.Hubbard(2, t=1, U=1, circular=False)
    nr_op_site = gqcms.NumberOperator([0], 'site', number_of_sites=sys.sites)
    nr_op_fci = gqcms.NumberOperator([0], sys.basis)
    
    # Perform constrained FCI via HF
    result_fci_hf = gqcms.ConstrainedSCI(sys, nr_op_site, 1, excitations=[1, 2])
    
    # Perform constrained FCI via ED
    result_ed = gqcms.ConstrainedFCI(sys, nr_op_fci, 1)
    
    assert np.isclose(result_fci_hf['E'], result_ed['E'][0]), f"Expected {result_ed['E']} but got {result_fci_hf['E'][0]}" 
    assert np.allclose(result_fci_hf['D_site'], result_ed['D'][0]), f"Expected {result_ed['D']} but got {result_fci_hf['D_site'][0]}"
    
        
        
if __name__ == "__main__":
    test_fci()
    print("all clear")
