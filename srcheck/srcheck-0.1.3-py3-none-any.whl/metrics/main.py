import torch
import numpy as np
from srcheck.metrics.pnsr import PNSR
from srcheck.metrics.ssim import SSIM

# Create the metrics
PNSR_METRIC = PNSR()
SSIM_METRIC = SSIM(5)


def check_tensor_sanity(y_pred, y_true, mask):
    if not isinstance(y_pred, torch.Tensor):
        raise TypeError(f"Expected torch.Tensor but got {type(y_pred)}.")

    if not isinstance(y_true, torch.Tensor):
        raise TypeError(f"Expected torch.Tensor but got {type(y_true)}.")

    if not isinstance(mask, torch.Tensor):
        raise TypeError(f"Expected torch.Tensor but got {type(mask)}.")

    if y_pred.shape != y_true.shape:
        raise TypeError(
            f"Expected tensors of equal shapes, but got {y_pred.shape} and {y_true.shape}"
        )

    if not len(y_pred.shape) == 4:
        raise ValueError(f"Invalid y_pred shape, we expect BxCxHxW. Got: {y_pred.shape}")

    if not len(y_true.shape) == 4:
        raise ValueError(f"Invalid img2 shape, we expect BxCxHxW. Got: {y_true.shape}")

    return True

def metrics_generator(yhat, y, mask):

    # Check tensor sanity
    check_tensor_sanity(yhat, y, mask)

    # PSNR
    pnsr_value = float(PNSR_METRIC(yhat, y, mask).detach().numpy())

    # SSIM
    ssim_metric = float(np.mean(SSIM_METRIC(yhat, y).detach().numpy()))
    
    
    return pnsr_value, ssim_metric
