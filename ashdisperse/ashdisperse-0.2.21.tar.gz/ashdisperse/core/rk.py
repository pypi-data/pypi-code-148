from functools import cache

import numpy as np
from numba import complex128, float64, int64, jit, njit

# from numba.pycc import CC
from numba.types import Tuple

from ..containers.cheb import ChebContainer_type
from ..containers.velocities import VelocityContainer_type
from ..met.met import MetData_type
from ..params.params import Parameters_type
from .getters import (
    Source_z_dimless_value,
    lower_dWsdz,
    lower_U,
    lower_V,
    lower_Ws,
    upper_dWsdz,
    upper_U,
    upper_V,
    upper_Ws,
)

# Cash-Karp tableau
C2 = 0.2
C3 = 0.3
C4 = 0.6
C5 = 1.0
C6 = 0.875
A21 = 0.2
A31 = 3.0 / 40.0
A32 = 9.0 / 40.0
A41 = 0.3
A42 = -0.9
A43 = 1.2
A51 = -11.0 / 54.0
A52 = 2.5
A53 = -70.0 / 27.0
A54 = 35.0 / 27.0
A61 = 1631.0 / 55296.0
A62 = 175.0 / 512.0
A63 = 575.0 / 13824.0
A64 = 44275.0 / 110592.0
A65 = 253.0 / 4096.0
B1 = 37.0 / 378.0
B2 = 0.0
B3 = 250.0 / 621.0
B4 = 125.0 / 594.0
B5 = 0.0
B6 = 512.0 / 1771.0
DB1 = B1 - 2825.0 / 27648.0
DB2 = 0.0
DB3 = B3 - 18575.0 / 48384.0
DB4 = B4 - 13525.0 / 55296.0
DB5 = -277.0 / 14336.0
DB6 = B6 - 0.25


@jit(
    complex128(
        float64,
        complex128,
        complex128,
        float64,
        float64,
        int64,
        Parameters_type,
        MetData_type,
    ),
    nopython=True,
    cache=True,
    fastmath=True,
)
# @njit(cache=True)
def ode_homo(x, y0, y1, kx, ky, grain_i, parameters, Met):

    pi = np.pi
    Lx = parameters.model.Lx[grain_i]
    Ly = parameters.model.Ly[grain_i]
    Pe = parameters.model.Peclet_number
    Vratio = parameters.model.Velocity_ratio[grain_i]
    R = parameters.model.Diffusion_ratio

    U_scale = parameters.met.U_scale
    Ws_scale = parameters.met.Ws_scale[grain_i]

    z = -np.log(x)

    U = Met.wind_U_value(z, U_scale)
    V = Met.wind_V_value(z, U_scale)

    Ws = Met.settling_speed_for_grain_class_value(parameters, grain_i, z, Ws_scale)
    dz = 1e-4
    Ws1 = Met.settling_speed_for_grain_class_value(
        parameters, grain_i, z + dz, Ws_scale
    )
    dWsdz = (Ws1 - Ws) / dz

    t1 = (R * Ws / Pe / Vratio - 1.0) * y1 / x

    c2 = (
        1j * pi * (kx / Lx * U + ky / Ly * V)
        + pi * pi * Pe / Vratio * (kx * kx / Lx / Lx + ky * ky / Ly / Ly)
        - dWsdz
    )
    t2 = c2 * R / Pe / Vratio * y0 / x / x

    return t1 + t2


@jit(
    complex128[::1](
        float64,
        complex128[::1],
        float64,
        float64,
        complex128,
        int64,
        Parameters_type,
        MetData_type,
    ),
    nopython=True,
    cache=True,
    fastmath=True,
)
# @njit(cache=True)
def ode(xt, yt, kx, ky, fxy_ij, grain_i, parameters, Met):

    dy = np.zeros_like(yt, dtype=np.complex128)

    z = -np.log(xt)
    fz = Source_z_dimless_value(z, parameters.source.Suzuki_k)

    dy[0] = yt[1]
    dy[1] = ode_homo(xt, yt[0], yt[1], kx, ky, grain_i, parameters, Met)
    dy[1] = dy[1] - fxy_ij * fz / xt / xt
    dy[2] = yt[3]
    dy[3] = ode_homo(xt, yt[2], yt[3], kx, ky, grain_i, parameters, Met)

    return dy


@jit(
    Tuple((complex128[::1], complex128[::1]))(
        float64,
        complex128[::1],
        complex128[::1],
        float64,
        int64,
        float64,
        float64,
        complex128,
        Parameters_type,
        MetData_type,
    ),
    nopython=True,
    cache=True,
    fastmath=True,
)
# @njit(cache=True)
def rkCK(x_in, y_in, dy, h, grain_i, kx, ky, fxy_ij, parameters, Met):

    xt = x_in
    k1 = dy

    xt = x_in + C2 * h
    yt = y_in + A21 * k1 * h
    k2 = ode(xt, yt, kx, ky, fxy_ij, grain_i, parameters, Met)

    xt = x_in + C3 * h
    yt = y_in + (A31 * k1 + A32 * k2) * h
    k3 = ode(xt, yt, kx, ky, fxy_ij, grain_i, parameters, Met)

    xt = x_in + C4 * h
    yt = y_in + (A41 * k1 + A42 * k2 + A43 * k3) * h
    k4 = ode(xt, yt, kx, ky, fxy_ij, grain_i, parameters, Met)

    xt = x_in + C5 * h
    yt = y_in + (A51 * k1 + A52 * k2 + A53 * k3 + A54 * k4) * h
    k5 = ode(xt, yt, kx, ky, fxy_ij, grain_i, parameters, Met)

    xt = x_in + C6 * h
    yt = y_in + (A61 * k1 + A62 * k2 + A63 * k3 + A64 * k4 + A65 * k5) * h
    k6 = ode(xt, yt, kx, ky, fxy_ij, grain_i, parameters, Met)

    # Accumulate increments with proper weights.
    y_out = y_in + h * (B1 * dy + B3 * k3 + B4 * k4 + B6 * k6)
    y_err = h * (DB1 * dy + DB3 * k3 + DB4 * k4 + DB5 * k5 + DB6 * k6)

    return y_out, y_err


@jit(
    Tuple((float64, complex128[::1], float64))(
        float64,
        complex128[::1],
        complex128[::1],
        float64,
        int64,
        float64,
        float64,
        complex128,
        Parameters_type,
        MetData_type,
    ),
    nopython=True,
    cache=True,
    fastmath=True,
)
# @njit(cache=True)
def rkstep(x, y, dy, h_in, grain_i, kx, ky, fxy_ij, parameters, Met):

    rtol = parameters.solver.rtol
    maxStep = parameters.solver.maxStep
    meps = parameters.solver.meps

    h = h_in
    while True:
        yt, y_err = rkCK(x, y, dy, h, grain_i, kx, ky, fxy_ij, parameters, Met)

        y_scal = np.absolute(yt) + np.absolute(h * dy) + meps
        errmax = np.max(np.absolute(y_err) / np.absolute(y_scal)) / rtol

        if errmax <= 1:
            break

        htemp = 0.9 * h * (np.power(errmax, -0.25))
        htemp = np.maximum(np.abs(htemp), 0.1 * np.abs(h))
        h = np.abs(htemp) * np.sign(h)

    h_out = h

    if errmax > 1.89e-4:
        h_next = 0.9 * h / (np.power(errmax, 0.2))
    else:
        h_next = 5.0 * h  # Numerical Recipes criteria

    x_out = x + h_out
    y_out = yt

    h_next = np.minimum(h_next, maxStep)

    return x_out, y_out, h_next


@jit(
    Tuple((complex128[::1], complex128[::1], float64))(
        float64,
        float64,
        complex128[::1],
        complex128[::1],
        float64,
        int64,
        float64,
        float64,
        complex128,
        Parameters_type,
        MetData_type,
    ),
    nopython=True,
    cache=True,
    fastmath=True,
)
# @njit(cache=True)
def integrateTo(x0, x1, y, dy, h_in, grain_i, kx, ky, fxy_ij, parameters, Met):

    x = x0
    h = h_in
    h_next = h_in
    while x < x1:
        x, y, h_next = rkstep(x, y, dy, h, grain_i, kx, ky, fxy_ij, parameters, Met)

        dy = ode(x, y, kx, ky, fxy_ij, grain_i, parameters, Met)

        if x + h_next > x1:
            h = x1 - x

    return y, dy, h_next
