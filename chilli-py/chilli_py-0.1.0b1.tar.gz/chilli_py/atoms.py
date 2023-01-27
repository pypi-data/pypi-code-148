import numpy as np 
from chilli_py.constants import ANG2BOHR

class Atoms:
    """
        Atoms class
        Contains variables describing the system. 

        Input
            - sym: list(str), chemical symbols 
            - pos: list(list(3,), positions 
            - spin: int(), spin of the system 
            - charge: int(), charge of the system 
    """
    def __init__(self,sym,pos,spin=0,charge=0):
        """
            __init__
            Initialize class instance. 
        """
        # Chemical symbols 
        self.sym = sym
        # Positions 
        self.pos = np.array(pos)
        # Spin 
        self.spin = spin 
        # Charge 
        self.charge = charge
        self.Z, self.Nelec = self._get_Z_and_Nelec()
        self.Natoms = len(self.sym) 
        self.Species = list(set(self.sym))
        self.Nspecies = len(self.Species)
        # Center 
        self.center = self._get_center() 

    def _get_Z_and_Nelec(self): 
        """
            _get_Z_and_Nelec
            Determine get Z values from chemical symbols sym. 
            Calculate the number of electrons Nelec. 
        """
        Z = np.zeros(len(self.sym)) 
        Nelec = 0
        for isp,sym in enumerate(self.sym): 
            z = int(ZATOMS[sym])
            Z[isp] = z 
            Nelec += z 
        return Z, Nelec 

    def _center(self):
        """
            _center
            Calculate geometric center of system. 
        """
        return self.pos.sum(axis=0)/self.Natoms

    def _center_of_charge(self): 
        """
            _center_of_charge
            Calculate center of charge.
        """
        cx = sum([Z*pos[0] for Z,pos in zip(self.Z,self.pos)])
        cy = sum([Z*pos[1] for Z,pos in zip(self.Z,self.pos)])
        cz = sum([Z*pos[2] for Z,pos in zip(self.Z,self.pos)])
        coc = np.array([cx,cy,cz])
        coc /= sum(self.Z)
        return coc

    def _get_center(self,typ="coc"):
        """
            _get_center 
            Calculate center of the system.
            
            Input 
                - typ: str(), "coc" center of charge 
        """
        if typ == "center":
            center = _center()
        if typ == "coc":
            center = self._center_of_charge()
        return center 


    def show(self): 
        """
            show 
            Show the representation 
            of a class instance. 
        """
        print(self.__repr__) 

    def __repr__(self): 
        """
            __repr__
            Representation of 
            a class instance. 
        """
        s = "-----"
        s += "\n"
        s += "Atoms"
        s += "\n"
        s += "-----" 
        s += "\n"
        s += f"Natoms   = {self.Natoms: 5d}"
        s += "\n"
        s += f"Nelec    = {self.Nelec: 5d}"
        s += "\n"
        s += f"Nspecies = {self.Nspecies: 5d}"
        s += "\n"
        for isp in range(self.Nspecies):
            s += f"Species {isp}: sym: {self.Species[isp]} Z: {int(ZATOMS[self.Species[isp]])}"
            s += "\n"
        s += "Coordinates in bohr:"
        s += "\n"
        for ia in range(self.Natoms):
            s += f"{self.sym[ia]} {self.pos[ia][0]:+18.10f} {self.pos[ia][1]:+18.10f} {self.pos[ia][2]:+18.10f}"
            s += "\n"
        return s 

    def __len__(self):
        return len(self.sym)

# Species name to species number 
ZATOMS = {
        # FODs
        "X"   :  1,
        "Z"   :  1,
        # Nuclei  
        "H"   :  1,
        "He"  :  2,
        "Li"  :  3,
        "Be"  :  4,
        "B"   :  5,
        "C"   :  6,
        "N"   :  7,
        "O"   :  8,
        "F"   :  9,
        "Ne"  :  10,
        "Na"  :  11,
        "Mg"  :  12,
        "Al"  :  13,
        "Si"  :  14,
        "P"   :  15,
        "S"   :  16,
        "Cl"  :  17,
        "Ar"  :  18,
        "K"   :  19,
        "Ca"  :  20,
        "Sc"  :  21,
        "Ti"  :  22,
        "V"   :  23,
        "Cr"  :  24,
        "Mn"  :  25,
        "Fe"  :  26,
        "Co"  :  27,
        "Ni"  :  28,
        "Cu"  :  29,
        "Zn"  :  30,
        "Ga"  :  31,
        "Ge"  :  32,
        "As"  :  33,
        "Se"  :  34,
        "Br"  :  35,
        "Kr"  :  36,
        "Rb"  :  37,
        "Sr"  :  38,
        "Y"   :  39,
        "Zr"  :  40,
        "Nb"  :  41,
        "Mo"  :  42,
        "Tc"  :  43,
        "Ru"  :  44,
        "Rh"  :  45,
        "Pd"  :  46,
        "Ag"  :  47,
        "Cd"  :  48,
        "In"  :  49,
        "Sn"  :  50,
        "Sb"  :  51,
        "Te"  :  52,
        "I"   :  53,
        "Xe"  :  54
}


def atoms_from_xyz(f_xyz,spin=0,charge=0):
    """
        atoms_from_xyz
        Initialize atoms object from xyz file. 
        It is assumed that xyz contain 
        the positions in [Angstroem]. 
        The routine converts the position 
        from the input [Angstroem]
        to the code units [Bohr]. 

        Input
            - f_xyz, str(), path to xyz file 
            - spin, int(), spin of the system 
            - charge, int(), charge of the system 
    """
    f = open(f_xyz, "r")
    ll = f.readlines()
    f.close() 
    Natoms = int(ll[0].split()[0])
    pos = np.zeros((Natoms,3),dtype=float)
    sym = np.zeros((Natoms),dtype=object) 
    
    for l in range(2,len(ll)): 
        tmp = ll[l].split()
        sym[l-2]= tmp[0]
        pos[l-2]= [float(tmp[1]), float(tmp[2]), float(tmp[3])]
    
    # Convert positions from [Angstroem] to [Bohr] 
    pos = np.array(pos)*ANG2BOHR
    atoms = Atoms(sym,pos,spin=spin,charge=charge) 
    return atoms 

def main():
    """
        main 
        Main function testing the routine. 
    """
    atoms = Atoms(['H','Li'],[[0,0,0],[1.4,0,0]])
    print(atoms)

if __name__ == '__main__': 
    main() 
