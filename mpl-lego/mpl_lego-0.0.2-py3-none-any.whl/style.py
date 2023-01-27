import matplotlib.pyplot as plt
import warnings


from distutils.spawn import find_executable


def check_latex_style_on():
    """Checks whether LaTeX style has been turned on."""
    return plt.rcParams.get('text.usetex')


def use_latex_style(check_latex=True):
    """Use a style that uses Computer Modern font and LaTeX for mathtype.

    Parameters
    ----------
    check_latex : bool
        If True, checks whether LaTeX exists on the machine. If False, this
        safety check is overridden, and LaTeX style is turned on regardless.
        Turning this off may result in errors if LaTeX is not installed
        properly on the system.
    """
    # Check whether LaTeX is available on the machine
    if check_latex and find_executable('latex'):
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "font.sans-serif": ["Computer Modern Roman"]})
    else:
        # LaTeX is not available on this machine; raise warning
        warnings.warn("LaTeX not found on this machine. Falling back on default RC parameters.", RuntimeWarning)
