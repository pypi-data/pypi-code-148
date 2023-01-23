import os

import pytorch_lightning as pl
import torch
from torchvision import utils as vutils

from gemovi.common.utils import tensor_keys_to_items
from gemovi.gan.models import DCGAN


class GANTrainerState(pl.LightningModule):
    # Unused locals are captured by "self.save_hyperparameters()"
    # noinspection PyUnusedLocal
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__()
        self.model = DCGAN(**kwargs)
        latent_dim = self.model.opts.num_latent_dims
        self.model.manage_gradients = False
        self.save_hyperparameters()

        self.validation_z = torch.randn(25, latent_dim, 1, 1)

        self.example_input_array = torch.zeros(2, latent_dim, 1, 1)

    def forward(self, noise):
        return self.model.generator(noise)

    def adversarial_loss(self, y_hat, y):
        return self.model.criterion(y_hat, y)

    def training_step(self, batch, batch_idx, optimizer_idx):
        loss, log = self.get_loss_and_cvt_log(
            self.model.training_step(batch, optimizer_idx)
        )
        return dict(loss=loss, progress_bar=log, log=log)

    def get_loss_and_cvt_log(self, log):
        err_keys = [k for k in log if k.startswith("err_")]
        assert len(err_keys) == 1, f"Got multiple err keys: {err_keys}"
        loss = log[err_keys[0]]
        log = tensor_keys_to_items(log)
        return loss, log

    def validation_step(self, batch, batch_idx):
        batch, noise = self.model.resolve_batch_and_noise(batch)
        old_state = self.model.training
        try:
            self.model.eval()
            loss, log = self.get_loss_and_cvt_log(
                self.model.gen_train_step(batch, noise)
            )
        finally:
            self.model.train(old_state)
        self.log("val_loss", loss)
        return dict(val_loss=loss, progress_bar=log, log=log)

    def configure_optimizers(self):
        opts = self.model.configure_optimizers()
        return [o for o in opts if o is not None]

    def on_validation_end(self):
        noise = self.validation_z.type_as(self.model.generator.main[0].weight)

        # log sampled images
        sample_imgs = self(noise)
        # grid = vutils.make_grid(sample_imgs)
        # self.logger.experiment.add_image("generated_images", grid, self.current_epoch)
        vutils.save_image(
            sample_imgs.detach().cpu(),
            os.path.join(
                self.logger.log_dir,
                "Samples",
                f"{self.logger.name}_Epoch_{self.current_epoch}.jpg",
            ),
            normalize=True,
            nrow=5,
        )
