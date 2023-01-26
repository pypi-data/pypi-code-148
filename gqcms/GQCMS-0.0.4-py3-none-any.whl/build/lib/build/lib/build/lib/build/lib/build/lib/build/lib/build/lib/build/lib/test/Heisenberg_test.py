import gqcms
import scipy.linalg as sp


def test_heisenberg():
    # Reference data gathered from
    # Kuijper, D. (2020). Solutions to the one-dimensional Heisenberg model (Bachelor's thesis).
    # Pires, A. S. T. The Heisenberg model.
    # Powell, B. J. (2009). An introduction to effective low-energy Hamiltonians in condensed matter physics and chemistry. arXiv preprint arXiv:0906.1640.

    test_values = []
    test_cases = [2, 4, 6, 8, 10]
    for test_case in test_cases:
        ham = gqcms.heisenberg(test_case).calculateHamiltonian(1, periodic=True)
        check = sp.eigh(ham)[0][0]/test_case
        test_values.append(check)
    
    for place, value in enumerate([-0.75000, -0.50000, -0.46713, -0.45639, -0.45154]):
        assert round(test_values[place], 5) == value, f"Mistake for system with {test_cases[place]} sites. Expected {value} but got {round(test_values[place], 5)}"
    

if __name__ == "__main__":
    test_heisenberg()
    print("All clear")