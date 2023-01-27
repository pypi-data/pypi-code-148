from chilli_py.tests import bench_rhf
from chilli_py.tests import bench_uhf 
from chilli_py.tests import bench_rks 
from chilli_py.tests import bench_uks

def main():
    """
        main 
        Check the chilli_py package for ESP manuscript. 
        Calculate small benchmark sets with 
            - chilli_py 
            - chilli_cpp 
            - chilli_jl 

        Note 
            - not includes all tests 
            - you need chilli_cpp and chilli_jl installed 
            - run the script with python-jl instead of python3 
    """
    s0 = "DISCLAIMER"
    s1 = "You need to have installed \nchilli_cpp and chilli_jl \nto run this script."
    s2 = "You need to run this with python-jl."
    print(f"{s0} \n {s1} \n {s2}")
    bench_rhf.test_rhf(use_ref=True,
                       run_chilli_cpp=bench_rhf.run_chilli_cpp,
                       run_chilli_jl=bench_rhf.run_chilli_jl)
    bench_uhf.test_uhf(use_ref=True,
                       run_chilli_cpp=bench_uhf.run_chilli_cpp,
                       run_chilli_jl=bench_uhf.run_chilli_jl)
    bench_rks.test_rks(use_ref=True,
                       run_chilli_cpp=bench_rks.run_chilli_cpp,
                       run_chilli_jl=bench_rks.run_chilli_jl)
    bench_uks.test_uks(use_ref=True,
                       run_chilli_cpp=bench_uks.run_chilli_cpp,
                       run_chilli_jl=bench_uks.run_chilli_jl)

if __name__ == '__main__':
    main()

