import numpy as np 
from chilli_py.bench import H2 #, H2O 
from chilli_py.atoms import Atoms
from chilli_py.constants import ANG2BOHR

def H2O():
    """
        H2O 
        The water molecule (H2O)
        Atoms + FODs 
    """
    sym_nuc = ["O"] + 2 * ["H"]
    sym_fod =  5 * ["X"]
    p0 = [+0.00000000, +0.00000000, +0.11730000]
    p1 = [+0.00000000, +0.75720000, -0.46920000]
    p2 = [+0.00000000, -0.75720000, -0.46920000]
    p3 = [+0.10000000, +0.00000000, +0.11730000]
    p4 = [+0.00000000, +0.64362000, -0.38122500]
    p5 = [+0.00000000, -0.64362000, -0.38122500]
    p6 = [+0.44297121, +0.00000000, +0.56027121]
    p7 = [-0.44297121, +0.00000000, +0.56027121]
    pos_nuc = np.array([p0, p1, p2])*ANG2BOHR
    pos_fod = np.array([p3, p4, p5, p6, p7])*ANG2BOHR
    charge = 0
    spin = 0
    atoms = Atoms(sym_nuc, pos_nuc, spin=spin, charge=charge)
    fods = Atoms(sym_fod, pos_fod)
    return atoms, fods

class LJ: 
    def __init__(self,atoms,sigma,epsilon):
        self.atoms = atoms 
        self.sigma = sigma 
        self.epsilon = epsilon

    def kernel(self,atoms=None):
        if atoms == None: 
            atoms = self.atoms 
        natoms = len(atoms.pos) 
        pos = atoms.pos 

        rc = 3.*self.sigma 
        rc2 = rc**2. 
        sigma_div_rc = self.sigma/rc
        e0 = 4. * self.epsilon * (sigma_div_rc**12. - sigma_div_rc**6.) 
        #print(f"e0 : {e0}") 
        forces = np.zeros((natoms,3))
        Etot = 0. 
        for i in range(0,natoms): 
            for j in range(i+1,natoms): 
                dr = pos[i] - pos[j]
                #print(f"dr : {dr}")
                r2 = np.linalg.norm(dr)**2. 
                #print(f"r2 : {r2}") 
                if r2 <= rc2: 
                    c6 = (self.sigma**2./r2)**3.
                    Etot -= e0 
                    c12 = c6**2.
                    #print(f"c6: {c6} \n c12: {c12}")
                    Etot += 4.* self.epsilon * (c12 - c6) 

                    forces_scalar = -24. * self.epsilon * (2. * c12 - c6) / r2 
                    forces[i,:] -= forces_scalar * dr 
                    forces[j,:] += forces_scalar * dr 
        return Etot, forces

def get_fmax(f):
    """
        get_fmax
        Get maximal force component
    """
    print((f**2).sum(axis=1))
    fmax = np.sqrt((f**2).sum(axis=1).max())
    return fmax


def main(): 
    atoms, fods = H2O() 
    lj = LJ(atoms,sigma=2,epsilon=11.) 
    Etot, forces = lj.kernel() 
    print(f"Etot : {Etot} \n forces: {forces}") 
    get_fmax(forces)
if __name__ == "__main__": 
    main() 
