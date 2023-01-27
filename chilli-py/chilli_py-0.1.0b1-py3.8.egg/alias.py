import numpy as np 
from scipy.special import factorial, factorial2
from scipy.special import comb 
from scipy.special import gamma

""" Short forms for mathematical functions """ 

def norm(inp):
    """
        norm 
        Short form for norm. 
    """
    return np.linalg.norm(inp)

def dist2(inp):
    """
        dist2 
        The function dist2 returns the 
        squared distance of inp. 
    """
    return np.linalg.norm(inp)**2 

def binomial(N,k):
    """
        binomial
        Binomial coefficient
    """
    return comb(N, k, exact=True)

def div(a,b):
    """
        div 
        (q,r) = div(a,b) 
        Here q is quotient and r the remainder. 
        This function returns q. 
    """
    return divmod(a,b)[0]

def lgamma(x): 
    """
        lgamma 
        Log(gamma(x) function. 
        Accurate log(gamma(x)) for large x

        import math 
        math.lgamma(x) 

        is the same 
    """
    return np.log(gamma(x))

def ortho(S):
    """
        Cholesky orthogonalization
    """
    return np.linalg.inv(np.linalg.cholesky(S)).T

