import os

import pytorch_lightning as pl
import torch
import torchvision.utils as vutils
from torch import optim

from gemovi.vae.models import BaseVAE

Tensor = torch.Tensor


class VAEXperiment(pl.LightningModule):
    def __init__(self, vae_model: BaseVAE, params: dict) -> None:
        super(VAEXperiment, self).__init__()

        self.model = vae_model
        self.params = params
        self.curr_device = None
        self.hold_graph = False
        try:
            self.hold_graph = self.params["retain_first_backpass"]
        except:
            pass

    def forward(self, input: Tensor, **kwargs) -> Tensor:
        return self.model(input, **kwargs)

    def training_step(self, batch, batch_idx, optimizer_idx=0):
        real_img, labels = batch
        self.curr_device = real_img.device

        results = self.forward(real_img, labels=labels)
        train_loss = self.model.loss_function(
            *results,
            M_N=self.params["kld_weight"],  # al_img.shape[0]/ self.num_train_imgs,
            optimizer_idx=optimizer_idx,
            batch_idx=batch_idx,
        )

        self.log_dict(
            {key: val.item() for key, val in train_loss.items()}, sync_dist=True
        )

        return train_loss["loss"]

    def validation_step(self, batch, batch_idx, optimizer_idx=0):
        real_img, labels = batch
        self.curr_device = real_img.device

        results = self.forward(real_img, labels=labels)
        val_loss = self.model.loss_function(
            *results,
            M_N=1.0,  # real_img.shape[0]/ self.num_val_imgs,
            optimizer_idx=optimizer_idx,
            batch_idx=batch_idx,
        )

        self.log_dict(
            {f"val_{key}": val.item() for key, val in val_loss.items()}, sync_dist=True
        )

    def on_validation_end(self) -> None:
        self.sample_images()

    def sample_images(self, n_images=64):
        # Get sample reconstruction image
        dataset = self.trainer.datamodule.test_dataloader()
        test_input, test_label = [], []
        retrieved = 0
        for images, labels in dataset:
            if retrieved >= n_images:
                break
            test_input.append(images)
            test_label.append(labels)
            retrieved += images.shape[0]
        test_input = torch.cat(test_input, dim=0)[:n_images].to(self.curr_device)
        test_label = torch.cat(test_label, dim=0)[:n_images].to(self.curr_device)

        #         test_input, test_label = batch
        recons = self.model.generate(test_input, labels=test_label)
        vutils.save_image(
            recons.data,
            os.path.join(
                self.logger.log_dir,
                "Reconstructions",
                f"Recons_{self.logger.name}_Epoch_{self.current_epoch}.jpg",
            ),
            normalize=True,
        )

        try:
            samples = self.model.sample(n_images, self.curr_device, labels=test_label)
            vutils.save_image(
                samples.cpu().data,
                os.path.join(
                    self.logger.log_dir,
                    "Samples",
                    f"{self.logger.name}_Epoch_{self.current_epoch}.jpg",
                ),
                normalize=True,
            )
        except Warning:
            pass

    def configure_optimizers(self):

        optims = []
        scheds = []

        optimizer = optim.Adam(
            self.model.parameters(),
            lr=self.params["LR"],
            weight_decay=self.params["weight_decay"],
        )
        optims.append(optimizer)
        # Check if more than 1 optimizer is required (Used for adversarial training)
        try:
            if self.params["LR_2"] is not None:
                optimizer2 = optim.Adam(
                    getattr(self.model, self.params["submodel"]).parameters(),
                    lr=self.params["LR_2"],
                )
                optims.append(optimizer2)
        except:
            pass

        try:
            if self.params["scheduler_gamma"] is not None:
                scheduler = optim.lr_scheduler.ExponentialLR(
                    optims[0], gamma=self.params["scheduler_gamma"]
                )
                scheds.append(scheduler)

                # Check if another scheduler is required for the second optimizer
                try:
                    if self.params["scheduler_gamma_2"] is not None:
                        scheduler2 = optim.lr_scheduler.ExponentialLR(
                            optims[1], gamma=self.params["scheduler_gamma_2"]
                        )
                        scheds.append(scheduler2)
                except:
                    pass
                return optims, scheds
        except:
            return optims

    def load_state_dict(self, state_dict, strict=False):
        """
        DFCVAE allows stripping frozen weights that greatly increase storage size.
        This is the easiest point to fix this missing information and work with
        resuming a lightning training point.
        """
        return super().load_state_dict(state_dict, strict)
