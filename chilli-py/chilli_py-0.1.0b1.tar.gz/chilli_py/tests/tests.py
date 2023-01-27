from chilli_py.tests.bench_rhf import test_rhf
from chilli_py.tests.bench_uhf import test_uhf 
from chilli_py.tests.bench_rks import test_rks 
from chilli_py.tests.bench_uks import test_uks
#from chilli_py.tests.bench_dip import test_dip

def main():
    """
        main 
        Check the chilli_py package. 
        Calculate small benchmark sets. 

        Note 
            - not includes all tests 
    """
    test_rhf() 
    test_uhf()
    test_rks() 
    test_uks()
    #test_dip()

if __name__ == '__main__':
    main()

