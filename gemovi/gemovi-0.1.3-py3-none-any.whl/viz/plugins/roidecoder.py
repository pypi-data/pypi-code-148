from __future__ import annotations

import itertools
import typing as t

import numpy as np
import pyqtgraph as pg
import torch
from pyqtgraph import QtCore
from pyqtgraph.parametertree import InteractiveFunction
from qtextras import ParameterEditor, bindInteractorOptions as bind, fns

from gemovi.common.utils import tensor_to_np
from gemovi.viz.plugins import GenerativeTabPlugin
from gemovi.viz.plugins.helpers import NumberedItemContainer

if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab
__all__ = [
    "AreaROIHelper",
    "ImageROIHelper",
    "ImagePerimeterROI",
    "ImageFilledROI",
    "PerimeterROIHelper",
    "ROIDecoderPlugin",
]


class ROIDecoderPlugin(GenerativeTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.plot_widget = tab.plot_widget

        self.area_roi_helper = AreaROIHelper(tab)
        self.perimeter_roi_helper = PerimeterROIHelper(tab)

    def register_functions(self, editor: ParameterEditor):
        for helper in self.area_roi_helper, self.perimeter_roi_helper:
            editor.registerFunction(helper.interactive_decode_samples)


class ImageFilledROI(QtCore.QObject):
    sig_image_positions_changed = QtCore.Signal()

    def __init__(self, plot_widget: pg.PlotWidget):
        super().__init__()
        self.plot_widget = plot_widget
        self.roi_item = self._make_roi()
        self.image_group = NumberedItemContainer(pg.ImageItem, parent=self.roi_item)
        self.spacing = []
        self._region_change_approximate_n_samples = 0

    def _make_roi(self):
        roi = pg.RectROI((0, 0), (3, 3), pen="k")
        self.plot_widget.addItem(roi)
        roi.setZValue(11)
        while roi.getHandles():
            roi.removeHandle(0)
        # Add abundance of handles on all sides
        for handle_x, handle_y in itertools.product(*[[0, 0.5, 1]] * 2):
            if handle_x == handle_y == 0.5:
                continue
            roi.addScaleHandle([handle_x, handle_y], [1 - handle_x, 1 - handle_y])
        return roi

    def hide(self):
        self.roi_item.hide()

    def show(self):
        self.roi_item.show()

    def get_image_items(self, approximate_n_samples: int):
        positions = self.get_image_positioning(approximate_n_samples - 1)
        if len(positions) <= 1:
            return

        self.image_group.ensure_n_items(len(positions))

        for img_item, grid_pt in zip(self.image_group, positions):
            img_item.setPos(*grid_pt)

        return self.image_group

    def set_image_data(self, image_data: t.Sequence[np.ndarray]):
        for img_item, img_data, spacing in zip(
            self.image_group, image_data, self.spacing
        ):
            img_item.setImage(img_data, rect=(0, 0, *spacing))

    def get_image_positioning(self, n_samples: int) -> np.ndarray:
        """
        Determine the positions of the images in the ROI, and set self's state
        with relevant positioning metadata such as spacing, etc.

        For a rect ROI, solve the system of equations:

        * nx * ny = approximate_n_samples
        * x spacing = width / nx
        * y spacing = height / ny
        * x spacing = y spacing

        -> nx = approximate_n_samples * sqrt(width / (height * approximate_n_samples))
        -> ny = sqrt(approximate_n_samples * height / width)
        """
        # Items use the roi as their parent, so (0,0) is their origin
        top_left_xy, width_height = pg.Point(0, 0), self.roi_item.size()
        if n_samples < 1:
            self.spacing = []
            return np.empty((0, 2))
        nx = n_samples * np.sqrt(width_height[0] / (width_height[1] * n_samples))
        ny = np.sqrt(n_samples * width_height[1] / width_height[0])
        bottom_right_xy = np.array(top_left_xy) + width_height
        spacing_x = width_height[0] / nx
        spacing_y = width_height[1] / ny
        x_pos, y_pos = np.meshgrid(
            np.arange(top_left_xy[0], bottom_right_xy[0], spacing_x),
            np.arange(top_left_xy[1], bottom_right_xy[1], spacing_y),
        )
        positions = np.column_stack([x_pos.ravel(), y_pos.ravel()])
        self.spacing = [(spacing_x, spacing_y)] * len(positions)
        return positions

    def change_images_with_roi(self, update_on_changing=True, approximate_n_samples=0):
        self.set_listening_for_changes(update_on_changing=update_on_changing)
        self._region_change_approximate_n_samples = approximate_n_samples

    def on_region_changed(self):
        self.get_image_items(self._region_change_approximate_n_samples)
        self.sig_image_positions_changed.emit()

    def set_listening_for_changes(self, listening=True, update_on_changing=True):
        signals = [
            self.roi_item.sigRegionChanged,
            self.roi_item.sigRegionChangeFinished,
        ]
        for signal in signals:
            pg.disconnect(signal, self.on_region_changed)
        if not listening:
            return
        connect_idx = 0 if update_on_changing else 1
        signals[connect_idx].connect(self.on_region_changed)


class ImagePerimeterROI(ImageFilledROI):
    number_points_per_handle: list[int]
    roi_item: pg.PolyLineROI

    def _make_roi(self):
        roi = pg.PolyLineROI(
            [], pen="k", movable=False, resizable=False, rotatable=False, closed=True
        )
        roi.handleSize = 1
        # Don't split segment when clicked
        roi.segmentClicked = lambda *args, **kwargs: None
        self.plot_widget.addItem(roi)
        roi.setZValue(11)
        return roi

    def get_image_positioning(self, n_samples: int) -> np.ndarray:
        side_lengths = []
        handles = self.roi_item.getHandles()
        num_sides = len(handles) - 1
        for handle_idx in range(num_sides):
            start = handles[handle_idx].pos()
            end = handles[handle_idx + 1].pos()
            side_lengths.append(np.linalg.norm(np.array(start) - np.array(end)))

        positions, spacings, interp_idxs, pts_per_handle = [], [], [], []
        total_length = sum(side_lengths)

        for handle_idx in range(num_sides):
            n_pts = int(n_samples * side_lengths[handle_idx] / total_length)
            n_pts = max(n_pts, 1)
            pts_per_handle.append(n_pts)
            start_pos = handles[handle_idx].pos()
            end_pos = handles[handle_idx + 1].pos()
            new_positions = np.linspace(start_pos, end_pos, n_pts)
            positions.extend(new_positions)
            spacing_hw = [side_lengths[handle_idx] / n_pts] * 2
            spacings.extend([spacing_hw] * len(new_positions))
        positions = np.array(positions)
        self.spacing = np.array(spacings)
        self.number_points_per_handle = pts_per_handle
        return positions


class ImageROIHelper:
    """
    Contains a few helpful methods to allow code reuse between perimeter/area
    ROI management
    """

    registration_prefix = ""

    def __init__(self, tab: GenerativeTab, roi_class: t.Type[ImageFilledROI]):
        super().__init__()
        self.roi = roi_class(tab.plot_widget)
        self.roi.sig_image_positions_changed.connect(self.update_roi_contents)
        self.roi.hide()
        self.sample_indexes = []

        self.tab = tab
        self._interactive_selection_listener = InteractiveFunction(
            self.selection_listener
        )
        name = f"{self.registration_prefix}_decode_listener"
        self._interactive_selection_listener.__name__ = name

        tab.sig_samples_selected.connect(self.on_samples_selected)
        tab.register_selection_listener(
            self._interactive_selection_listener, enabled=False
        )

        self.interactive_decode_samples = InteractiveFunction(self.decode_samples)
        name = f"{self.registration_prefix}_decode_samples"
        self.interactive_decode_samples.__name__ = name

    def on_samples_selected(self, sample_indexes: list[int]):
        # Get a slice with just the top sample intead of scalar indexing
        # to avoid length checking for empty values
        use_range = sample_indexes[0:1]
        if self.sample_indexes[-1:] == use_range:
            return
        self.sample_indexes.extend(use_range)

    @bind(sample_indexes=dict(ignore=True))
    def decode_samples(
        self,
        sample_indexes: list[int] | None = None,
        n_images=50,
        update_on_changing=True,
    ):
        """
        Decode the selected sample and a surrounding set of points.

        The grid is filled with approximately ``n_samples`` points and spaced
        in proportion to how the rectangular ROI is scaled.

        Parameters
        ----------
        sample_indexes
            The index of the sample to decode. If None, the last selected sample
            is used.
        n_images
            The approximate number of samples to decode. The actual number of samples
            may be slightly different to ensure the grid is totally filled.
        update_on_changing
            If ``True``, the decoding will be updated as the ROI is moved or resized.
            Otherwise, the decoding will only be updated when the ROI is released.
        """
        if sample_indexes is None:
            sample_indexes = self.sample_indexes
        else:
            self.sample_indexes = sample_indexes
        if not len(sample_indexes):
            n_images = 0

        n_images = max(n_images, 0)
        self.roi.change_images_with_roi(update_on_changing, n_images)
        if n_images <= 0:
            self.roi.hide()
            return

        self._init_decoding_roi()
        self.roi.show()
        self.update_roi_contents()

    def get_transformed_selected_samples(
        self,
        flatten=False,
        xy_dims_only=False,
    ):
        sample_indexes = self.sample_indexes
        if flatten and len(sample_indexes) != 1:
            raise ValueError(
                f"Cannot flatten unless exactly one sample is selected, got "
                f"{len(sample_indexes)}"
            )
        decoded = self.tab.get_transformed_samples(sample_indexes)
        if xy_dims_only:
            decoded = decoded[:, [self.tab.xdim, self.tab.ydim]]
        if flatten:
            decoded = decoded[0]
        return decoded

    def get_image_data(self) -> t.Sequence[np.ndarray]:
        raise NotImplementedError

    def _init_decoding_roi(self):
        raise NotImplementedError

    def update_roi_contents(self):
        if not self.roi.roi_item.isVisible() or not len(self.sample_indexes):
            return
        self.roi.set_image_data(self.get_image_data())

    def selection_listener(self, sample_indexes: list[int]):
        if not len(sample_indexes):
            self.sample_indexes.clear()
        self.interactive_decode_samples()

    def images_from_transformed_samples(self, transformed_samples):
        samples = self.tab.dim_transformer.inverse_transform(
            transformed_samples
        ).type_as(self.tab.samples)
        pred = self.tab.forward(samples)
        pred_imgs = tensor_to_np(pred).transpose((0, 2, 3, 1))
        return pred_imgs


class AreaROIHelper(ImageROIHelper):
    registration_prefix = "area"

    def __init__(self, tab: GenerativeTab, roi_class=ImageFilledROI):
        super().__init__(tab, roi_class)

    def get_image_data(
        self,
    ):
        items = self.roi.image_group
        origin = np.array(self.roi.roi_item.pos())
        positions = torch.tensor(
            np.row_stack([item.pos() for item in items]) + origin,
            dtype=self.tab.samples.dtype,
        )
        xformed = (
            self.get_transformed_selected_samples()
            .broadcast_to(len(positions), -1)
            .clone()
        )
        xformed[:, self.tab.xdim] = positions[:, 0]
        xformed[:, self.tab.ydim] = positions[:, 1]
        return self.images_from_transformed_samples(xformed)

    def on_samples_selected(self, sample_indexes: list[int]):
        super().on_samples_selected(sample_indexes)
        # Ensure at most one point is kept
        if len(self.sample_indexes) > 1:
            self.sample_indexes = self.sample_indexes[-1:]

    def _init_decoding_roi(self):
        xformed_xy = tensor_to_np(
            self.get_transformed_selected_samples(flatten=True, xy_dims_only=True)
        )
        roi_size = np.array(self.roi.roi_item.size())
        new_roi_pos = xformed_xy - roi_size / 2
        self.roi.roi_item.setPos(new_roi_pos)


class PerimeterROIHelper(ImageROIHelper):
    registration_prefix = "perimeter"
    roi: ImagePerimeterROI

    def __init__(self, tab: GenerativeTab, roi_class=ImagePerimeterROI):
        super().__init__(tab, roi_class)

    def _init_decoding_roi(self):
        xformed_xy = tensor_to_np(
            self.get_transformed_selected_samples(xy_dims_only=True)
        )
        with fns.makeDummySignal(self.roi, "sig_image_positions_changed"):
            self.roi.roi_item.setPoints(xformed_xy, closed=False)

    def get_image_data(self) -> t.Sequence[np.ndarray]:
        tformed_samples = tensor_to_np(self.get_transformed_selected_samples())
        samples_for_images = []
        for ii, n_pts in enumerate(self.roi.number_points_per_handle):
            interp_info = np.linspace(
                tformed_samples[ii], tformed_samples[ii + 1], n_pts
            )
            samples_for_images.extend(interp_info)
        return self.images_from_transformed_samples(np.array(samples_for_images))

    def update_roi_contents(self):
        if len(self.sample_indexes) < 2:
            self.roi.image_group.ensure_n_items(0)
            return
        super().update_roi_contents()

    def on_samples_selected(self, sample_indexes: list[int]):
        use_range = sample_indexes[0:1]
        if self.sample_indexes[-1:] == use_range:
            del self.sample_indexes[-1:]
        else:
            self.sample_indexes.extend(use_range)
