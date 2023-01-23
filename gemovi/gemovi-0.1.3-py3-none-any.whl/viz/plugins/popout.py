from __future__ import annotations

import typing as t

import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtCore
from pyqtgraph.parametertree import RunOptions
from qtextras import ParameterContainer, ParameterEditor, bindInteractorOptions as bind

from gemovi.common.utils import disconnected_signal, tensor_to_np
from gemovi.viz.plugins import GenerativeTabPlugin
from gemovi.viz.plugins.helpers import (
    UNSET,
    ImageSizeType,
    NumberedItemContainer,
    PixelSizedImageItem,
    closest_point_on_line,
)

if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab


def upsample_polygon(polygon: np.ndarray, n_points: int = 0):
    """
    Given a set of points, return a new set that is evenly spaced
    """
    # Calculate the cumulative distance along the path
    dist = np.cumsum(np.sqrt(np.sum(np.diff(polygon, axis=0) ** 2, axis=1)))
    dist = np.insert(dist, 0, 0)
    # Interpolate to get the new set of points
    if n_points <= 0:
        new_dist = np.arange(len(dist))
    else:
        new_dist = np.linspace(0, dist[-1], n_points)
    new_vertices = np.column_stack(
        [
            np.interp(new_dist, dist, polygon[:, 0]),
            np.interp(new_dist, dist, polygon[:, 1]),
        ]
    )
    return new_vertices


class TargetPathLoop:
    def __init__(self, target_item: pg.TargetItem, roi_class=pg.EllipseROI):
        self.target_item = target_item
        self.roi = roi_class((0, 0), (3, 3))
        self.timer = QtCore.QTimer()
        self.current_index = 0
        self.timer.timeout.connect(self.update_loop)
        self.vertices = np.array([[]], dtype=int)
        self.roi.hide()

    @bind(reset=dict(ignore=True))
    def start_loop(self, *, n_points=100, duration_s=3.0, reset=False):
        if not self.target_item.isVisible():
            return
        roi = self.roi
        vertices = self.get_roi_vertices()
        if reset:
            self.stop_loop()
            # There is an offset between the roi shape and it's position (top left)
            # so we need to add that to the target item position as well
            # to place the target item on the roi directly
            closest_index = np.argmin(np.sum(np.abs(vertices - roi.pos()), axis=1))
            origin = vertices[closest_index]
            vertex_pos_offset = origin - roi.pos()
            new_roi_pos = self.target_item.pos() - vertex_pos_offset
            vertex_adjustment = new_roi_pos - roi.pos()
            roi.setPos(new_roi_pos)
            # Update vertices to match new position
            vertices += vertex_adjustment
            roi.sigRegionChanged.connect(
                self.on_roi_move, QtCore.Qt.ConnectionType.UniqueConnection
            )
            self.current_index = 0

        self.roi.show()
        self.vertices = upsample_polygon(vertices, n_points)
        self.timer.start(duration_s * 1000 / len(self.vertices))

    def stop_loop(self):
        pg.disconnect(self.roi.sigRegionChanged, self.on_roi_move)
        self.timer.stop()
        self.vertices = self.vertices[:0]
        self.current_index = 0
        self.roi.hide()

    def update_loop(self):
        if (
            not len(self.vertices)
            or not self.roi.isVisible()
            or not self.target_item.isVisible()
        ):
            self.stop_loop()
            return
        self.current_index = (self.current_index + 1) % len(self.vertices)
        self.target_item.setPos(self.vertices[self.current_index])

    def on_roi_move(self):
        if self.timer.isActive():
            self.start_loop()

    def get_roi_vertices(self):
        roi = self.roi
        roi_poly = roi.shape().toFillPolygon()
        vertices = np.row_stack([(p.x(), p.y()) for p in roi_poly]) + roi.pos()
        # Allow vertex 0 to be closest to pos()
        dist_to_pos = np.sum(np.abs(vertices - roi.pos()), axis=1)
        vertices = np.roll(vertices, -np.argmin(dist_to_pos), axis=0)
        return vertices


class PopoutImageTargetItem(pg.TargetItem):
    def __init__(self, image=None, name=None, sample_index: int = None):
        self.default_label_opts = dict(anchor=(0.5, 1.25), offset=(0, 0))
        super().__init__(label=name, labelOpts=self.default_label_opts)

        self.image_item = PixelSizedImageItem(image)
        self.image_item.setParentItem(self)
        self.image_item.setFlag(self.GraphicsItemFlag.ItemIgnoresParentOpacity, True)

        self.default_image_size: ImageSizeType = None
        self.start_index = sample_index
        self.end_index = sample_index

    def unset_indexes(self):
        self.hide()
        self.start_index = None
        self.end_index = None

    def set_indexes(self, start_index, end_index=None):
        self.start_index = start_index

        if end_index is None:
            end_index = start_index
        self.end_index = end_index

    def set_name(self, name):
        self.setLabel(name, labelOpts=self.default_label_opts)

    def set_image(self, image, image_size=UNSET):
        if image_size is UNSET:
            image_size = self.default_image_size
        self.image_item.setImage(image, shape=image_size)


class PopoutPlugin(GenerativeTabPlugin):
    def __init__(self, tab: GenerativeTab):
        super().__init__(tab)
        self.popout_target = self.register_item(PopoutImageTargetItem(), hide=True)
        self.popout_loop = TargetPathLoop(self.popout_target)
        self.register_item(self.popout_loop.roi, hide=True)

        self.selection_properties = ParameterContainer()

        self.global_popout_group = self.register_item(
            NumberedItemContainer(PopoutImageTargetItem)
        )

        ti = self.popout_target
        ti.setZValue(100)

        self.tab.register_selection_listener(self.popout_selection_listener)
        self.popout_target.sigPositionChanged.connect(self.on_target_move)

    def popout_selection_listener(self, sample_indexes: list[int]):
        if not len(sample_indexes):
            self.popout_target.unset_indexes()
            self.popout_loop.stop_loop()
            self.clear_popout_samples()
            return
        self.popout_target.set_indexes(sample_indexes[0])
        self.popout_target.show()
        xformed = self.tab.get_transformed_samples(sample_indexes[0])
        self.popout_target.setPos(xformed[self.tab.xdim], xformed[self.tab.ydim])
        if self.selection_properties["loop_over_roi"]:
            self.popout_loop.start_loop(reset=True)

    def on_target_move(self, target: PopoutImageTargetItem):
        sample_index = target.start_index
        if sample_index is None:
            return
        selected_sample = self.get_latent_value_at_target(target)
        pred = self.tab.forward(selected_sample)
        pred_imgs = tensor_to_np(pred).transpose((0, 2, 3, 1))
        target.set_image(pred_imgs[0])
        target.set_name(str(sample_index))

    def get_latent_value_at_target(
        self, target: PopoutImageTargetItem, snap_to_line=True
    ):
        samples = self.tab.samples
        idxs = [target.start_index, target.end_index]
        # Avoid duplicating transforming work below when both indexes are the same
        if idxs[0] == idxs[1] or not snap_to_line:
            idxs.pop()

        x, y = target.pos()
        xformed = self.tab.get_transformed_samples(idxs)
        tgt_point = xformed[[0]].clone()
        tgt_point[0, self.tab.xdim] = x
        tgt_point[0, self.tab.ydim] = y

        if len(idxs) == 1:
            return self.tab.dim_transformer.inverse_transform(tgt_point).type_as(
                samples
            )
        else:
            # FIXME: General logic is to interpolate between start and end points,
            #   ensuring along the way that the target lies on the line between the
            #   two points. Logic fails for now, so revisit in the future.
            start_sample, end_sample = [
                tensor_to_np(samples[idx]).reshape(-1, 1) for idx in idxs
            ]
            interped = closest_point_on_line(
                tensor_to_np(tgt_point), start_sample, end_sample
            ).reshape(1, -1)
            x_interp, y_interp = interped[0, self.tab.xdim], interped[0, self.tab.ydim]
            if abs(x_interp - x) + abs(y_interp - y) > 0.1:
                with disconnected_signal(
                    target.sigPositionChanged, self.on_target_move
                ):
                    target.setPos(x_interp, y_interp)
            return self.tab.dim_transformer.inverse_transform(interped).type_as(samples)

    def popout_selected_samples(
        self,
        sample_indexes: list[int],
        image_size: ImageSizeType = None,
        show_targets=True,
    ):
        added = self.global_popout_group.ensure_n_items(len(sample_indexes))["added"]
        for item in added:
            item.sigPositionChanged.connect(self.on_target_move)
        for sample_index, popout in zip(sample_indexes, self.global_popout_group):
            xformed = self.tab.get_transformed_samples(sample_index)
            popout.setPos(xformed[self.tab.xdim], xformed[self.tab.ydim])
            popout.set_indexes(sample_index)
            popout.default_image_size = image_size
            popout.setOpacity(1 if show_targets else 0)
            self.on_target_move(popout)
            popout.show()

    @bind(n_samples=dict(limits=[0, None]), image_size=dict(limits=[2, None]))
    def popout_random_samples(
        self, n_samples=15, image_size: ImageSizeType = 64, show_targets=True
    ):
        """
        Display image popups of random samples from the latent space

        Parameters
        ----------
        n_samples
            Number of samples to display
        image_size
            Size of the displayed images in screen pixels
        show_targets
            Whether to show the target points for the popups
        """
        samples = self.tab.samples
        if samples is None or not len(samples):
            return
        n_samples = min(n_samples, len(samples))
        n_samples = max(n_samples, 0)
        sample_indexes = np.random.choice(len(samples), n_samples, replace=False)
        self.popout_selected_samples(
            sample_indexes, image_size=image_size, show_targets=show_targets
        )

    def clear_popout_samples(self):
        self.global_popout_group.ensure_n_items(0)

    def update_popout_listener_properties(self, image_size=64, loop_over_roi=False):
        self.popout_target.default_image_size = image_size
        if loop_over_roi and self.popout_target.start_index is not None:
            self.popout_loop.start_loop(reset=not self.popout_loop.timer.isActive())
        else:
            self.popout_loop.stop_loop()

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.popout_random_samples)
        properties_proc = editor.registerFunction(
            self.update_popout_listener_properties,
            runOptions=RunOptions.ON_CHANGED,
            container=self.selection_properties,
        )
        # Allow `self.popout_loop.start_loop` to retain user-set values when called
        # without parameters
        fmt = editor.defaultInteractor.titleFormat
        sample_param = next(iter(properties_proc.parameters.values()))
        self.popout_loop.start_loop = editor.registerFunction(
            self.popout_loop.start_loop,
            runOptions=RunOptions.ON_CHANGED,
            parent=sample_param.parent(),
            nest=False,
            n_points=dict(title=fmt("n_loop_points")),
            duration_s=dict(title=fmt("loop_duration_s")),
        )
        # Don't retain "reset" value at all
        self.popout_loop.start_loop.extra.clear()
