import numpy as np 

class BasisSetParams:
    """
        BasisSetParams class
        Basisset parameters for one species. 
       
        Input 
            - Nsyms
            - syms
            - Ncontr
            - expns
            - coeffs

        e.g., H : Basisdata 
    """
    def __init__(self, Nsyms, syms, Ncontr, expns, coeffs): 
        """
            __init__
            Initialize instance of class. 
        """
        self.Nsyms = Nsyms 
        self.syms = syms
        self.Ncontr = Ncontr 
        self.expns = expns 
        self.coeffs = coeffs 

    def __repr__(self):
        """
            __repr__
            Representation of an instance of the class. 
        """
        s = f'Nsyms : {self.Nsyms} \n'
        s += f'syms: {self.syms} \n'
        s += f'Ncontr : {self.Ncontr} \n'
        s += f'expns : {self.expns} \n'
        s += f'coeffs : {self.coeffs} \n'
        return s  

def read_species(filename): 
    """
        read_species         
        Read species in blocks, i.e., 

            Block start: "*****"
                Species data 
            Block end: "*****"

        Input 
            - filename: str(), file name
    """
    f = open(filename, "r")
    s = f.read()
    f.close() 
    ll = s.split("****")
    return ll 

def read_basis_set_g94(fname):
    """
        read_basis_set_g94
        Read basis set data in GAUSSIAN94 (g94) format. 

        Input 
            - fname: plain-textfile, containing a g94 basis set. 

        Output 
            - BasisSetData: {"species_name": BasisSetData, },  contains BasisSetData for all species 
    """
    slines = read_species(fname)
    BasisSetData = {}
    for l in slines:
        if not ( (l == "\n") or (l == "") ):
            key, value = read_species_basisdata(l)
            BasisSetData[key] = value 
        else:
            continue    
    return BasisSetData

def calc_Nsyms(lines):
    """
        calc_Nsyms 

        Input 
            - lines 
    """
    ls = lines.split("\n")
    # start from line 2
    il = 1  
    Nsyms = 0
    while il< len(ls)-1:
        il += 1 
        tmp = ls[il].split()
        if len(tmp) > 1: 
            sym_read  = tmp[0]
            if sym_read in ["SP","S","P","D","F"]:
                if sym_read == "SP":
                    Nsyms = Nsyms + 2
                    il = il + int(tmp[1])
                elif (sym_read == "S") or  (sym_read == "P") or (sym_read == "D") or (sym_read == "F"): 
                    Nsyms = Nsyms + 1
                    il = il + int(tmp[1])
            else:
                print("Unknown sym_read: ", sym_read)
                break 
    return Nsyms

def read_species_basisdata(lines): 
    """
        read_species_basisdata
        Within a species block, 
        determine basisdata for that species.  

        Input 
            - lines 

        Needs 
            - calc_Nsym
    """
    Nsyms = calc_Nsyms(lines)
    ls = lines.split("\n")
    # start from line 2
    atsymb = ls[1].split()[0]
    il = 1
    
    Ncontr = np.empty(Nsyms,dtype=int)
    syms = np.empty(Nsyms,dtype=str)
    expns = []  
    coeffs = [] 
    
    isym = 0

    while il < len(ls)-2:
        
        il = il + 1
        sym_read = ls[il].split()[0] 
        ncontr = int(ls[il].split()[1]) 
        # SP 
        if sym_read == "SP":
            expn = np.zeros(ncontr)
            coeff_s = np.zeros(ncontr)
            coeff_p = np.zeros(ncontr)
            
            for i in range(ncontr):
                il = il + 1 # don't forget to increament index for line
                expn[i] = float(ls[il].split()[0])
                coeff_s[i] = float(ls[il].split()[1])
                coeff_p[i] = float(ls[il].split()[2])
            
            # S 
            isym = isym + 1 
            syms[isym-1] = "S"
            Ncontr[isym-1] = ncontr
            expns.append(expn[:])
            coeffs.append(coeff_s[:])
        
            # P 
            isym = isym + 1  
            syms[isym-1] = "P"
            Ncontr[isym-1] = ncontr
            expns.append(expn[:])
            coeffs.append(coeff_p[:])

        else:
            # other than sym_read == "SP"

            expn = np.zeros(ncontr)
            coeff = np.zeros(ncontr)
            
            for i in range(ncontr):
                il = il + 1 # don't forget to increament index for line
                expn[i] = float(ls[il].split()[0])
                coeff[i] = float(ls[il].split()[1])
            
            isym = isym + 1
            syms[isym-1] = sym_read
            Ncontr[isym-1] = ncontr
            expns.append(expn[:])
            coeffs.append(coeff[:])
    expns = np.array(expns,dtype=object) 
    coeffs = np.array(coeffs,dtype=object) 
    return atsymb, BasisSetParams(Nsyms, syms, Ncontr, expns, coeffs)

def main():
    """
        main
        Test functionality of this routine. 
    """
    from chilli_py import BasisSet 
    basis = read_basis_set_g94(BasisSet._full_path("sto-3g"))
    print(basis['Te']) 

if __name__ == '__main__': 
    main() 
