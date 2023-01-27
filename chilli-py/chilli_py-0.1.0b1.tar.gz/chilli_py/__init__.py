""" 

chilli_py 
------
| This is a pure Python self-consistent field code utilizing
| Gaussian-type orbitals (GTOs).
| Thus you will find only source code written
| in this package in Python and no other language.
|
| by Sebastian Schwalbe and Kai Trepte 

How to use
----------

    >>> from chilli_py import simple_run
    >>> simple_run.run("H2","RHF")

"""
from chilli_py.atoms import Atoms 
from chilli_py.BasisSet import BasisSet 
from chilli_py.grids import Grids 
from chilli_py.RHF import RHF 
from chilli_py.RKS import RKS 
__all__ = ['Atoms','BasisSet','Grids','RHF','RKS']
