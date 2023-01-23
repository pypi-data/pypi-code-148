from __future__ import annotations

from typing import List

import pyqtgraph as pg
from qtextras import widgets

from gemovi.gan.models import DCGAN
from gemovi.viz.base import GenerativeTab, ModelTab, ModelWindow
from gemovi.viz.plugins.prediction import PredictionPlugin


class GANDiscriminitiveTab(ModelTab):
    preview_items: List[List[pg.ImageItem]]
    preview_widget: pg.GraphicsView

    def setup_gui(self):
        return widgets.EasyWidget.buildWidget([self.editor])

    def get_num_latent_dims(self):
        try:
            return GenerativeTab.get_num_latent_dims(self)
        except NotImplementedError:
            return self.model.opts["num_latent_dims"]

    get_image_size = GenerativeTab.get_image_size

    def forward(self, input):
        return GenerativeTab.forward(self, input)

    def get_plugin_classes(self):
        return [PredictionPlugin]


class GANGenerativeTab(GenerativeTab):
    def get_num_latent_dims(self):
        return self.model.opts.num_latent_dims


class GANWindow(ModelWindow):
    tab_types = [GANGenerativeTab, GANDiscriminitiveTab]
    model_cls = DCGAN
