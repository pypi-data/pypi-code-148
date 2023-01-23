from .base import BaseVAE
from .beta_vae import BetaVAE
from .dfcvae import DFCVAE
from .mssim_vae import MSSIMVAE

vae_models = {
    "BetaVAE": BetaVAE,
    "DFCVAE": DFCVAE,
    "MSSIMVAE": MSSIMVAE,
}

__all__ = [cls.__name__ for cls in vae_models.values()] + ["vae_models"]
