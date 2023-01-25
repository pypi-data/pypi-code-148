import torch
import numpy as np
import random

from typing import Union


def v_debug():
    import pdb

    pdb.set_trace()


def set_global_random_seed(rd_seed: int = 314):
    random.seed(rd_seed)
    np.random.seed(rd_seed)
    torch.manual_seed(rd_seed)
    torch.cuda.manual_seed(rd_seed)
    torch.cuda.manual_seed_all(rd_seed)
    # torch.backends.cudnn.benchmark = False
    # torch.backends.cudnn.deterministic = True


"""
scale action from range [-1,1] to range [low,high]
"""


def scale_actions(actions: Union[np.ndarray, torch.Tensor], low, high):
    if isinstance(actions, np.ndarray):
        return np.clip((actions + 1) * (high - low) / 2 + low, low, high)
    elif isinstance(actions, torch.Tensor):
        return torch.clamp((actions + 1) * (high - low) / 2 + low, low, high)
    raise ValueError("Unsupported type of actions: {}".format(type(actions)))


"""
unscale action from range [low,high] to range [-1,1]
"""


def unscale_actions(actions: Union[np.ndarray, torch.Tensor], low, high):
    if isinstance(actions, np.ndarray):
        return np.clip((actions - low) * 2 / (high - low) - 1, -1, 1)
    elif isinstance(actions, torch.Tensor):
        return torch.clamp((actions - low) * 2 / (high - low) - 1, -1, 1)
    raise ValueError("Unsupported type of actions: {}".format(type(actions)))
