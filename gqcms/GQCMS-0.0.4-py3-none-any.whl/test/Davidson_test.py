import gqcms


    # reference data generated with the GQCP package
    # https://gqcg.github.io/GQCP/landing-page.html

    # We will test hexatriene, benzene and benzene with a potential applied.
def test_davidson():
    mol = gqcms.Hubbard(6, t=1, U=2, circular=False)

    hexatriene = mol.Hamiltonian()

    mol = gqcms.Hubbard(6, t=1, U=2, circular=True)
    benzene = mol.Hamiltonian()
    mol.AddPotential({0:3})
    ionic = mol.Hamiltonian()

    checklist = [-4.54631, -5.40946, -3.39497]
    for place, molecule in enumerate([hexatriene, benzene, ionic]):
        assert round(gqcms.Davidson(molecule, subspace_size=20, requested_roots=1)["E"][0], 5) == checklist[place], f"Mistake for molecule {place}. Expected {checklist[place]} but got {round(gqcms.FCI(molecule, state=0)['E'][0], 5)}"


if __name__ == "__main__":
    test_davidson()
    print("all clear")