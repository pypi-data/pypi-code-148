import math

from lightly.utils import dist
from loguru import logger


def infer_lr(base_lr: float, current_batch_size: int, base_batch_size: int, scaling: str = "linear"):
    """
    Infer learning rate set for a base_batch_size. Helps define a LR only once and batch-size can be
    varied as needed.

    base_lr: The base learning rate for a specific batch size
    base_batch_size: The batch size that `base_lr` is locked to
    current_batch_size: Batch size used in current training
    scaling: Method to scale the learning rate. linear | sqrt supported
    """
    world_size = dist.world_size()
    effective_batch_size = current_batch_size * world_size
    base_lr = base_lr
    base_lr_batch_size = base_batch_size
    scaling = scaling

    assert scaling in [
        "sqrt",
        "linear",
    ], "Only linear | sqrt scaling_types are supported"

    scale_factor = float(effective_batch_size) / base_lr_batch_size
    if scaling == "sqrt":
        scale_factor = math.pow(scale_factor, 0.5)
    scaled_lr = base_lr * scale_factor
    logger.info(f"Scaled learning rate: {scaled_lr}, {type(scaled_lr)}")
    return scaled_lr
