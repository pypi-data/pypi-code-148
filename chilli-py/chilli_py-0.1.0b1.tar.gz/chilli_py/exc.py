import numpy as np
from chilli_py.utils import myprint 

""" Exchange-correlation functionals """

# Notes 
#   - the density rho can get zero or very close to zero 
#   - such values cause problems 
#   - currently in the correlation routines 
#   - those values are masked 
#   - e.g., see rho = np.ma.masked_where(rho == 0,rho)

def lda_slater_x(rho):
    """
        lda_slater_x
        type: spin-unpolarized exchange

        Input
            - rho: np.array(), density of one channel

        Reference 
            - https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_x_slater.jl
    """
    third = 1.0/3.0
    pi34 = 0.6203504908994  # pi34=(3/4*np.pi)**(1/3)
    rs = pi34/rho**third

    f = -0.687247939924714
    alpha = 2.0/3.0

    ex = f * alpha / rs
    vx = 4.0 / 3.0 * f * alpha / rs
    # SS: fx= rho*ex 
    return rho*ex, vx

def lda_slater_spin_x(rho,zeta):
    """
        lda_slater_spin_x
        type: spin-polarized exchange 

        Input
            - rho: np.array(), rho  = rho_a + rho_b, density
            - zeta: np.array(), zeta = (rhoa - rhob)/(rho)

        Notes
            - a,b: spin indices

        Reference 
            - https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_x_slater_spin.jl
    """
    f = -1.10783814957303361 # f = -9/8*(3/np.pi)**(1/3)
    alpha = 2.0/3.0
    third = 1.0/3.0
    p43 = 4.0/3.0

    rho13 = ((1.0 + zeta) * rho)**third
    exa = f * alpha * rho13
    vxa = p43 * f * alpha * rho13

    rho13 = ((1.0 - zeta) * rho)**third
    exb = f * alpha * rho13
    vxb = p43 * f * alpha * rho13
    ex = 0.5 * ((1.0 + zeta) * exa + (1.0 - zeta) * exb)

    # SS: fx = rho*ex 
    return rho*ex, vxa, vxb


def lda_vwn_c(rho): 
    """
        lda_vwn_c
        type: spin-unpolarized correlation 

        Input
            - rho: np.array(), density of one channel 

        Reference 
            - https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_c_vwn.jl
    """
    #rho = np.ma.masked_where(rho == 0,rho)

    third = 1.0/3.0
    pi34 = 0.6203504908994  # pi34=(3/4*np.pi)**(1/3)
    rs = pi34/rho**third

    a = 0.0310907
    b = 3.72744
    c = 12.9352
    x0 = -0.10498

    q = np.sqrt(4.0 * c - b * b)
    f1 = 2.0 * b / q
    f2 = b * x0 / (x0 * x0 + b * x0 + c)
    f3 = 2.0 * (2.0 * x0 + b) / q
    rs12 = np.sqrt(rs)
    fx = rs + b * rs12 + c
    qx = np.arctan(q/(2.0 * rs12 + b))

    # SS: to omit evaluation of log(0) -> warning, value = -inf 
    log1 = np.log(rs/fx,where=fx>0)
    arg2 = (rs12 - x0)**2/fx
    log2 = np.log(arg2,where=arg2>0)

    ec = a * (log1 + f1 * qx - f2 * (log2 + f3 * qx))

    tx = 2.0 * rs12 + b
    tt = tx * tx + q * q
    vc = ec - rs12 * a / 6.0 * (2.0 / rs12 - tx / fx - 4.0 * b / tt - 
         f2 * (2.0 / (rs12 - x0) - tx / fx - 4.0 * (2.0 * x0 + b) / tt))
    # SS: fc = rho*ex 
    return rho*ec, vc

def lda_vwn_spin_c(rho,zeta):
    """
        lda_vwn_spin_c
        type: spin-polarized correlation
       
        Input 
            - rho: np.array(), rho  = rho_a + rho_b, density 
            - zeta: np.array(), zeta = (rhoa - rhob)/(rho) 

        Needs
            - padefit 

        Notes
            - a,b: spin indices
            - zeta = 1, fully spin-polarized 
            - zeta = 0, fully spin-unpolarized
        

        Reference 
            - https://raw.githubusercontent.com/f-fathurrahman/PWDFT.jl/master/src/XC_funcs/XC_c_vwn_spin.jl
    """
    rho = np.ma.masked_where(rho == 0,rho)

    third = 1.0/3.0
    pi34 = 0.6203504908994  # pi34=(3/4pi)**(1/3)
    rs = pi34/rho**third

    A      = ( 0.0310907, 0.01554535, -0.01688686394039 )
    x0     = ( -0.10498, -0.32500, -0.0047584 )
    b      = ( 3.72744, 7.06042, 1.13107 )
    c      = ( 12.9352, 18.0578, 13.0045 )
    Q      = ( 6.15199081975908, 4.73092690956011, 7.12310891781812 )
    tbQ    = ( 1.21178334272806, 2.98479352354082, 0.31757762321188 )
    fx0    = ( 12.5549141492, 15.8687885, 12.99914055888256 )
    bx0fx0 = ( -0.03116760867894, -0.14460061018521, -0.00041403379428 )

    # N.B.: A is expressed in Hartree
    # Q = sqrt(4*c - b**2)
    # tbQ = 2*b/Q
    # fx0 = X(x_0) = x_0**2 + b*x_0 + c
    # bx0fx0 = b*x_0/X(x_0)

    cfz = 2.0**(4.0/3.0) - 2.0
    cfz1 = 1.0 / cfz
    cfz2 = 4.0/3.0 * cfz1
    iddfz0 = 9.0 / 8.0 *cfz
    sqrtrs = np.sqrt(rs)
    zeta3 = zeta**3
    zeta4 = zeta3*zeta
    tra = 1.0 + zeta
    trb = 1.0 - zeta
    tra13 = tra**(1.0/3.0)
    trb13 = trb**(1.0/3.0)
    fz = cfz1 * (tra13*tra + trb13*trb - 2.0) # f(zeta)
    dfz = cfz2 * (tra13 - trb13)     # d f / d zeta

    ecP, vcP = padefit(sqrtrs, 0, x0, Q, b, c, A, tbQ, bx0fx0)    # ecF = e_c Paramagnetic
    ecF, vcF = padefit(sqrtrs, 1, x0, Q, b, c, A, tbQ, bx0fx0)    # ecP = e_c Ferromagnetic
    ac, dac  = padefit(sqrtrs, 2, x0, Q, b, c, A, tbQ, bx0fx0)    # ac = "spin stiffness"

    ac = ac * iddfz0
    dac = dac * iddfz0
    De = ecF - ecP - ac # e_c[F] - e_c[P] - alpha_c/(ddf/ddz(z=0))
    fzz4 = fz * zeta4
    ec = ecP + ac * fz  + De * fzz4

    dec1 = vcP + dac*fz + (vcF - vcP - dac) * fzz4     # e_c - (r_s/3)*(de_c/dr_s)
    dec2 = ac*dfz + De*(4.0*zeta3*fz + zeta4*dfz)      # de_c/dzeta

    # v_c[s] = e_c - (r_s/3)*(de_c/dr_s) + [sign(s)-zeta]*(de_c/dzeta)
    vca = dec1 + (1.0 - zeta)*dec2
    vcb = dec1 - (1.0 + zeta)*dec2

    # SS: fc = rho*ec 
    return rho*ec, vca, vcb


def padefit(x,i,x0,Q,b,c,A,tbQ,bx0fx0):
    """
        padefit 
        Implementation of Eq.(4.4) (VWN1980)

        Reference 
            - S.H. Vosko, L. Wilk, and M. Nusair, Can. J. Phys. 58, 1200 (1980)
            - https://raw.githubusercontent.com/f-fathurrahman/PWDFT.jl/master/src/XC_funcs/XC_c_vwn_spin.jl
    """
    # Pade fit calculated in x and its derivative w.r.t. rho
    # rs = inv((rho*)**(1/3)) = x**2
    # fit  [eq. 4.4]
    # dfit/drho = fit - (rs/3)*dfit/drs = ec - (x/6)*dfit/dx

    sqx = x*x                            # x^2 = r_s
    xx0 = x - x0[i]                      # x - x_0
    Qtxb = Q[i] / (2.0*x + b[i])         # Q / (2x+b)
    atg = np.arctan(Qtxb)                # tan**-1(Q/(2x+b))
    fx = sqx + b[i]*x + c[i]             # X(x) = x**2 + b*x + c

    # SS: to omit np.log(0) -> warning, val=-inf
    log1 = np.log(sqx/fx, where=fx>0)
    log2 = np.log(xx0*xx0/fx, where=fx>0) 

    fit = A[i] * (log1 + tbQ[i]*atg - bx0fx0[i] * (log2 + (tbQ[i] + 4.0*x0[i]/Q[i]) * atg))

    txb = 2.0*x + b[i]
    txbfx = txb / fx
    itxbQ = 1.0 / (txb*txb + Q[i]*Q[i])

    dfit = fit - A[i] / 3.0 + A[i]*x/6.0 * (txbfx + 4.0*b[i]*itxbQ + bx0fx0[i] * (2.0/xx0 - txbfx - 4.0*(b[i] + 2.0*x0[i])*itxbQ))

    return fit, dfit

def lda_pw_c(rho):
    """
        lda_pw_c
        type: spin-unpolarized correlation 

        Input 
            - rho: np.array(), density only in spin channel 

        Reference 
            - https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_c_pw.jl
    """
    rho = np.ma.masked_where(rho == 0,rho)

    third = 1.0/3.0
    pi34 = 0.6203504908994
    rs = pi34/rho**third

    a = 0.031091
    a1 = 0.21370
    b1 = 7.5957
    b2 = 3.5876
    b3 = 1.6382
    b4 = 0.49294

    # interpolation formula
    rs12 = np.sqrt(rs)
    rs32 = rs * rs12
    rs2 = rs**2
    
    om = 2.0 * a * (b1 * rs12 + b2 * rs + b3 * rs32 + b4 * rs2)
    dom = 2.0 * a * (0.5 * b1 * rs12 + b2 * rs + 1.5 * b3 * rs32 + 2.0 * b4 * rs2)
    #print(f"om: {om}")
    olog = np.log(1.0 + 1.0/om,where=om>0)
    ec = -2.0 * a * (1.0 + a1 * rs) * olog
    vc = -2.0*a*(1.0 + 2.0/3.0 * a1 * rs) * olog - 2.0/3.0 * a * (1.0 + a1*rs) * dom/ (om * (om + 1.0) )
    # SS: fc = rho*ec
    return rho*ec, vc


def lda_pw_spin_c(rho,zeta):
    """
        lda_pw_spin_c
        type: spin-polarized correlation 

        Input
            - rho: np.array(), rho  = rho_a + rho_b, density
            - zeta: np.array(), zeta = (rhoa - rhob)/(rho)

        Reference 
            - https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_c_pw_spin.jl
    """
    rho = np.ma.masked_where(rho == 0,rho)

    third = 1.0/3.0
    pi34 = 0.6203504908994  # pi34=(3/4pi)**(1/3)
    rs = pi34/rho**third

    # J.P. Perdew and Y. Wang, PRB 45, 13244 (1992)
    # xc parameters, unpolarised
    a = 0.031091
    a1 = 0.21370
    b1 = 7.5957
    b2 = 3.5876
    b3 = 1.6382
    b4 = 0.49294
    c0 = a
    c1 = 0.046644
    c2 = 0.00664
    c3 = 0.01043
    d0 = 0.4335
    d1 = 1.4408
    
    # xc parameters, polarised
    ap = 0.015545
    a1p = 0.20548
    b1p = 14.1189
    b2p = 6.1977
    b3p = 3.3662
    b4p = 0.62517
    c0p = ap
    c1p = 0.025599
    c2p = 0.00319
    c3p = 0.00384
    d0p = 0.3287
    d1p = 1.7697
  
    # xc parameters, antiferro
    aa = 0.016887
    a1a = 0.11125
    b1a = 10.357
    b2a = 3.6231
    b3a = 0.88026
    b4a = 0.49671
    c0a = aa
    c1a = 0.035475
    c2a = 0.00188
    c3a = 0.00521
    d0a = 0.2240
    d1a = 0.3969
  
    fz0 = 1.709921

    #
    #     if(rs.lt.0.5d0) then
    # high density formula (not implemented)
    #
    #     else if(rs.gt.100.d0) then
    # low density formula  (not implemented)
    #
    #     else
    # interpolation formula
  
    zeta2 = zeta * zeta
    zeta3 = zeta2 * zeta
    zeta4 = zeta3 * zeta
  
    rs12 = np.sqrt(rs)
    rs32 = rs * rs12
    rs2 = rs**2
  
    # unpolarised
    om = 2.0 * a * (b1 * rs12 + b2 * rs + b3 * rs32 + b4 * rs2)
    dom = 2.0 * a * (0.5 * b1 * rs12 + b2 * rs + 1.5 * b3 * rs32 + 2.0 * b4 * rs2)
    olog = np.log(1.0 + 1.0 / om, where=om>0)
    epwc = -2.0 * a * (1.0 + a1 * rs) * olog
    vpwc = -2.0 * a * (1.0 + 2.0 / 3.0 * a1 * rs) * olog - 2.0/3.0 * a * (1.0 + a1 * rs) * dom / (om * (om + 1.0))
  
    # polarized
    omp = 2.0 * ap * (b1p * rs12 + b2p * rs + b3p * rs32 + b4p * rs2)
    domp = 2.0 * ap * (0.5 * b1p * rs12 + b2p * rs + 1.5 * b3p * rs32 + 2.0 * b4p * rs2)
    ologp = np.log(1.0 + 1.0 / omp, where=omp>0)
    epwcp = -2.0 * ap * (1.0 + a1p * rs) * ologp
    vpwcp = -2.0 * ap * (1.0 + 2.0 / 3.0 * a1p * rs) * ologp - 2.0/3.0 * ap * (1.0 + a1p * rs) * domp / (omp * (omp + 1.0))
  
    # antiferro
    oma = 2.0 * aa * (b1a * rs12 + b2a * rs + b3a * rs32 + b4a * rs2)
    doma = 2.0 * aa * (0.5 * b1a * rs12 + b2a * rs + 1.5 * b3a * rs32 + 2.0 * b4a * rs2)
    ologa = np.log(1.0 + 1.0 / oma, where=oma>0)
    alpha = 2.0 * aa * (1.0 + a1a * rs) * ologa
    vpwca = 2.0 * aa * (1.0 + 2.0 / 3.0 * a1a * rs) * ologa + 2.0/3.0 * aa * (1.0 + a1a * rs) * doma / (oma * (oma + 1.0))
  
    fz =  ((1.0 + zeta)**(4.0/3.0) + (1.0 - zeta)**(4.0/3.0) - 2.0) / (2.0**(4.0/3.0) - 2.0)
    dfz = ((1.0 + zeta)**(1.0/3.0) - (1.0 - zeta)**(1.0/3.0) ) * 4.0 / (3.0 * (2.0**(4.0/3.0) - 2.0))
  
    ec = epwc + alpha * fz * (1.0 - zeta4) / fz0 + (epwcp - epwc) * fz * zeta4
  
    vcup = vpwc + vpwca * fz * (1.0 - zeta4) / fz0 + (vpwcp - vpwc)*fz*zeta4 + \
            (alpha / fz0 * (dfz * (1.0 - zeta4) - 4.0*fz*zeta3) + \
            (epwcp - epwc) * (dfz * zeta4 + 4.0 * fz * zeta3)) * (1.0 - zeta)

    vcdw = vpwc + vpwca * fz * (1.0 - zeta4) / fz0 + (vpwcp - vpwc) * fz * zeta4 - \
          (alpha / fz0 * (dfz * (1.0 - zeta4) - 4.0 * fz * zeta3) + \
            (epwcp - epwc) * (dfz * zeta4 + 4.0 * fz * zeta3)) * (1.0 + zeta)

    # SS: fc = rho*ec
    return rho*ec, vcup, vcdw

def lda_chachiyo_c(rho):
    """
        lda_chachiyo_c
        type: spin-unpolarized correlation

        Input
            - rho: np.array(), density of one channel

        Reference
            - https://aip.scitation.org/doi/10.1063/1.4958669
            - https://tu-freiberg.de/sites/default/files/media/institut-fuer-theoretische-physik-10451/Lehre/Dichtefunktionaltheorie/sheet07-2018.pdf
    """
    rho = np.ma.masked_where(rho == 0,rho)

    third = 1.0/3.0
    pi34 = 0.6203504908994  # pi34=(3/4pi)**(1/3)
    rs = pi34/rho**third
    
    a = (np.log(2)-1)/(2*np.pi**2)
    b = 20.4562557
    ec = a*np.log(1+b/rs+b/rs**2) 
    vc = ec + a*b*(2+rs)/(3*(b+b*rs+rs**2))
    return rho*ec, vc


def lda_chachiyo_spin_c(rho,zeta):
    """
        lda_chachiyo_spin_c
        type: spin-polarized correlation

        Input
            - rho: np.array(), rho  = rho_a + rho_b, density
            - zeta: np.array(), zeta = (rhoa - rhob)/(rho)

        Reference
            - https://aip.scitation.org/doi/10.1063/1.4958669
            - https://tu-freiberg.de/sites/default/files/media/institut-fuer-theoretische-physik-10451/Lehre/Dichtefunktionaltheorie/sheet07-2018.pdf
    """
    rho = np.ma.masked_where(rho == 0,rho)

    third = 1.0/3.0
    pi34 = 0.6203504908994  # pi34=(3/4pi)**(1/3)
    rs = pi34/rho**third

    a0 = (np.log(2)-1)/(2*np.pi**2)
    b0 = 20.4562557
    ec0 = a0*np.log(1+b0/rs+b0/rs**2)
    
    a1 = (np.log(2)-1)/(4*np.pi**2)
    b1 = 27.4203609
    ec1 = a1*np.log(1+b1/rs+b1/rs**2)
    
    # If you run into numerical issues uncomment the nan_to_num functions below
    # With those additions the function generates the same values as LibXC
    fzeta = ((1+zeta)**(4/3)+(1-zeta)**(4/3)-2)/(2*(2**third-1))
    # fzeta = np.nan_to_num(fzeta, nan=0, posinf=0, neginf=0)
    ec = ec0+(ec1-ec0)*fzeta
    # ec = np.nan_to_num(ec, nan=0, posinf=0, neginf=0)

    dec0drs = a0/(1+b0/rs+b0/rs**2)*b0*(-1/rs**2-2/rs**3)
    dec1drs = a1/(1+b1/rs+b1/rs**2)*b1*(-1/rs**2-2/rs**3)

    dfdzeta = (2*(1-zeta)**third-2*(1+zeta)**third)/(3-3*2**third)
    # dfdzeta = np.nan_to_num(dfdzeta, nan=0, posinf=0, neginf=0)
    prefactor = ec-rs/3*(dec0drs+(dec1drs-dec0drs)*fzeta)
    # prefactor = np.nan_to_num(prefactor, nan=0, posinf=0, neginf=0)
    # (1 - zeta) = (rho_a + rho_b) / rho - (rho_a - rho_b) / rho = 2rho_b/ rho 
    # (1 + zeta) = (rho_a + rho_b) / rho + (rho_a - rho_b) / rho = 2rho_a/ rho
    vca = prefactor+(ec1-ec0)*dfdzeta*(1-zeta)
    vcb = prefactor-(ec1-ec0)*dfdzeta*(1+zeta)
    # vca = np.nan_to_num(vca, nan=0, posinf=0, neginf=0)
    # vcb = np.nan_to_num(vcb, nan=0, posinf=0, neginf=0)
    return rho*ec, vca, vcb


def gga_pbe_x(rho,grho):
    """
       gga_pbe_x
       type: spin-unpolarized exchange 

       Input
            - rho: np.array(), density of one channel 
            - grho: np.array(), gradient of the density 

       Reference 
          - J.P.Perdew, K.Burke, M.Ernzerhof, PRL 77, 3865 (1996)
          - https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_x_pbe.jl
    """

    third = 1.0/3.0
    k = 0.804
    mu = 0.2195149727645171
    c1 = 0.75/np.pi
    c2 = 3.093667726280136
    c5 = 4.0*third

    agrho = np.sqrt(grho)
    kf = c2 * rho**third
    dsg = 0.5/kf
    s1 = agrho*dsg / rho
    s2 = s1 * s1
    ds = -c5 * s1
    
    # Energy
    f1 = s2 * mu/k
    f2 = 1.0 + f1
    f3 = k / f2
    fx = k - f3
    exunif = -c1 * kf
    sx = exunif * fx

    # Potential
    dxunif = exunif * third
    dfx1 = f2 * f2
    dfx = 2.0 * mu * s1 / dfx1
    
    v1x = sx + dxunif * fx + exunif * dfx * ds
    v2x = exunif * dfx * dsg / agrho
    sx = sx * rho
 
    # SS 
    #return sx, v1x, v2x
    return sx, v1x, v2x


def gga_pbe_c(rho,grho):
    """
       gga_pbe_c
       type: spin-unpolarized correlation 
       
       Input
            - rho: np.array(), density of one channel 
            - grho: np.array(), gradient of the density 

       Reference 
	  - J.P.Perdew, K.Burke, M.Ernzerhof, PRL 77, 3865 (1996).
          - https://github.com/f-fathurrahman/PWDFT.jl/blob/master/src/XC_funcs/XC_c_pbe.jl
    """
    #rho = np.ma.masked_where(rho == 0,rho)
    #grho = np.ma.masked_where(grho == 0,grho)

    ga = 0.0310906908696548950
    be = 0.06672455060314922
    third = 1.0/3.0
    pi34 = 0.6203504908994
    xkf = 1.919158292677513
    xks = 1.128379167095513

    rs = pi34/rho**third
    ec, vc = lda_pw_c(rho)
    ec /=rho

    kf = xkf/rs
    ks = xks * np.sqrt(kf)
    t = np.sqrt(grho) / (2.0 * ks * rho)
    
    expe = np.exp(-ec/ga)
    af = be / ga * (1.0 / (expe - 1.0) )
    
    bf = expe * (vc - ec)
    y = af * t * t
    xy = (1.0 + y) / (1.0 + y + y * y)
    qy = y * y * (2.0 + y) / (1.0 + y + y * y)**2
  
    s1 = 1.0 + be / ga * t * t * xy
    h0 = ga * np.log(s1)
    dh0 = be * t * t / s1 * ( -7.0 / 3.0 * xy - qy * (af * bf / be - 7.0 / 3.0) )
    ddh0 = be/(2.0 * ks * ks * rho) * (xy - qy) / s1
  
    sc = rho * h0
    v1c = h0 + dh0
    v2c = ddh0
    
    #SS 
    #return sc, v1c, v2c
    return sc, v1c, v2c

class Functional: 
    """
        Functional class 
        Defines a functional

        Input
           - name: str(), e.g., "LDA,VWN"
           - funcs:, dict('x' : func(), 'x' : func())
           - spin: int(), 0 == spin unpolarized, 1 == spin-polarized 
           - family; str(), "LDA" only density is needed, "GGA" density and derivative 

    """
    def __init__(self,name,funcs,spin,family):
        """
            __init__
            Initialize an instance of the class. 
        """
        self.name = name 
        self.funcs = funcs 
        self.spin = spin
        self.family = family 

    def kernel(self,**kwargs):
        """
            kernel 
            Calculate xc properties for a given 
            input. 
            
            Input
                - (rho) for RKS 
                - (rho, zeta) for UKS 

            Notes
                - use keyword arguments to differentiate between spin==0 and spin==1 input 
        """
        if self.spin == 0 and self.family == "LDA": 
            rho = kwargs.get("rho")
            fx, vx = self.funcs['x'](rho)
            fc, vc = self.funcs['c'](rho)  
            res = [fx,vx,fc,vc]
        if self.spin == 0 and self.family == "GGA":
            # Until now designed for PBE 
            rho = kwargs.get("rho")
            grho = kwargs.get("grho")
            fx, vx = func_unpol["LDA,PW"].funcs['x'](rho=rho)
            fc, vc = func_unpol["LDA,PW"].funcs['c'](rho=rho)
            fx1, vx1, vx2 = func_unpol["PBE,PBE"].funcs['x'](rho=rho,grho=grho)
            fc1, vc1, vc2 = func_unpol["PBE,PBE"].funcs['c'](rho=rho,grho=grho)
            Fx = (fx/rho + fx1/rho)
            Fc = (fc/rho + fc1/rho)
            Vx = ((vx + vx1), vx2)
            Vc = ((vc + vc1), vc2) 
            res = [Fx,Vx,Fc,Vc]

        if self.spin != 0 and self.family == "LDA":
            rho = kwargs.get("rho")
            zeta = kwargs.get("zeta")
            fx, vxa, vxb = self.funcs['x'](rho,zeta)
            fc, vca, vcb = self.funcs['c'](rho,zeta)
            res = [fx,vxa,vxb,fc,vca,vcb]
        return res


# spin-unpolarized functionals 
func_unpol = {
                "LDA,VWN"       : Functional("LDA,VWN",      {'x': lda_slater_x, 'c': lda_vwn_c},spin=0,family="LDA"), 
                "LDA,PW"        : Functional("LDA,PW",       {'x': lda_slater_x, 'c': lda_pw_c},spin=0,family="LDA"),
                "LDA,CHACHIYO"  : Functional("LDA,CHACHIYO", {'x': lda_slater_x, 'c': lda_chachiyo_c},spin=0,family="LDA"),
                "PBE,PBE"       : Functional("PBE,PBE",      {'x': gga_pbe_x,    'c': gga_pbe_c},spin=0,family="GGA")
}

# spin-polarized functionals 
func_pol  = {
                "LDA,VWN"       : Functional("LDA,VWN",{'x': lda_slater_spin_x, 'c': lda_vwn_spin_c},spin=1,family="LDA"),
                "LDA,PW"        : Functional("LDA,PW", {'x': lda_slater_spin_x, 'c': lda_pw_spin_c},spin=1,family="LDA"),
                "LDA,CHACHIYO"  : Functional("LDA,CHACHIYO", {'x': lda_slater_spin_x, 'c': lda_chachiyo_spin_c},spin=1,family="LDA")
}

class XC:
    """
        XC class 
        Exchange-correlation functionals 
        Note: 
            - spin=0 -> spin-unpolarized functionals 
            - spin=1 -> spin-polarized functionals 
    """
    def __init__(self,grids,spin=0,xc_name="LDA,VWN"):
        """
            __init__ 
            Initialize instance of the class. 

            Input 
                - xc, str(), exchange-correlation functional 
        """
        self.grids=grids
        self.spin=spin 
        self.xc_name=xc_name 
        if spin== 0: 
            self.xc = func_unpol[xc_name]
        if spin== 1: 
            self.xc = func_pol[xc_name]

    def kernel(self,**kwargs):
        """
            get_Exc
            Get exchange-correlation (xc) energy Exc and potential matrix Vxc.

            Note
                - use keyword arguments to differtiate between spin=0 and spin=1 input 

        """
        # spin-unpolarized LDA 
        if self.spin == 0:
            if self.xc.family == "LDA": 
                D = kwargs.get('D')
                rho = self.grids.get_rho(D)
                rho = np.ma.masked_where(rho == 0,rho)
                fx,vx,fc,vc = self.xc.kernel(rho=rho)
                Exc = np.dot(self.grids.weights,fx+fc)
                Vxc = np.einsum('g,g,gI,gJ->IJ',self.grids.weights,vx+vc,self.grids.basis_ongrid,self.grids.basis_ongrid)
                res = [Exc,Vxc]
            if self.xc.family == "GGA":
                D = kwargs.get('D')
                D = (D+D.conj().T)
                D *= 0.5
                rho = self.grids.get_rho(D*2)/2.
                grho,vsigma = self.grids.get_grad(D*2)
                grho /= 2 
                vsigma = (grho[:,0]**2 + grho[:,1]**2 + grho[:,2]**2) # 0.25
                #print(f"exc: rho: {rho} \n dx: {grho[:,0]} \n dy: {grho[:,1]} \n dz: {grho[:,2]}")
                rho = np.ma.masked_where(rho == 0,rho)
                vsigma = np.ma.masked_where(vsigma == 0,vsigma)
                fx,vx,fc,vc = self.xc.kernel(rho=rho,grho=vsigma)
                vx1, vx2 = vx 
                vc1, vc2 = vc
                fxc = fx + fc 
                vxc1 = vx1 + vc1   
                vxc2 = vx2 + vc2   
                Exc = np.dot(self.grids.weights*rho,fxc)
                ## vrho
                #Vxc = np.einsum('g,g,gI,gJ->IJ',self.grids.weights,vxc1,self.grids.basis_ongrid,self.grids.basis_ongrid)
                #Vtmp = np.einsum('pb,p,p,pa->ab', self.grids.basis_ongrid, vxc1, self.grids.weights, self.grids.basis_ongrid, optimize=True) # *0.5
                #print(f"Hans vs. Ingo {Vxc} {Vtmp}")
                ## dx 
                #Vxc += 1*np.einsum('g,g,gI,gJ->IJ',self.grids.weights*grho[:,0],vxc2,self.grids.basis_ongrid,self.grids.basis_ongrid)
                ## dy
                #Vxc += 1*np.einsum('g,g,gI,gJ->IJ',self.grids.weights*grho[:,1],vxc2,self.grids.basis_ongrid,self.grids.basis_ongrid)
                ## dz 
                #Vxc += 1*np.einsum('g,g,gI,gJ->IJ',self.grids.weights*grho[:,2],vxc2,self.grids.basis_ongrid,self.grids.basis_ongrid) 
                ##print(f"Exc: {Exc} Vxc: {Vxc}") 
                ## psi4numpy 
                ## phi -> basis function on grid -> self.grids.basis_ongrid
                ## grho <-> vsigma 
                #Vtmp += np.einsum('pb,p,p,p,pa->ab',self.grids.basisgrad_ongrid[:,:,0], vxc2, vsigma, self.grids.weights, self.grids.basis_ongrid, optimize=True)
                #Vtmp += np.einsum('pb,p,p,p,pa->ab',self.grids.basisgrad_ongrid[:,:,1], vxc2, vsigma, self.grids.weights, self.grids.basis_ongrid, optimize=True)
                #Vtmp += np.einsum('pb,p,p,p,pa->ab',self.grids.basisgrad_ongrid[:,:,2], vxc2, vsigma, self.grids.weights, self.grids.basis_ongrid, optimize=True)
                #Vtmp += Vtmp.T
                #Vtmp *= 0.5 
                #print(f"Exc: {Exc} Vxc: {Vxc}")
                #print(f"Hans vs. Ingo {Vxc} {Vtmp}")
                #Vxc += Vxc.conj().T 
                #res = [Exc,Vxc]
                # Test 
                def _get_rks_gga_wv(rho, vxc, weight):

                       """
                           Needed by
                               - rks_gga
                       """
                       vrho, vgamma = vxc[:2]
                       ngrid = vrho.size
                       wv = np.empty((4,ngrid))
                       wv[0]  = weight * vrho
                       wv[1:] = (weight * vgamma * 2) * rho[1:4]
                       wv[0] *= .5  # b/c v+v.T 
                       return wv

                def rks_gga(grids,rho,fxc,vxc):
                    weight=grids.weights.T
                    # ao ... atomic orbital values on the grid 
                    ao=(grids.basis_ongrid,
                        grids.basisgrad_ongrid[:,:,0],
                        grids.basisgrad_ongrid[:,:,1],
                        grids.basisgrad_ongrid[:,:,2])
                    aow = None 
                    aow = np.ndarray(ao[0].shape, order='F', buffer=aow)
                    def _rks_gga_wv0(rho, vxc, weight):
                        """
                            Needed by
                                - nr_rks
                        """
                        vrho, vgamma = vxc[:2]
                        ngrid = vrho.size
                        wv = np.empty((4,ngrid))
                        wv[0]  = weight * vrho
                        wv[1:] = (weight * vgamma * 2) * rho[1:4]
                        wv[0] *= .5  # v+v.T should be applied in the caller
                        return wv

                    vrho = vxc[0]
                    den = rho[0] * weight
                    Nelec = den.sum()
                    Exc = np.dot(den, fxc)
                    wv = _rks_gga_wv0(rho, vxc, weight)
                    aow = np.einsum('npi,np->pi', ao, wv, out=aow)
                    Vxc = np.dot(ao[0].T,aow)
                    # Hermitian 
                    Vxc = Vxc + Vxc.conj().T
                    return Nelec, Exc, Vxc

                Nelec, Exc, Vxc = rks_gga(grids=self.grids,
                                          rho=(rho,grho[:,0],grho[:,1],grho[:,2]),
                                          fxc=fxc,
                                          vxc=(vxc1,vxc2/2))
                res = [Exc,Vxc]
            

        # spin-polarized LDA 
        if self.spin != 0: 
            Da = kwargs.get('Da') 
            Db = kwargs.get('Db')
            rhoa = self.grids.get_rho(Da/2)
            rhob = self.grids.get_rho(Db/2)
            rho = rhoa+rhob
            rho = np.ma.masked_where(rho == 0,rho)
            #rho = np.ma.masked_where(np.isfinite(rho),0)
            zeta = np.ma.masked_where(rho == 0, (rhoa-rhob)/rho)
            #zeta = np.ma.masked_where(np.isfinite(zeta),0)

            fx,vxa,vxb,fc,vca,vcb = self.xc.kernel(rho=rho,zeta=zeta)
            Exc = np.dot(self.grids.weights,fx+fc)
            Vxca = np.einsum('g,g,gI,gJ->IJ',self.grids.weights,vxa+vca,self.grids.basis_ongrid,self.grids.basis_ongrid)
            Vxcb = np.einsum('g,g,gI,gJ->IJ',self.grids.weights,vxb+vcb,self.grids.basis_ongrid,self.grids.basis_ongrid)
            res = [Exc, Vxca, Vxcb]
        return res

    def __repr__(self): 
        """
            __repr__
            Representation of the instance of the class.
        """
        return f"{self.xc_name}"

def main():
    #from chilli_py.exc import lda_vwn_c
    n = 3.4  
    na = np.array([2.0,1.])
    nb = np.array([4.0,1.]) 
    data_spinunpol0 = lda_vwn_c(na+nb)
    
    zeta = (na - nb) / (na + nb) 
    
    print(f"zeta: {zeta}")
    data_spinpol = lda_vwn_spin_c(na+nb,zeta=1)
    data_spinunpol = (1/(na+nb))*lda_vwn_spin_c(na+nb,zeta=0)
    print(f"spinunpol routine: {data_spinunpol0}")
    print(f"spinpol routine (spinpol): {data_spinpol}")
    print(f"spinpol routine (spinunpol): {data_spinunpol}") 

if __name__ == '__main__':
    main() 
