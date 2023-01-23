from __future__ import annotations

import functools
import typing as t

import numpy as np
import pyqtgraph as pg
import torch
from pyqtgraph import QtCore
from qtextras import (
    ParameterContainer,
    ParameterEditor,
    RunOptions,
    bindInteractorOptions as bind,
    widgets,
)

from gemovi.common.utils import tensor_to_np
from gemovi.viz.plugins import GenerativeEncoderTabPlugin, _mkspec
from gemovi.viz.plugins.helpers import NumberedItemContainer

if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab


class ReencodingPlugin(GenerativeEncoderTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.plot_widget = tab.plot_widget
        self.arrow_item_group = self.register_item(NumberedItemContainer(pg.ArrowItem))
        self.arrow_properties = ParameterContainer()
        self.reencoding_properties = ParameterContainer()
        self.window_handle = None
        self.n_encodings = 10

        tab.register_selection_listener(self.reencoding_trail_listener, enabled=False)

    def multiple_encode(self):
        """
        Opens a dialog allowing the user to reencode the selected samples multiple times
        and observe trends in differential error
        """
        if not (image := self.tab.get_index_as_image()):
            return
        image_tensor = self.tab.image_as_normed_tensor(image)

        layout = pg.GraphicsLayout()
        view = pg.GraphicsView()
        view.setCentralItem(layout)

        ref_vb = layout.addViewBox(row=0, col=0, lockAspect=True)
        ref_img = pg.ImageItem(np.array(image))
        ref_vb.addItem(ref_img)

        encoded_vb = layout.addViewBox(row=0, col=1, lockAspect=True)
        encoded_img = pg.ImageItem(ref_img.image)
        encoded_vb.addItem(encoded_img)
        err_plot = layout.addPlot(row=1, col=0, colspan=2)
        err_curve = pg.PlotCurveItem(pen="r", width=3)
        err_plot.addItem(err_curve)

        @functools.lru_cache(maxsize=30)
        def cached_encode(n=0):
            diffs = []
            if n <= 0:
                return diffs, image_tensor
            diffs, prev_image = cached_encode(n - 1)
            mu, _ = self.tab.forward_encoder(prev_image)
            next_image = self.tab.forward(mu)
            diffs = diffs.copy()
            diffs.append(torch.abs(next_image - prev_image).sum().item())
            return diffs, next_image

        def encode_decode(n=0):
            """
            Encodes and decodes the image n times, plotting the error at each step

            Parameters
            ----------
            n
                Number of times to encode and decode the image
            """
            diffs, encoded_tensor = cached_encode(n)
            image_np = tensor_to_np(encoded_tensor[0]).transpose((1, 2, 0))
            encoded_img.setImage(image_np)
            err_curve.setData(np.arange(n), diffs)
            err_plot.autoRange()

        editor = ParameterEditor()
        editor.registerFunction(encode_decode, runOptions=RunOptions.ON_CHANGED)

        window = widgets.EasyWidget.buildWidget([view, editor], "H", useSplitter=True)
        window.show()
        window.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.window_handle = window

    def reencoding_trail_listener(self, sample_indexes: list[int]):
        if len(sample_indexes):
            sample_indexes = [sample_indexes[0]]
        self.make_reencoding_arrow_trail(
            **self.reencoding_properties, sample_indexes=sample_indexes
        )

    def make_reencoding_arrow_trail(
        self, sample_indexes: list[int], n_encodings: int, batch_size=16
    ):
        """
        Creates a trail of arrows showing the path of a sample as it is progressively
        encoded and decoded

        Parameters
        ----------
        sample_indexes
            Indexes of the samples to encode/decode
        n_encodings
            Number of times to encode/decode the sample
        batch_size
            When many samples are specified, pytorch can run out of error attempting
            to get all encoding trails at once. This parameter controls how many
            samples are encoded at once, but has no impact on the final output other
            than computing efficiency.
        """
        samples = self.tab.samples
        if samples is None or n_encodings <= 0 or not len(sample_indexes):
            self.arrow_item_group.ensure_n_items(0)
            return
        samples = samples[sample_indexes]

        batch_size = min(batch_size, len(samples))

        all_trail_locations = np.empty(
            (len(samples), n_encodings + 1, 2), dtype=np.float32
        )
        for batch_start in range(0, len(samples), batch_size):
            batch = samples[batch_start : batch_start + batch_size]
            batch_end = batch_start + len(batch)
            for ii in range(n_encodings):
                cur_locations = self.tab.dim_transformer.transform(batch)[
                    :, [self.tab.xdim, self.tab.ydim]
                ]
                all_trail_locations[batch_start:batch_end, ii] = tensor_to_np(
                    cur_locations
                )
                images = self.tab.forward(batch)
                batch, _ = self.tab.forward_encoder(images)
            # Add last batch
            cur_locations = self.tab.dim_transformer.transform(batch)[
                :, [self.tab.xdim, self.tab.ydim]
            ]
            all_trail_locations[batch_start:batch_end, -1] = tensor_to_np(cur_locations)

        # Diff is approximate_n_samples x n_encodings x 2
        diffs = np.diff(all_trail_locations, axis=1)
        # Make arrow items pointing in diff direction, length proportional to diff
        angles = np.arctan2(diffs[:, :, 1], diffs[:, :, 0])
        # 0 degrees points left in arrow item, but we want it to point right
        angles = 180 + np.rad2deg(angles)
        lengths = np.linalg.norm(diffs, axis=2)

        default_properties = dict(
            pxMode=False, headLen=0.05, tailWidth=0.01, **self.arrow_properties
        )
        angles = angles.ravel()
        # Tail length is independent of head length, so subtract it to keep arrows
        # ending at the right place
        lengths = lengths.ravel() - default_properties["headLen"]
        all_trail_locations = all_trail_locations[:, 1:, :].reshape(-1, 2)
        self.arrow_item_group.ensure_n_items(len(angles))

        for arrow, pos, angle, tailLength in zip(
            self.arrow_item_group, all_trail_locations, angles, lengths
        ):
            arrow.setPos(*pos)
            arrow.setStyle(**default_properties, angle=angle, tailLen=tailLength)

        return all_trail_locations

    @bind(brush=_mkspec("color"), pen=_mkspec("pen", expanded=False))
    def update_arrow_properties(self, brush="b", pen="w"):
        """
        Change the appearance of reencoding arrows

        Parameters
        ----------
        brush
            Arrow brush color
        pen
            Arrow pen color
        """
        for arrow in self.arrow_item_group:
            arrow.setBrush(pg.mkBrush(brush))
            arrow.setPen(pg.mkPen(pen))

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.multiple_encode)
        editor.registerFunction(
            self.random_reencoding_trails, container=self.reencoding_properties
        )
        self.reencoding_properties.pop("n_samples")
        editor.registerFunction(
            self.update_arrow_properties,
            runOptions=RunOptions.ON_CHANGED,
            container=self.arrow_properties,
        )

    def random_reencoding_trails(self, n_encodings=10, n_samples=100):
        """
        Create reencoding trails for a random sample of the data

        Parameters
        ----------
        n_encodings
            Number of times to encode/decode the sample
        n_samples
            Number of samples to encode/decode
        """
        if self.tab.samples is None:
            return
        n_samples = min(n_samples, len(self.tab.samples))
        n_samples = max(0, n_samples)
        sample_indexes = np.random.choice(
            len(self.tab.samples), n_samples, replace=False
        )
        self.make_reencoding_arrow_trail(
            n_encodings=n_encodings, sample_indexes=sample_indexes
        )
