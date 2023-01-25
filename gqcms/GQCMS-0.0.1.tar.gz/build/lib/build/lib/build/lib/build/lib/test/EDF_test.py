import gqcms
import numpy as np

def testEDF():
    # test data verified using data from the implementation by drs. Daria Van Hende @ GQCG
    three_site = gqcms.Hubbard(3, 1, 0, circular=False, nalpha=2, nbeta=2)
    wf = gqcms.FCI(three_site.Hamiltonian())

    distribution_function = gqcms.FullEDF(three_site, wf, [[0], [1], [2]])

    checkdict = {(0,2,2):0.0625, (1,1,2):0.25, (1,2,1):0.125, (2,2,0):0.0625, (2,1,1):0.25, (2,0,2):0.25}

    for part in checkdict.keys():
        assert checkdict[part] == np.round(distribution_function[part], 5)
    
    distribution_function = gqcms.FullEDF(three_site, wf, [[0], [1,2]])

    checkdict = {(0,4):0.0625, (1,3):0.375, (2,2):0.5625}

    for part in checkdict.keys():
        assert checkdict[part] == np.round(distribution_function[part], 5)

if __name__ == "__main__":
    testEDF()
    print("All clear")

