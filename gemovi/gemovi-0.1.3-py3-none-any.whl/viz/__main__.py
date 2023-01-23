from __future__ import annotations

import pyqtgraph as pg
import torch
from pyqtgraph import QtCore

from gemovi.common.utils import get_config, try_fire_cli
from gemovi.vae.models import vae_models
from gemovi.viz.gan import GANWindow
from gemovi.viz.vae import MultiVAEWindow, VAEWindow


def main(
    model_class: str = None,
    weights_file="",
    config_file="model_defaults.yaml",
):
    """
    Main entry point for the gemovi.viz package

    Parameters
    ----------
    model_class
        The model class to use (case-insensitive). Can be one of "dcgan", "multivae",
        or a string name of an implemented VAE model class.
            - If "dcgan", loads a GANWindow.
            - If "multivae", loads a MultiVAEWindow. In this case, the see notes
              for the `weights_file` parameter and ``config_file``.
            - If *None* or falsy, assumes a valid ``config_file`` is given and loads
              ``trainer_params["model_name"]``.
            - Otherwise, loads a VAEWindow with the specified model class.
    weights_file
        The path to the weights file to load. If `model_class` is "multivae", this
        should be a path to a YAML file with a dictionary of ``{model_name:
        weights_file}`` pairs. Otherwise, should be a file path compatible with the
        outputs of ``gemovi.vae.train`` or ``gemovi.dcgan.train``.
    config_file
        The path to the config file to load. Should contain most critical keys
        from ``gemovi.common.configs -> model.defaults.yaml``. If `model_class` is
        "multivae", each key in ``model_params`` will be added as another model
        class if it is present in ``gemovi.vae.models.vae_models``.
    """
    pg.mkQApp()
    pg.setConfigOptions(imageAxisOrder="row-major")

    if not model_class and not config_file:
        raise ValueError("If `model_class` is None, `config_file` must be given.")
    elif not model_class:
        config = get_config(config_file)
        model_class = config["trainer_params"]["model_name"]

    window_type_map = {
        "dcgan": GANWindow,
        "multivae": MultiVAEWindow,
    }
    lowercase_models = {k.lower(): v for k, v in vae_models.items()}
    allowed_models = list(window_type_map) + list(lowercase_models)

    model_class = model_class.lower()
    if model_class not in allowed_models:
        raise ValueError(
            f"Invalid model_class: {model_class}. Must be one of: {allowed_models}"
        )
    window_class = window_type_map.get(model_class, VAEWindow)
    if window_class == VAEWindow:
        window_class.model_cls = lowercase_models[model_class]
    window = window_class(config_file)
    if weights_file:
        if model_class != "multivae":
            window.update_weights_proc(weights=weights_file)
        else:
            window.update_multiple_weights_proc(name_weights_map_file=weights_file)
    else:
        # Fire signal anyway to populate random samples
        window.sig_model_changed.emit()

    QtCore.QTimer.singleShot(0, window.showMaximized)
    pg.exec()


if __name__ == "__main__":
    # Ensure reruns are determinisic
    torch.manual_seed(0)

    try_fire_cli(main)
