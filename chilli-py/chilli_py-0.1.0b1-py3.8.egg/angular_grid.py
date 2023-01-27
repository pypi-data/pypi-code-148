import numpy as np 

""" Angular grids """

# Reference
# ---------
#   - [1] https://github.com/gabrielelanaro/pyquante/blob/master/Data/lebedev_write.py
#
# DOC string from pyquante: 
# 
# C version: Dmitri Laikov
# F77 version: Christoph van Wuellen, http://www.ccl.net
# Python version: Richard P. Muller, 2002.
# Python chilli_py: S. Schwalbe, K. Trepte 2021
#   + switch from math to numpy 
#   + added doc strings 
# 
# This subroutine is part of a set of subroutines that generate
# Lebedev grids [1-6] for integration on a sphere. The original 
# C-code [1] was kindly provided by Dr. Dmitri N. Laikov and 
# translated into fortran by Dr. Christoph van Wuellen.
# This subroutine was translated from C to fortran77 by hand.
#
# Users of this code are asked to include reference [1] in their
# publications, and in the user- and programmers-manuals 
# describing their codes.
# 
#   [1] V.I. Lebedev, and D.N. Laikov
#       'A quadrature formula for the sphere of the 131st
#        algebraic order of accuracy'
#       Doklady Mathematics, Vol. 59, No. 3, 1999, pp. 477-481.
#
#   [2] V.I. Lebedev
#       'A quadrature formula for the sphere of 59th algebraic
#        order of accuracy'
#       Russian Acad. Sci. Dokl. Math., Vol. 50, 1995, pp. 283-286. 
#
#   [3] V.I. Lebedev, and A.L. Skorokhodov
#       'Quadrature formulas of orders 41, 47, and 53 for the sphere'
#       Russian Acad. Sci. Dokl. Math., Vol. 45, 1992, pp. 587-592. 
#
#   [4] V.I. Lebedev
#       'Spherical quadrature formulas exact to orders 25-29'
#       Siberian Mathematical Journal, Vol. 18, 1977, pp. 99-107. 
#
#   [5] V.I. Lebedev
#       'Quadratures on a sphere'
#       Computational Mathematics and Mathematical Physics, Vol. 16,
#       1976, pp. 10-24. 
#
#   [6] V.I. Lebedev
#       'Values of the nodes and weights of ninth to seventeenth 
#        order Gauss-Markov quadrature formulae invariant under the 
#        octahedron group with inversion'
#       Computational Mathematics and Mathematical Physics, Vol. 15,
#       1975, pp. 44-51.

def genOh_a00(v):
    """
        genOh_a00
        (0,0,a) etc. (6 points)
    """
    a=1.0
    return [(a,0,0,v),(-a,0,0,v),(0,a,0,v),(0,-a,0,v),(0,0,a,v),(0,0,-a,v)]

def genOh_aa0(v):
    """
        genOh_aa0
        (0,a,a) etc, a=1/sqrt(2) (12 points)
    """
    a=np.sqrt(0.5)
    return [(0,a,a,v),(0,-a,a,v),(0,a,-a,v),(0,-a,-a,v),
            (a,0,a,v),(-a,0,a,v),(a,0,-a,v),(-a,0,-a,v),
            (a,a,0,v),(-a,a,0,v),(a,-a,0,v),(-a,-a,0,v)]

def genOh_aaa(v):
    """
        genOh_aaa
        (a,a,a) etc, a=1/sqrt(3) (8 points)
    """
    a = np.sqrt(1./3.)
    return [(a,a,a,v),(-a,a,a,v),(a,-a,a,v),(-a,-a,a,v),
            (a,a,-a,v),(-a,a,-a,v),(a,-a,-a,v),(-a,-a,-a,v)]

def genOh_aab(v,a):
    """
        genOh_aab
        (a,a,b) etc, b=sqrt(1-2 a^2), a input (24 points)
    """
    b = np.sqrt(1.0 - 2.0*a*a)
    return [(a,a,b,v),(-a,a,b,v),(a,-a,b,v),(-a,-a,b,v),
            (a,a,-b,v),(-a,a,-b,v),(a,-a,-b,v),(-a,-a,-b,v),
            (a,b,a,v),(-a,b,a,v),(a,-b,a,v),(-a,-b,a,v),
            (a,b,-a,v),(-a,b,-a,v),(a,-b,-a,v),(-a,-b,-a,v),
            (b,a,a,v),(-b,a,a,v),(b,-a,a,v),(-b,-a,a,v),
            (b,a,-a,v),(-b,a,-a,v),(b,-a,-a,v),(-b,-a,-a,v)]
    
def genOh_ab0(v,a):
    """
        genOh_ab0
        (a,b,0) etc, b=sqrt(1-a^2), a input (24 points)
    """
    b=np.sqrt(1.0-a*a)
    return [(a,b,0,v),(-a,b,0,v),(a,-b,0,v),(-a,-b,0,v),
            (b,a,0,v),(-b,a,0,v),(b,-a,0,v),(-b,-a,0,v),
            (a,0,b,v),(-a,0,b,v),(a,0,-b,v),(-a,0,-b,v),
            (b,0,a,v),(-b,0,a,v),(b,0,-a,v),(-b,0,-a,v),
            (0,a,b,v),(0,-a,b,v),(0,a,-b,v),(0,-a,-b,v),
            (0,b,a,v),(0,-b,a,v),(0,b,-a,v),(0,-b,-a,v)]

def genOh_abc(v,a,b):
    """
        genOh_abc
        (a,b,c) etc, c=sqrt(1-a^2-b^2), a,b input  (48 points)
    """
    c=np.sqrt(1.0 - a*a - b*b)
    return [(a,b,c,v),(-a,b,c,v),(a,-b,c,v),(-a,-b,c,v),
            (a,b,-c,v),(-a,b,-c,v),(a,-b,-c,v),(-a,-b,-c,v),
            (a,c,b,v),(-a,c,b,v),(a,-c,b,v),(-a,-c,b,v),
            (a,c,-b,v),(-a,c,-b,v),(a,-c,-b,v),(-a,-c,-b,v),
            (b,a,c,v),(-b,a,c,v),(b,-a,c,v),(-b,-a,c,v),
            (b,a,-c,v),(-b,a,-c,v),(b,-a,-c,v),(-b,-a,-c,v),
            (b,c,a,v),(-b,c,a,v),(b,-c,a,v),(-b,-c,a,v),
            (b,c,-a,v),(-b,c,-a,v),(b,-c,-a,v),(-b,-c,-a,v),
            (c,a,b,v),(-c,a,b,v),(c,-a,b,v),(-c,-a,b,v),
            (c,a,-b,v),(-c,a,-b,v),(c,-a,-b,v),(-c,-a,-b,v),
            (c,b,a,v),(-c,b,a,v),(c,-b,a,v),(-c,-b,a,v),
            (c,b,-a,v),(-c,b,-a,v),(c,-b,-a,v),(-c,-b,-a,v)]

def leb6():
    """
        leb6
        Lebedev grid of degree 6 
    """
    g = genOh_a00(0.1666666666666667)
    return g 

def leb14():
    """
        leb14
        Lebedev grid of degree 14
    """
    g1 = genOh_a00(0.06666666666666667)
    g2 = genOh_aaa(0.07500000000000000)
    g = g1 + g2 
    return g 

def leb26():
    """
        leb26
        Lebedev grid of degree 26 
    """
    g1 = genOh_a00(0.04761904761904762)
    g2 = genOh_aa0(0.03809523809523810) 
    g3 = genOh_aaa(0.03214285714285714)
    g = g1 + g2 + g3
    return g 

def leb38():
    """
        leb38
        Lebedev grid of degree 38
    """
    g1 = genOh_a00(0.009523809523809524)
    g2 = genOh_aaa(0.3214285714285714E-1) 
    g3 = genOh_ab0(0.2857142857142857E-1,0.4597008433809831E+0)
    g = g1 + g2 + g3
    return g 

def leb50():
    """
        leb50
        Lebedev grid of degree 50
    """
    return genOh_a00(0.1269841269841270E-1)\
           + genOh_aa0(0.2257495590828924E-1) \
           + genOh_aaa(0.2109375000000000E-1) \
           + genOh_aab(0.2017333553791887E-1,0.3015113445777636E+0)

def leb74():
    """
        leb74
        Lebedev grid of degree 74 
    """
    return genOh_a00(0.5130671797338464E-3)\
           + genOh_aa0(0.1660406956574204E-1) \
           + genOh_aaa(-0.2958603896103896E-1) \
           + genOh_aab(0.2657620708215946E-1,0.4803844614152614E+0) \
           + genOh_ab0(0.1652217099371571E-1,0.3207726489807764E+0)

def leb86():
    """
        leb86
        Lebedev grid of degree 86 
    """
    return genOh_a00(0.1154401154401154E-1) \
           + genOh_aaa(0.1194390908585628E-1) \
           + genOh_aab(0.1111055571060340E-1,0.3696028464541502E+0) \
           + genOh_aab(0.1187650129453714E-1,0.6943540066026664E+0) \
           + genOh_ab0(0.1181230374690448E-1,0.3742430390903412E+0)

def leb110():
    """
        leb110
        Lebedev grid of degree 110 
    """
    return genOh_a00(0.3828270494937162E-2) \
           + genOh_aaa(0.9793737512487512E-2) \
           + genOh_aab(0.8211737283191111E-2,0.1851156353447362E+0) \
           + genOh_aab(0.9942814891178103E-2,0.6904210483822922E+0) \
           + genOh_aab(0.9595471336070963E-2,0.3956894730559419E+0) \
           + genOh_ab0(0.9694996361663028E-2,0.4783690288121502E+0)

def leb146():
    """
        leb146
        Lebedev grid of degree 146 
    """
    return genOh_a00(0.5996313688621381E-3) \
           + genOh_aa0(0.7372999718620756E-2) \
           + genOh_aaa(0.7210515360144488E-2) \
           + genOh_aab(0.7116355493117555E-2,0.6764410400114264E+0) \
           + genOh_aab(0.6753829486314477E-2,0.4174961227965453E+0) \
           + genOh_aab(0.7574394159054034E-2,0.1574676672039082E+0) \
           + genOh_abc(0.6991087353303262E-2,0.1403553811713183E+0,
                     0.4493328323269557E+0)

def leb170():
    """
        leb170
        Lebedev grid of degree 170 
    """
    return genOh_a00(0.5544842902037365E-2) \
           + genOh_aa0(0.6071332770670752E-2) \
           + genOh_aaa(0.6383674773515093E-2) \
           + genOh_aab(0.5183387587747790E-2,0.2551252621114134E+0) \
           + genOh_aab(0.6317929009813725E-2,0.6743601460362766E+0) \
           + genOh_aab(0.6201670006589077E-2,0.4318910696719410E+0) \
           + genOh_ab0(0.5477143385137348E-2,0.2613931360335988E+0) \
           + genOh_abc(0.5968383987681156E-2,0.4990453161796037E+0,
                     0.1446630744325115E+0)

def leb194():
    """
        leb194
        Lebedev grid of degree 194 
    """
    return genOh_a00(0.1782340447244611E-2) \
           + genOh_aa0(0.5716905949977102E-2) \
           + genOh_aaa(0.5573383178848738E-2) \
           + genOh_aab(0.5608704082587997E-2,0.6712973442695226E+0) \
           + genOh_aab(0.5158237711805383E-2,0.2892465627575439E+0) \
           + genOh_aab(0.5518771467273614E-2,0.4446933178717437E+0) \
           + genOh_aab(0.4106777028169394E-2,0.1299335447650067E+0) \
           + genOh_ab0(0.5051846064614808E-2,0.3457702197611283E+0) \
           + genOh_abc(0.5530248916233094E-2,0.1590417105383530E+0,
                     0.8360360154824589E+0)

def Lebedev(n):
    """
        Lebedev
        Calculate Lebdev Laikov angular grid.

        Input 
            n: int(), special integer numbers 

        Reference
            - https://github.com/gabrielelanaro/pyquante/blob/master/Data/lebedev_write.py

    """
    lebedev = {
        6: leb6,
        14: leb14,
        26: leb26,
        38: leb38,
        50: leb50,
        74: leb74,
        86: leb86,
        110: leb110,
        146: leb146,
        170: leb170,
        194: leb194
    }

    try:
        return np.array(lebedev[n]())
    except:
        raise f"No grid available for {n}" 

def main():
    """
        main 
        Main function to test this routine. 
    """
    print(Lebedev(6))

if __name__ == '__main__':
    main()
