# Code adapted from kornia project
# https://github.com/kornia/kornia/blob/master/kornia/metrics/psnr.py
import torch

class PNSR(torch.nn.Module):
    """ Peak Signal to Noise Ratio (PSNR) metric."""
    def __init__(self):
        super(PNSR, self).__init__()

    # The isinstance checks order are inverted
    def forward(self, y_pred, y_true, mask):
        y_pred = y_pred.masked_select(mask)
        y_true = y_true.masked_select(mask)
        return -10.0 * torch.log10(
            torch.nn.functional.mse_loss(y_pred, y_true, reduction='mean')
        )
