import basis_set_exchange as bse 

def gen_basis(basis_name,elements=None,f_name=None):
    """
        gen_basis 
        Generate basisset in Gaussian94 format (slighly adjusted)
            - no basis set exchange header 
            - add "****" at the 1st line 
            - no empty line at the end of the file

        Input 
            - basis_name: str(), basis set name 
            - elements: None or list(), e.g., ["H","He"]

        Notes
            - this script needs the python basis_set_exchange package installed 
    """
    if f_name is None: 
        f_name = basis_name 
    # Standard all elements in the basisset 
    if elements is None: 
        a = bse.get_basis(basis_name,
                          fmt='gaussian94',
                          header=False)
    if elements is not None: 
        a = bse.get_basis(basis_name,
                          elements=elements,
                          fmt='gaussian94',
                          header=False)
    # Proposed by KT needs to be tested 
    a = a.replace("D+","E+")
    a = a.replace("D-","E-")
    f = open(f_name,"w") 
    f.write("****\n")
    f.writelines(a) 
    f.close() 

def main(basis_name,elements=None,f_name=None):
    """
        main 
        Main function to test this routine.
    """
    gen_basis(basis_name=basis_name,elements=elements,f_name=f_name)

if __name__ == "__main__": 
    main(basis_name="pc-1",f_name="pc-1") 
