from __future__ import annotations

import typing as t
from pathlib import Path

import numpy as np
import pyqtgraph as pg
from qtextras import (
    ParameterContainer,
    ParameterEditor,
    RunOptions,
    bindInteractorOptions as bind,
    fns,
)

from gemovi.common.utils import tensor_to_np, to_pil_image
from gemovi.viz.plugins import GenerativeTabPlugin, _colormap_spec, _mkspec
from gemovi.viz.plugins.helpers import (
    UNSET,
    NumberedItemContainer,
    PixelSizedImageItem,
    TooltipData,
)

if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab


class ScatterplotPlugin(GenerativeTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.scatterplot = self.register_item(
            pg.ScatterPlotItem(brush=None, pen="w", hoverable=True, tip=None)
        )
        self.image_plot_group = self.register_item(
            NumberedItemContainer(PixelSizedImageItem), hide=True
        )
        self.image_group_needs_update = True
        self.scatterplot_properties = ParameterContainer()
        self.image_plot_properties = ParameterContainer()
        self.colormap = pg.colormap.get("plasma")

        for signal in tab.sig_samples_changed, tab.sig_transformer_changed:
            signal.connect(self.on_samples_or_transformer_changed)

        self.scatterplot.sigHovered.connect(self.on_scatter_hover)
        self.scatterplot.sigClicked.connect(self.on_scatter_click)

    def on_samples_or_transformer_changed(self):
        self.plot_samples()

    def plot_samples(self):
        def img_getter(idx: int):
            info = self.tab.samples_info
            if info.image_files and info.image_files[idx]:
                image = info.image_files[idx]
            else:
                image = self.tab.forward(self.tab.samples[idx].unsqueeze(0))[0]
            return to_pil_image(image)

        s_info = self.tab.samples_info
        if s_info.image_files is not None:
            names = [Path(f).name for f in s_info.image_files]
        else:
            names = [f"Sample {ii}" for ii in range(len(s_info.samples))]
        user_data = [
            TooltipData(name=name, image_data=ii, image_read_function=img_getter)
            for ii, name in enumerate(names)
        ]
        tformed = tensor_to_np(
            self.tab.get_transformed_samples()[:, [self.tab.xdim, self.tab.ydim]]
        )
        brushes = None
        if s_info.numeric_labels is not None:
            brushes = self.colormap.map(s_info.numeric_labels)

        props = self.scatterplot_properties
        self.scatterplot.setData(
            tformed[:, 0],
            tformed[:, 1],
            data=user_data,
            brush=brushes,
            pen=props["pen"],
            pxMode=props["pixel_mode"],
            size=props["size"],
        )
        self.image_group_needs_update = True
        if self.image_plot_group.isVisible():
            self.update_image_group()

    def on_scatter_hover(self, item, points, _evt):
        if not len(points):
            item.setToolTip(None)
            return
        tooltip: TooltipData = points[0].data()
        if tooltip.label is None:
            numeric_lbl = self.tab.numeric_labels[points[0].index()]
            tooltip.label = self.tab.samples_info.number_label_map[numeric_lbl]
        item.setToolTip(tooltip.to_html())

    def on_scatter_click(self, _item, points, _evt):
        indexes = [p.index() for p in points]
        self.tab.update_selected_samples(indexes)

    def on_image_click(self, item, _evt):
        self.tab.update_selected_samples(
            [self.image_plot_group.childItems().index(item)]
        )

    @bind(colormap=_colormap_spec, pen=_mkspec("pen", expanded=False))
    def update_scatterplot_properties(
        self, colormap="plasma", pen="w", size=15.0, pixel_mode=True  # noqa
    ):
        """
        Change the scatterplot's appearance. Note that `colormap` is also recycled
        by image plots (if they are active) to color their border.

        Parameters
        ----------
        colormap
            The name of the colormap to use for coloring the scatterplot points
        pen
            The pen to use for drawing the scatterplot point borders
        size
            The size of the scatterplot points. Note this is in screen pixels
            when `pixel_mode` is True, and in data units when `pixel_mode` is False.
        pixel_mode
            Whether to draw the scatterplot points in screen pixels or in data units
        """
        self.colormap = fns.getAnyPgColormap(colormap, forceExist=True)
        # Properties are captured by `self.scatterplot_properties`, so no need
        # to do anything here other than set colormap and replot. Noqa above to avoid
        # unused argument warning.
        self.plot_samples()

    def update_image_plot_properties(self, image_size=64, border_thickness=0):  # noqa
        """
        Change the appearance of the image plots when they are active

        Parameters
        ----------
        image_size
            The size of each image item in screen pixels
        border_thickness
            How thick the border around each image item should be
        """
        # Properties are captured by `self.image_plot_properties`, so no need
        # to do anything here other than request a replot. Hence, noqa above.
        self.image_group_needs_update = True
        if self.image_plot_group.isVisible():
            self.update_image_group(image_size)

    def set_active_plots(self, image_plots=False, scatterplot=True):
        """
        Set whether the image plots, scatterplot, or both are active. Note the first
        time an image plot is activated, it might delay a bit while the images are
        loaded.

        Parameters
        ----------
        image_plots
            Whether to show the image plots
        scatterplot
            Whether to show the scatterplot
        """
        # Images might be costly to compute, so only do this when previously not
        # shown and the data has changed
        self.image_plot_group.setVisible(image_plots)
        self.scatterplot.setVisible(scatterplot)

        if self.image_plot_group.isVisible() and self.image_group_needs_update:
            self.update_image_group()

    def update_image_group(
        self,
        image_size: int | tuple[int, int] | t.Type[UNSET] | None = UNSET,
        border_thickness=UNSET,
    ):
        if image_size is UNSET:
            image_size = self.image_plot_properties["image_size"]
        if border_thickness is UNSET:
            border_thickness = self.image_plot_properties["border_thickness"]
        if isinstance(image_size, int):
            image_size = (image_size, image_size)

        spots: list[pg.SpotItem] = self.scatterplot.points()
        added = self.image_plot_group.ensure_n_items(len(spots))["added"]
        for item in added:
            item.sig_clicked.connect(self.on_image_click)
            item.setPxMode(True)

        for item, spot in zip(self.image_plot_group, spots):
            tooltip: TooltipData = spot.data()
            # False positive on "asarray"
            image = np.asarray(tooltip.evaluate_image_data(tuple(image_size)))  # noqa
            image_xy = spot.pos()
            item.setImage(
                image,
                border=pg.mkPen(color=spot.brush().color(), width=border_thickness),
            )
            if image_size is not None:
                item.setRect(0, 0, *image_size)
            item.setPos(*image_xy)
        self.image_group_needs_update = False

    def register_functions(self, editor: ParameterEditor):
        with editor.defaultInteractor.optsContext(runOptions=RunOptions.ON_CHANGED):
            editor.registerFunction(
                self.update_scatterplot_properties,
                container=self.scatterplot_properties,
            )
            editor.registerFunction(
                self.update_image_plot_properties, container=self.image_plot_properties
            )
            editor.registerFunction(self.set_active_plots)
