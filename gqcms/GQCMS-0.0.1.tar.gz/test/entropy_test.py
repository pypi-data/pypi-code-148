import gqcms
import numpy as np

def test_entropy():
    # reference data was provided by using the code by drs. Daria Van Hende (github: dariavh)
    S_ref = 1.8022448354652179

    a = gqcms.Hubbard(6, t=1, U=0, circular=True)
    ham = a.Hamiltonian()
    df = gqcms.FCI(ham, states=0)
    wf = df["C"][0]
    S = gqcms.Entropy(wf, a, [0,1])

    assert np.isclose(S, S_ref, 1e-5), f"expected {round(S_ref, 5)} but got {S}"

if __name__ == "__main__":
    test_entropy()
    print("all clear")

    
