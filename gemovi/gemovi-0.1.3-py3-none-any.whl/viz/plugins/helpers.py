from __future__ import annotations

import base64
import typing as t
from dataclasses import dataclass
from io import BytesIO

import pyqtgraph as pg
from PIL import Image
from pyqtgraph import QtCore

from gemovi.common.utils import pad_image_to_size, to_pil_image


def closest_point_on_line(point, line_point_a, line_point_b):
    """Find the closest point on a line to a given point."""
    # https://stackoverflow.com/a/6853926/353337
    # Equation below comes from taking the derivative of the distnace from `point` to
    # the line and setting it equal to zero. Or by using the projection of (
    # line_point_a -> point) onto (line_point_a -> line_point_b) and moving
    # `line_point_a` to the point of projection.
    a_to_p = point - line_point_a
    line = line_point_b - line_point_a
    projection_distance = (a_to_p.T @ line) / (line.T @ line) * line
    closest_point = line_point_a + projection_distance
    return closest_point


class UNSET:
    """Indicates an option is unset when None is a valid value"""


class NumberedItemContainer(pg.ItemGroup):
    def __init__(self, item_factory: t.Callable, parent=None):
        super().__init__(parent)
        self.item_factory = item_factory

    def ensure_n_items(self, n: int) -> dict[str, t.Any]:
        added, removed = [], []
        while len(self) < n:
            item = self.item_factory()
            self._add_to_views(item)
            self.addItem(item)
            added.append(item)
        while len(self) > n:
            item = self[-1]
            self._remove_from_views(item)
            if item.parentItem() is self:
                # No views, so no triggers to item.setParentItem(None). Do so manually
                item.setParentItem(None)
            removed.append(item)
        if added or removed:
            self.informViewBoundsChanged()
        return dict(added=added, removed=removed)

    def _add_to_views(self, item):
        if scene := self.scene():
            for view in scene.views():
                view.addItem(item)

    def _remove_from_views(self, item):
        if scene := self.scene():
            for view in scene.views():
                view.removeItem(item)

    def __iter__(self):
        return iter(self.childItems())

    def __getitem__(self, item):
        return self.childItems()[item]

    def __len__(self):
        return len(self.childItems())

    def __contains__(self, item):
        return item in self.childItems()


ImageSizeType = t.Union[int, tuple[int, int], None]


@dataclass
class TooltipData:
    name: str = None
    label: str = None
    image_data: Image.Image | t.Any = None
    image_read_function: t.Callable[[t.Any], Image.Image] = to_pil_image

    default_image_size: ImageSizeType = 64

    def to_html(self, include_image=True):
        label_str = f"Label: {self.label}<br/>" if self.label else ""
        name_str = self.name or "<None>"
        html = (
            f'<div style="text-align:center">'
            f"Name: {name_str}<br/>"
            f"{label_str}"
            f"</div>"
        )
        if include_image and (img_bytes := self.image_bytes):
            img = img_bytes.decode()
            html += f'<img src="data:image/jpeg;base64,{img}"/>'
        return html

    def image_data_to_b64(self, size: ImageSizeType = None) -> bytes:
        self.evaluate_image_data(size)
        return self.image_bytes

    def evaluate_image_data(self, size: ImageSizeType = None):
        if size is None:
            size = self.default_image_size
        image_data = self.image_data
        if image_data is None or isinstance(image_data, Image.Image):
            # Already converted / doesn't exist, nothing to replace
            return image_data
        # Lazy evaluation in all other cases
        image_data = self.image_read_function(image_data)
        image_data = pad_image_to_size(image_data, size)
        self.image_data = image_data
        return image_data

    @property
    def image_bytes(self):
        buff = BytesIO()
        image_data = self.evaluate_image_data()
        if image_data is None:
            return None
        self.image_data.save(buff, format="jpeg", quality=80)
        return base64.b64encode(buff.getvalue())


class PixelSizedImageItem(pg.ImageItem):
    sig_clicked = QtCore.Signal(object, object)  # self (or None on exit), ev

    def __init__(self, image=None, **kargs):
        super().__init__(image, **kargs)
        self.setPxMode(True)

    def set_shape(self, shape_wh: ImageSizeType = None):
        if shape_wh is None:
            return
        if isinstance(shape_wh, int):
            shape_wh = (shape_wh, shape_wh)
        self.setRect(QtCore.QRectF(0, 0, *shape_wh))

    def setOpts(self, update=True, **kargs):
        if "shape" in kargs:
            self.set_shape(kargs.pop("shape"))
        super().setOpts(update, **kargs)

    def dataBounds(self, ax, frac, orthoRange=None):
        """
        Viewbox uses this method to determine auto ranging. Set to 0 to exclude
        this item from the range bounds considerations.
        """
        return [0, 0]

    def mouseClickEvent(self, ev):
        self.sig_clicked.emit(self, ev)
        super().mouseClickEvent(ev)
