from __future__ import annotations

import functools
from typing import Type

import torch
from qtextras import bindInteractorOptions as bind, fns

from gemovi.common.utils import get_config
from gemovi.vae.models import BaseVAE, vae_models
from gemovi.viz import ModelTab
from gemovi.viz.base import GenerativeTab, ModelWindow, device
from gemovi.viz.plugins.metadata import FileSampleMetadataPlugin, SampleMetadataPlugin
from gemovi.viz.plugins.reencoding import ReencodingPlugin
from gemovi.viz.plugins.roiencoder import ROIEncoderPlugin


class VAEGenerativeTab(GenerativeTab):
    model: BaseVAE

    def forward(self, input):
        return self.model.decode(input)

    def get_num_latent_dims(self):
        if hasattr(self.model, "latent_dim"):
            return self.model.latent_dim
        try:
            return super().get_num_latent_dims()
        except NotImplementedError:
            dummy_inputs = torch.Tensor(1, 3, 64, 64).to(device)
            latents = self.forward(dummy_inputs)
            if isinstance(latents, list):
                return latents[0].shape[1]
            else:
                return latents.shape[1]


class VAEEncoderTab(VAEGenerativeTab):
    def get_plugin_classes(self):
        classes = super().get_plugin_classes()
        replace_idx = classes.index(SampleMetadataPlugin)
        classes[replace_idx] = FileSampleMetadataPlugin
        classes.append(ROIEncoderPlugin)
        classes.append(ReencodingPlugin)
        return classes

    def forward_encoder(self, input):
        mu, log_var = self.model.encode(input)
        std = torch.exp(0.5 * log_var)
        return mu, std


class VAEWindow(ModelWindow):
    tab_types = [VAEEncoderTab]
    model_cls = None


class MultiModel:
    def __init__(self, **named_models):
        if not named_models:
            named_models = vae_models
        self.named_models = named_models

        for method in "to", "eval", "train":
            func = functools.partial(self.call_with_models, method)
            setattr(self, method, func)

    def call_with_models(self, method, *args, **kwargs):
        for model in self.named_models.values():
            getattr(model, method)(*args, **kwargs)
        return self

    def load_state_dict(self, state_dict, strict=True):
        for kk, vv in state_dict.values():
            self.named_models[kk].load_state_dict(vv, strict=strict)


class MultiVAEWindow(ModelWindow):
    tab_types = [VAEEncoderTab]
    model_cls = None
    model: MultiModel

    def __init__(self, parameter_info=None):
        super().__init__(parameter_info)
        self.update_multiple_weights_proc = self.settings_editor.registerFunction(
            self.update_multiple_weights
        )

    @classmethod
    def make_model(cls, param_info=None) -> MultiModel:
        if isinstance(param_info, str):
            param_info = get_config(param_info)
        out_models = {}
        # Need to load param info for both model types
        for model_name, model_params in param_info["model_params"].items():
            if model_name not in vae_models:
                continue
            out_models[model_name] = vae_models[model_name](**model_params)
        return MultiModel(**out_models)

    @bind(
        weights=dict(type="file"),
        model=dict(type="list", value="", limits=list(vae_models)),
    )
    def update_weights(self, weights="", model=None):
        old_model: MultiModel = self.model
        model_name = model
        if model_name not in old_model.named_models:
            raise ValueError(
                f"Invalid model name: {model_name}. "
                f"Must be one of: {list(old_model.named_models)}"
            )

        model_to_update = old_model.named_models[model_name]
        super().update_weights(weights, model_to_update)

    @bind(name_weights_map_file=dict(type="file"))
    def update_multiple_weights(
        self,
        name_weights_map_file="",
    ):
        name_weights_map = fns.attemptFileLoad(name_weights_map_file)
        if not name_weights_map:
            return
        for model_name, weights_file in name_weights_map.items():
            self.update_weights(weights_file, model_name)

    def insert_tab(self, tab_type: Type[ModelTab], tab_name: str = None):
        tab_name_base = tab_name or tab_type.__name__.replace("Tab", "")
        for model_name, model_inst in self.model.named_models.items():
            tab_inst = tab_type(model_inst)
            tab_name = f" {tab_name_base} - &{model_name}"
            self.tab_group.addTab(tab_inst, tab_name)
