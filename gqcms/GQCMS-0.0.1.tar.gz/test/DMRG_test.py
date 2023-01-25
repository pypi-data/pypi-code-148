import gqcms
import numpy as np


def testDMRG():
    # Reference data from James R. Garrison and Ryan V. Mishmash
    # https://simple-dmrg.readthedocs.io/en/latest/01_infinite_system.html
    # https://simple-dmrg.readthedocs.io/en/latest/02_finite_system.html

    test_sytem = gqcms.DMRG(1)
    infinite_energies, entropy, error, entropies_lost_kept, number_list = test_sytem.infinite(5, 4, mute=True)
    check_values = [-0.40401, -0.41560, -0.42148, -0.42540, -0.42771]
    results = np.round(np.array(infinite_energies)/np.array([4, 6, 8, 10, 12]), 5)
    assert np.all(results == check_values), "infinite algorithm is faulty"

    finite_energies, entropy, error, size, env, pop_list = test_sytem.finite(4)
    check_values = [-0.42771, -0.42789, -0.4277, -0.42784, -0.4277, -0.42784, -0.4277, -0.42789, -0.42771, -0.42789, -0.4277, -0.42784, -0.4277, -0.42784, -0.4277, -0.42789, -0.42771] 
    results = np.round(np.array(finite_energies)/12, 5)
    assert np.all(results == check_values), "finite algorithm is faulty"


if __name__ == "__main__":
    testDMRG()
    print("All clear")