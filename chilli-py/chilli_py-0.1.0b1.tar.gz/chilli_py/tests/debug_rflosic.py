import numpy as np 
from chilli_py.RFLOSIC_simple import FLOSIC 
from chilli_py.bench import H2, Ne, H2O, CH4, COH2 

def run():  
    # atoms, fods = H2()
    #atoms, fods = Ne() 
    #atoms, fods = H2O()
    atoms, fods = CH4() 
    #atoms, fods = COH2() 
    # fods.pos[0] += np.array([0,0,0.1])

    # SCF: FLOSIC1 
    mflo = FLOSIC(atoms,
                  fods,
                  xc_name="LDA,PW",
                  #basis_name="sto-3g",
                  basis_name="pc-0",
                  scf_type="FLOSIC2",
                  opt_method="BFGS",
                  maxiter=300,
                  gtol=0.0005)
    mflo.verbose = 4 
    mflo.kernel()

if __name__ == "__main__": 
    run()
