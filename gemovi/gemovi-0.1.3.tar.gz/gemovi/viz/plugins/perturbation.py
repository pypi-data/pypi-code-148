from __future__ import annotations

import typing as t

import numpy as np
import pyqtgraph as pg
import torch
from qtextras import ParameterEditor, RunOptions, bindInteractorOptions as bind, fns
from scipy import stats

from gemovi.viz.plugins import GenerativeTabPlugin, _colormap_spec, _mkspec, device

if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab


class PerturbationPlugin(GenerativeTabPlugin):
    mapping_granularity = 0.05

    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.gaus_overlay_item = self.register_item(pg.ImageItem())
        self.gaus_overlay_item.setZValue(-10)
        self.gaus_overlay_item.setOpacity(0.75)
        self.gaus_overlay_item.setColorMap("inferno")
        self.create_uniform_map()

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.create_uniform_map)
        editor.registerFunction(self.create_perturbation_map)
        editor.registerFunction(
            self.update_overlay_properties, runOptions=RunOptions.ON_CHANGED
        )

    @bind(granularity=_mkspec("float", limits=(0.01, 0.5)), colormap=_colormap_spec)
    def update_overlay_properties(self, granularity=0.05, colormap="inferno"):
        """
        Updates the properties of the overlay image and perturbation resolution

        Parameters
        ----------
        granularity
            When creating perturbation maps, this is the granularity of the mapping,
            i.e., how much resolution should be applied when samplng points in the
            latent space. The lower the value, the higher the resolution, but the
            longer it will take to create the map.
        colormap
            The colormap to use for the perturbation map image
        """
        self.mapping_granularity = granularity
        if isinstance(colormap, str):
            colormap = fns.getAnyPgColormap(colormap, forceExist=True)
        self.gaus_overlay_item.setColorMap(colormap)

    def create_perturbation_map(self, n_samples=100, standard_deviations=3):
        """
        Creates a map of how strongly minor changes in the currently viewed dimensions
        affect the generated image.

        Parameters
        ----------
        n_samples
            Number of samples to use for each point in the map
        standard_deviations
            How many standard deviations to use for the gaussian perturbation
        """
        samples = (
            torch.rand(n_samples, self.tab.get_num_latent_dims(), device=device)
            * standard_deviations
            - standard_deviations / 2
        )
        base_pred = self.tab.forward(samples).detach()
        check_space = torch.linspace(
            -1, 1, int(1 / self.mapping_granularity), device=device
        )
        dy, dx = torch.meshgrid(check_space, check_space, indexing="ij")
        dx_vec = dx.reshape(-1)
        dy_vec = dy.reshape(-1)
        map_xy = np.arange(
            -standard_deviations, standard_deviations, self.mapping_granularity
        )
        out_map = np.zeros((len(map_xy), len(map_xy)), dtype=np.float32)
        for ii, sample in enumerate(samples):
            # TODO: Tile somehow to get shapes broadcastable without inplace update
            batch = sample.unsqueeze(0).expand(dx_vec.size(0), *sample.shape)
            # Clone for in-place operations
            batch = batch.clone()
            batch[:, self.tab.xdim] += dx_vec
            batch[:, self.tab.ydim] += dy_vec
            pred = self.tab.forward(batch).detach()
            ref = base_pred[ii]
            diff = torch.abs(pred - ref).view(len(dx_vec), -1).mean(dim=1).cpu().numpy()
            # Find out which output locations should be updated
            xy_batch = (
                batch[:, [self.tab.xdim, self.tab.ydim]].cpu().numpy().reshape(-1, 2)
            )
            x_idxs = np.searchsorted(map_xy, xy_batch[:, 0])
            y_idxs = np.searchsorted(map_xy, xy_batch[:, 1])
            # f = interpolate.interp2d(xy_batch[:, 0], xy_batch[:, 1], diff, kind="cubic")
            x_interp = np.interp(map_xy[x_idxs], xy_batch[:, 0], diff)
            y_interp = np.interp(map_xy[y_idxs], xy_batch[:, 1], diff)
            out_map[y_idxs, x_idxs] += (x_interp + y_interp) / 2
        self.gaus_overlay_item.setImage(
            out_map,
            rect=(
                -standard_deviations,
                -standard_deviations,
                standard_deviations * 2,
                standard_deviations * 2,
            ),
        )

    def create_uniform_map(self, standard_deviations=5):
        """
        Displays a simple 0-mean, unit-variance gaussian distribution over the latent
        space. This is useful to visually calibrate where samples lie relative to
        the expected latent space distribution.

        Parameters
        ----------
        standard_deviations
            How many standard deviations to show in the displayed image
        """
        # Shorten name for brevity below
        std_devs = standard_deviations
        gran = self.mapping_granularity
        yy, xx = np.mgrid[-std_devs:std_devs:gran, -std_devs:std_devs:gran]
        gaus_data = stats.norm.pdf(yy) * stats.norm.pdf(xx)
        self.gaus_overlay_item.setImage(
            gaus_data,
            rect=(-std_devs, -std_devs, std_devs * 2, std_devs * 2),
        )
