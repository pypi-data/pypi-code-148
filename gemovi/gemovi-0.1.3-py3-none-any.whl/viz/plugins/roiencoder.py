from __future__ import annotations

import typing as t

import pyqtgraph as pg

from gemovi.common.utils import tensor_to_np
from gemovi.viz.plugins import GenerativeEncoderTabPlugin

if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab


class ROIEncoderPlugin(GenerativeEncoderTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.encoded_roi = self.register_item(
            pg.CircleROI((0, 0), radius=0.1, pen="r", movable=False), hide=True
        )

        while self.encoded_roi.handles:
            self.encoded_roi.removeHandle(0)

        # Not featureful enough yet to be worth exposing
        # tab.register_selection_listener(self.encode_sample_listener, enabled=False)

    def encode_sample_listener(self, sample_indexes: list[int]):
        if (
            not len(sample_indexes)
            or (image := self.tab.get_index_as_image(sample_indexes[0])) is None
        ):
            self.encoded_roi.hide()
            return
        self.encoded_roi.show()
        input_image = self.tab.image_as_normed_tensor(image)
        xdim, ydim = self.tab.xdim, self.tab.ydim

        mu, std = self.tab.forward_encoder(input_image)
        mu_xform = self.tab.dim_transformer.transform(mu).view(-1)
        std_xform = self.tab.dim_transformer.transform(std).view(-1)
        self.encoded_roi.setSize(tuple(tensor_to_np(std_xform[[xdim, ydim]])))
        new_pos = tensor_to_np(mu_xform[[xdim, ydim]])
        self.encoded_roi.setPos(pg.Point(*new_pos) - self.encoded_roi.size() / 2)
