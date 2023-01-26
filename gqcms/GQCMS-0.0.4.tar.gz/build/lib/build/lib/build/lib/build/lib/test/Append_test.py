import gqcms
import numpy as np


    # reference data generated with the GQCP package
    # https://gqcg.github.io/GQCP/landing-page.html

    # We will test hexatriene, benzene and benzene with a potential applied.
    # It is obvious that it does not make a difference whether the molecules
    # are made by appending pieces together or that they are defined as is
def test_append():
    
    # test energy of model systems
    part_1 = gqcms.Hubbard(4, 1, 2, circular=False)
    part_2 = gqcms.Hubbard(2, 1, 2, circular=False)
    part_1.Append(part_2, {3:0})
    hexatriene = part_1.Hamiltonian()

    part_1 = gqcms.Hubbard(4, 1, 2, circular=False)
    part_2 = gqcms.Hubbard(2, 1, 2, circular=False)
    part_1.Append(part_2, {3:0, 0:1})
    benzene = part_1.Hamiltonian()
    
    part_1 = gqcms.Hubbard(4, 1, 2, circular=False)
    part_2 = gqcms.Hubbard(2, 1, 2, circular=False)
    part_2.AddPotential({1:3})
    part_1.Append(part_2, {3:0, 0:1})
    ionic = part_1.Hamiltonian()

    checklist = [-4.54631, -5.40946, -3.39497]
    for place, molecule in enumerate([hexatriene, benzene, ionic]):
        assert round(gqcms.FCI(molecule, states=0)["E"][0], 5) == checklist[place], f"Mistake for molecule {place}. Expected {checklist[place]} but got {round(gqcms.FCI(molecule, state=0)['E'][0], 5)}"

    # test if mirroring changes the final product
    part_1 = gqcms.Hubbard(4, 1, 2, circular=False)
    part_2 = gqcms.Hubbard(2, 1, 2, circular=False)
    part_2.Append(part_1, {1:0})
    mirrored = part_2.Hamiltonian()

    assert round(gqcms.FCI(hexatriene, states=0)["E"][0], 5) == round(gqcms.FCI(mirrored, states=0)["E"][0], 5), f"Mirror images do not have the same energy"


if __name__ == "__main__":
    test_append()
    print("all clear")
