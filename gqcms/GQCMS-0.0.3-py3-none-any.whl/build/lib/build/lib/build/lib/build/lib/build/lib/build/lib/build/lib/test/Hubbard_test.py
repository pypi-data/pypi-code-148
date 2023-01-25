import gqcms
import numpy as np

# test if Hubbard class calculates correct Hamiltonian
def test_Hubbard():
    # reference data for the 2-site Hamiltonian from https://doi.org/10.48550/arXiv.0807.4878
    ref = np.array([[2, -1, -1, 0], [-1, 0, 0, -1], [-1, 0, 0, -1], [0, -1, -1, 2]])

    a = gqcms.Hubbard(sites=2, t=1, U=2, circular=False)
    assert np.all(
        a.Hamiltonian() == ref
    ), f"wrong hamiltonian. expected {ref} but got {a.Hamiltonian()}"


if __name__ == "__main__":
    test_Hubbard()
    print("all clear")
