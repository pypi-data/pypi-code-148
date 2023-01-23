from __future__ import annotations

import typing as t
from pathlib import Path

import numpy as np
import pyqtgraph as pg
import torch
from PIL import Image
from pyqtgraph import QtCore
from qtextras import ParameterEditor, bindInteractorOptions as bind

from gemovi.common.utils import read_image_folder, tensor_to_np
from gemovi.viz.plugins import TabPlugin, _mkspec

if t.TYPE_CHECKING:
    from gemovi.viz.base import ModelTab


class PredictionPlugin(TabPlugin):
    def __init__(self, tab: ModelTab):
        super().__init__(tab)
        self.window_handle = None

    def register_functions(self, editor: ParameterEditor):
        editor.registerFunction(self.predict_on_samples)

    @bind(image_or_path=_mkspec("file", fileMode="Directory"))
    def predict_on_samples(self, image_or_path=""):
        """
        Discriminator prediction of how likely each sample is to be real. Each image
        is displayed along with its confidence in a gridded window.

        Parameters
        ----------
        image_or_path
            Path to a directory of images on which to run the prediction,
            or a single numpy image
        """
        if isinstance(image_or_path, np.ndarray):
            images = [Image.fromarray(image_or_path)]
            names = ["Confidence"]
        elif isinstance(image_or_path, (str, Path)):
            images, names = read_image_folder(image_or_path)
        else:
            raise ValueError(f"Invalid image or path type: {type(image_or_path)}")

        img_as_batch = torch.cat(
            [self.tab.image_as_normed_tensor(image) for image in images]
        )
        confidences = (
            self.tab.model.discriminator(img_as_batch)
            .view(-1)
            .detach()
            .cpu()
            .numpy()
            .round(2)
        )
        num_rows = int(np.sqrt(len(images)))
        num_cols = int(np.ceil(len(images) / num_rows))
        images_np = [tensor_to_np(im).transpose((1, 2, 0)) for im in img_as_batch]
        preview = PreviewItemsMixin()
        out_widget = preview.preview_widget
        preview.make_previews(num_rows, num_cols)
        preview.update_previews(images_np, confidences, names, show_labels=True)
        out_widget.show()
        out_widget.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.window_handle = out_widget


class NamedImageItem(pg.ImageItem):
    sig_clicked = QtCore.Signal(object)

    def __init__(self, name=None):
        super().__init__()
        # Update anchor to center the label above the image
        self.name_label = pg.TextItem(
            text=name, color=(255, 255, 255, 255), anchor=(0.5, 1)
        )

    def setName(self, name):
        self.name_label.setText(name)

    def addToParent(self, parent):
        parent.addItem(self)
        parent.addItem(self.name_label)

    def centerLabel(self):
        center_pos = self.boundingRect().center()
        self.name_label.setPos(center_pos.x(), 0)

    def mouseClickEvent(self, ev):
        self.sig_clicked.emit(self)
        super().mouseClickEvent(ev)


class PreviewItemsMixin(QtCore.QObject):
    sig_preview_clicked = QtCore.Signal(object, int)
    """Item clicked and it's raveled preview index"""

    def __init__(self):
        super().__init__()
        view = pg.GraphicsView()
        layout = pg.GraphicsLayout()
        view.setCentralItem(layout)
        self.popouts = {}
        self.selected_preview_idx = 0
        self.preview_widget, self.preview_layout = view, layout
        self.preview_items: list[list[NamedImageItem]] = [[]]
        self.num_preview_rows, self.num_preview_cols = 0, 0

        old_resize = view.resizeEvent

        def new_resize(event):
            old_resize(event)
            self.trigger_autorange()

        view.resizeEvent = new_resize

    def update_previews(
        self, images, confidences=None, names: list[str] | str = "", show_labels=False
    ):
        preview_items = self.preview_items
        if not names:
            names = [""] * len(images)
        else:
            names = [str(name) + ": " for name in names]
        if confidences is None or not len(confidences):
            confidences = [None] * len(images)
        for ii in range(len(preview_items)):
            for jj in range(len(preview_items[ii])):
                ravel_idx = ii * len(preview_items[ii]) + jj
                if ravel_idx < len(images):
                    item = preview_items[ii][jj]
                    item.setImage(images[ravel_idx])
                    item.name_label.setText(
                        names[ravel_idx] + str(confidences[ravel_idx])
                    )
                    item.centerLabel()
                    item.name_label.setVisible(show_labels)
        self.trigger_autorange()

    def trigger_autorange(self):
        if len(self.preview_items):
            # Autoranging one will autorange all since they are linked
            self.preview_items[0][0].getViewBox().autoRange()

    def make_previews(self, num_rows=0, num_cols=0):
        self.num_preview_rows, self.num_preview_cols = num_rows, num_cols
        preview_items = [
            [NamedImageItem() for _ in range(num_cols)] for _ in range(num_rows)
        ]
        layout = self.preview_layout
        layout.clear()
        self.preview_items = preview_items
        referencevb = None
        for ii in range(num_rows):
            for jj in range(num_cols):
                proxy = layout.addViewBox(ii, jj, lockAspect=True)
                preview_items[ii][jj].addToParent(proxy)
                proxy.autoRange()
                proxy.invertY()
                preview_items[ii][jj].sig_clicked.connect(self.on_image_click)
                if referencevb:
                    proxy.setXLink(referencevb)
                    proxy.setYLink(referencevb)
                referencevb = referencevb or proxy

    def on_image_click(self, item):
        ravel_idx = 0
        for ii in range(self.num_preview_rows):
            for jj in range(self.num_preview_cols):
                if self.preview_items[ii][jj] is item:
                    self.sig_preview_clicked.emit(item, ravel_idx)
                    return
                ravel_idx += 1

    def popout_sample(self, sample_idx=0, stay_on_top=True):
        pw = pg.PlotWidget()
        item = pg.ImageItem()
        pw.addItem(item)
        row, col = np.unravel_index(
            sample_idx, (self.num_preview_rows, self.num_preview_cols)
        )
        ref_item = self.preview_items[row][col]

        def on_update():
            item.setImage(ref_item.image)

        ref_item.sigImageChanged.connect(on_update)
        on_update()
        item.getViewBox().autoRange()
        if stay_on_top:
            # False positive
            # noinspection PyTypeChecker
            pw.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        pw.show()
        pw.setAspectLocked(True)
        pw.invertY()
        self.popouts[sample_idx] = pw

    @bind(preview_idx=dict(value=0))
    def update_selected_preview(
        self, preview_idx: int = None, image_data: np.ndarray = None
    ):
        """
        If the selected sample is already present in the previews, highlight it.
        Otherwise, evict the oldest sample and add the new one before highlighting.
        :param preview_idx: Index of the sample to update
        :param image_data: If not None, replaces the image data in the preview
        """
        if preview_idx == self.selected_preview_idx and image_data is None:
            return
        nrows, ncols = self.num_preview_rows, self.num_preview_cols

        old_sample_idx = self.selected_preview_idx
        if old_sample_idx is not None:
            oldrow, oldcol = np.unravel_index(old_sample_idx, (nrows, ncols))
            self.preview_items[oldrow][oldcol].setBorder(None)
        self.selected_preview_idx = preview_idx

        if preview_idx is None:
            return

        newrow, newcol = np.unravel_index(preview_idx, (nrows, ncols))
        self.preview_items[newrow][newcol].setBorder(pg.mkPen("r", width=5))
        if image_data is not None:
            self.preview_items[newrow][newcol].setImage(image_data)
        self.preview_widget.update()
