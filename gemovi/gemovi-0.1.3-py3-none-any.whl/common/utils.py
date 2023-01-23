from __future__ import annotations

import contextlib
import os
from pathlib import Path
from typing import Any, Tuple, Union

import numpy as np
import pyqtgraph as pg
import torch
import yaml
from PIL import Image
from qtextras import fns


def get_config(config_file: str):
    here = Path(__file__).parent
    check_loc = here / "configs" / config_file
    if check_loc.exists():
        config_file = check_loc
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config


def update_config_from_kwargs(
    config: dict, subdict_keys=("trainer_params", "exp_params", "data_params"), **kwargs
) -> dict[str, Any]:
    """
    Helper function to pass kwargs without needing a nested structure to slightly
    alter a config dict. For example, if you want to change the ``batch_size`` in
    ``trainer_params``, you can call ``update_config_from_kwargs(config, batch_size=32)``.

    Note that ``config`` is updated in-place, so you may want to pass in a copy
    if the original should remain unmodified:
    ``updated = update_config_from_kwargs(config.copy(), ...)``.
    """
    for key in subdict_keys:
        config_subdict = config[key]
        for config_key in set(config_subdict).intersection(kwargs):
            config_subdict[config_key] = kwargs.pop(config_key)
    return config


def tensor_keys_to_items(in_dict):
    out_dict = {}
    for key, value in in_dict.items():
        if isinstance(value, torch.Tensor):
            out_dict[key] = value.item()
        else:
            out_dict[key] = value
    return out_dict


def load_trainer_state_dict(model: torch.nn.Module, state_dict: dict, strict=True):
    """
    Wrapper around ``model.load_state_dict`` that handles the case where the state_dict
    was generated during ignite or lightning training. Checks for nested ``state_dict``
    key and prefixes resulting from saving trainer state instead of raw model state.
    """
    if "state_dict" in state_dict:
        state_dict = state_dict["state_dict"]
    # Strip prefixes resulting from training structures to just end up with names that
    # match the model
    expected_names = set(name for (name, _) in model.named_children())
    prefix_idxs = set()
    for name in expected_names:
        for state_key in state_dict:
            if name in state_key:
                prefix_idxs.add(state_key.index(name))
                break
    if len(prefix_idxs) > 1:
        raise ValueError("Found multiple viable prefixes for state_dict keys")
    prefix_idx = 0 if not prefix_idxs else prefix_idxs.pop()
    state_dict = {key[prefix_idx:]: value for (key, value) in state_dict.items()}
    return model.load_state_dict(state_dict, strict=strict)


class ParamDict(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


def tensor_to_np(tensor) -> np.ndarray:
    return tensor.detach().cpu().numpy()


def to_pil_image(image, none_if_error=False):
    suppress = False
    if isinstance(image, torch.Tensor):
        image = tensor_to_np(image).transpose((1, 2, 0))
    if isinstance(image, np.ndarray):
        # Handle float images from 0->1 by turning to uint
        if np.issubdtype(image.dtype, np.floating):
            image = (image - image.min()) / image.ptp() * 255
            image = image.astype("uint8")
        image = Image.fromarray(image)
    elif isinstance(image, (str, Path)):
        try:
            image = Image.open(image)
        except IOError:
            if not none_if_error:
                raise
            suppress = True
            image = None
    if not isinstance(image, Image.Image) and not suppress:
        raise TypeError(f"Unsupported image type: {type(image)}")
    return image


def pad_image_to_size(
    image: Image.Image,
    size_wh: Union[int, Tuple[int, int]] = None,
    fill_color: Any = 0,
    **resize_kwargs,
) -> Image.Image:
    """
    Keeps an image's aspect ratio by resizing until the largest side is constrained
    by the specified output size. Then, the deficient dimension is padded until
    the image is the specified size.
    """
    if size_wh is None:
        size_wh = max(image.size)

    if isinstance(size_wh, int):
        size_wh = (size_wh, size_wh)

    im_size_wh = np.array(image.size)
    ratios = im_size_wh / size_wh

    # Resize until the largest side is constrained by the specified output size
    im_size_wh = np.ceil(im_size_wh / ratios.max()).astype(int)
    # Prefer 1-pixel difference in aspect ratio vs. odd padding
    pad_amt = np.array(size_wh) - im_size_wh
    use_ratio_idx = np.argmax(ratios)
    unused_ratio_idx = 1 - use_ratio_idx

    # Sanity check for floating point accuracy: At least one side must match
    # user-requested dimension
    if np.all(pad_amt != 0):
        # Adjust dimension that is supposed to match
        im_size_wh[use_ratio_idx] += pad_amt[use_ratio_idx]
    # Prefer skewing aspect ratio by 1 pixel instead of odd padding
    # If odd, 1 will be added. Otherwise, the dimension remains unchanged
    im_size_wh[unused_ratio_idx] += pad_amt[unused_ratio_idx] % 2
    image = image.resize(tuple(im_size_wh), **resize_kwargs)

    new_im = Image.new("RGB", size_wh, fill_color)
    width, height = image.size
    new_im.paste(image, (int((size_wh[0] - width) / 2), int((size_wh[1] - height) / 2)))
    return new_im


def read_image_folder(folder_or_file_list, ext="*"):
    images, names = [], []
    if os.path.isfile(folder_or_file_list):
        folder_or_file_list = [Path(folder_or_file_list)]
    else:
        folder_or_file_list = fns.naturalSorted(
            Path(folder_or_file_list).glob(f"*.{ext}")
        )
    for file in folder_or_file_list:
        try:
            images.append(Image.open(file))
        except IOError:
            continue
        names.append(file.name)
    return images, names


def try_fire_cli(main_function):
    try:
        import fire

        fire.Fire(main_function)
    except ImportError:
        cli = fns.makeCli(main_function)
        main_function(**vars(cli.parse_args()))


@contextlib.contextmanager
def disconnected_signal(signal, slot):
    """
    Context manager that disconnects a signal handler while the context is active.
    """
    oldConnected = pg.disconnect(signal, slot)
    try:
        yield oldConnected
    finally:
        if oldConnected:
            signal.connect(slot)
