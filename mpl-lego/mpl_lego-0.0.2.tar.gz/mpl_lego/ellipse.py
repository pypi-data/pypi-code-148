import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import numpy as np

from matplotlib.patches import Ellipse


def plot_cov_ellipse(cov, mu=None, ax=None, n_std=2.0, include_mu=False,
                     mu_color=None, **kwargs):
    """Plots a 2-d covariance matrix as an ellipse on a set of axes.

    Parameters
    ----------
    cov : np.ndarray, shape (2, 2)
        The covariance matrix.
    mu : np.ndarray, shape (2,)
        The center of the covariance matrix, if desired.
    ax : matplotlib axis
        The axis on which to plot the covariance ellipse. If None, a new one
        will be created.
    **kwargs : keyword arguments
        Arguments for the ellipse artist.

    Returns
    -------
    ax : matplotlib axis
        The axis on which the ellipse is plotted.
    """
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(5, 5))

    if mu is None:
        mu_x = 0.
        mu_y = 0.
    else:
        mu_x, mu_y = mu

    pearson = cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    scale_x = np.sqrt(cov[0, 0]) * n_std
    scale_y = np.sqrt(cov[1, 1]) * n_std
    transform = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mu_x, mu_y)

    ellipse = Ellipse(
        xy=(0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        **kwargs)
    ellipse.set_transform(transform + ax.transData)
    if include_mu:
        ax.scatter(mu[0], mu[1], color=mu_color)
    ax.add_patch(ellipse)
    return ax
