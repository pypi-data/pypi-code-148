import math
import numpy as np
import matplotlib.pyplot as plt

def utility(α):
    """
    Return a CRRA utility function parametrized by `α` 
    
    """
    if α == 1.:
        return lambda consumption: np.log(consumption)
    else: 
        return lambda consumption: consumption ** (1 - α) / (1 - α)
def main():
    a=utility(0.2)
    print(a(199))
if __name__ == '__main__':
    main()