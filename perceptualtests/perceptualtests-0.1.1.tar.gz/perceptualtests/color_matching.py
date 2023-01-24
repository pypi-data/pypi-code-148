import numpy as np
from scipy import integrate
from scipy import interpolate

km = 683

def monochomatic_stimulus(central_lambda, lambdas, width, max_radiance, background):
    """
    Generates a quasi-monochromatic spectrum. Gaussian centered in central lambda with desired width and peak on max_radiance over a background.
    """
    spectrum = (max_radiance - background)*np.exp(-(lambdas-central_lambda)**2/width**2) + background
    return spectrum

def norm_spectrum_luminance(lambdas, spectrum, luminance):
    """
    Normalize a spectrum with a desired luminance. Returns the original luminance and the new lambdas and normalized spectrum after the interpolation.
    """
    V_l = T_lambda[:,2]
    lambdas_Y = T_lambda[:,0]

    min_abs, max_abs = np.min(np.concatenate([lambdas_Y, lambdas])), np.max(np.concatenate([lambdas_Y, lambdas]))
    new_lambda = np.arange(min_abs, max_abs, 1)

    f_spectrum = interpolate.interp1d(lambdas, spectrum, bounds_error=False, fill_value=(spectrum[0],spectrum[-1]))
    interpol_spectrum = f_spectrum(new_lambda)
    f_V_l = interpolate.interp1d(lambdas_Y, V_l, bounds_error=False, fill_value=(V_l[0],V_l[-1]))
    interpol_V_l = f_V_l(new_lambda)

    Y = km*integrate.trapezoid(interpol_spectrum*interpol_V_l, new_lambda, 1)

    interpol_spectrum = luminance * interpol_spectrum/Y
    return Y, new_lambda, interpol_spectrum