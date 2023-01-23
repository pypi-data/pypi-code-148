from __future__ import annotations

import typing as t

from qtextras import ParameterEditor, fns

from gemovi.common.constants import get_device

T = t.TypeVar("T")
if t.TYPE_CHECKING:
    from gemovi.viz.base import GenerativeTab, ModelTab


def _mkspec(typ: str = None, **opts):
    out = opts.copy()
    if typ is not None:
        out["type"] = typ
    return out


_colormap_spec = _mkspec("popuplineeditor", limits=fns.listAllPgColormaps())
device = get_device(1)


class TabPlugin:
    name: str | None = None

    def __init__(self, tab: ModelTab):
        if self.name is None:
            self.name = fns.nameFormatter(self.__class__.__name__.replace("Plugin", ""))
        self.tab = tab

    def register_functions(self, editor: ParameterEditor):
        ...


class GenerativeTabPlugin(TabPlugin):
    tab: GenerativeTab

    def register_item(self, item: T, hide=False) -> T:
        self.tab.plot_widget.addItem(item)
        if hide:
            item.hide()
        return item


class GenerativeEncoderTabPlugin(GenerativeTabPlugin):
    tab: t.Any


from gemovi.viz.plugins.metadata import FileSampleMetadataPlugin, SampleMetadataPlugin
from gemovi.viz.plugins.perturbation import PerturbationPlugin
from gemovi.viz.plugins.popout import PopoutImageTargetItem, PopoutPlugin
from gemovi.viz.plugins.prediction import PredictionPlugin
from gemovi.viz.plugins.reencoding import ReencodingPlugin
from gemovi.viz.plugins.roidecoder import *
from gemovi.viz.plugins.roiencoder import ROIEncoderPlugin
from gemovi.viz.plugins.scatterplot import ScatterplotPlugin
